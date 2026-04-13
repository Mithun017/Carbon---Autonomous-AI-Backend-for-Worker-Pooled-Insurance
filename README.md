# 🚀 Carbon - Autonomous AI Backend for Worker Pooled Insurance

Carbon is a production-grade, event-driven financial insurance backend designed for modern worker ecosystems. It automates the entire lifecycle of a claim—from disruption detection to idempotent payout—with zero human intervention.

---

## 🏗️ Architecture

The project follows a **Modular Monolith** architecture with clearly defined domain boundaries:
- **`/app/api`**: RESTful entry points organized by service domain.
- **`/app/services`**: Domain services holding the business logic (Auth, Claims, AI Risk, Fraud, Payouts, etc.).
- **`/app/models`**: Centralized SQLModel definitions representing the platform's state.
- **`/app/core`**: System configuration, security protocols, and database connectivity.

---

## 🧠 AI & ML Intelligence

Carbon features a multi-layered intelligence suite that governs every financial decision:

### 📡 AI Risk Service
The system evaluates worker risk using engineered features such as **disruption frequency**, **historical volatility**, and **location risk indices**. It provides:
- **Predictive Scoring**: Real-time risk evaluation (0-1).
- **Dynamic Calibration**: Automatic categorization (LOW/MEDIUM/HIGH) with premium multipliers.
- **MLOps Monitoring**: Built-in endpoints for model health and drift detection.

### 🚨 Automated Fraud Shield
A dedicated layer that protects the insurance pool from abusive behavior:
- **Anomaly Detection**: Identifies irregularities in claim frequency and amounts.
- **Audit Trails**: Returns detailed sub-check reports (e.g., identity consistency) for every flag.

### ⚙️ Autonomous Decision Engine
The core claims pipeline orchestrates AI Risk and Fraud scores to deliver **zero-human intervention** outcomes. Every claim is automatically approved, rejected, or flagged for review based on predictive confidence.

### 📈 Inference Logging
Every prediction is logged with its unique `prediction_id` and contributing factors, ensuring full explainability (XAI) and enabling continuous model retraining.

---

## 🚀 Key Features

- 🔐 **Secure Auth**: OTP-based authentication with JWT session management.
- 🧠 **AI Risk Intelligence**: Real-time risk scoring and premium multiplier calibration.
- 🚨 **Fraud Shield**: Automated fraud detection and audit trail for every claim.
- 🌩️ **Event Simulation**: Trigger-driven simulations for disaster response testing.
- 💸 **Deterministic Payouts**: Idempotent financial disbursements with pool validation.
- 📊 **Operational Analytics**: KPI dashboards and time-series performance metrics.

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.11+**
- **pip** (Python package manager)

### Installation & Run
Simply run the provided batch file in the `Code` directory:
```bash
run_backend.bat
```
*This will automatically install dependencies and launch the server at `http://localhost:8000`.*

---

## 📮 API Reference (v1)

### 🔑 Authentication (`auth`)
| Method | Endpoint | Description | Payload / Params |
| :--- | :--- | :--- | :--- |
| **POST** | `/auth/otp/send` | Send OTP for login/register | `{ "phone": "string" }` |
| **POST** | `/auth/otp/verify` | Verify OTP & obtain JWT | `{ "phone": "string", "otp": "string" }` |
| **POST** | `/auth/register` | Register new worker | `{ "phone": "s", "full_name": "s", "email": "s" }` |
| **POST** | `/auth/login` | Secure worker login | `{ "phone": "string", "otp": "string" }` |
| **POST** | `/auth/refresh` | Refresh JWT session | None |
| **GET** | `/auth/validate` | Validate session token | None (Headers: Auth Bearer) |
| **POST** | `/auth/logout` | Invalidate session | None (Headers: Auth Bearer) |

### 👤 Workers (`workers`)
| Method | Endpoint | Description | Payload / Params |
| :--- | :--- | :--- | :--- |
| **POST** | `/workers/profile` | Create/Join profile | `{ "phone": "s", "full_name": "s", "email": "s" }` |
| **GET** | `/workers/{user_id}` | Retrieve profile | `user_id` (Path UUID) |
| **PUT** | `/workers/{user_id}` | Update profile | `{ "full_name": "s", "email": "s" }` |

### 🛡️ Policy & Pricing (`policy` / `pricing`)
| Method | Endpoint | Description | Payload / Params |
| :--- | :--- | :--- | :--- |
| **POST** | `/policy/opt-in` | Join coverage pool | `{ "worker_id": "uuid", "premium_amount": 0.0 }` |
| **POST** | `/policy/opt-out` | Leave coverage pool | `worker_id` (Query UUID) |
| **POST** | `/policy/validate` | Verify worker eligibility | `worker_id` (Query UUID) |
| **GET** | `/policy/{user_id}` | View active policy | `user_id` (Path UUID) |
| **POST** | `/pricing/calculate` | Compute premium | `{ "base_amount": 0.0, "risk_score": 0.5 }` |
| **POST** | `/pricing/recalculate` | Update worker premium | `worker_id` (Query UUID) |

### 📄 Claims & Fraud (`claims` / `fraud`)
| Method | Endpoint | Description | Payload / Params |
| :--- | :--- | :--- | :--- |
| **POST** | `/claims/auto` | Trigger claim flow | `{ "worker_id": "uuid", "event_type": "s", "amount": 0.0 }` |
| **GET** | `/claims/{user_id}` | View claim history | `user_id` (Path UUID) |
| **POST** | `/fraud/check` | Analyze claim risk | `claim_id` (Query UUID) |
| **GET** | `/fraud/{claim_id}` | Get fraud report | `claim_id` (Path UUID) |
| **POST** | `/fraud/override` | Admin approval | `claim_id` (Query UUID) |

### 🌩️ Trigger & AI Risk (`trigger` / `risk`)
| Method | Endpoint | Description | Payload / Params |
| :--- | :--- | :--- | :--- |
| **POST** | `/trigger/mock` | Simulate catastrophe | `event_type` (Query: WEATHER/PLATFORM) |
| **GET** | `/trigger/active` | Current disruptions | None |
| **POST** | `/risk/evaluate` | Run AI risk engine | `worker_id` (Query UUID) |
| **GET** | `/risk/health` | Service monitoring | None |
| **POST** | `/risk/feedback` | Train model feedback | `prediction_id` (Query), `is_accurate` (Query) |

### 💰 Payout & Financials (`payout` / `pool` / `ledger`)
| Method | Endpoint | Description | Payload / Params |
| :--- | :--- | :--- | :--- |
| **POST** | `/payout/process` | Execute settlement | `claim_id`, `worker_id`, `amount` (Query) |
| **GET** | `/payout/{user_id}` | Payout history | `user_id` (Path UUID) |
| **POST** | `/payout/retry` | Retry failed payout | `payout_id` (Query UUID) |
| **GET** | `/pool/status` | Current pool liquidity | None |
| **POST** | `/ledger/entry` | Manual ledger entry | `type`, `amount`, `desc`, `worker_id` (Query) |
| **GET** | `/ledger/{user_id}` | Audit trail | `user_id` (Path UUID) |

### 🔔 Notification & Analytics (`notify` / `analytics`)
| Method | Endpoint | Description | Payload / Params |
| :--- | :--- | :--- | :--- |
| **POST** | `/notify/send` | Send push message | `worker_id`, `title`, `message` (Query) |
| **GET** | `/notify/{user_id}` | Notification inbox | `user_id` (Path UUID) |
| **GET** | `/analytics/dashboard` | Global KPIs | None |
| **GET** | `/analytics/timeseries` | Volume trends | `days` (Query, default 7) |

---

## 🛠️ Core System Workflows & Documentation

### 1. User Onboarding & Policy Flow
The system uses a frictionless onboarding process designed for mobile workers:
- **Registration**: Users register via `/auth/register`. A `Worker` profile is created, and a JWT session is issued.
- **Opt-In**: The worker joins the shared risk pool via `/policy/opt-in`. This calculates their initial premium and records their first contribution in the **Ledger**.
- **Pool Ownership**: Every premium payment increases the `Pool` liquidity, supporting the collective security of all members.

### 2. Disruption & Automated Claims Flow
Carbon's unique value is its zero-human intervention claim cycle:
- **Detection**: The `Trigger Service` simulates or polls external events (Weather, Platform outages).
- **Fan-Out**: When a disruption is detected, the system identifies all active policyholders in the impacted category.
- **Decision Engine**: For each impacted worker, an automated claim is created (`/claims/auto`). The **AI Risk Service** evaluates behavioral risk, and the **Fraud Shield** checks for anomalies.
- **Approval**: If scores are within safe thresholds, the claim is auto-approved.

### 3. Idempotent Payout & Ledger Flow
Financial integrity is maintained through multi-step transactional safety:
- **Pool Debit**: On approval, the `Payout Service` debits the shared pool balance.
- **Ledger Record**: A `WITHDRAW` entry is recorded in the double-entry ledger for auditability.
- **Settlement**: The payout is processed idempotentally—ensuring that even if a network failure occurs, the same claim can never be paid twice.
- **Notification**: The worker receives an instant push notification (`/notify`) about their successful settlement.

---

## 🧪 Simulation Flow: Full Cycle Example
Follow this sequence to test a complete "Rain -> Payout" insurance cycle:

1.  **Register & Opt-In**:
    - `POST /auth/register` (Phone: 9876543210)
    - `POST /policy/opt-in` (Worker UUID from registration, Premium: 50.0)
2.  **Trigger Disaster**:
    - `POST /trigger/mock?event_type=WEATHER`
3.  **Verify Outcome**:
    - `GET /claims/{user_id}` (Check status: APPROVED)
    - `GET /payout/{user_id}` (Verify settlement record)
    - `GET /ledger/{user_id}` (Review the audit trail)

---

## 📊 Observability
- **Interactive Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Analytics Dashboard**: `GET /api/v1/analytics/dashboard`
- **Health Checks**: `GET /api/v1/analytics/health`

---

## 🛡️ Financial Guarantees
- ✅ **Idempotency**: Payouts are protected by unique claim-based keys.
- ✅ **Integrity**: Pool balance is validated before any disbursement.
- ✅ **Transparency**: Full audit logs for every state transition in the ledger.
