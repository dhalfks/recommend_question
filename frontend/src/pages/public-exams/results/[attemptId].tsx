import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import ProtectedPage from '@/components/ProtectedPage';
import { PublicExamResult, PublicExamResultItem, publicExamsAPI } from '@/lib/api';

function formatDuration(totalSeconds: number) {
  const safe = Math.max(0, Math.floor(totalSeconds));
  const hours = Math.floor(safe / 3600);
  const minutes = Math.floor((safe % 3600) / 60);
  const seconds = safe % 60;
  return [hours, minutes, seconds].map((value) => String(value).padStart(2, '0')).join(':');
}

function errorMessage(error: unknown, fallback: string) {
  return (error as { response?: { data?: { detail?: string } } }).response?.data?.detail ?? fallback;
}

function answerLabel(item: PublicExamResultItem, selected: boolean) {
  if (item.question_type === 'SHORT_ANSWER') {
    return selected ? item.written_answer?.trim() || '미응답' : item.correct_answer?.trim() || '정답 정보 없음';
  }
  const number = selected ? item.selected_option : item.correct_option;
  if (number == null) return selected ? '미응답' : '정답 정보 없음';
  return `${number}번 ${item.options?.[number - 1] ?? ''}`.trim();
}

export default function PublicExamResultPage() {
  const router = useRouter();
  const attemptId = typeof router.query.attemptId === 'string' ? router.query.attemptId : '';
  const [result, setResult] = useState<PublicExamResult | null>(null);
  const [wrongItems, setWrongItems] = useState<PublicExamResultItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [wrongItemsError, setWrongItemsError] = useState('');
  const [wrongItemsLoaded, setWrongItemsLoaded] = useState(false);
  const [retryMode, setRetryMode] = useState(false);
  const [retryAnswers, setRetryAnswers] = useState<Record<number, number | string>>({});
  const [checked, setChecked] = useState<Record<number, boolean>>({});

  useEffect(() => {
    if (!router.isReady || !attemptId) return;
    let active = true;
    publicExamsAPI.getResult(attemptId)
      .then((resultResponse) => {
        if (!active) return;
        setResult(resultResponse.data);
        setLoading(false);
        return publicExamsAPI.getWrongAnswers(attemptId)
          .then((wrongResponse) => {
            if (!active) return;
            setWrongItems(wrongResponse.data.items);
            setWrongItemsLoaded(true);
          })
          .catch((caught) => {
            if (!active) return;
            setWrongItemsError(errorMessage(caught, '오답 목록만 불러오지 못했습니다.'));
          });
      })
      .catch((caught) => {
        if (active) setError(errorMessage(caught, '시험 결과를 불러오지 못했습니다.'));
      })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [attemptId, router.isReady]);

  const retryCorrect = (item: PublicExamResultItem) => {
    const value = retryAnswers[item.question_id];
    if (item.question_type === 'MULTIPLE_CHOICE') return value === item.correct_option;
    return String(value ?? '').trim().replace(/\r\n/g, '\n')
      === String(item.correct_answer ?? '').trim().replace(/\r\n/g, '\n');
  };

  return (
    <ProtectedPage roles={['STUDENT']}>
      <div className="app-shell flex min-h-screen flex-col">
        <Navbar />
        <main className="mx-auto w-full max-w-5xl flex-1 px-4 py-10">
          {loading ? (
            <div className="surface-card p-12 text-center text-[#6C757D]">채점 결과를 불러오는 중...</div>
          ) : error ? (
            <div className="surface-card p-10 text-center">
              <p className="text-red-700">{error}</p>
              <button type="button" className="secondary-button mt-5" onClick={() => router.push('/public-exams')}>시험 목록으로</button>
            </div>
          ) : result ? (
            <>
              <section className="overflow-hidden rounded-3xl bg-[#242C34] p-7 text-white shadow-lg sm:p-10">
                <p className="font-semibold text-[#63E64B]">제출 완료</p>
                <div className="mt-2 flex flex-wrap items-end justify-between gap-5">
                  <div>
                    <h1 className="text-3xl font-bold">{result.exam_name}</h1>
                    <p className="mt-2 text-slate-300">{result.exam_year}년 {result.round_identifier} · {result.subject_name}</p>
                  </div>
                  <div className="text-right">
                    <strong className="text-4xl text-[#63E64B]">{result.score_percent}%</strong>
                    <p className="mt-1 text-sm text-slate-300">총 소요 {formatDuration(result.total_elapsed_seconds)}</p>
                  </div>
                </div>
              </section>

              <section className="my-7 grid gap-4 sm:grid-cols-4">
                <div className="surface-card p-5"><p className="text-sm text-[#6C757D]">전체 문항</p><strong className="mt-2 block text-3xl">{result.total_questions}</strong></div>
                <div className="surface-card p-5"><p className="text-sm text-[#6C757D]">정답</p><strong className="mt-2 block text-3xl text-green-600">{result.correct_answers}</strong></div>
                <div className="surface-card p-5"><p className="text-sm text-[#6C757D]">오답</p><strong className="mt-2 block text-3xl text-red-600">{result.incorrect_answers}</strong></div>
                <div className="surface-card p-5"><p className="text-sm text-[#6C757D]">전체 시간</p><strong className="mt-2 block font-mono text-xl">{formatDuration(result.total_elapsed_seconds)}</strong></div>
              </section>

              <div className="mb-6 flex flex-wrap gap-3">
                <button type="button" className={retryMode ? 'secondary-button' : 'primary-button'} onClick={() => setRetryMode(false)}>전체 정오표</button>
                <button type="button" className={retryMode ? 'success-button' : 'secondary-button'}
                  disabled={!wrongItemsLoaded || !wrongItems.length} onClick={() => setRetryMode(true)}>오답 다시 풀기 ({wrongItems.length})</button>
                <button type="button" className="secondary-button" onClick={() => router.push('/public-exams')}>다른 시험 선택</button>
              </div>

              {wrongItemsError && (
                <div className="mb-6 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
                  {wrongItemsError} 결과 요약과 문항별 채점 결과는 정상적으로 표시됩니다.
                </div>
              )}

              {!retryMode ? (
                <section className="space-y-5">
                  {result.items.map((item) => (
                    <article key={item.question_id} className={`surface-card border-l-4 p-6 ${item.is_correct ? 'border-l-green-500' : 'border-l-red-500'}`}>
                      <div className="flex flex-wrap items-center justify-between gap-3">
                        <span className="font-bold">문항 {item.sequence_number} · 원문 {item.question_number}번</span>
                        <div className="flex items-center gap-3">
                          <span className="font-mono text-sm text-[#6C757D]">{formatDuration(item.elapsed_seconds)}</span>
                          <strong className={item.is_correct ? 'text-green-600' : 'text-red-600'}>{item.is_correct ? '정답' : '오답'}</strong>
                        </div>
                      </div>
                      <p className="mt-4 whitespace-pre-wrap leading-7">{item.content}</p>
                      <div className="mt-5 grid gap-3 sm:grid-cols-2">
                        <div className="rounded-xl bg-[#F8F9FA] p-4"><p className="text-xs font-semibold text-[#6C757D]">제출 답안</p><p className="mt-1 font-semibold">{answerLabel(item, true)}</p></div>
                        <div className="rounded-xl bg-green-50 p-4"><p className="text-xs font-semibold text-green-700">정답</p><p className="mt-1 font-semibold">{answerLabel(item, false)}</p></div>
                      </div>
                      <div className="mt-4 rounded-xl border border-[#E9ECEF] p-4">
                        <p className="text-sm font-bold">해설</p>
                        <p className="mt-2 whitespace-pre-wrap text-sm leading-6 text-[#495057]">{item.explanation?.trim() || '등록된 해설이 없습니다.'}</p>
                      </div>
                    </article>
                  ))}
                </section>
              ) : (
                <section className="space-y-5">
                  {!wrongItems.length ? <div className="surface-card p-10 text-center">다시 풀 오답이 없습니다.</div> : wrongItems.map((item) => {
                    const isChecked = checked[item.question_id] === true;
                    const isCorrect = isChecked && retryCorrect(item);
                    return (
                      <article key={item.question_id} className="surface-card p-6">
                        <div className="flex justify-between gap-3"><strong>오답 문항 {item.sequence_number}</strong><span className="text-sm text-[#6C757D]">원문 {item.question_number}번</span></div>
                        <p className="mt-4 whitespace-pre-wrap leading-7">{item.content}</p>
                        {item.question_type === 'MULTIPLE_CHOICE' ? (
                          <div className="mt-5 space-y-2">
                            {(item.options ?? []).map((option, index) => {
                              const number = index + 1;
                              return <label key={number} className="flex cursor-pointer gap-3 rounded-xl border border-[#E9ECEF] p-4"><input type="radio" name={`retry-${item.question_id}`} checked={retryAnswers[item.question_id] === number} disabled={isChecked} onChange={() => setRetryAnswers((current) => ({ ...current, [item.question_id]: number }))} /><span>{number}. {option}</span></label>;
                            })}
                          </div>
                        ) : (
                          <textarea className="form-control mt-5" rows={4} disabled={isChecked} value={String(retryAnswers[item.question_id] ?? '')} onChange={(event) => setRetryAnswers((current) => ({ ...current, [item.question_id]: event.target.value }))} />
                        )}
                        {!isChecked ? (
                          <button type="button" className="primary-button mt-5" disabled={retryAnswers[item.question_id] == null || retryAnswers[item.question_id] === ''} onClick={() => setChecked((current) => ({ ...current, [item.question_id]: true }))}>정답 확인</button>
                        ) : (
                          <div className={`mt-5 rounded-xl p-4 ${isCorrect ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'}`}>
                            <strong>{isCorrect ? '정답입니다.' : `정답: ${answerLabel(item, false)}`}</strong>
                            <p className="mt-2 whitespace-pre-wrap text-sm">{item.explanation?.trim() || '등록된 해설이 없습니다.'}</p>
                          </div>
                        )}
                      </article>
                    );
                  })}
                </section>
              )}
            </>
          ) : null}
        </main>
        <Footer />
      </div>
    </ProtectedPage>
  );
}
