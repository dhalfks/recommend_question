import { useRouter } from 'next/router';
import ExamPaperEditor from '@/components/ExamPaperEditor';

export default function EditExamPaperPage() {
  const router = useRouter();
  const raw = router.query.paperId;
  const paperId = typeof raw === 'string' ? Number(raw) : NaN;
  if (!router.isReady || !Number.isInteger(paperId) || paperId <= 0) return null;
  return <ExamPaperEditor paperId={paperId} />;
}
