-- 결제 데이터가 생성된 운영 환경에서는 이 파일을 그대로 실행하지 마세요.
-- 필요한 결제 및 감사 데이터를 먼저 보존한 뒤 역마이그레이션해야 합니다.

BEGIN;

DROP TABLE payment_webhook_events;
DROP TABLE ai_usage_events;
DROP TABLE payment_transactions;
DROP TABLE payment_orders;
DROP TABLE user_subscriptions;
DROP TABLE billing_plans;

COMMIT;
