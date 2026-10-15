import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { useRouter } from 'next/router';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import ProtectedPage from '@/components/ProtectedPage';
import {
  PublicExamAttempt,
  PublicExamAttemptAnswer,
  publicExamsAPI,
} from '@/lib/api';

type SaveState = 'idle' | 'saving' | 'saved' | 'error';

function formatDuration(totalSeconds: number) {
  const safe = Math.max(0, Math.floor(totalSeconds));
  const hours = Math.floor(safe / 3600);
  const minutes = Math.floor((safe % 3600) / 60);
  const seconds = safe % 60;
  return [hours, minutes, seconds].map((value) => String(value).padStart(2, '0')).join(':');
}

function errorMessage(error: unknown, fallback: string) {
  const response = (error as { response?: { status?: number; data?: { detail?: string } } }).response;
  return { status: response?.status, message: response?.data?.detail ?? fallback };
}

export default function PublicExamAttemptPage() {
  const router = useRouter();
  const attemptId = typeof router.query.attemptId === 'string' ? router.query.attemptId : '';
  const [attempt, setAttempt] = useState<PublicExamAttempt | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [saveStates, setSaveStates] = useState<Record<number, SaveState>>({});
  const [pendingDebounceCount, setPendingDebounceCount] = useState(0);
  const [, setClockTick] = useState(0);
  const attemptRef = useRef<PublicExamAttempt | null>(null);
  const enteredAtRef = useRef(Date.now());
  const elapsedBaseRef = useRef<Record<number, number>>({});
  const saveQueuesRef = useRef<Record<number, Promise<void>>>({});
  const localVersionsRef = useRef<Record<number, number>>({});
  const savedVersionsRef = useRef<Record<number, number>>({});
  const debounceTimersRef = useRef<Record<number, number>>({});
  const pendingDebouncesRef = useRef<Set<number>>(new Set());

  const syncPendingDebounceCount = useCallback(() => {
    setPendingDebounceCount(pendingDebouncesRef.current.size);
  }, []);

  const clearPendingDebounce = useCallback((questionId: number) => {
    const timer = debounceTimersRef.current[questionId];
    if (timer) window.clearTimeout(timer);
    delete debounceTimersRef.current[questionId];
    if (pendingDebouncesRef.current.delete(questionId)) syncPendingDebounceCount();
  }, [syncPendingDebounceCount]);

  const updateAttempt = useCallback((updater: (current: PublicExamAttempt) => PublicExamAttempt) => {
    const current = attemptRef.current;
    if (!current) return;
    const next = updater(current);
    attemptRef.current = next;
    setAttempt(next);
  }, []);

  useEffect(() => {
    if (!router.isReady || !attemptId) return;
    let active = true;
    publicExamsAPI.getAttempt(attemptId)
      .then((response) => {
        if (!active) return;
        attemptRef.current = response.data;
        setAttempt(response.data);
        elapsedBaseRef.current = Object.fromEntries(
          response.data.answers.map((answer) => [answer.question.id, answer.elapsed_seconds]),
        );
        enteredAtRef.current = Date.now();
      })
      .catch((caught) => {
        const apiError = errorMessage(caught, '응시 정보를 불러오지 못했습니다.');
        if (apiError.status === 409) {
          router.replace(`/public-exams/results/${attemptId}`);
          return;
        }
        if (active) setError(apiError.message);
      })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [attemptId, router]);

  useEffect(() => {
    const timer = window.setInterval(() => setClockTick((value) => value + 1), 1000);
    return () => window.clearInterval(timer);
  }, []);

  const currentAnswer = attempt?.answers[currentIndex] ?? null;
  const currentQuestionId = currentAnswer?.question.id;

  const currentElapsed = useCallback((questionId: number) => {
    const base = elapsedBaseRef.current[questionId] ?? 0;
    const activeQuestion = attemptRef.current?.answers[currentIndex]?.question.id;
    if (activeQuestion !== questionId) return base;
    return base + Math.max(0, (Date.now() - enteredAtRef.current) / 1000);
  }, [currentIndex]);

  const enqueueSave = useCallback((answer: PublicExamAttemptAnswer, elapsedSeconds: number) => {
    if (!attemptId) return Promise.reject(new Error('응시 ID가 없습니다.'));
    const questionId = answer.question.id;
    const version = localVersionsRef.current[questionId] ?? 0;
    setSaveStates((current) => ({ ...current, [questionId]: 'saving' }));
    const previous = saveQueuesRef.current[questionId] ?? Promise.resolve();
    const next = previous.catch(() => undefined).then(async () => {
      await publicExamsAPI.saveAnswer(attemptId, questionId, {
        selected_option: answer.question.question_type === 'MULTIPLE_CHOICE'
          ? answer.selected_option ?? null
          : null,
        written_answer: answer.question.question_type === 'SHORT_ANSWER'
          ? answer.written_answer ?? ''
          : null,
        elapsed_seconds: Number(elapsedSeconds.toFixed(3)),
      });
      savedVersionsRef.current[questionId] = Math.max(savedVersionsRef.current[questionId] ?? 0, version);
      if (localVersionsRef.current[questionId] === version && !pendingDebouncesRef.current.has(questionId)) {
        setSaveStates((current) => ({ ...current, [questionId]: 'saved' }));
      }
    }).catch((caught) => {
      if (localVersionsRef.current[questionId] === version) {
        setSaveStates((current) => ({ ...current, [questionId]: 'error' }));
      }
      throw caught;
    });
    saveQueuesRef.current[questionId] = next;
    return next;
  }, [attemptId]);

  const saveQuestion = useCallback((questionId: number) => {
    const current = attemptRef.current;
    const answer = current?.answers.find((item) => item.question.id === questionId);
    if (!answer) return Promise.resolve();
    return enqueueSave(answer, currentElapsed(questionId));
  }, [currentElapsed, enqueueSave]);

  const flushQuestionSave = useCallback((questionId: number) => {
    clearPendingDebounce(questionId);
    return saveQuestion(questionId);
  }, [clearPendingDebounce, saveQuestion]);

  const flushPendingSaves = useCallback(async () => {
    const pendingQuestionIds = Array.from(pendingDebouncesRef.current);
    const pendingResults = await Promise.allSettled(
      pendingQuestionIds.map((questionId) => flushQuestionSave(questionId)),
    );
    const queueResults = await Promise.allSettled(Object.values(saveQueuesRef.current));
    const failed = [...pendingResults, ...queueResults]
      .find((result): result is PromiseRejectedResult => result.status === 'rejected');
    if (failed) throw failed.reason;
    return new Set(pendingQuestionIds);
  }, [flushQuestionSave]);

  useEffect(() => {
    if (!currentQuestionId) return;
    const timer = window.setInterval(() => {
      void flushQuestionSave(currentQuestionId).catch(() => undefined);
    }, 10000);
    return () => window.clearInterval(timer);
  }, [currentQuestionId, flushQuestionSave]);

  useEffect(() => () => {
    Object.values(debounceTimersRef.current).forEach((timer) => window.clearTimeout(timer));
    debounceTimersRef.current = {};
    pendingDebouncesRef.current.clear();
  }, []);

  useEffect(() => {
    const warnIfSaving = (event: BeforeUnloadEvent) => {
      if (pendingDebouncesRef.current.size > 0
        || Object.values(saveStates).some((state) => state === 'saving' || state === 'error')
        || Object.entries(localVersionsRef.current).some(([questionId, version]) =>
          (savedVersionsRef.current[Number(questionId)] ?? 0) < version)) {
        event.preventDefault();
        event.returnValue = '';
      }
    };
    window.addEventListener('beforeunload', warnIfSaving);
    return () => window.removeEventListener('beforeunload', warnIfSaving);
  }, [pendingDebounceCount, saveStates]);

  const totalElapsed = attempt
    ? Math.max(0, (Date.now() - Date.parse(attempt.started_at)) / 1000)
    : 0;
  const answeredCount = useMemo(() => attempt?.answers.filter((answer) =>
    answer.selected_option != null || Boolean(answer.written_answer?.trim()),
  ).length ?? 0, [attempt]);

  const selectOption = (option: number) => {
    if (!currentAnswer || submitting) return;
    const questionId = currentAnswer.question.id;
    localVersionsRef.current[questionId] = (localVersionsRef.current[questionId] ?? 0) + 1;
    updateAttempt((current) => ({
      ...current,
      answers: current.answers.map((answer) => answer.question.id === questionId
        ? { ...answer, selected_option: option, written_answer: null }
        : answer),
    }));
    void saveQuestion(questionId).catch((caught) => {
      setError(errorMessage(caught, '답안을 저장하지 못했습니다.').message);
    });
  };

  const changeWrittenAnswer = (value: string) => {
    if (!currentAnswer || submitting) return;
    const questionId = currentAnswer.question.id;
    localVersionsRef.current[questionId] = (localVersionsRef.current[questionId] ?? 0) + 1;
    updateAttempt((current) => ({
      ...current,
      answers: current.answers.map((answer) => answer.question.id === questionId
        ? { ...answer, written_answer: value, selected_option: null }
        : answer),
    }));
    clearPendingDebounce(questionId);
    pendingDebouncesRef.current.add(questionId);
    syncPendingDebounceCount();
    setSaveStates((current) => ({ ...current, [questionId]: 'idle' }));
    debounceTimersRef.current[questionId] = window.setTimeout(() => {
      clearPendingDebounce(questionId);
      void saveQuestion(questionId).catch((caught) => {
        setError(errorMessage(caught, '답안을 저장하지 못했습니다.').message);
      });
    }, 700);
  };

  const moveTo = async (nextIndex: number) => {
    if (!currentAnswer || submitting || nextIndex === currentIndex) return;
    const questionId = currentAnswer.question.id;
    const elapsed = currentElapsed(questionId);
    try {
      await flushPendingSaves();
      elapsedBaseRef.current[questionId] = elapsed;
      updateAttempt((current) => ({
        ...current,
        answers: current.answers.map((answer) => answer.question.id === questionId
          ? { ...answer, elapsed_seconds: elapsed }
          : answer),
      }));
      setCurrentIndex(nextIndex);
      enteredAtRef.current = Date.now();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (caught) {
      setError(errorMessage(caught, '저장을 확인하지 못해 문항을 이동하지 않았습니다.').message);
    }
  };

  const submit = async () => {
    if (!attempt || !currentAnswer || submitting) return;
    if (!window.confirm(`답안 ${answeredCount}/${attempt.total_questions}개가 저장되었습니다. 최종 제출할까요?`)) return;
    setSubmitting(true);
    setError('');
    try {
      const flushed = await flushPendingSaves();
      if (!flushed.has(currentAnswer.question.id)) await flushQuestionSave(currentAnswer.question.id);
      const response = await publicExamsAPI.submitAttempt(attempt.id);
      await router.replace(`/public-exams/results/${response.data.attempt_id}`);
    } catch (caught) {
      setError(errorMessage(caught, '최종 제출하지 못했습니다. 저장 상태를 확인한 뒤 다시 시도해 주세요.').message);
      setSubmitting(false);
    }
  };

  const leaveForLater = async () => {
    if (!currentAnswer || submitting) return;
    setError('');
    try {
      const flushed = await flushPendingSaves();
      if (!flushed.has(currentAnswer.question.id)) await flushQuestionSave(currentAnswer.question.id);
      await router.push('/public-exams');
    } catch (caught) {
      setError(errorMessage(caught, '현재 문항을 저장하지 못해 화면을 나가지 않았습니다.').message);
    }
  };

  const saveState = currentAnswer ? saveStates[currentAnswer.question.id] ?? 'idle' : 'idle';
  const currentSavePending = currentAnswer
    ? pendingDebouncesRef.current.has(currentAnswer.question.id)
      || (savedVersionsRef.current[currentAnswer.question.id] ?? 0) < (localVersionsRef.current[currentAnswer.question.id] ?? 0)
    : false;

  const retryCurrentSave = async () => {
    if (!currentAnswer || submitting) return;
    setError('');
    try {
      await flushQuestionSave(currentAnswer.question.id);
    } catch (caught) {
      setError(errorMessage(caught, '답안을 저장하지 못했습니다. 다시 시도해 주세요.').message);
    }
  };

  return (
    <ProtectedPage roles={['STUDENT']}>
      <div className="app-shell flex min-h-screen flex-col">
        <Navbar />
        <main className="mx-auto w-full max-w-4xl flex-1 px-4 py-8">
          {loading ? (
            <div className="surface-card p-12 text-center text-[#6C757D]">응시 기록을 복구하는 중...</div>
          ) : error && !attempt ? (
            <div className="surface-card p-10 text-center">
              <p className="text-red-700">{error}</p>
              <button type="button" className="secondary-button mt-5" onClick={() => router.push('/public-exams')}>시험 선택으로</button>
            </div>
          ) : attempt && currentAnswer ? (
            <>
              <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
                <div>
                  <p className="text-sm font-semibold text-[#3B86D1]">공통 기출 응시</p>
                  <h1 className="mt-1 text-2xl font-bold">문항 {currentIndex + 1} / {attempt.total_questions}</h1>
                </div>
                <div className="rounded-xl bg-[#242C34] px-5 py-3 text-white">
                  <span className="mr-2 text-sm text-slate-300">전체 경과</span>
                  <strong className="font-mono text-lg">{formatDuration(totalElapsed)}</strong>
                </div>
              </div>

              {error && <div className="mb-5 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}

              <div className="mb-5">
                <div className="mb-2 flex justify-between text-sm text-[#6C757D]">
                  <span>{answeredCount}/{attempt.total_questions} 답안 입력</span>
                  <span>{saveState === 'saving' ? '저장 중...' : saveState === 'error' ? '저장 실패' : currentSavePending ? '저장 대기 중...' : saveState === 'saved' ? '저장됨' : '자동 저장'}</span>
                </div>
                <div className="h-2 overflow-hidden rounded-full bg-[#E9ECEF]">
                  <div className="h-full bg-[#3B86D1] transition-all" style={{ width: `${(currentIndex + 1) / attempt.total_questions * 100}%` }} />
                </div>
              </div>

              {saveState === 'error' && (
                <div className="mb-5 flex items-center justify-between gap-3 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
                  <span>로컬 답안은 유지되지만 최신 답안이 서버에 저장되지 않았습니다.</span>
                  <button type="button" className="secondary-button shrink-0" disabled={submitting} onClick={retryCurrentSave}>저장 재시도</button>
                </div>
              )}

              <article className="surface-card p-6 sm:p-8">
                <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
                  <span className="rounded-full bg-blue-50 px-3 py-1 text-sm font-semibold text-[#3B86D1]">
                    원문 {currentAnswer.question.question_number}번
                  </span>
                  <span className="font-mono text-sm text-[#6C757D]">
                    문항 시간 {formatDuration(currentElapsed(currentAnswer.question.id))}
                  </span>
                </div>
                <p className="whitespace-pre-wrap text-lg leading-8 text-[#242C34]">{currentAnswer.question.content}</p>

                {currentAnswer.question.question_type === 'MULTIPLE_CHOICE' ? (
                  <div className="mt-7 space-y-3">
                    {(currentAnswer.question.options ?? []).map((option, index) => {
                      const optionNumber = index + 1;
                      const selected = currentAnswer.selected_option === optionNumber;
                      return (
                        <label key={optionNumber} className={`flex cursor-pointer gap-3 rounded-xl border p-4 transition ${selected ? 'border-[#3B86D1] bg-blue-50' : 'border-[#E9ECEF] hover:border-[#3B86D1]/50'}`}>
                          <input type="radio" name={`question-${currentAnswer.question.id}`} checked={selected}
                            disabled={submitting} onChange={() => selectOption(optionNumber)} className="mt-1 accent-[#3B86D1]" />
                          <span><strong className="mr-2">{optionNumber}.</strong>{option}</span>
                        </label>
                      );
                    })}
                  </div>
                ) : (
                  <textarea rows={6} className="form-control mt-7" disabled={submitting}
                    value={currentAnswer.written_answer ?? ''} onChange={(event) => changeWrittenAnswer(event.target.value)}
                    placeholder="답안을 입력하세요." />
                )}
              </article>

              <div className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-4">
                <button type="button" className="secondary-button" disabled={currentIndex === 0 || submitting}
                  onClick={() => moveTo(currentIndex - 1)}>이전 문제</button>
                <button type="button" className="secondary-button" disabled={currentIndex >= attempt.answers.length - 1 || submitting}
                  onClick={() => moveTo(currentIndex + 1)}>다음 문제</button>
                <button type="button" className="secondary-button" disabled={submitting}
                  onClick={leaveForLater}>나중에 계속</button>
                <button type="button" className="success-button" disabled={submitting || saveState === 'saving'} onClick={submit}>
                  {submitting ? '제출 중...' : '최종 제출'}
                </button>
              </div>

              <div className="mt-6 flex flex-wrap gap-2">
                {attempt.answers.map((answer, index) => {
                  const answered = answer.selected_option != null || Boolean(answer.written_answer?.trim());
                  return (
                    <button key={answer.question.id} type="button" disabled={submitting}
                      onClick={() => moveTo(index)}
                      className={`h-10 w-10 rounded-lg border text-sm font-bold ${index === currentIndex ? 'border-[#3B86D1] bg-[#3B86D1] text-white' : answered ? 'border-green-300 bg-green-50 text-green-700' : 'border-[#DCE3EA] bg-white'}`}>
                      {index + 1}
                    </button>
                  );
                })}
              </div>
            </>
          ) : null}
        </main>
        <Footer />
      </div>
    </ProtectedPage>
  );
}
