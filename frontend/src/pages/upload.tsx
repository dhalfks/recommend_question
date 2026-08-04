import { useEffect, useState } from 'react';
import Footer from '@/components/Footer';
import Navbar from '@/components/Navbar';
import ProtectedPage from '@/components/ProtectedPage';
import { filesAPI, subjectsAPI } from '@/lib/api';

type CreatedQuestion = {
  id: number; title: string; content: string; difficulty: string; options: string[];
  correct_option: number; correct_answer: string; explanation: string; source_file: string;
};
type UploadResult = { file_name: string; questions_generated: number; message: string; questions: CreatedQuestion[] };

const allowedExtensions = ['.java', '.js', '.sql', '.txt', '.md'];
const difficultyLabels: Record<string, string> = { EASY: '초급', MEDIUM: '중급', HARD: '고급', EXPERT: '전문가' };

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [subjectId, setSubjectId] = useState('');
  const [subjects, setSubjects] = useState<Array<{ id: number; name: string }>>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<UploadResult | null>(null);

  useEffect(() => { subjectsAPI.getAll().then(({ data }) => setSubjects(data)).catch(() => setError('과목 목록을 불러오지 못했습니다.')); }, []);

  const selectFile = (event: React.ChangeEvent<HTMLInputElement>) => {
    const nextFile = event.target.files?.[0] ?? null;
    setError(''); setResult(null);
    if (!nextFile) { setFile(null); return; }
    const extension = `.${nextFile.name.split('.').pop()?.toLowerCase()}`;
    if (!allowedExtensions.includes(extension)) {
      setFile(null); event.target.value = '';
      setError(`지원하지 않는 파일입니다. ${allowedExtensions.join(', ')} 형식만 업로드할 수 있습니다.`);
      return;
    }
    if (nextFile.size > 10 * 1024 * 1024) {
      setFile(null); event.target.value = ''; setError('파일 크기는 10MB 이하여야 합니다.'); return;
    }
    setFile(nextFile);
  };

  const upload = async (event: React.FormEvent) => {
    event.preventDefault(); setError(''); setResult(null);
    if (!subjectId) { setError('과목을 선택해 주세요.'); return; }
    if (!file) { setError('문제를 만들 파일을 선택해 주세요.'); return; }
    setLoading(true);
    try {
      const response = await filesAPI.uploadCode(file, Number(subjectId), true);
      setResult(response.data); setFile(null);
      const input = document.getElementById('question-file') as HTMLInputElement | null;
      if (input) input.value = '';
    } catch (uploadError: any) {
      setError(uploadError.response?.data?.detail ?? uploadError.message ?? '문제 생성 중 오류가 발생했습니다.');
    } finally { setLoading(false); }
  };

  return <ProtectedPage roles={['PROFESSOR', 'ADMIN']}><div className="app-shell flex flex-col"><Navbar />
    <main className="page-container flex-1 py-10"><div className="mx-auto max-w-4xl">
      <div className="mb-8"><p className="font-semibold text-[#3B86D1]">AI 문제 생성</p><h1 className="mt-1 text-3xl font-bold text-[#242C34]">문제 업로드</h1><p className="mt-2 text-[#6C757D]">파일 내용을 OpenAI가 분석하여 관련 문제, 정답과 해설을 생성하고 DB에 등록합니다.</p></div>
      <section className="surface-card p-6 sm:p-8"><form onSubmit={upload} className="space-y-6">
        <div><label htmlFor="subject" className="mb-2 block text-sm font-bold">등록할 과목</label><select id="subject" className="form-control" value={subjectId} onChange={(event) => setSubjectId(event.target.value)}><option value="">과목을 선택해 주세요</option>{subjects.map((subject) => <option key={subject.id} value={subject.id}>{subject.name}</option>)}</select></div>
        <div><label htmlFor="question-file" className="mb-2 block text-sm font-bold">문제 생성 파일</label><div className="rounded-2xl border-2 border-dashed border-[#B9C6D2] bg-[#F8FAFC] p-7 text-center"><input id="question-file" type="file" accept={allowedExtensions.join(',')} onChange={selectFile} className="block w-full text-sm file:mr-4 file:rounded-xl file:border-0 file:bg-[#3B86D1] file:px-5 file:py-3 file:font-semibold file:text-white hover:file:bg-[#2F70B5]" />{file && <p className="mt-4 font-semibold text-[#245E96]">선택됨: {file.name} · {(file.size / 1024).toFixed(1)}KB</p>}</div><p className="mt-2 text-sm text-[#6C757D]">지원 형식: .java, .js, .sql, .txt, .md · 최대 10MB</p></div>
        {error && <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}
        <button type="submit" disabled={loading} className="primary-button w-full">{loading ? <><span className="mr-2 inline-block h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white" />OpenAI가 파일을 분석하는 중...</> : '문제 업로드 및 AI 자동 생성'}</button>
        {loading && <p className="text-center text-sm text-[#6C757D]">파일 내용에 따라 생성에 시간이 걸릴 수 있습니다. 창을 닫지 마세요.</p>}
      </form></section>

      {result && <section className="mt-8"><div className="mb-5 rounded-2xl border border-[#BFE6B7] bg-[#F3FBF1] p-5"><p className="font-bold text-[#168A04]">등록 완료</p><p className="mt-1 text-sm text-[#3E6A36]">{result.message}</p></div><div className="mb-4 flex items-center justify-between"><h2 className="text-2xl font-bold">등록된 문제</h2><span className="rounded-full bg-[#EAF3FC] px-3 py-1 text-sm font-bold text-[#245E96]">{result.questions_generated}개</span></div><div className="space-y-5">{result.questions.map((question, index) => <article key={question.id} className="surface-card overflow-hidden"><div className="border-b bg-[#F8F9FA] px-6 py-4"><div className="flex flex-wrap items-center gap-2"><span className="rounded-full bg-[#3B86D1] px-2.5 py-1 text-xs font-bold text-white">문제 {index + 1}</span><span className="rounded-full bg-[#E9ECEF] px-2.5 py-1 text-xs font-semibold">{difficultyLabels[question.difficulty] ?? question.difficulty}</span><span className="text-xs text-[#6C757D]">DB ID {question.id}</span></div><h3 className="mt-3 text-lg font-bold">{question.title}</h3></div><div className="p-6"><p className="whitespace-pre-wrap leading-7">{question.content}</p><ol className="mt-5 grid gap-2 sm:grid-cols-2">{question.options.map((option, optionIndex) => <li key={optionIndex} className={`rounded-xl border p-3 text-sm ${optionIndex + 1 === question.correct_option ? 'border-[#21BF06] bg-green-50 font-bold text-[#168A04]' : 'border-[#E9ECEF]'}`}>{optionIndex + 1}. {option}{optionIndex + 1 === question.correct_option && ' ✓ 정답'}</li>)}</ol><div className="mt-5 rounded-xl bg-[#F3F7FB] p-4"><p className="text-sm font-bold text-[#245E96]">정답 해설</p><p className="mt-2 whitespace-pre-wrap text-sm leading-6">{question.explanation}</p></div></div></article>)}</div></section>}
    </div></main><Footer /></div></ProtectedPage>;
}
