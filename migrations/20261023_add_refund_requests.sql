BEGIN;

CREATE TABLE refund_requests (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES payment_orders(id) ON DELETE RESTRICT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    reason TEXT NOT NULL,
    eligibility_snapshot JSONB NOT NULL,
    decision_reason TEXT,
    reviewed_by INTEGER REFERENCES users(id) ON DELETE RESTRICT,
    refund_transaction_id BIGINT REFERENCES payment_transactions(id) ON DELETE RESTRICT,
    requested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    reviewed_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT refund_requests_status_valid
        CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED')),
    CONSTRAINT refund_requests_reason_not_blank CHECK (BTRIM(reason) <> ''),
    CONSTRAINT refund_requests_snapshot_object
        CHECK (jsonb_typeof(eligibility_snapshot) = 'object'),
    CONSTRAINT refund_requests_decision_consistent CHECK (
        (status = 'PENDING' AND reviewed_by IS NULL AND reviewed_at IS NULL)
        OR
        (status IN ('APPROVED', 'REJECTED') AND reviewed_by IS NOT NULL AND reviewed_at IS NOT NULL)
    )
);

CREATE UNIQUE INDEX uq_refund_requests_pending_order
    ON refund_requests (order_id)
    WHERE status = 'PENDING';
CREATE INDEX idx_refund_requests_user_requested
    ON refund_requests (user_id, requested_at DESC);
CREATE INDEX idx_refund_requests_status_requested
    ON refund_requests (status, requested_at);

COMMIT;
