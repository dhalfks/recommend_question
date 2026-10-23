BEGIN;

CREATE TABLE billing_customers (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    customer_key VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_billing_customers_user_id UNIQUE (user_id),
    CONSTRAINT uq_billing_customers_customer_key UNIQUE (customer_key),
    CONSTRAINT billing_customers_key_length CHECK (
        CHAR_LENGTH(customer_key) BETWEEN 10 AND 50
    ),
    CONSTRAINT billing_customers_key_format CHECK (
        customer_key ~ '^[A-Za-z0-9._=@-]+$'
    )
);

COMMIT;
