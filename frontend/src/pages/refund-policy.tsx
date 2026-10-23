import Footer from '@/components/Footer';
import Navbar from '@/components/Navbar';

export default function RefundPolicyPage() {
  return (
    <div className="app-shell flex min-h-screen flex-col">
      <Navbar />
      <main className="page-container flex-1 py-12">
        <article className="surface-card mx-auto max-w-3xl space-y-7 p-8 text-[#495057]">
          <div><p className="font-semibold text-[#3B86D1]">결제 정책</p><h1 className="mt-1 text-3xl font-bold text-[#242C34]">환불 및 이용권 취소 정책</h1><p className="mt-2 text-sm">시행일: 2026년 10월 23일</p></div>
          <section><h2 className="text-xl font-bold text-[#242C34]">1. 적용 대상</h2><p className="mt-2">학생 Pro 및 교수자 Pro 30일 이용권과 이에 포함된 유료 AI 기능에 적용됩니다. 현재 상품은 자동 갱신되지 않습니다.</p></section>
          <section><h2 className="text-xl font-bold text-[#242C34]">2. 기본 전액 환불</h2><p className="mt-2">결제 후 7일 이내이며 해당 결제 이후 유료 AI 기능을 사용하지 않은 경우 전액 환불 기준에 해당합니다. 환불이 완료되면 해당 주문으로 추가된 30일 이용 기간이 회수됩니다.</p></section>
          <section><h2 className="text-xl font-bold text-[#242C34]">3. 관리자 검토</h2><p className="mt-2">7일이 지났거나 유료 AI 기능을 사용한 경우에도 자동으로 환불을 거절하지 않습니다. 이용 내역, 상품 제공 상태 및 관계 법령을 확인해 처리합니다. 현재 부분 환불은 자동 계산하지 않습니다.</p></section>
          <section><h2 className="text-xl font-bold text-[#242C34]">4. 예외 사유</h2><p className="mt-2">중복 결제, 과오 청구, 표시·광고 또는 계약 내용과 다른 제공, 서비스 장애로 유료 기능을 정상 이용하지 못한 경우에는 확인 후 취소·환불 또는 적절한 조치를 제공합니다.</p></section>
          <section><h2 className="text-xl font-bold text-[#242C34]">5. 처리 시점</h2><p className="mt-2">서비스에서 환불 처리가 완료된 뒤 실제 카드 승인 취소가 반영되는 시점은 결제수단과 카드사 일정에 따라 달라질 수 있습니다. 계약 및 청약철회 관련 기록은 관계 법령에 따라 보존합니다.</p></section>
          <section><h2 className="text-xl font-bold text-[#242C34]">6. 법령 우선</h2><p className="mt-2">본 정책은 관계 법령이 보장하는 청약철회 및 환불 권리를 제한하지 않습니다. 정책과 관계 법령이 충돌하는 경우 관계 법령을 우선 적용합니다.</p></section>
          <p className="rounded-xl bg-amber-50 p-4 text-sm text-amber-900">운영 공개 전 사업자 정보, 고객센터 접수 방법 및 실제 상품 제공 방식에 맞춘 법률 검토가 필요합니다.</p>
        </article>
      </main>
      <Footer />
    </div>
  );
}
