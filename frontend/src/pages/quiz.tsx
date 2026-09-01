'use client';

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { useRouter } from 'next/router';
import { progressAPI, questionsAPI, recommendationsAPI } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import CodeBlock from '@/components/CodeBlock';
import ProtectedPage from '@/components/ProtectedPage';

type QuizQuestion = {
  id: number;
  title: string;
  content: string;
  difficulty: string;
  question_type: string;
  answer_type: 'MULTIPLE_CHOICE' | 'SUBJECTIVE' | 'CODE_INPUT';
  options?: string | string[] | null;
  correct_answer?: string | null;
  correct_option?: number | null;
  explanation?: string | null;
  code_snippet?: string | null;
  answer_code_snippet?: string | null;
  source_file?: string | null;
};

const difficultyLabels: Record<string, string> = {
  EASY: '초급',
  MEDIUM: '중급',
  HARD: '고급',
  EXPERT: '전문가',
};

function getOptions(question: QuizQuestion): string[] {
  if (Array.isArray(question.options)) {
    return question.options.map(String).filter((option) => option.trim() !== '');
  }
  if (!question.options) return [];
  try {
    const parsed = JSON.parse(question.options);
    return Array.isArray(parsed)
      ? parsed.map(String).filter((option) => option.trim() !== '')
      : [];
  } catch {
    return [];
  }
}

function getCorrectIndex(question: QuizQuestion): number | null {
  if (typeof question.correct_option === 'number' && question.correct_option >= 1) {
    return question.correct_option - 1;
  }
  if (question.correct_answer == null) return null;
  const parsed = Number.parseInt(String(question.correct_answer).trim(), 10);
  return Number.isInteger(parsed) && parsed >= 0 ? parsed : null;
}

function normalizeAnswer(value?: string | null) {
  return value?.trim().replace(/\r\n/g, '\n') ?? '';
}

function isSubjectiveCorrect(question: QuizQuestion, answer?: string) {
  const submitted = normalizeAnswer(answer);
  if (!submitted) return false;
  return [question.correct_answer, question.answer_code_snippet]
    .some((correctAnswer) => normalizeAnswer(correctAnswer) === submitted);
}

function formatTime(seconds: number) {
  const minutes = Math.floor(seconds / 60);
  const remainder = seconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(remainder).padStart(2, '0')}`;
}

function createSessionId() {
  return typeof crypto !== 'undefined' && 'randomUUID' in crypto
    ? crypto.randomUUID()
    : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

export default function QuizPage() {
  const router = useRouter();
  const { user } = useAuth();
  const [questions, setQuestions] = useState<QuizQuestion[]>([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, number>>({});
  const [writtenAnswers, setWrittenAnswers] = useState<Record<number, string>>({});
  const [gradingResults, setGradingResults] = useState<Record<number, {
    is_correct: boolean;
    grading_explanation?: string | null;
  }>>({});
  const [durations, setDurations] = useState<Record<number, number>>({});
  const [currentIndex, setCurrentIndex] = useState(0);
  const [submitted, setSubmitted] = useState(false);
  const [totalElapsed, setTotalElapsed] = useState(0);
  const [sessionId, setSessionId] = useState('');
  const quizStartedAt = useRef(0);
  const questionStartedAt = useRef(0);

  const startTiming = useCallback(() => {
    const now = Date.now();
    quizStartedAt.current = now;
    questionStartedAt.current = now;
    setTotalElapsed(0);
    setDurations({});
    setSessionId(createSessionId());
  }, []);

  const fetchRandomQuestions = useCallback(async (
    subjectId?: number,
    subjectUnit?: string,
    difficulty?: string,
    count: number = 5,
    adaptive: boolean = false,
    mode: 'STANDARD' | 'CODE' = 'STANDARD',
  ) => {
    setLoading(true);
    try {
      const response = adaptive
        ? await recommendationsAPI.getQuiz({ count, subject_id: subjectId })
        : await questionsAPI.getRandomQuestions({
            subject_id: subjectId,
            subject_unit: subjectUnit,
            difficulty,
            count,
            mode,
          });
      setQuestions(response.data.questions);
      setSelectedAnswers({});
      setWrittenAnswers({});
      setGradingResults({});
      setCurrentIndex(0);
      setSubmitted(false);
      startTiming();
    } catch (error: any) {
      const detail = error.response?.data?.detail ?? '문제를 불러오지 못했습니다.';
      alert(detail);
    } finally {
      setLoading(false);
    }
  }, [startTiming]);

  useEffect(() => {
    if (!router.isReady || !router.query.count) return;
    const subjectId = router.query.subjectId ? Number(router.query.subjectId) : undefined;
    const subjectUnit = typeof router.query.subjectUnit === 'string'
      ? router.query.subjectUnit
      : undefined;
    const difficulty = typeof router.query.difficulty === 'string'
      ? router.query.difficulty
      : undefined;
    const adaptive = router.query.adaptive === '1';
    const mode = router.query.mode === 'CODE' ? 'CODE' : 'STANDARD';
    fetchRandomQuestions(subjectId, subjectUnit, difficulty, Number(router.query.count) || 5, adaptive, mode);
  }, [router.isReady, router.query.subjectId, router.query.subjectUnit, router.query.difficulty, router.query.count, router.query.adaptive, router.query.mode, fetchRandomQuestions]);

  useEffect(() => {
    if (!questions.length || submitted) return;
    const timer = window.setInterval(() => {
      setTotalElapsed(Math.floor((Date.now() - quizStartedAt.current) / 1000));
    }, 1000);
    return () => window.clearInterval(timer);
  }, [questions.length, submitted]);

  const commitCurrentTime = () => {
    const question = questions[currentIndex];
    if (!question || submitted) return durations;
    const elapsed = Math.max((Date.now() - questionStartedAt.current) / 1000, 0);
    const updated = {
      ...durations,
      [question.id]: (durations[question.id] ?? 0) + elapsed,
    };
    setDurations(updated);
    questionStartedAt.current = Date.now();
    return updated;
  };

  const moveTo = (nextIndex: number) => {
    commitCurrentTime();
    setCurrentIndex(nextIndex);
    questionStartedAt.current = Date.now();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const score = useMemo(
    () => questions.reduce((total, question) => {
      const options = getOptions(question);
      const correct = gradingResults[question.id]?.is_correct ?? (
        question.answer_type === 'CODE_INPUT' ? false :
        options.length > 0
          ? selectedAnswers[question.id] === getCorrectIndex(question)
          : isSubjectiveCorrect(question, writtenAnswers[question.id])
      );
      return total + (correct ? 1 : 0);
    }, 0),
    [questions, selectedAnswers, writtenAnswers, gradingResults]
  );

  const handleSubmit = async () => {
    const finalDurations = commitCurrentTime();
    const totalSeconds = Math.max((Date.now() - quizStartedAt.current) / 1000, 0);
    setSubmitting(true);
    try {
      if (user?.role === 'STUDENT') {
        const response = await progressAPI.submit({
          session_id: sessionId,
          total_seconds: totalSeconds,
          answers: questions.map((question, index) => ({
            question_id: question.id,
            answer: getOptions(question).length > 0
              ? selectedAnswers[question.id] ?? null
              : writtenAnswers[question.id]?.trim() || null,
            sequence_number: index + 1,
            elapsed_seconds: Number((finalDurations[question.id] ?? 0).toFixed(2)),
          })),
        });
        const results = response.data.results ?? [];
        setGradingResults(Object.fromEntries(
          results.map((result: any) => [result.question_id, result])
        ));
      }
      setTotalElapsed(Math.floor(totalSeconds));
      setSubmitted(true);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (error: any) {
      const detail = error.response?.data?.detail;
      alert(`풀이 결과를 저장하지 못했습니다.\n${detail ?? '백엔드 서버를 재시작한 뒤 다시 시도해 주세요.'}`);
    } finally {
      setSubmitting(false);
    }
  };

  const retryQuiz = () => {
    setSelectedAnswers({});
    setWrittenAnswers({});
    setGradingResults({});
    setCurrentIndex(0);
    setSubmitted(false);
    startTiming();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const question = questions[currentIndex];
  const options = question ? getOptions(question) : [];
  const selectedIndex = question ? selectedAnswers[question.id] : undefined;
  const writtenAnswer = question ? writtenAnswers[question.id] ?? '' : '';
  const correctIndex = question ? getCorrectIndex(question) : null;
  const isCorrect = question
    ? options.length > 0
      ? selectedIndex !== undefined && selectedIndex === correctIndex
      : isSubjectiveCorrect(question, writtenAnswer)
    : false;

  return (
    <ProtectedPage>
      <div className="app-shell flex flex-col">
        <Navbar />
        <main className="mx-auto w-full max-w-4xl flex-1 px-4 py-10">
          <div className="mb-7 flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="font-semibold text-[#21BF06]">오늘의 학습</p>
              <h1 className="mt-1 text-4xl font-bold text-[#242C34]">문제 풀기</h1>
            </div>
            {questions.length > 0 && (
              <div className="rounded-xl bg-[#242C34] px-5 py-3 text-white">
                <span className="mr-2 text-sm text-slate-300">전체 풀이 시간</span>
                <strong className="font-mono text-lg">{formatTime(totalElapsed)}</strong>
              </div>
            )}
          </div>

          {submitted && (
            <>
              <section className="mb-6 rounded-2xl border border-[#21BF06]/30 bg-[#F1FCEB] p-6">
                <p className="font-semibold text-[#168A04]">채점 결과</p>
                <div className="mt-2 flex flex-wrap items-end justify-between gap-3">
                  <h2 className="text-3xl font-bold">{score} / {questions.length} 정답</h2>
                  <strong className="text-xl text-[#168A04]">
                    {questions.length ? Math.round(score / questions.length * 100) : 0}점
                  </strong>
                </div>
                <p className="mt-3 text-sm text-[#495057]">
                  전체 문항의 답과 해설을 아래에서 한 번에 확인할 수 있습니다.
                </p>
              </section>

              <section className="space-y-6">
                {questions.map((reviewQuestion, reviewIndex) => {
                  const reviewOptions = getOptions(reviewQuestion);
                  const reviewSelected = selectedAnswers[reviewQuestion.id];
                  const reviewWritten = writtenAnswers[reviewQuestion.id] ?? '';
                  const reviewCorrect = getCorrectIndex(reviewQuestion);
                  const reviewGrade = gradingResults[reviewQuestion.id];
                  const reviewIsCorrect = reviewGrade?.is_correct ?? (
                    reviewOptions.length > 0
                      ? reviewSelected !== undefined && reviewSelected === reviewCorrect
                      : isSubjectiveCorrect(reviewQuestion, reviewWritten)
                  );

                  return (
                    <article key={reviewQuestion.id}
                      className={`surface-card overflow-hidden border-l-4 p-6 sm:p-8 ${
                        reviewIsCorrect ? 'border-l-[#21BF06]' : 'border-l-[#E5484D]'
                      }`}>
                      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
                        <span className="rounded-full bg-blue-50 px-3 py-1 text-sm font-semibold text-[#3B86D1]">
                          문제 {reviewIndex + 1}
                        </span>
                        <span className={`font-bold ${reviewIsCorrect ? 'text-[#168A04]' : 'text-[#C62F34]'}`}>
                          {reviewIsCorrect
                            ? '정답'
                            : reviewOptions.length === 0
                              ? reviewWritten.trim() ? '오답' : '미응답'
                              : reviewSelected === undefined ? '미응답' : '오답'}
                        </span>
                      </div>
                      <h2 className="text-xl font-bold text-[#242C34]">{reviewQuestion.title}</h2>
                      <p className="mt-3 whitespace-pre-wrap text-[#495057]">{reviewQuestion.content}</p>
                      {reviewQuestion.code_snippet && (
                        <div className="mt-5">
                          <CodeBlock code={reviewQuestion.code_snippet}
                            language={reviewQuestion.source_file} label="문제 코드" />
                        </div>
                      )}

                      <div className="mt-5 grid gap-3 sm:grid-cols-2">
                        <div className="rounded-xl bg-[#F8F9FA] p-4">
                          <p className="text-sm font-semibold text-[#6C757D]">내가 선택한 답</p>
                          <p className="mt-1 font-semibold">
                            {reviewQuestion.answer_type === 'CODE_INPUT'
                              ? 'GPT가 문제 요구사항을 기준으로 채점'
                              : reviewOptions.length === 0
                              ? reviewWritten.trim() || '답하지 않음'
                              : reviewSelected !== undefined && reviewOptions[reviewSelected]
                                ? `${reviewSelected + 1}번 ${reviewOptions[reviewSelected]}`
                                : '선택하지 않음'}
                          </p>
                        </div>
                        <div className="rounded-xl bg-[#F1FCEB] p-4">
                          <p className="text-sm font-semibold text-[#168A04]">정답</p>
                          <p className="mt-1 font-semibold">
                            {reviewOptions.length === 0
                              ? reviewQuestion.correct_answer?.trim()
                                || reviewQuestion.answer_code_snippet?.trim()
                                || '정답 정보 없음'
                              : reviewCorrect !== null && reviewOptions[reviewCorrect]
                                ? `${reviewCorrect + 1}번 ${reviewOptions[reviewCorrect]}`
                                : '정답 정보 없음'}
                          </p>
                        </div>
                      </div>

                      <div className="mt-4 rounded-xl border border-[#E9ECEF] p-5">
                        <p className="text-sm font-bold text-[#242C34]">해설</p>
                        <p className="mt-2 whitespace-pre-wrap text-[#495057]">
                          {reviewQuestion.explanation?.trim() || '등록된 해설이 없습니다.'}
                        </p>
                      </div>
                      {reviewGrade?.grading_explanation && (
                        <div className="mt-4 rounded-xl border border-blue-200 bg-blue-50 p-5">
                          <p className="text-sm font-bold text-[#242C34]">코드 채점 해설</p>
                          <p className="mt-2 whitespace-pre-wrap text-[#495057]">
                            {reviewGrade.grading_explanation}
                          </p>
                        </div>
                      )}
                      {reviewQuestion.answer_code_snippet && (
                        <div className="mt-4">
                          <CodeBlock code={reviewQuestion.answer_code_snippet}
                            language={reviewQuestion.source_file} label="정답 코드" />
                        </div>
                      )}
                    </article>
                  );
                })}

                <div className="grid gap-3 sm:grid-cols-2">
                  <button type="button" onClick={retryQuiz} className="secondary-button">
                    같은 문제 다시 풀기
                  </button>
                  <button type="button" onClick={() => router.push('/')} className="success-button">
                    대시보드 보기
                  </button>
                </div>
              </section>
            </>
          )}

          {submitted ? null : !question ? (
            <section className="surface-card p-10 text-center">
              <h2 className="text-xl font-bold">풀 문제를 불러오세요.</h2>
              <p className="mt-2 text-[#6C757D]">대시보드에서 조건을 선택하거나 무작위 문제를 시작할 수 있습니다.</p>
              <button onClick={() => fetchRandomQuestions(undefined, undefined, undefined, 5)}
                disabled={loading} className="primary-button mt-6">
                {loading ? '불러오는 중...' : '무작위 5문제 시작'}
              </button>
            </section>
          ) : (
            <>
              <div className="mb-4">
                <div className="mb-2 flex justify-between text-sm text-[#6C757D]">
                  <span>{currentIndex + 1} / {questions.length}</span>
                  <span>{difficultyLabels[question.difficulty] ?? question.difficulty}</span>
                </div>
                <div className="h-2 overflow-hidden rounded-full bg-[#E9ECEF]">
                  <div className="h-full bg-[#3B86D1] transition-all"
                    style={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }} />
                </div>
              </div>

              <article className={`surface-card overflow-hidden p-6 sm:p-8 ${
                submitted ? isCorrect ? 'border-[#21BF06]' : 'border-[#E5484D]' : ''
              }`}>
                <div className="mb-4 flex items-center justify-between">
                  <span className="rounded-full bg-blue-50 px-3 py-1 text-sm font-semibold text-[#3B86D1]">
                    문제 {currentIndex + 1}
                  </span>
                  {(selectedIndex !== undefined || writtenAnswer.trim()) && !submitted && (
                    <span className="text-sm font-semibold text-[#168A04]">답변 완료</span>
                  )}
                </div>
                <h2 className="mb-4 text-xl font-semibold text-[#242C34]">{question.title}</h2>
                <p className="mb-5 whitespace-pre-wrap text-[#495057]">{question.content}</p>
                {question.code_snippet && (
                  <CodeBlock code={question.code_snippet} language={question.source_file} label="문제 코드" />
                )}

                <div className="space-y-3">
                  {options.map((option, optionIndex) => {
                    const selected = selectedIndex === optionIndex;
                    const correct = correctIndex === optionIndex;
                    const style = submitted
                      ? correct ? 'border-[#21BF06] bg-[#F1FCEB]'
                        : selected ? 'border-[#E5484D] bg-[#FFF1F1]'
                          : 'border-[#E9ECEF] opacity-70'
                      : selected ? 'border-[#3B86D1] bg-blue-50'
                        : 'border-[#E9ECEF] hover:border-[#3B86D1]/50';
                    return (
                      <label key={optionIndex}
                        className={`flex rounded-xl border p-4 transition ${style} ${submitted ? 'cursor-default' : 'cursor-pointer'}`}>
                        <input type="radio" name={`question-${question.id}`}
                          checked={selected} disabled={submitted}
                          onChange={() => setSelectedAnswers((current) => ({
                            ...current, [question.id]: optionIndex,
                          }))}
                          className="mr-3 accent-[#3B86D1]" />
                        <span className="flex-1">{option}</span>
                        {submitted && correct && <strong className="text-[#168A04]">정답</strong>}
                        {submitted && selected && !correct && <strong className="text-[#C62F34]">내 답</strong>}
                      </label>
                    );
                  })}
                  {options.length === 0 && (
                    <label className="block">
                      <span className="mb-2 block text-sm font-semibold text-[#242C34]">
                        답안 (텍스트 또는 코드)
                      </span>
                      <textarea
                        rows={10}
                        value={writtenAnswer}
                        onChange={(event) => setWrittenAnswers((current) => ({
                          ...current,
                          [question.id]: event.target.value,
                        }))}
                        className="form-control font-mono text-sm"
                        placeholder={question.answer_type === 'CODE_INPUT' ? '채점할 코드를 입력하세요.' : '주관식 정답을 입력하세요.'}
                        spellCheck={false}
                      />
                    </label>
                  )}
                </div>

                {submitted && (
                  <div className={`mt-6 rounded-xl border p-5 ${
                    isCorrect ? 'border-[#21BF06]/30 bg-[#F1FCEB]' : 'border-[#E5484D]/30 bg-[#FFF6F6]'
                  }`}>
                    <p className={`text-lg font-bold ${isCorrect ? 'text-[#168A04]' : 'text-[#C62F34]'}`}>
                      {isCorrect ? '정답입니다.' : selectedIndex === undefined ? '답하지 않았습니다.' : '오답입니다.'}
                    </p>
                    <p className="mt-3 font-semibold">
                      정답: {correctIndex !== null && options[correctIndex]
                        ? `${correctIndex + 1}번 ${options[correctIndex]}` : '정답 정보 없음'}
                    </p>
                    <div className="mt-3 border-t border-black/10 pt-3">
                      <p className="text-sm font-semibold">해설</p>
                      <p className="mt-1 whitespace-pre-wrap text-[#495057]">
                        {question.explanation?.trim() || '등록된 해설이 없습니다.'}
                      </p>
                    </div>
                    {question.answer_code_snippet && (
                      <div className="mt-4">
                        <CodeBlock code={question.answer_code_snippet}
                          language={question.source_file} label="정답 코드" />
                      </div>
                    )}
                  </div>
                )}
              </article>

              <div className="mt-5 grid grid-cols-2 gap-3 sm:flex">
                <button type="button" disabled={currentIndex === 0}
                  onClick={() => moveTo(currentIndex - 1)}
                  className="secondary-button disabled:cursor-not-allowed disabled:opacity-40">
                  이전 문제
                </button>
                {currentIndex < questions.length - 1 ? (
                  <button type="button" onClick={() => moveTo(currentIndex + 1)}
                    className="primary-button sm:ml-auto">
                    다음 문제
                  </button>
                ) : !submitted ? (
                  <button type="button" onClick={handleSubmit} disabled={submitting}
                    className="success-button sm:ml-auto">
                    {submitting ? '저장 중...' : '채점하고 해설 보기'}
                  </button>
                ) : (
                  <button type="button" onClick={() => router.push('/')}
                    className="success-button sm:ml-auto">
                    대시보드 보기
                  </button>
                )}
              </div>

              {submitted && (
                <button type="button" onClick={retryQuiz}
                  className="mt-3 w-full rounded-xl border border-[#CED4DA] px-6 py-3 font-semibold">
                  같은 문제 다시 풀기
                </button>
              )}
            </>
          )}
        </main>
        <Footer />
      </div>
    </ProtectedPage>
  );
}
