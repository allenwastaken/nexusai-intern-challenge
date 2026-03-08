import asyncpg

class CallRecordRepository:

    def __init__(self, pool):
        self.pool = pool


    async def save(self, call_data: dict):

        query = """
        INSERT INTO call_records
        (
            customer_phone,
            channel,
            transcript,
            ai_response,
            intent,
            outcome,
            confidence,
            csat,
            duration
        )
        VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
        """

        async with self.pool.acquire() as conn:
            await conn.execute(
                query,
                call_data["customer_phone"],
                call_data["channel"],
                call_data["transcript"],
                call_data["ai_response"],
                call_data["intent"],
                call_data["outcome"],
                call_data["confidence"],
                call_data.get("csat"),
                call_data["duration"]
            )


    async def get_recent(self, phone: str, limit: int = 5) -> list:

        query = """
        SELECT *
        FROM call_records
        WHERE customer_phone = $1
        ORDER BY timestamp DESC
        LIMIT $2
        """

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, phone, limit)

        return [dict(r) for r in rows]
    
async def get_lowest_resolution_intents(pool):

    query = """
    SELECT
        intent,
        COUNT(*) AS total_calls,
        SUM(CASE WHEN outcome='resolved' THEN 1 ELSE 0 END)::float / COUNT(*) AS resolution_rate,
        AVG(csat) AS avg_csat
    FROM call_records
    WHERE timestamp >= NOW() - INTERVAL '7 days'
    GROUP BY intent
    ORDER BY resolution_rate ASC
    LIMIT 5
    """

    async with pool.acquire() as conn:
        rows = await conn.fetch(query)

    return [dict(r) for r in rows]
