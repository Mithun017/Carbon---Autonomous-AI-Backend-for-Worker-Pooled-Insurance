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
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/auth/otp/send` | Send OTP for login/register |
| **POST** | `/auth/otp/verify` | Verify OTP & obtain JWT tokens |
| **POST** | `/auth/register` | Create new worker profile and join |
| **POST** | `/auth/login` | Secure login for existing workers |
| **GET** | `/auth/validate` | Validate session token integrity |

### 🛡️ Policy & Pricing (`policy` / `pricing`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/policy/opt-in` | Join the insurance pool |
| **POST** | `/policy/validate` | Check active policy eligibility |
| **POST** | `/pricing/calculate` | Calculate premium based on risk |

### 📄 Claims & Fraud (`claims` / `fraud`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/claims/auto` | Trigger automated claim evaluation |
| **POST** | `/fraud/check` | Analyze claim for fraudulent patterns |
| **POST** | `/fraud/override` | Manual admin override for approvals |

### 🌩️ Trigger & AI Risk (`trigger` / `risk`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/trigger/mock` | Simulate a disruption event |
| **POST** | `/risk/evaluate` | Generate AI risk score for worker |
| **GET** | `/risk/drift` | Monitor model accuracy and drift |

### 💰 Payout & Financials (`payout` / `pool` / `ledger`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/payout/process` | Execute idempotent payout |
| **GET** | `/pool/status` | Current shared pool liquidity |
| **GET** | `/ledger/{user_id}` | Personal transaction audit log |

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
