# Task 1 

Function:

    handle_message(customer_message, customer_id, channel)

Returns:

-   response_text
-   confidence
-   suggested_action
-   channel_formatted_response
-   error

Features:

-   async API calls
-   timeout handling
-   rate‑limit retry
-   structured output parsing
-   channel-specific formatting

Run:

    python task1/message_handler.py


# Task 2 Database Schema

Defines the PostgreSQL table storing all customer interactions.

## Setup PostgreSQL

Start PostgreSQL:

    psql -U postgres

Create database:

    CREATE DATABASE telecom_ai;

Connect:

    \c telecom_ai

Run schema:

    psql -U postgres -d telecom_ai -f task2/schema.sql

Repository Methods

`repository.py` contains:

-   save(call_data)
-   get_recent(phone, limit=5)

Analytics Query

The function:

    get_lowest_resolution_intents(pool)

returns the top 5 intents with the lowest resolution rate in the last 7
days.



# Task 3 Async Parallel

Simulates retrieving customer information from multiple systems.

Mock systems:

-   CRM
-   Billing
-   Ticket history

Two execution modes:

Sequential:
    fetch_sequential(phone)

Parallel:
    fetch_parallel(phone)

Run:
    python task3/parallel_fetcher.py

Expected behavior:

Sequential runtime ≈ sum of delays
Parallel runtime ≈ slowest delay

# Task 4 Escalation System

Determines whether AI should handle the request or escalate to a human
agent.

Function:

    should_escalate(context, confidence_score, sentiment_score, intent)

Returns:

    (bool, reason)

Rules:

1.  confidence < 0.65 → escalate
2.  sentiment < -0.6 → escalate
3.  repeated intent > 3 times → escalate
4.  service cancellation → always escalate
5.  VIP + overdue billing → escalate
6.  incomplete data + confidence < 0.80 → escalate

Run tests:

    pytest task4/ -v
