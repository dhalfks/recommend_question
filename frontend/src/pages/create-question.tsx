import { ChangeEvent, FormEvent, useEffect, useRef, useState } from 'react';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import ProtectedPage from '@/components/ProtectedPage';
import { filesAPI, questionsAPI, subjectsAPI } from '@/lib/api';

type Subject = { id: number; name: string };
type Tab = 'manual' | 'excel';

const initialForm = {
  subject_id: '', title: '', content: '', difficulty: 'MEDIUM',
  options: ['', '', '', ''], correct_answer: '0', explanation: '',
  code_snippet: '', answer_code_snippet: '', is_required: false,
};

function errorMessage(error: any, fallback: string) {
  const detail = error.response?.data?.detail;
  return typeof detail === 'string' ? detail : error.message || fallback;
}

export default function CreateQuestionPage() {
  const [tab, setTab] = useState<Tab>('manual');
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [form, setForm] = useState(initialForm);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [excelSubjectId, setExcelSubjectId] = useState('');
  const [excelFile, setExcelFile] = useState<File | null>(null);
  const [excelMessage, setExcelMessage] = useState('');
  const [excelError, setExcelError] = useState('');
  const [excelLoading, setExcelLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    subjectsAPI.getAll().then(({ data }) => setSubjects(data))
      .catch(() => setMessage('과목 목록을 불러오지 못했습니다.'));
  }, []);

  const updateOption = (index: number, value: string) => {
    const options = [...form.options]; options[index] = value; setForm({ ...form, options });
  };

  const submit = async (event: FormEvent) => {
    event.preventDefault(); setLoading(true); setMessage('');
    try {
      const hasOptions = form.options.some((option) => option.trim());
      if (hasOptions && form.options.some((option) => !option.trim())) {
        setMessage('객관식 문제는 선택지 4개를 모두 입력해 주세요.'); return;
      }
      await questionsAPI.create({
        ...form, subject_id: Number(form.subject_id),
        options: hasOptions ? JSON.stringify(form.options) : null,
        correct_answer: hasOptions ? form.correct_answer : null,
        code_snippet: form.code_snippet || null,
        answer_code_snippet: form.answer_code_snippet || null,
      });
      setForm({ ...initialForm, subject_id: form.subject_id });
      setMessage('문제가 성공적으로 등록되었습니다.');
    } catch (error: any) { setMessage(`문제 등록에 실패했습니다. ${errorMessage(error, '서버 연결을 확인해 주세요.')}`); }
    finally { setLoading(false); }
  };

  const selectExcel = (event: ChangeEvent<HTMLInputElement>) => {
    setExcelError(''); setExcelMessage('');
    const file = event.target.files?.[0] ?? null;
    if (file && !file.name.toLowerCase().endsWith('.xlsx')) {
      event.target.value = ''; setExcelFile(null); setExcelError('.xlsx 파일만 업로드할 수 있습니다.'); return;
    }
    setExcelFile(file);
  };

  const uploadExcel = async (event: FormEvent) => {
    event.preventDefault(); setExcelError(''); setExcelMessage('');
    if (!excelSubjectId) { setExcelError('등록할 과목을 선택해 주세요.'); return; }
    if (!excelFile) { setExcelError('업로드할 Excel 파일을 선택해 주세요.'); return; }
    setExcelLoading(true);
    try {
      const { data } = await filesAPI.uploadExcel(excelFile, Number(excelSubjectId));
      setExcelMessage(`${data.questions_created}개 문제가 DB에 등록되었습니다.`);
      setExcelFile(null); if (fileInputRef.current) fileInputRef.current.value = '';
    } catch (error: any) { setExcelError(errorMessage(error, 'Excel 업로드 중 오류가 발생했습니다.')); }
    finally { setExcelLoading(false); }
  };

  return <ProtectedPage roles={['PROFESSOR', 'ADMIN']}><div className="app-shell flex flex-col"><Navbar />
    <main className="mx-auto w-full max-w-3xl flex-1 px-4 py-12">
      <h1 className="text-4xl font-bold text-[#242C34]">문제 출제</h1>
      <p className="mt-3 text-[#6C757D]">직접 입력하거나 Excel 파일로 여러 문제를 한 번에 등록할 수 있습니다.</p>
      <div className="mt-8 flex border-b border-[#DCE3EA]" role="tablist">
        {([['manual', '직접 출제'], ['excel', 'Excel 업로드']] as const).map(([value, label]) =>
          <button key={value} type="button" role="tab" aria-selected={tab === value} onClick={() => setTab(value)}
            className={`px-6 py-3 font-bold ${tab === value ? 'border-b-2 border-[#3B86D1] text-[#2F70B5]' : 'text-[#6C757D]'}`}>{label}</button>)}
      </div>

      {tab === 'manual' ? <form onSubmit={submit} className="surface-card mt-6 space-y-6 p-8">
        <div className="grid gap-5 sm:grid-cols-2">
          <label className="text-sm font-semibold">과목<select required value={form.subject_id} onChange={(e) => setForm({ ...form, subject_id: e.target.value })} className="form-control mt-2"><option value="">과목 선택</option>{subjects.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}</select></label>
          <label className="text-sm font-semibold">난이도<select value={form.difficulty} onChange={(e) => setForm({ ...form, difficulty: e.target.value })} className="form-control mt-2"><option value="EASY">초급</option><option value="MEDIUM">중급</option><option value="HARD">고급</option><option value="EXPERT">전문가</option></select></label>
        </div>
        <label className="flex items-start gap-3 rounded-xl border border-[#F4C76A] bg-[#FFF9E8] p-4"><input type="checkbox" checked={form.is_required} onChange={(e) => setForm({ ...form, is_required: e.target.checked })} className="mt-1 h-4 w-4" /><span><strong className="block text-sm text-[#8A5A00]">필수 문제</strong><span className="mt-1 block text-xs text-[#7A6843]">랜덤 출제 시 일반 문제보다 먼저 포함됩니다.</span></span></label>
        <label className="block text-sm font-semibold">제목<input required value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} className="form-control mt-2" /></label>
        <label className="block text-sm font-semibold">문제 내용<textarea required rows={4} value={form.content} onChange={(e) => setForm({ ...form, content: e.target.value })} className="form-control mt-2" /></label>
        <label className="block text-sm font-semibold">문제 소스 코드<textarea rows={8} value={form.code_snippet} onChange={(e) => setForm({ ...form, code_snippet: e.target.value })} className="form-control mt-2 font-mono text-sm" placeholder="필요한 경우 입력하세요." spellCheck={false} /></label>
        <fieldset><legend className="mb-3 text-sm font-semibold">선택지와 정답</legend><div className="space-y-3">{form.options.map((option, index) => <label key={index} className="flex items-center gap-3"><input type="radio" name="correct" checked={form.correct_answer === String(index)} onChange={() => setForm({ ...form, correct_answer: String(index) })} /><input value={option} onChange={(e) => updateOption(index, e.target.value)} className="form-control" placeholder={`${index + 1}번 선택지`} /></label>)}</div></fieldset>
        <label className="block text-sm font-semibold">해설<textarea rows={4} value={form.explanation} onChange={(e) => setForm({ ...form, explanation: e.target.value })} className="form-control mt-2" /></label>
        <label className="block text-sm font-semibold">정답 소스 코드<textarea rows={8} value={form.answer_code_snippet} onChange={(e) => setForm({ ...form, answer_code_snippet: e.target.value })} className="form-control mt-2 font-mono text-sm" placeholder="모범 답안 코드를 입력할 수 있습니다." spellCheck={false} /></label>
        {message && <p className="rounded-lg bg-blue-50 p-3 text-sm text-[#2F70B5]">{message}</p>}
        <button disabled={loading} className="primary-button w-full">{loading ? '등록 중...' : '문제 등록'}</button>
      </form> : <section className="surface-card mt-6 p-8">
        <h2 className="text-xl font-bold">Excel로 문제 일괄 등록</h2>
        <p className="mt-2 text-sm leading-6 text-[#6C757D]">sample.xlsx의 열 이름과 형식을 유지한 뒤 문제 행을 작성해 주세요. 오류가 있는 경우 전체 등록이 취소됩니다.</p>
        <a href={filesAPI.excelTemplateUrl()} download="sample.xlsx" className="mt-4 inline-block text-sm font-bold text-[#2F70B5] underline">sample.xlsx 다운로드</a>
        <form onSubmit={uploadExcel} className="mt-6 space-y-6">
          <label className="block text-sm font-semibold">등록할 과목<select required value={excelSubjectId} onChange={(e) => setExcelSubjectId(e.target.value)} className="form-control mt-2"><option value="">과목 선택</option>{subjects.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}</select></label>
          <label className="block text-sm font-semibold">Excel 파일<input ref={fileInputRef} type="file" accept=".xlsx,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" onChange={selectExcel} className="mt-2 block w-full rounded-xl border border-[#DCE3EA] p-3 text-sm file:mr-4 file:rounded-lg file:border-0 file:bg-[#3B86D1] file:px-4 file:py-2 file:font-semibold file:text-white" /></label>
          {excelFile && <p className="rounded-lg bg-[#F3F7FB] p-3 text-sm">선택 파일: <strong>{excelFile.name}</strong> ({(excelFile.size / 1024).toFixed(1)} KB)</p>}
          {excelError && <p className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{excelError}</p>}
          {excelMessage && <p className="rounded-lg border border-green-200 bg-green-50 p-3 text-sm font-semibold text-green-700">{excelMessage}</p>}
          <button disabled={excelLoading} className="primary-button w-full">{excelLoading ? '등록 중...' : 'Excel 문제 DB 등록'}</button>
        </form>
      </section>}
    </main><Footer /></div></ProtectedPage>;
}
