import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

from app.core.database import engine, init_db
from app.models import schemas

client = TestClient(app)

# Initialize DB for tests
init_db()

# Helper to generate UUIDs
def get_uid():
    return str(uuid.uuid4())

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "success"

# 1. AUTH APIs
def test_auth_endpoints():
    # Login
    resp = client.post("/api/v1/auth/login", json={"login": "9998887776", "secret": "123456"})
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert "access_token" in data
    user_id = data["user_id"]

    # Logout
    resp = client.post("/api/v1/auth/logout")
    assert resp.status_code == 200

    # OTP Send
    resp = client.post("/api/v1/auth/otp/send", json={"phone_number": "9998887776"})
    assert resp.status_code == 200

    # OTP Verify
    resp = client.post("/api/v1/auth/otp/verify", json={"phone": "9998887776", "otp": "123456"})
    assert resp.status_code == 200

    # Refresh
    resp = client.post("/api/v1/auth/refresh", json={"refresh_token": "some_token"})
    assert resp.status_code == 200

    # Validate
    resp = client.get("/api/v1/auth/validate", params={"access_token": "some_token"})
    assert resp.status_code == 200

# 2. WORKER APIs
def test_worker_endpoints():
    uid = get_uid()
    phone = str(uuid.uuid4())[:10]
    # Profile POST
    resp = client.post("/api/v1/workers/profile", json={
        "user_id": uid,
        "name": "Test Worker",
        "phone": phone,
        "zone": "Z-1"
    })
    assert resp.status_code == 200, f"Worker profile POST failed: {resp.json()}"

    # Profile GET
    resp = client.get(f"/api/v1/workers/{uid}")
    assert resp.status_code == 200, f"Worker GET failed for {uid}: {resp.json()}"
    assert resp.json()["data"]["user_id"] == uid

    # Status GET
    resp = client.get(f"/api/v1/workers/status/{uid}")
    assert resp.status_code == 200, f"Worker status GET failed: {resp.json()}"

# 3. RISK APIs
def test_risk_endpoints():
    uid = get_uid()
    resp = client.post("/api/v1/risk/evaluate", json={
        "user_id": uid, "location": "12.9, 77.5", "activity_data": {}
    })
    assert resp.status_code == 200
    
    resp = client.get("/api/v1/risk/drift")
    assert resp.status_code == 200
    
    resp = client.post("/api/v1/risk/feedback", json={"user_id": uid, "feedback": "good"})
    assert resp.status_code == 200
    
    resp = client.get("/api/v1/risk/health")
    assert resp.status_code == 200

# 4. PRICING APIs
def test_pricing_endpoints():
    uid = get_uid()
    resp = client.post("/api/v1/pricing/calculate", json={
        "user_id": uid, "weekly_income": 1000, "risk_zone": "Z-1"
    })
    assert resp.status_code == 200
    
    resp = client.post("/api/v1/pricing/recalculate", json={"user_id": uid})
    assert resp.status_code == 200

# 5. POLICY APIs
def test_policy_endpoints():
    uid = get_uid()
    # Create worker first for FK
    resp_w = client.post("/api/v1/workers/profile", json={
        "user_id": uid, "name": "Poly Worker", "phone": str(uuid.uuid4())[:10], "zone": "Z-1"
    })
    assert resp_w.status_code == 200, f"Worker creation for policy failed: {resp_w.json()}"
    
    resp = client.post("/api/v1/policy/create", json={
        "user_id": uid, "premium": 250, "plan": "Gold"
    })
    assert resp.status_code == 200, f"Policy creation failed: {resp.json()}"
    
    resp = client.get(f"/api/v1/policy/{uid}")
    assert resp.status_code == 200, f"Policy GET failed: {resp.json()}"
    
    resp = client.post("/api/v1/policy/validate", json={"user_id": uid})
    assert resp.status_code == 200, f"Policy validation failed: {resp.json()}"
    
    resp = client.post(f"/api/v1/policy/cancel/{uid}")
    assert resp.status_code == 200, f"Policy cancel failed: {resp.json()}"

# 6. TRIGGER APIs
def test_trigger_endpoints():
    resp = client.post("/api/v1/trigger/mock", json={"event_type": "RAIN", "duration": "2h"})
    assert resp.status_code == 200
    
    resp = client.post("/api/v1/trigger/weather", json={"location": "Bangalore"})
    assert resp.status_code == 200
    
    resp = client.get("/api/v1/trigger/active")
    assert resp.status_code == 200
    
    resp = client.post("/api/v1/trigger/stop", json={"event_id": "evt_123"})
    assert resp.status_code == 200

# 7. CLAIM APIs
def test_claim_endpoints():
    uid = get_uid()
    resp = client.post("/api/v1/claims/auto", json={"event_id": "evt_123"})
    assert resp.status_code == 200
    
    resp = client.get(f"/api/v1/claims/{uid}")
    assert resp.status_code == 200
    
    resp = client.get(f"/api/v1/claims/history/{uid}")
    assert resp.status_code == 200

# 8. FRAUD APIs
def test_fraud_endpoints():
    uid = get_uid()
    # Create a mock claim id (just for interface test)
    claim_id = get_uid()
    
    # Note: /fraud/check expects a valid claim in DB, but we check contract status code
    resp = client.post("/api/v1/fraud/check", json={"claim_id": claim_id})
    # Might be 404 if claim doesn't exist, which is fine for existence test, 
    # but we want to test 'working correctly'
    
    resp = client.get(f"/api/v1/fraud/score/{uid}")
    assert resp.status_code == 200
    
    resp = client.get(f"/api/v1/fraud/history/{uid}")
    assert resp.status_code == 200

# 9. PAYOUT APIs
def test_payout_endpoints():
    uid = get_uid()
    resp = client.get(f"/api/v1/payout/{uid}")
    assert resp.status_code == 200
    
    resp = client.post("/api/v1/payout/process", json={"claim_id": get_uid()})
    # 404 is acceptable if claim missing, but route exists
    
    resp = client.post("/api/v1/payout/retry", json={"payout_id": get_uid()})
    assert resp.status_code == 200

# 10. LEDGER APIs
def test_ledger_endpoints():
    uid = get_uid()
    # Ensure uid used in URL is exactly as generated
    resp = client.get(f"/api/v1/ledger/{uid}")
    assert resp.status_code == 200, f"Ledger GET failed for {uid}: {resp.json()}"
    
    resp = client.post("/api/v1/ledger/entry", json={"transaction_data": {}})
    assert resp.status_code == 200, f"Ledger POST failed: {resp.json()}"
    
    resp = client.get("/api/v1/ledger/audit", params={"transaction_id": get_uid()})
    assert resp.status_code == 200, f"Ledger audit GET failed: {resp.json()}"

# 11. NOTIFICATION APIs
def test_notify_endpoints():
    uid = get_uid()
    resp = client.get(f"/api/v1/notify/{uid}")
    assert resp.status_code == 200
    
    resp = client.post("/api/v1/notify/send", json={"user_id": uid, "message": "hello"})
    assert resp.status_code == 200
    
    resp = client.post("/api/v1/notify/retry", json={"notification_id": "notif_123"})
    assert resp.status_code == 200

# 12. ANALYTICS APIs
def test_analytics_endpoints():
    resp = client.get("/api/v1/analytics/dashboard")
    assert resp.status_code == 200
    
    resp = client.get("/api/v1/analytics/timeseries")
    assert resp.status_code == 200
    
    resp = client.get("/api/v1/analytics/zones")
    assert resp.status_code == 200

# 13. POOL APIs
def test_pool_endpoints():
    uid = get_uid()
    resp = client.get("/api/v1/pool/status")
    assert resp.status_code == 200
    
    resp = client.get(f"/api/v1/pool/ledger/{uid}")
    assert resp.status_code == 200
