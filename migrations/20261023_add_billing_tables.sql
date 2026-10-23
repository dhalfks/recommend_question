BEGIN;

CREATE TABLE billing_plans (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    audience_role VARCHAR(20) NOT NULL,
    price BIGINT NOT NULL,
    currency CHAR(3) NOT NULL DEFAULT 'KRW',
    billing_period VARCHAR(20) NOT NULL,
    entitlement_days INTEGER NOT NULL,
    features JSONB NOT NULL DEFAULT '{}'::jsonb,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_billing_plans_code UNIQUE (code),
    CONSTRAINT billing_plans_code_not_blank CHECK (BTRIM(code) <> ''),
    CONSTRAINT billing_plans_audience_role_valid CHECK (
        audience_role IN ('STUDENT', 'PROFESSOR')
    ),
    CONSTRAINT billing_plans_price_positive CHECK (price > 0),
    CONSTRAINT billing_plans_currency_valid CHECK (currency = 'KRW'),
    CONSTRAINT billing_plans_period_valid CHECK (billing_period IN ('ONE_TIME', 'MONTHLY')),
    CONSTRAINT billing_plans_entitlement_days_positive CHECK (entitlement_days > 0),
    CONSTRAINT billing_plans_features_object CHECK (jsonb_typeof(features) = 'object')
);

CREATE TABLE user_subscriptions (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    plan_id BIGINT NOT NULL REFERENCES billing_plans(id) ON DELETE RESTRICT,
    status VARCHAR(20) NOT NULL,
    started_at TIMESTAMPTZ,
    current_period_start TIMESTAMPTZ,
    current_period_end TIMESTAMPTZ,
    cancel_at_period_end BOOLEAN NOT NULL DEFAULT FALSE,
    canceled_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT user_subscriptions_status_valid CHECK (
        status IN ('PENDING', 'ACTIVE', 'PAST_DUE', 'CANCELED', 'EXPIRED')
    ),
    CONSTRAINT user_subscriptions_period_valid CHECK (
        current_period_end IS NULL
        OR current_period_start IS NULL
        OR current_period_end > current_period_start
    )
);

CREATE TABLE payment_orders (
    id BIGSERIAL PRIMARY KEY,
    order_id VARCHAR(100) NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    plan_id BIGINT NOT NULL REFERENCES billing_plans(id) ON DELETE RESTRICT,
    subscription_id BIGINT REFERENCES user_subscriptions(id) ON DELETE RESTRICT,
    plan_code VARCHAR(50) NOT NULL,
    plan_name VARCHAR(100) NOT NULL,
    amount BIGINT NOT NULL,
    currency CHAR(3) NOT NULL DEFAULT 'KRW',
    status VARCHAR(20) NOT NULL DEFAULT 'READY',
    provider VARCHAR(20) NOT NULL DEFAULT 'TOSS',
    failure_code VARCHAR(100),
    failure_message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    paid_at TIMESTAMPTZ,
    canceled_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_payment_orders_order_id UNIQUE (order_id),
    CONSTRAINT payment_orders_amount_positive CHECK (amount > 0),
    CONSTRAINT payment_orders_currency_valid CHECK (currency = 'KRW'),
    CONSTRAINT payment_orders_status_valid CHECK (
        status IN ('READY', 'PAID', 'FAILED', 'CANCELED', 'REFUNDED')
    ),
    CONSTRAINT payment_orders_provider_valid CHECK (provider = 'TOSS')
);

CREATE TABLE payment_transactions (
    id BIGSERIAL PRIMARY KEY,
    payment_order_id BIGINT NOT NULL REFERENCES payment_orders(id) ON DELETE RESTRICT,
    provider_payment_id VARCHAR(200),
    transaction_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    amount BIGINT NOT NULL,
    currency CHAR(3) NOT NULL DEFAULT 'KRW',
    idempotency_key VARCHAR(100) NOT NULL,
    provider_response JSONB,
    failure_code VARCHAR(100),
    failure_message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_payment_transactions_idempotency_key UNIQUE (idempotency_key),
    CONSTRAINT payment_transactions_type_valid CHECK (
        transaction_type IN ('PAYMENT', 'REFUND')
    ),
    CONSTRAINT payment_transactions_status_valid CHECK (
        status IN ('PENDING', 'SUCCEEDED', 'FAILED')
    ),
    CONSTRAINT payment_transactions_amount_positive CHECK (amount > 0),
    CONSTRAINT payment_transactions_currency_valid CHECK (currency = 'KRW'),
    CONSTRAINT payment_transactions_provider_response_object CHECK (
        provider_response IS NULL OR jsonb_typeof(provider_response) = 'object'
    )
);

CREATE TABLE ai_usage_events (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    feature_code VARCHAR(50) NOT NULL,
    subscription_id BIGINT REFERENCES user_subscriptions(id) ON DELETE SET NULL,
    request_id VARCHAR(100) NOT NULL,
    input_tokens INTEGER,
    output_tokens INTEGER,
    status VARCHAR(20) NOT NULL,
    failure_code VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    CONSTRAINT uq_ai_usage_events_request_id UNIQUE (request_id),
    CONSTRAINT ai_usage_events_feature_valid CHECK (
        feature_code IN ('AI_EXPLANATION', 'CODE_REVIEW', 'QUESTION_GENERATION')
    ),
    CONSTRAINT ai_usage_events_status_valid CHECK (
        status IN ('STARTED', 'SUCCEEDED', 'FAILED')
    ),
    CONSTRAINT ai_usage_events_input_tokens_nonnegative CHECK (
        input_tokens IS NULL OR input_tokens >= 0
    ),
    CONSTRAINT ai_usage_events_output_tokens_nonnegative CHECK (
        output_tokens IS NULL OR output_tokens >= 0
    )
);

CREATE TABLE payment_webhook_events (
    id BIGSERIAL PRIMARY KEY,
    provider VARCHAR(20) NOT NULL DEFAULT 'TOSS',
    event_id VARCHAR(200) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'RECEIVED',
    payload JSONB NOT NULL,
    error_message TEXT,
    received_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    processed_at TIMESTAMPTZ,
    CONSTRAINT uq_payment_webhook_provider_event UNIQUE (provider, event_id),
    CONSTRAINT payment_webhook_provider_valid CHECK (provider = 'TOSS'),
    CONSTRAINT payment_webhook_status_valid CHECK (
        status IN ('RECEIVED', 'PROCESSED', 'FAILED')
    ),
    CONSTRAINT payment_webhook_payload_object CHECK (jsonb_typeof(payload) = 'object')
);

CREATE UNIQUE INDEX uq_payment_transactions_provider_payment_success
    ON payment_transactions (provider_payment_id, transaction_type)
    WHERE provider_payment_id IS NOT NULL AND status = 'SUCCEEDED';

CREATE UNIQUE INDEX uq_user_subscriptions_active_plan
    ON user_subscriptions (user_id, plan_id)
    WHERE status = 'ACTIVE';

CREATE INDEX idx_user_subscriptions_user_status_end
    ON user_subscriptions (user_id, status, current_period_end DESC);
CREATE INDEX idx_payment_orders_user_created
    ON payment_orders (user_id, created_at DESC);
CREATE INDEX idx_payment_orders_status_created
    ON payment_orders (status, created_at);
CREATE INDEX idx_payment_transactions_order_created
    ON payment_transactions (payment_order_id, created_at);
CREATE INDEX idx_ai_usage_events_user_feature_created
    ON ai_usage_events (user_id, feature_code, created_at DESC);
CREATE INDEX idx_payment_webhook_events_status_received
    ON payment_webhook_events (status, received_at);

INSERT INTO billing_plans (
    code,
    name,
    audience_role,
    price,
    currency,
    billing_period,
    entitlement_days,
    features
)
VALUES
    (
        'STUDENT_PRO',
        '학생 Pro 30일 이용권',
        'STUDENT',
        4900,
        'KRW',
        'ONE_TIME',
        30,
        '{"AI_EXPLANATION":{"daily_limit":50},"CODE_REVIEW":{"daily_limit":50}}'::jsonb
    ),
    (
        'TEACHER_PRO',
        '교수자 Pro 30일 이용권',
        'PROFESSOR',
        49000,
        'KRW',
        'ONE_TIME',
        30,
        '{"QUESTION_GENERATION":{"daily_limit":100},"CODE_REVIEW":{"daily_limit":100}}'::jsonb
    );

COMMIT;
