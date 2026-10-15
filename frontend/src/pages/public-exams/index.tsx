import { useEffect, useMemo, useState } from 'react';
import { useRouter } from 'next/router';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import ProtectedPage from '@/components/ProtectedPage';
import {
  PublicExam,
  PublicExamAttempt,
  PublicExamRound,
  PublicExamSubject,
  publicExamsAPI,
} from '@/lib/api';

type SubjectLabel = {
  examName: string;
  roundName: string;
  subjectName: string;
};

function errorMessage(error: unknown, fallback: string) {
  const response = (error as { response?: { data?: { detail?: string } } }).response;
  return response?.data?.detail ?? fallback;
}

export default function PublicExamsPage() {
  const router = useRouter();
  const [exams, setExams] = useState<PublicExam[]>([]);
  const [rounds, setRounds] = useState<PublicExamRound[]>([]);
  const [subjects, setSubjects] = useState<PublicExamSubject[]>([]);
  const [attempts, setAttempts] = useState<PublicExamAttempt[]>([]);
  const [subjectLabels, setSubjectLabels] = useState<Record<number, SubjectLabel>>({});
  const [examId, setExamId] = useState<number | null>(null);
  const [roundId, setRoundId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectionLoading, setSelectionLoading] = useState(false);
  const [startingSubjectId, setStartingSubjectId] = useState<number | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;
    Promise.all([publicExamsAPI.getExams(), publicExamsAPI.getInProgressAttempts()])
      .then(async ([examResponse, attemptResponse]) => {
        if (!active) return;
        setExams(examResponse.data);
        setAttempts(attemptResponse.data);

        const labelEntries = await Promise.all(examResponse.data.map(async (exam) => {
          const roundResponse = await publicExamsAPI.getRounds(exam.id);
          const subjectsByRound = await Promise.all(roundResponse.data.map(async (examRound) => {
            const subjectResponse = await publicExamsAPI.getSubjects(examRound.id);
            return subjectResponse.data.map((subject) => [subject.id, {
              examName: exam.name,
              roundName: examRound.display_name
                || `${examRound.exam_year}년 ${examRound.round_identifier}`,
              subjectName: subject.name,
            }] as const);
          }));
          return subjectsByRound.flat();
        }));
        if (active) setSubjectLabels(Object.fromEntries(labelEntries.flat()));
      })
      .catch((caught) => {
        if (active) setError(errorMessage(caught, '공통 기출 목록을 불러오지 못했습니다.'));
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => { active = false; };
  }, []);

  const selectedExam = useMemo(
    () => exams.find((exam) => exam.id === examId) ?? null,
    [examId, exams],
  );
  const selectedRound = useMemo(
    () => rounds.find((examRound) => examRound.id === roundId) ?? null,
    [roundId, rounds],
  );

  const chooseExam = async (nextExam: PublicExam) => {
    setExamId(nextExam.id);
    setRoundId(null);
    setSubjects([]);
    setSelectionLoading(true);
    setError('');
    try {
      const response = await publicExamsAPI.getRounds(nextExam.id);
      setRounds(response.data);
    } catch (caught) {
      setRounds([]);
      setError(errorMessage(caught, '시험 회차를 불러오지 못했습니다.'));
    } finally {
      setSelectionLoading(false);
    }
  };

  const chooseRound = async (nextRound: PublicExamRound) => {
    setRoundId(nextRound.id);
    setSelectionLoading(true);
    setError('');
    try {
      const response = await publicExamsAPI.getSubjects(nextRound.id);
      setSubjects(response.data);
    } catch (caught) {
      setSubjects([]);
      setError(errorMessage(caught, '시험 과목을 불러오지 못했습니다.'));
    } finally {
      setSelectionLoading(false);
    }
  };

  const startAttempt = async (subjectId: number) => {
    setStartingSubjectId(subjectId);
    setError('');
    try {
      const response = await publicExamsAPI.startAttempt(subjectId);
      await router.push(`/public-exams/attempt/${response.data.id}`);
    } catch (caught) {
      setError(errorMessage(caught, '응시를 시작하지 못했습니다.'));
      setStartingSubjectId(null);
    }
  };

  return (
    <ProtectedPage roles={['STUDENT']}>
      <div className="app-shell flex min-h-screen flex-col">
        <Navbar />
        <main className="page-container flex-1 py-10">
          <div className="mb-8 flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="font-semibold text-[#3B86D1]">공통 기출문제</p>
              <h1 className="mt-1 text-3xl font-bold text-[#242C34]">자격증 시험 선택</h1>
              <p className="mt-2 text-[#6C757D]">강사 지정과 관계없이 등록된 공통 기출을 풀 수 있습니다.</p>
            </div>
            <button type="button" className="secondary-button" onClick={() => router.push('/')}>대시보드로</button>
          </div>

          {error && <div className="mb-6 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}

          {!!attempts.length && (
            <section className="surface-card mb-8 overflow-hidden">
              <div className="border-b border-[#E9ECEF] p-6">
                <h2 className="text-xl font-bold">진행 중인 응시</h2>
                <p className="mt-1 text-sm text-[#6C757D]">저장된 답안과 문항별 시간을 이어서 복구합니다.</p>
              </div>
              <div className="divide-y divide-[#E9ECEF]">
                {attempts.map((attempt) => {
                  const label = subjectLabels[attempt.subject_id];
                  const answered = attempt.answers.filter((answer) =>
                    answer.selected_option != null || Boolean(answer.written_answer?.trim()),
                  ).length;
                  return (
                    <div key={attempt.id} className="flex flex-wrap items-center justify-between gap-4 p-5">
                      <div>
                        <p className="font-bold text-[#242C34]">
                          {label ? `${label.examName} · ${label.subjectName}` : `공통 기출 과목 #${attempt.subject_id}`}
                        </p>
                        <p className="mt-1 text-sm text-[#6C757D]">
                          {label?.roundName ?? '등록된 회차'} · {answered}/{attempt.total_questions} 답안 저장
                        </p>
                      </div>
                      <button type="button" className="primary-button" onClick={() => router.push(`/public-exams/attempt/${attempt.id}`)}>
                        이어서 풀기
                      </button>
                    </div>
                  );
                })}
              </div>
            </section>
          )}

          {loading ? (
            <div className="surface-card p-12 text-center text-[#6C757D]">시험 목록을 불러오는 중...</div>
          ) : !exams.length ? (
            <div className="surface-card p-12 text-center">
              <h2 className="text-xl font-bold text-[#242C34]">등록된 공통 기출 시험이 없습니다.</h2>
              <p className="mt-2 text-[#6C757D]">관리자가 시험과 공개 회차를 등록하면 이곳에 표시됩니다.</p>
            </div>
          ) : (
            <div className="space-y-8">
              <section>
                <h2 className="mb-4 text-xl font-bold">1. 시험 선택</h2>
                <div className="grid gap-4 sm:grid-cols-2">
                  {exams.map((exam) => (
                    <button key={exam.id} type="button" onClick={() => chooseExam(exam)}
                      className={`surface-card p-6 text-left transition ${examId === exam.id ? 'ring-2 ring-[#3B86D1]' : 'surface-card-hover'}`}>
                      <p className="text-sm font-semibold text-[#3B86D1]">{exam.code}</p>
                      <h3 className="mt-2 text-2xl font-bold text-[#242C34]">{exam.name}</h3>
                      {exam.description && <p className="mt-2 text-sm text-[#6C757D]">{exam.description}</p>}
                    </button>
                  ))}
                </div>
              </section>

              {selectedExam && (
                <section>
                  <h2 className="mb-4 text-xl font-bold">2. 연도·회차 선택</h2>
                  {!selectionLoading && !rounds.length ? (
                    <div className="surface-card p-8 text-center text-[#6C757D]">공개된 회차가 없습니다.</div>
                  ) : (
                    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                      {rounds.map((examRound) => (
                        <button key={examRound.id} type="button" onClick={() => chooseRound(examRound)}
                          className={`surface-card p-5 text-left ${roundId === examRound.id ? 'ring-2 ring-[#21BF06]' : 'surface-card-hover'}`}>
                          <strong>{examRound.display_name || `${examRound.exam_year}년 ${examRound.round_identifier}`}</strong>
                          {examRound.held_on && <p className="mt-1 text-sm text-[#6C757D]">시행일 {examRound.held_on}</p>}
                        </button>
                      ))}
                    </div>
                  )}
                </section>
              )}

              {selectedRound && (
                <section>
                  <h2 className="mb-4 text-xl font-bold">3. 과목 선택</h2>
                  {!selectionLoading && !subjects.length ? (
                    <div className="surface-card p-8 text-center text-[#6C757D]">등록된 공개 과목이 없습니다.</div>
                  ) : (
                    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                      {subjects.map((subject) => (
                        <div key={subject.id} className="surface-card p-6">
                          <p className="text-sm font-semibold text-[#6C757D]">과목 {subject.display_order}</p>
                          <h3 className="mt-2 text-xl font-bold">{subject.name}</h3>
                          <button type="button" className="success-button mt-5 w-full"
                            disabled={startingSubjectId !== null}
                            onClick={() => startAttempt(subject.id)}>
                            {startingSubjectId === subject.id ? '응시 준비 중...' : '문제 풀기'}
                          </button>
                        </div>
                      ))}
                    </div>
                  )}
                </section>
              )}
            </div>
          )}
        </main>
        <Footer />
      </div>
    </ProtectedPage>
  );
}
