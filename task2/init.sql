CREATE TABLE call_records (

    id BIGSERIAL PRIMARY KEY,

    customer_phone TEXT NOT NULL,

    channel TEXT NOT NULL CHECK (channel IN ('voice','whatsapp','chat')),

    transcript TEXT NOT NULL,

    ai_response TEXT NOT NULL,

    intent TEXT NOT NULL,

    outcome TEXT NOT NULL CHECK (outcome IN ('resolved','escalated','failed')),

    confidence NUMERIC(3,2) NOT NULL
        CHECK (confidence >= 0 AND confidence <= 1),

    csat INTEGER
        CHECK (csat BETWEEN 1 AND 5),

    duration INTEGER NOT NULL,

    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_call_records_phone
ON call_records(customer_phone);

CREATE INDEX idx_call_records_timestamp
ON call_records(timestamp DESC);

CREATE INDEX idx_call_records_intent
ON call_records(intent);

SELECT
    intent,
    COUNT(*) AS total_calls,
    SUM(CASE WHEN outcome='resolved' THEN 1 ELSE 0 END)::float / COUNT(*) AS resolution_rate,
    AVG(csat) AS avg_csat
FROM call_records
WHERE timestamp >= NOW() - INTERVAL '7 days'
GROUP BY intent
ORDER BY resolution_rate ASC
LIMIT 5;
