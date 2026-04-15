# Carbon Backend Task List

## API Verification (44 Endpoints)

- [x] **1. AUTH APIs**
    - [x] `POST /api/v1/auth/login`
    - [x] `POST /api/v1/auth/logout`
    - [x] `POST /api/v1/auth/otp/send`
    - [x] `POST /api/v1/auth/otp/verify`
    - [x] `POST /api/v1/auth/refresh`
    - [x] `GET /api/v1/auth/validate`

- [x] **2. WORKER APIs**
    - [x] `POST /api/v1/workers/profile`
    - [x] `GET /api/v1/workers/{id}`
    - [x] `GET /api/v1/workers/status/{id}`

- [x] **3. RISK APIs**
    - [x] `POST /api/v1/risk/evaluate`
    - [x] `GET /api/v1/risk/drift`
    - [x] `POST /api/v1/risk/feedback`
    - [x] `GET /api/v1/risk/health`

- [x] **4. PRICING APIs**
    - [x] `POST /api/v1/pricing/calculate`
    - [x] `POST /api/v1/pricing/recalculate`

- [x] **5. POLICY APIs**
    - [x] `POST /api/v1/policy/create`
    - [x] `GET /api/v1/policy/{user_id}`
    - [x] `POST /api/v1/policy/validate`
    - [x] `POST /api/v1/policy/cancel/{user_id}`

- [x] **6. TRIGGER APIs**
    - [x] `POST /api/v1/trigger/mock`
    - [x] `POST /api/v1/trigger/weather`
    - [x] `GET /api/v1/trigger/active`
    - [x] `POST /api/v1/trigger/stop`

- [x] **7. CLAIM APIs**
    - [x] `POST /api/v1/claims/auto`
    - [x] `GET /api/v1/claims/{user_id}`
    - [x] `GET /api/v1/claims/history/{user_id}`

- [x] **8. FRAUD APIs**
    - [x] `POST /api/v1/fraud/check`
    - [x] `GET /api/v1/fraud/score/{user_id}`
    - [x] `GET /api/v1/fraud/history/{user_id}`

- [x] **9. PAYOUT APIs**
    - [x] `GET /api/v1/payout/{user_id}`
    - [x] `POST /api/v1/payout/process`
    - [x] `POST /api/v1/payout/retry`

- [x] **10. LEDGER APIs**
    - [x] `GET /api/v1/ledger/{user_id}`
    - [x] `POST /api/v1/ledger/entry`
    - [x] `GET /api/v1/ledger/audit`

- [x] **11. NOTIFICATION APIs**
    - [x] `GET /api/v1/notify/{user_id}`
    - [x] `POST /api/v1/notify/send`
    - [x] `POST /api/v1/notify/retry`

- [x] **12. ANALYTICS APIs**
    - [x] `GET /api/v1/analytics/dashboard`
    - [x] `GET /api/v1/analytics/timeseries`
    - [x] `GET /api/v1/analytics/zones`

- [x] **13. POOL APIs**
    - [x] `GET /api/v1/pool/status`
    - [x] `GET /api/v1/pool/ledger/{user_id}`

- [x] **14. GENERAL**
    - [x] `GET /`

## Phase 3 Gaps & Production Finalization

- [x] **Orchestration Engine**: Robust failure handling and decoupling implemented.
- [x] **Automated Claims**: Full integration from trigger to notification verified.
- [x] **Fraud Integration**: Connected every claim check to the autonomous pipeline.
- [x] **Eligibility Engine**: Centralized validation logic in EligibilityService.
- [x] **Resilience**: Added exponential backoff and persistent event logging.
- [x] **Data Simulation**: Seeded pool and initial workers for demonstration.
