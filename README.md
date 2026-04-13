# 🚀 Carbon - Autonomous AI Backend for Worker Pooled Insurance

Carbon is a production-grade, event-driven financial insurance backend designed for modern worker ecosystems. It automates the entire lifecycle of a claim—from disruption detection to idempotent payout—with zero human intervention.

---

## 🏗️ Architecture

The project follows a modular, domain-driven structure:
- `/app/api`: Clean RESTful endpoints organized by domain.
- `/app/services`: Decoupled business logic (Ledger, Pool, Claims, Fraud).
- `/app/models`: Unified SQLModel definitions for database and validation.
- `/app/core`: Centralized configuration and database initialization.

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.9+**
- **pip** (Python package manager)

### Installation & Run (One-Click)
Simply run the provided batch file in the `Code` directory:
```bash
run_backend.bat
```
*This will automatically install dependencies and launch the server.*

---

## 📮 Postman Guide: Full API Reference

Base URL: `http://localhost:8000/api/v1`

### 🔑 Authentication (`auth`)
| Method | Endpoint | Description | Body (JSON) |
| :--- | :--- | :--- | :--- |
| **POST** | `/auth/otp/send` | Send OTP to phone | `{ "phone": "string" }` |
| **POST** | `/auth/otp/verify` | Verify OTP & Get Token | `{ "phone": "string", "otp": "string" }` |
| **GET** | `/auth/validate` | Check if token is valid | *Headers: Authorization: Bearer <token>* |
| **POST** | `/auth/logout` | Invalidate session | *Headers: Authorization: Bearer <token>* |

### 👤 Workers (`workers`)
| Method | Endpoint | Description | Body (JSON) |
| :--- | :--- | :--- | :--- |
| **GET** | `/workers/{user_id}` | Get worker profile | None |
| **PUT** | `/workers/{user_id}` | Update worker profile | `{ "phone": "str", "full_name": "str", "email": "str" }` |

### 🛡️ Policy (`policy`)
| Method | Endpoint | Description | Body (JSON) |
| :--- | :--- | :--- | :--- |
| **POST** | `/policy/opt-in` | Opt-in to insurance pool | `{ "worker_id": "uuid", "premium_amount": 0.0 }` |
| **GET** | `/policy/{user_id}` | View active policy | None |

### 🏦 Pool & Ledger (`pool`)
| Method | Endpoint | Description | Body (JSON) |
| :--- | :--- | :--- | :--- |
| **GET** | `/pool/status` | Current pool balance | None |
| **GET** | `/pool/ledger/{user_id}` | View transaction history | None |

### 📄 Claims (`claims`)
| Method | Endpoint | Description | Body (JSON) |
| :--- | :--- | :--- | :--- |
| **POST** | `/claims/auto` | Manually trigger auto-claim | `{ "worker_id": "uuid", "event_type": "str", "amount": 0.0 }` |
| **GET** | `/claims/{user_id}` | View worker claims | None |

### 🌩️ Simulation (`simulation`)
| Method | Endpoint | Description | Query Params |
| :--- | :--- | :--- | :--- |
| **POST** | `/simulation/mock-disruption` | Trigger a disaster (Weather/Platform) | `?event_type=WEATHER` |

---

## 🗄️ Viewing the Database
All data is stored locally in **`carbon.db`** (SQLite).
1. **VS Code**: Install the **"SQLite Viewer"** extension. Click on `carbon.db`.
2. **External**: Use **DB Browser for SQLite** to see the Ledger and Payouts.

---

## 📡 API Documentation
Live interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🛡️ Financial Guarantees
- ✅ **No Duplicate Payouts** (Idempotency)
- ✅ **No Negative Balance** (Fund Validation)
- ✅ **Full Audit Trail** (Double-Entry Ledger)
