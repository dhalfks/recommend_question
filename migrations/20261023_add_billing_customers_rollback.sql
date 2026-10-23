-- 결제 요청이 시작된 환경에서는 customerKey 보존 정책을 확인한 뒤 실행하세요.

BEGIN;

DROP TABLE billing_customers;

COMMIT;
