# 🚀 Carbon — Autonomous AI Backend for Worker Pooled Insurance

> **Production-grade, event-driven micro-insurance platform** built with FastAPI + SQLModel.
> Designed for gig workers (delivery partners, ride-share drivers, freelancers) — fully autonomous from disruption detection to payout, with zero human intervention.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![SQLModel](https://img.shields.io/badge/SQLModel-0.0.14-orange)](https://sqlmodel.tiangolo.com)
[![Tests](https://img.shields.io/badge/Tests-14%2F14%20passing-brightgreen)](#-running-the-tests)
[![License](https://img.shields.io/badge/License-MIT-purple)](LICENSE)

---

## 📋 Table of Contents

1. [What is Carbon?](#-what-is-carbon)
2. [System Architecture](#️-system-architecture)
3. [Tech Stack](#-tech-stack)
4. [Project Structure](#-project-structure)
5. [Database Models](#️-database-models)
6. [Quick Start](#-quick-start)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Environment Setup (.env)](#environment-setup-env)
   - [Database Setup & Migration](#database-setup--migration)
   - [Running the Server](#running-the-server)
   - [Running with MySQL (Production)](#running-with-mysql-production)
7. [API Reference (44+ Endpoints)](#-api-reference-44-endpoints)
8. [Autonomous Lifecycle Flow](#-autonomous-insurance-lifecycle)
9. [AI & Risk Services](#-ai--risk-services)
10. [Response Standards](#️-response-standards--error-handling)
11. [Running the Tests](#-running-the-tests)
12. [Admin Dashboard Contract Alignment](#-admin-dashboard-contract-v10)
13. [Conclusion](#-conclusion)

---

## 🧠 What is Carbon?

Carbon is a **fully autonomous AI-driven backend** for pooled micro-insurance. Workers collectively pool their weekly premiums into a shared fund. When a disruption event occurs (e.g., heavy rain, platform outage), Carbon:

1. **Auto-detects** it via weather/platform APIs
2. **Identifies** all eligible, opted-in workers in the affected zone
3. **Runs AI risk + fraud scoring** on every claim
4. **Auto-approves & disburses** payouts from the pool — idempotently, with no duplicate risk
5. **Logs every transaction** in a full double-entry ledger
6. **Notifies** workers in real-time

> 🔥 The entire pipeline — from rain detection to cash in wallet — runs **automatically, every 60 seconds**, with no human in the loop.

---

## 🏗️ System Architecture

```mermaid
graph TD
    A[🌩️ Disruption: Weather / Platform] --> B[OrchestrationEngine background_monitor]
    B --> C[EligibilityService: opted-in + active?]
    C --> D[AIRiskService: risk_score 0–1]
    D --> E[FraudService: fraud_score 0–1]
    E --> F{Decision Engine}
    F -->|APPROVED| G[PayoutService: Idempotent debit from Pool]
    F -->|FRAUD_DETECTED| H[🚨 Flag & Notify]
    F -->|PENDING| I[📋 Manual Review Queue]
    G --> J[LedgerService: Double-entry record]
    J --> K[NotificationService: Push alert]
```

### Autonomous Background Loop
```
Server Startup
    └── OrchestrationEngine.background_monitor()  ← async task, runs forever
            ├── [every 60s] TriggerService.check_weather_disruption()
            ├── If disruption → run_automation_cycle()
            │       ├── Fetch all active workers
            │       ├── EligibilityService.check_eligibility(worker)
            │       └── ClaimService.process_auto_claim(worker, event_id)
            │               ├── AIRiskService.evaluate_risk()
            │               ├── FraudService.run_check()
            │               ├── Create Claim record (with event_id)
            │               └── If APPROVED → PayoutService.process_payout()
            └── Exponential backoff on errors (5s → 10s → ... → 300s max)
```

---

## 🔧 Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Framework | FastAPI | 0.109.0 |
| ORM | SQLModel (wraps SQLAlchemy) | 0.0.14 |
| Database (Dev) | SQLite | built-in |
| Database (Prod) | MySQL via PyMySQL | latest |
| Auth | JWT (`python-jose`) | 3.3.0 |
| Config | pydantic-settings + `.env` | 2.1.0 |
| HTTP Client | httpx | 0.26.0 |
| Migrations | Alembic | 1.13.1 |
| Tests | pytest | 9.0+ |
| Weather API | Open-Meteo | (free, no API key) |

---

## 📁 Project Structure

```
Code/
├── app/
│   ├── main.py                        ← FastAPI app + startup hook
│   ├── core/
│   │   ├── config.py                  ← Settings (reads .env)
│   │   ├── database.py                ← SQLAlchemy engine + session
│   │   ├── create_db.py               ← MySQL database creator
│   │   └── seed.py                    ← Seed demo workers & pool data
│   ├── models/
│   │   └── schemas.py                 ← 9 SQLModel ORM tables
│   ├── schemas/
│   │   └── api.py                     ← All Pydantic request/response models
│   ├── api/v1/
│   │   ├── api.py                     ← Master router
│   │   └── endpoints/
│   │       ├── auth.py                ← /auth/*
│   │       ├── workers.py             ← /workers/*
│   │       ├── policy.py              ← /policy/*
│   │       ├── pricing.py             ← /pricing/*
│   │       ├── pool.py                ← /pool/*
│   │       ├── trigger.py             ← /trigger/*
│   │       ├── claims.py              ← /claims/*
│   │       ├── fraud.py               ← /fraud/*
│   │       ├── risk.py                ← /risk/*
│   │       ├── payout.py              ← /payout/*
│   │       ├── ledger.py              ← /ledger/*
│   │       ├── notify.py              ← /notify/*
│   │       ├── analytics.py           ← /analytics/*
│   │       └── simulation.py          ← /simulation/*
│   ├── services/
│   │   ├── orchestration_service.py   ← 🧠 Central automation engine
│   │   ├── claims.py                  ← Claim pipeline (risk+fraud+payout)
│   │   ├── payout_service.py          ← Idempotent payout + pool debit
│   │   ├── pool.py                    ← Pool balance + ledger management
│   │   ├── fraud_service.py           ← Fraud score calculation
│   │   ├── ai_risk_service.py         ← Risk scoring + AI audit log
│   │   ├── trigger_service.py         ← Disruption detection (weather API)
│   │   ├── eligibility_service.py     ← Policy + activity gating
│   │   ├── notification_service.py    ← In-app notification dispatch
│   │   ├── analytics_service.py       ← Dashboard KPI aggregation
│   │   ├── pricing_service.py         ← Premium calculation
│   │   └── worker_service.py          ← Worker CRUD helpers
│   └── tests/
│       ├── test_api_contracts.py      ← 14-test contract suite (all passing)
│       ├── seed_data.py               ← Test data seeder
│       └── contract_test.py           ← Contract shape validators
├── carbon.db                          ← SQLite DB (dev)
├── test.db                            ← SQLite DB (test runner)
├── requirements.txt
├── .env                               ← Environment configuration
└── run_backend.bat                    ← Windows one-click start
```

---

## 🗄️ Database Models

9 tables, all managed by SQLModel ORM. Schema auto-created on first run.

| Table | Key Fields | Purpose |
|-------|-----------|---------|
| `Worker` | `id`, `phone`, `zone`, `weekly_income`, `balance`, `is_active` | Registered gig workers |
| `Policy` | `worker_id`, `is_opted_in`, `premium_amount`, `last_payment_date` | Insurance membership |
| `Pool` | `total_balance`, `last_audit_date` | Shared risk fund (singleton) |
| `Ledger` | `transaction_type`, `amount`, `worker_id`, `reference_id` | Double-entry audit trail |
| `Claim` | `worker_id`, `event_id`, `event_type`, `status`, `fraud_score`, `ai_risk_score` | Insurance claims |
| `Payout` | `claim_id`, `worker_id`, `amount`, `idempotency_key`, `status` | Processed payouts |
| `Notification` | `worker_id`, `title`, `message`, `type`, `status`, `retry_count` | In-app alerts |
| `AIRiskLog` | `prediction_id`, `risk_score`, `risk_category`, `top_factors` | AI decision audit |
| `EventLog` | `event_id`, `event_type`, `status`, `details` | Disruption cycle logs |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **pip**
- Git
- (Optional for production) MySQL 8.0+

---

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Mithun017/Carbon---Autonomous-AI-Backend-for-Worker-Pooled-Insurance.git
cd "Carbon---Autonomous-AI-Backend-for-Worker-Pooled-Insurance/Code"

# 2. Create a virtual environment (recommended)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

### Environment Setup (.env)

Create a `.env` file in the `Code/` directory (a template is already included):

```ini
# ─── Core ────────────────────────────────────────────────────────────────────
PROJECT_NAME="Carbon Backend"
SECRET_KEY="super-secret-key-change-me-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# ─── Database ─────────────────────────────────────────────────────────────────
# SQLite (development — no setup needed)
DATABASE_URL="sqlite:///./carbon.db"

# MySQL (production — uncomment and fill in your credentials)
# DATABASE_URL="mysql+pymysql://root:yourpassword@localhost:3306/carbon_db"

# ─── Behaviour ────────────────────────────────────────────────────────────────
MOCK_OTP=true        # true = any OTP accepted (dev mode); false = real SMS
DEBUG=true

# ─── External APIs ────────────────────────────────────────────────────────────
OPEN_METEO_URL="https://api.open-meteo.com/v1/forecast"

# ─── AI Thresholds ────────────────────────────────────────────────────────────
RISK_THRESHOLD_HIGH=0.8
FRAUD_THRESHOLD_HIGH=0.85
```

---

### Database Setup & Migration

Carbon uses **SQLModel** which auto-creates all tables on first startup. However, if you are upgrading an existing database (e.g., adding the new `event_id` column to `Claim`), you need to run the migration.

#### ✅ Option A — Fresh Start (Recommended for new clones)

Nothing special needed. Tables are created automatically when the server starts:

```bash
uvicorn app.main:app --reload
# Tables are created on startup via init_db()
```

#### ✅ Option B — Seed with Demo Data

After starting the server once (so tables exist), seed the database with test workers, a pool balance, and sample policies:

```bash
python -c "from app.core.database import SessionLocal; from app.core.seed import seed_data; 
session = SessionLocal().__enter__(); seed_data(session)"

# Or run the seed module directly if it exposes a main block:
python app/core/seed.py
```

#### ⚠️ Option C — Migrate Existing SQLite DB (schema update)

If you had a previous version of `carbon.db` and only need to add new columns without losing data:

```bash
python -c "
import sqlite3, os

for db_file in ['carbon.db', 'test.db']:
    if os.path.exists(db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('PRAGMA table_info(claim)')
        cols = [row[1] for row in cursor.fetchall()]
        if 'event_id' not in cols:
            cursor.execute('ALTER TABLE claim ADD COLUMN event_id VARCHAR NULL')
            conn.commit()
            print(f'{db_file}: migrated — event_id column added')
        else:
            print(f'{db_file}: already up to date')
        conn.close()
"
```

#### 🔧 Option D — MySQL (Production Setup)

```bash
# 1. Ensure MySQL is running and update DATABASE_URL in .env

# 2. Create the database (run once)
python app/core/create_db.py

# 3. Start the server — SQLModel will create all tables automatically
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

### Running the Server

```bash
# Development (auto-reload on file changes)
uvicorn app.main:app --reload --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Windows one-click (opens a terminal)
run_backend.bat
```

Once running:
- 📖 **Swagger UI (Interactive Docs)**: http://localhost:8000/docs
- 📘 **ReDoc**: http://localhost:8000/redoc
- ✅ **Health Check**: http://localhost:8000/

---

### Running with MySQL (Production)

1. Install and start MySQL 8.0
2. Update `.env`:
   ```ini
   DATABASE_URL="mysql+pymysql://root:yourpassword@localhost:3306/carbon_db"
   ```
3. Create the database:
   ```bash
   python app/core/create_db.py
   ```
4. Start the server — all tables are created automatically.

---

## 📮 API Reference (44+ Endpoints)

All endpoints return a standard `BaseResponse` envelope:

```json
{ "status": "success", "data": { ... } }
```

Base URL: `http://localhost:8000/api/v1`

---

### 1. 🔑 AUTH Service `/auth`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/login` | Login with phone + password/OTP → returns JWT pair |
| `POST` | `/auth/logout` | Invalidate current session |
| `POST` | `/auth/otp/send` | Send 6-digit OTP to phone |
| `POST` | `/auth/otp/verify` | Verify OTP → returns `access_token` + `refresh_token` |
| `POST` | `/auth/refresh` | Exchange refresh token for new access token |
| `GET` | `/auth/validate` | Check token validity, returns `user_id` |

**Example — OTP Verify:**
```json
POST /auth/otp/verify
{ "phone": "9988776655", "otp": "123456" }

→ { "status": "success", "data": { "verified": true, "access_token": "eyJ...", "refresh_token": "ref_..." } }
```

> ⚙️ `MOCK_OTP=true` in `.env` means **any 6-digit OTP is accepted** in development.

---

### 2. 👤 WORKER Service `/workers`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/workers/profile` | Create or update worker profile |
| `GET` | `/workers/{id}` | Get worker demographic + income data |
| `GET` | `/workers/status/{id}` | Get live activity status + zone |

**Example — Create Profile:**
```json
POST /workers/profile
{
  "user_id": "8031e51b-741a-4d43-8f0a-172183c5d799",
  "name": "Arjun Sharma",
  "phone": "9988776655",
  "zone": "MR-1"
}
```

---

### 3. 🧠 RISK Service `/risk`

AI-powered behavioral and environmental risk assessment. Each evaluation is logged to `AIRiskLog` for audit.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/risk/evaluate` | Run risk model → score (0–1), level, zone |
| `GET` | `/risk/health` | **Dynamic** DB check → `healthy` / `degraded` / `offline` |
| `GET` | `/risk/drift` | Model drift score (PSI/KS test simulation) |
| `POST` | `/risk/feedback` | Submit ground-truth feedback for model improvement |

**Example — Evaluate:**
```json
POST /risk/evaluate
{ "user_id": "...", "location": "12.97, 77.59", "activity_data": { "avg_speed": 45 } }

→ { "data": { "risk_score": 0.62, "risk_level": "MEDIUM", "risk_zone": "MEDIUM" } }
```

---

### 4. 💸 PRICING Service `/pricing`

Dynamic actuarial pricing: `premium = (weekly_income × 0.1 × risk_multiplier) + zone_surcharge`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/pricing/calculate` | Quote premium with full breakdown |
| `POST` | `/pricing/recalculate` | Recalculate from stored worker profile |

**Example — Calculate:**
```json
POST /pricing/calculate
{ "user_id": "...", "weekly_income": 1500.0, "risk_zone": "HIGH" }

→ { "data": { "premium": 380.0, "breakdown": { "base_rate": 150.0, "risk_multiplier": 2.2, "zone_surcharge": 50.0 } } }
```

---

### 5. 🛡️ POLICY Service `/policy`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/policy/create` | Issue policy + contribute premium to pool |
| `GET` | `/policy/{user_id}` | Get policy status, plan, premium |
| `POST` | `/policy/validate` | Check if policy is active (used by orchestrator) |
| `POST` | `/policy/cancel/{user_id}` | Terminate coverage (opt-out) |

**Example — Create Policy:**
```json
POST /policy/create
{ "user_id": "...", "premium": 250.0, "plan": "Carbon Gold" }

→ { "data": { "policy_id": "...", "status": "active", "premium": 250.0 } }
```

---

### 6. 🌩️ TRIGGER Service `/trigger`

The "Ear" of the system — ingests disruption signals and fires the autonomous pipeline.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/trigger/mock` | **SIMULATION**: Inject a disruption → runs full claim+payout cycle |
| `POST` | `/trigger/weather` | Ingest raw weather API signal |
| `GET` | `/trigger/active` | List active disruptions (includes `event_type` + `zone`) |
| `POST` | `/trigger/stop` | Gracefully end a disruption window |

**Example — Mock Disruption (triggers full pipeline!):**
```json
POST /trigger/mock
{ "event_type": "RAIN", "duration": "4h" }

→ { "data": { "event_id": "evt_a1b2c3d4", "event_type": "RAIN", "triggered": true } }
```

> 💡 This is the **fastest way to test the entire autonomous pipeline** — every opted-in worker gets a claim processed immediately.

---

### 7. 📄 CLAIMS Service `/claims`

The heart of autonomous settlement.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/claims/auto` | Trigger claims for ALL eligible workers for an event |
| `GET` | `/claims/{user_id}` | List user's claims with status + `event_id` |
| `GET` | `/claims/history/{user_id}` | Historical claim summary |

**Example — Auto Claims:**
```json
POST /claims/auto
{ "event_id": "evt_a1b2c3d4" }

→ { "data": { "claims_triggered": 42, "claims_created": 38 } }
```

**Claim Status Values:**

| Status | Meaning |
|--------|---------|
| `APPROVED` | Payout auto-processed |
| `PENDING` | High risk — manual review queue |
| `FRAUD_DETECTED` | Rejected — fraud score > 0.85 |

---

### 8. 🚨 FRAUD Service `/fraud`

Real-time integrity protection for the resource pool.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/fraud/check` | Run fraud analysis on a specific claim |
| `GET` | `/fraud/score/{user_id}` | Rolling fraud risk profile for a worker |
| `GET` | `/fraud/history/{user_id}` | Historical fraud check log |

**Fraud Score Logic:**
- Base score: `random(0.0, 0.3)` — simulates normal behavior
- High amount (> ₹1000): `+0.2` penalty
- 5% random spike: score jumps to `0.8–1.0` (simulates known fraudster)
- **Threshold**: `FRAUD_THRESHOLD_HIGH = 0.85` → auto-reject

---

### 9. 💰 PAYOUT Service `/payout`

Idempotent financial settlement from the shared pool.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/payout/{user_id}` | All payouts for a worker (with `paid_at` timestamp) |
| `POST` | `/payout/process` | Manually process payout for a specific claim |
| `POST` | `/payout/retry` | Retry a failed payout transaction |

**Idempotency Key**: `PAY-{claim_id}` — if a payout with this key already exists, it returns the existing record without double-processing.

---

### 10. 📖 LEDGER Service `/ledger`

Double-entry audit trail for all financial movements.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/ledger/{user_id}` | All premium + payout ledger entries for a worker |
| `POST` | `/ledger/entry` | Manual ledger entry (e.g., sponsor contribution) |
| `GET` | `/ledger/audit` | Global audit trail; filter by `transaction_id` |

**Transaction Types:** `PREMIUM`, `PAYOUT`, `CONTRIBUTION`, `WITHDRAW`

**Example — Manual Entry:**
```json
POST /ledger/entry
{ "transaction_data": { "type": "CONTRIBUTION", "amount": 50000.0, "source": "Govt Grant" } }
```

---

### 11. 🔔 NOTIFICATION Service `/notify`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/notify/{user_id}` | Notification history (newest first) |
| `POST` | `/notify/send` | Send custom message to a worker |
| `POST` | `/notify/retry` | Retry failed notification via fallback channel |

---

### 12. 📊 ANALYTICS Service `/analytics`

Executive dashboard for monitoring ecosystem health.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/analytics/dashboard` | **9-field KPI dashboard** (see below) |
| `GET` | `/analytics/timeseries` | 7-day claim + payout trend data |
| `GET` | `/analytics/zones` | Zone breakdown derived from `Worker.zone` DB field |

**Dashboard Response (all 9 fields):**
```json
GET /analytics/dashboard

{
  "status": "success",
  "data": {
    "total_workers": 120,
    "total_payout": 48500.0,
    "active_policies": 95,
    "pending_claims": 3,
    "approved_claims": 87,
    "rejected_claims": 5,
    "total_claims": 95,
    "system_health": "OPTIMAL",
    "last_updated": "2026-04-17T07:30:00.000000"
  }
}
```

**Zones Response (DB-derived):**
```json
GET /analytics/zones

{
  "data": [
    { "zone": "MR-1", "risk_level": "HIGH", "active_workers": 85 },
    { "zone": "GENERAL", "risk_level": "LOW", "active_workers": 35 }
  ]
}
```

---

### 13. 🌊 POOL Service `/pool`

Liquidity management for the shared worker fund.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/pool/status` | Current pool balance |
| `GET` | `/pool/ledger/{user_id}` | Worker's contribution vs. extraction ratio |

---

### 14. ⚡ SIMULATION Service `/simulation`

End-to-end scenario runner for demo and integration testing.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/simulation/run` | Full lifecycle: register → opt-in → trigger → payout |

---

## 🔄 Autonomous Insurance Lifecycle

Here is the complete step-by-step flow of what happens every 60 seconds:

```
1. [MONITOR]    background_monitor polls TriggerService.check_weather_disruption()
2. [DETECT]     25% chance of a WEATHER disruption (simulated; production = real API)
3. [ORCHESTRATE] OrchestrationEngine.run_automation_cycle(event_id, event_type)
4. [FIND]       Query all Workers WHERE is_active = TRUE
5. [GATE]       EligibilityService: skip workers without active Policy (is_opted_in)
6. [RISK]       AIRiskService.evaluate_risk() → logs to AIRiskLog table
7. [FRAUD]      FraudService.run_check() → fraud_score 0–1
8. [DECIDE]     fraud > 0.85 → FRAUD_DETECTED | risk > 0.8 → PENDING | else → APPROVED
9. [CLAIM]      Claim record created with event_id, status, fraud_score, ai_risk_score
10. [NOTIFY]    "Claim Initiated" notification sent to worker
11. [PAYOUT]    If APPROVED: PayoutService deducts from Pool → Ledger entry → "Payout Successful" notification
12. [LOG]       EventLog updated: COMPLETED with impacted worker count
```

---

## 🤖 AI & Risk Services

| Service | Logic | Threshold |
|---------|-------|-----------|
| **AIRiskService** | Random score (0.1–0.9), categorized LOW/MEDIUM/HIGH, premium multiplier: 1.0/1.1/1.25 | `RISK_THRESHOLD_HIGH = 0.80` |
| **FraudService** | Base random + high-amount penalty + 5% spike | `FRAUD_THRESHOLD_HIGH = 0.85` |
| **TriggerService** | 25% chance of WEATHER disruption per poll cycle (production: real Open-Meteo API) | — |

> ⚠️ **Note**: AI/Risk scoring is currently heuristic-based (engineered simulations). In production, replace with a trained ML model (e.g., XGBoost, sklearn pipeline) served via a microservice or FastAPI endpoint.

---

## 🛡️ Response Standards & Error Handling

All 44 endpoints return a standard `BaseResponse` envelope:

**Success (200 OK):**
```json
{ "status": "success", "data": { ... } }
```

**Client Error (4xx):**
```json
{ "status": "error", "message": "Worker not found", "data": null }
```

| Code | Meaning |
|------|---------|
| `200` | OK — request succeeded |
| `400` | Bad Request — payout already processed, etc. |
| `404` | Not Found — worker/claim/policy ID doesn't exist |
| `422` | Unprocessable Entity — Pydantic validation failure |
| `500` | Internal Server Error — unexpected exception |

---

## 🧪 Running the Tests

Carbon ships with a **14-test contract suite** that validates all major API endpoints against the Admin Dashboard contract shape.

```bash
# Make sure you are in the Code/ directory with venv active
cd Code

# Run all contract tests (14 tests)
python -m pytest app/tests/test_api_contracts.py -v

# Run with short traceback on failures
python -m pytest app/tests/test_api_contracts.py -v --tb=short

# Run a specific test
python -m pytest app/tests/test_api_contracts.py::test_analytics_endpoints -v
```

**Expected Output:**
```
app/tests/test_api_contracts.py::test_root                  PASSED  [  7%]
app/tests/test_api_contracts.py::test_auth_endpoints        PASSED  [ 14%]
app/tests/test_api_contracts.py::test_worker_endpoints      PASSED  [ 21%]
app/tests/test_api_contracts.py::test_risk_endpoints        PASSED  [ 28%]
app/tests/test_api_contracts.py::test_pricing_endpoints     PASSED  [ 35%]
app/tests/test_api_contracts.py::test_policy_endpoints      PASSED  [ 42%]
app/tests/test_api_contracts.py::test_trigger_endpoints     PASSED  [ 50%]
app/tests/test_api_contracts.py::test_claim_endpoints       PASSED  [ 57%]
app/tests/test_api_contracts.py::test_fraud_endpoints       PASSED  [ 64%]
app/tests/test_api_contracts.py::test_payout_endpoints      PASSED  [ 71%]
app/tests/test_api_contracts.py::test_ledger_endpoints      PASSED  [ 78%]
app/tests/test_api_contracts.py::test_notify_endpoints      PASSED  [ 85%]
app/tests/test_api_contracts.py::test_analytics_endpoints   PASSED  [ 92%]
app/tests/test_api_contracts.py::test_pool_endpoints        PASSED  [100%]

======================= 14 passed in ~14s =======================
```

> The test runner uses `test.db` (a separate SQLite file) — your main `carbon.db` is never touched during tests.

---

## 📐 Admin Dashboard Contract v1.0

This release aligns all endpoints with the **Admin Dashboard API Contract v1.0**. Key changes implemented:

| Gap | Fix Applied |
|-----|------------|
| `Claim` model missing `event_id` | Added `event_id: Optional[str]` field + SQLite migration |
| `TriggerMockData` missing `triggered` | Added `triggered: bool = True` + `event_type` to response |
| Analytics dashboard missing `system_health`, `last_updated` | `AnalyticsDashboardData` expanded to full 9-field shape |
| `GET /analytics/zones` was hardcoded | Now derives zones dynamically from `Worker.zone` DB field |
| `GET /risk/health` returned static string | Now performs real `AIRiskLog` DB query → `healthy`/`degraded`/`offline` |
| `POST /claims/auto` returned mock count | Now runs the real claim pipeline for all eligible workers |
| `payout.py` `AttributeError: processed_at` | Fixed to `created_at` (from `TimestampModel`) |
| `ledger.py` `NameError: uuid` | Added missing `import uuid` |
| `workers.py` `NameError: datetime` | Added missing `from datetime import datetime` |

---

## 🎯 Conclusion

Carbon is more than a backend — it's a **mission-critical financial ecosystem** designed to protect the world's most vulnerable workers. By combining **Autonomous AI Orchestration** with **Double-Entry Ledger Transparency** and **Idempotent Payout Safety**, the system eliminates the friction, bias, and delays of traditional insurance.

Whether it's a sudden rainstorm in a delivery zone or a complete platform outage, Carbon ensures the gig economy stays resilient — automatically, continuously, and transparently.

---

**👨‍💻 Developed by [Mithun](https://github.com/Mithun017)**
**📦 Repository**: [Carbon — Autonomous AI Backend](https://github.com/Mithun017/Carbon---Autonomous-AI-Backend-for-Worker-Pooled-Insurance)
