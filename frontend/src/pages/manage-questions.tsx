import { FormEvent, useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import Footer from '@/components/Footer';
import Navbar from '@/components/Navbar';
import ProtectedPage from '@/components/ProtectedPage';
import { questionsAPI, subjectsAPI } from '@/lib/api';

type Subject = { id: number; name: string };
type Question = {
  id: number; subject_id: number; title: string; content: string;
  difficulty: string; options?: string | null; correct_answer?: string | null;
  correct_option?: number | null; explanation?: string | null; subject_unit?: string | null;
  code_snippet?: string | null; answer_code_snippet?: string | null; is_required: boolean;
};

const difficultyLabels: Record<string, string> = {
  EASY: '초급', MEDIUM: '중급', HARD: '고급', EXPERT: '전문가',
};

function parseOptions(value?: string | null) {
  if (!value) return ['', '', '', ''];
  try {
    const parsed = JSON.parse(value);
    return Array.isArray(parsed) ? [...parsed.map(String), '', '', '', ''].slice(0, 4) : ['', '', '', ''];
  } catch { return ['', '', '', '']; }
}

function messageFrom(error: any, fallback: string) {
  const detail = error.response?.data?.detail;
  return typeof detail === 'string' ? detail : fallback;
}

export default function ManageQuestionsPage() {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [filters, setFilters] = useState({ search: '', subject: '', difficulty: '' });
  const [editing, setEditing] = useState<Question | null>(null);
  const [form, setForm] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [notice, setNotice] = useState('');

  const load = async () => {
    setLoading(true); setNotice('');
    try {
      const [questionResult, subjectResult] = await Promise.all([
        questionsAPI.getAll({ limit: 1000 }), subjectsAPI.getAll(),
      ]);
      setQuestions(questionResult.data); setSubjects(subjectResult.data);
    } catch (error: any) { setNotice(messageFrom(error, '문제 목록을 불러오지 못했습니다.')); }
    finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const visible = useMemo(() => questions.filter((question) => {
    const keyword = filters.search.trim().toLocaleLowerCase();
    return (!keyword || `${question.title} ${question.content} ${question.subject_unit ?? ''}`.toLocaleLowerCase().includes(keyword))
      && (!filters.subject || question.subject_id === Number(filters.subject))
      && (!filters.difficulty || question.difficulty === filters.difficulty);
  }), [filters, questions]);

  const openEdit = (question: Question) => {
    const answerIndex = question.correct_option
      ? question.correct_option - 1
      : Number.isInteger(Number(question.correct_answer)) ? Number(question.correct_answer) : 0;
    setEditing(question);
    setForm({
      subject_id: String(question.subject_id), title: question.title, content: question.content,
      subject_unit: question.subject_unit ?? '', difficulty: question.difficulty,
      options: parseOptions(question.options), correct_answer: String(Math.max(0, Math.min(3, answerIndex))),
      explanation: question.explanation ?? '', code_snippet: question.code_snippet ?? '',
      answer_code_snippet: question.answer_code_snippet ?? '', is_required: question.is_required,
    });
    setNotice('');
  };

  const save = async (event: FormEvent) => {
    event.preventDefault();
    if (!editing || !form) return;
    const hasOptions = form.options.some((option: string) => option.trim());
    if (hasOptions && form.options.some((option: string) => !option.trim())) {
      setNotice('객관식 문제는 선택지 4개를 모두 입력해 주세요.'); return;
    }
    setSaving(true); setNotice('');
    try {
      const answerIndex = Number(form.correct_answer);
      const { data } = await questionsAPI.update(editing.id, {
        subject_id: Number(form.subject_id), title: form.title, content: form.content,
        subject_unit: form.subject_unit || null, difficulty: form.difficulty,
        options: hasOptions ? JSON.stringify(form.options) : null,
        correct_answer: hasOptions ? String(answerIndex) : null,
        correct_option: hasOptions ? answerIndex + 1 : null,
        explanation: form.explanation || null, code_snippet: form.code_snippet || null,
        answer_code_snippet: form.answer_code_snippet || null, is_required: form.is_required,
      });
      setQuestions((current) => current.map((question) => question.id === editing.id ? data : question));
      setEditing(null); setForm(null); setNotice('문제를 수정했습니다.');
    } catch (error: any) { setNotice(messageFrom(error, '문제 수정에 실패했습니다.')); }
    finally { setSaving(false); }
  };

  const remove = async (question: Question) => {
    if (!window.confirm(`“${question.title}” 문제를 삭제할까요? 삭제 후 복구할 수 없습니다.`)) return;
    setNotice('');
    try {
      await questionsAPI.delete(question.id);
      setQuestions((current) => current.filter((item) => item.id !== question.id));
      setNotice('문제를 삭제했습니다.');
    } catch (error: any) { setNotice(messageFrom(error, '문제 삭제에 실패했습니다.')); }
  };

  const subjectName = (id: number) => subjects.find((subject) => subject.id === id)?.name ?? `과목 ${id}`;

  return <ProtectedPage roles={['PROFESSOR', 'ADMIN']}><div className="app-shell flex flex-col"><Navbar />
    <main className="page-container flex-1 py-10">
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end"><div><p className="font-semibold text-[#3B86D1]">교수자 전용</p><h1 className="mt-1 text-3xl font-bold">문제 관리</h1><p className="mt-2 text-[#6C757D]">교수자는 본인이 등록한 문제만 조회·수정·삭제할 수 있습니다.</p></div><Link href="/create-question" className="primary-button text-center">새 문제 출제</Link></div>
      <section className="surface-card mt-7 grid gap-3 p-4 md:grid-cols-[1.5fr_1fr_1fr]"><input className="form-control" placeholder="제목·내용·소제목 검색" value={filters.search} onChange={(e) => setFilters({ ...filters, search: e.target.value })} /><select className="form-control" value={filters.subject} onChange={(e) => setFilters({ ...filters, subject: e.target.value })}><option value="">전체 과목</option>{subjects.map((subject) => <option key={subject.id} value={subject.id}>{subject.name}</option>)}</select><select className="form-control" value={filters.difficulty} onChange={(e) => setFilters({ ...filters, difficulty: e.target.value })}><option value="">전체 난이도</option>{Object.entries(difficultyLabels).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></section>
      {notice && <p className="mt-4 rounded-xl border border-[#CFE1F3] bg-[#F3F8FD] p-4 text-sm text-[#245E96]">{notice}</p>}
      <section className="surface-card mt-5 overflow-hidden"><div className="overflow-x-auto"><table className="w-full min-w-[820px] text-left text-sm"><thead className="bg-[#F2F5F7] text-[#5E6872]"><tr><th className="px-5 py-4">문제</th><th className="px-4 py-4">과목</th><th className="px-4 py-4">난이도</th><th className="px-4 py-4">구분</th><th className="px-5 py-4 text-right">관리</th></tr></thead><tbody>
        {loading ? <tr><td colSpan={5} className="p-14 text-center text-[#6C757D]">문제를 불러오는 중...</td></tr> : !visible.length ? <tr><td colSpan={5} className="p-14 text-center text-[#6C757D]">조건에 맞는 문제가 없습니다.</td></tr> : visible.map((question) => <tr key={question.id} className="border-t border-[#E9ECEF]"><td className="max-w-[420px] px-5 py-4"><strong className="block truncate">#{question.id} · {question.title}</strong><span className="mt-1 block truncate text-[#6C757D]">{question.content}</span>{question.subject_unit && <span className="mt-1 block text-xs text-[#3B86D1]">{question.subject_unit}</span>}</td><td className="px-4 py-4">{subjectName(question.subject_id)}</td><td className="px-4 py-4"><span className="rounded-full bg-[#EEF1F4] px-2 py-1 text-xs">{difficultyLabels[question.difficulty] ?? question.difficulty}</span></td><td className="px-4 py-4">{question.is_required ? <span className="font-semibold text-[#B26A00]">필수</span> : '일반'}</td><td className="px-5 py-4"><div className="flex justify-end gap-2"><button type="button" onClick={() => openEdit(question)} className="rounded-lg bg-[#EAF3FC] px-3 py-2 font-semibold text-[#2F70B5]">수정</button><button type="button" onClick={() => remove(question)} className="rounded-lg bg-red-50 px-3 py-2 font-semibold text-red-700">삭제</button></div></td></tr>)}</tbody></table></div><div className="border-t border-[#E9ECEF] px-5 py-4 text-sm text-[#6C757D]">전체 {questions.length}문제 중 {visible.length}문제 표시</div></section>
    </main><Footer />
    {editing && form && <div className="fixed inset-0 z-[60] flex justify-end bg-black/35" onClick={() => setEditing(null)}><aside className="h-full w-full max-w-2xl overflow-y-auto bg-white p-6 shadow-2xl sm:p-8" onClick={(event) => event.stopPropagation()}><div className="flex items-start justify-between gap-4"><div><p className="text-sm font-semibold text-[#3B86D1]">문제 #{editing.id}</p><h2 className="mt-1 text-2xl font-bold">문제 수정</h2></div><button type="button" className="rounded-lg bg-[#EEF1F4] px-3 py-2" onClick={() => setEditing(null)}>닫기</button></div><form onSubmit={save} className="mt-7 space-y-5"><div className="grid gap-4 sm:grid-cols-2"><label className="text-sm font-semibold">과목<select required className="form-control mt-2" value={form.subject_id} onChange={(e) => setForm({ ...form, subject_id: e.target.value })}>{subjects.map((subject) => <option key={subject.id} value={subject.id}>{subject.name}</option>)}</select></label><label className="text-sm font-semibold">난이도<select className="form-control mt-2" value={form.difficulty} onChange={(e) => setForm({ ...form, difficulty: e.target.value })}>{Object.entries(difficultyLabels).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label></div><label className="block text-sm font-semibold">소제목<input className="form-control mt-2" value={form.subject_unit} onChange={(e) => setForm({ ...form, subject_unit: e.target.value })} /></label><label className="block text-sm font-semibold">제목<input required className="form-control mt-2" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} /></label><label className="block text-sm font-semibold">문제 내용<textarea required rows={5} className="form-control mt-2" value={form.content} onChange={(e) => setForm({ ...form, content: e.target.value })} /></label><label className="flex gap-3 rounded-xl bg-[#FFF9E8] p-4 text-sm font-semibold"><input type="checkbox" checked={form.is_required} onChange={(e) => setForm({ ...form, is_required: e.target.checked })} />필수 문제로 지정</label><fieldset><legend className="mb-3 text-sm font-semibold">선택지와 정답</legend><div className="space-y-3">{form.options.map((option: string, index: number) => <label key={index} className="flex items-center gap-3"><input type="radio" name="edit-correct" checked={form.correct_answer === String(index)} onChange={() => setForm({ ...form, correct_answer: String(index) })} /><input className="form-control" value={option} placeholder={`${index + 1}번 선택지`} onChange={(e) => { const options = [...form.options]; options[index] = e.target.value; setForm({ ...form, options }); }} /></label>)}</div></fieldset><label className="block text-sm font-semibold">해설<textarea rows={4} className="form-control mt-2" value={form.explanation} onChange={(e) => setForm({ ...form, explanation: e.target.value })} /></label><label className="block text-sm font-semibold">문제 소스 코드<textarea rows={6} className="form-control mt-2 font-mono text-sm" value={form.code_snippet} onChange={(e) => setForm({ ...form, code_snippet: e.target.value })} spellCheck={false} /></label><label className="block text-sm font-semibold">정답 소스 코드<textarea rows={6} className="form-control mt-2 font-mono text-sm" value={form.answer_code_snippet} onChange={(e) => setForm({ ...form, answer_code_snippet: e.target.value })} spellCheck={false} /></label><div className="flex gap-3"><button type="button" className="w-full rounded-xl border border-[#DCE3EA] px-4 py-3 font-bold" onClick={() => setEditing(null)}>취소</button><button disabled={saving} className="primary-button w-full">{saving ? '저장 중...' : '변경사항 저장'}</button></div></form></aside></div>}
  </div></ProtectedPage>;
}
