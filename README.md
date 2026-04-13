# 🚀 Carbon - Autonomous AI Backend for Worker Pooled Insurance

Carbon is a production-grade, event-driven financial insurance backend designed for modern worker ecosystems. It automates the entire lifecycle of a claim—from disruption detection to idempotent payout—with zero human intervention.

## 🧠 Core Features

- **Autonomous Claim Lifecycle**: Auto-detects disruptions (weather, platform downtime) and triggers claims.
- **Financial Integrity**: 
    - **Double-Entry Ledger**: Every transaction is recorded with auditability.
    - **Shared Risk Pool**: Efficient management of pooled funds with concurrency safety.
    - **Idempotent Payouts**: Prevents duplicate payments using unique claim keys.
- **AI-Driven Risk Logic**: Integrated hooks for fraud detection and risk evaluation (ready for Gemini/ML integration).
- **Mobile-First Auth**: Secured with Phone-based OTP and JWT session management, optimized for Flutter apps.

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

*This will automatically install dependencies from `requirements.txt` and launch the server.*

### Manual Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Server**:
   ```bash
   uvicorn app.main:app --reload
   ```

---

## 📮 Postman Guide: How to Test

To use Postman, set the base URL to: `http://localhost:8000/api/v1`

### 1. Authentication (OTP Flow)
*   **Step 1: Send OTP**
    *   **Method**: `POST`
    *   **URL**: `/auth/otp/send`
    *   **Body** (JSON): `{ "phone": "9876543210" }`
*   **Step 2: Verify OTP**
    *   **Method**: `POST`
    *   **URL**: `/auth/otp/verify`
    *   **Body** (JSON): `{ "phone": "9876543210", "otp": "123456" }`
    *   **Result**: Copy the `user_id` and `access_token` from the response.

### 2. Worker Profile
*   **Method**: `PUT`
*   **URL**: `/workers/{{user_id}}`
*   **Body** (JSON):
    ```json
    {
      "phone": "9876543210",
      "full_name": "John Doe",
      "email": "john@example.com"
    }
    ```

### 3. Opt-In to Insurance
*   **Method**: `POST`
*   **URL**: `/policy/opt-in`
*   **Body** (JSON):
    ```json
    {
      "worker_id": "YOUR_USER_ID_HERE",
      "premium_amount": 100.0
    }
    ```

### 4. Run Disaster Simulation
*   **Method**: `POST`
*   **URL**: `/simulation/mock-disruption?event_type=WEATHER`
*   **Result**: This triggers the "Autonomous" part. It automatically scans all opted-in workers and issues payouts.

---

## 🗄️ Viewing the Database

All data is stored locally in a file named **`carbon.db`** (SQLite).

### How to see the tables & data:
1.  **VS Code**: Install the **"SQLite Viewer"** extension. Then just click on `carbon.db`.
2.  **External Tool**: Download [DB Browser for SQLite](https://sqlitebrowser.org/). Open `carbon.db` to see the Ledger and Payouts.

---

## 📡 API Documentation

Once the server is running, you can access the interactive Swagger documentation:

🔗 **Local API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

### Key Endpoints

| Domain | Endpoint | Description |
| :--- | :--- | :--- |
| **Auth** | `POST /auth/otp/send` | Generic OTP trigger for workers |
| **Pool** | `GET /pool/status` | Real-time transparency of the shared fund |
| **Claims** | `POST /claims/auto` | Trigger an autonomous claim check |
| **Simulation** | `POST /simulation/mock-disruption` | Simulate a disaster (e.g., Weather) to test auto-payouts |

---

## 🧪 Simulation & Testing

To test the full autonomous flow without waiting for a real-world event:

1. Start the server.
2. Run the simulation endpoint:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/simulation/mock-disruption?event_type=WEATHER"
   ```
3. Check the ledger and claims status in the API docs to see the auto-payouts recorded.

---

## 🛡️ Financial Guarantees

- ✅ **No Duplicate Payouts**: Guaranteed by idempotency keys on every transaction.
- ✅ **No Negative Balance**: The pool validates funds before any payout execution.
- ✅ **Full Audit Trail**: Every movement of funds has a corresponding ledger entry.

---

## 📝 License

Internal Project - Development Prototype.
