import httpx
import time
import json
import uuid

BASE_URL = "http://localhost:8001"

def test_endpoint(name, method, endpoint, payload=None, params=None):
    print(f"Testing {name} ({method} {endpoint})...")
    try:
        if method == "POST":
            response = httpx.post(f"{BASE_URL}{endpoint}", json=payload, params=params, timeout=10)
        else:
            response = httpx.get(f"{BASE_URL}{endpoint}", params=params, timeout=10)
        
        print(f"  Status: {response.status_code}")
        data = response.json()
        
        # Contract Check
        if "status" in data and "data" in data:
            print(f"  Contract: PASS (status={data['status']})")
            return response.status_code, data
        else:
            print(f"  Contract: FAIL (Missing status or data)")
            return response.status_code, data
    except Exception as e:
        print(f"  Error: {str(e)}")
        return 500, str(e)

def run_all_tests():
    report = {}
    
    # 1. General
    report["General"] = test_endpoint("Health", "GET", "/")
    
    # 2. Auth (OTP Send)
    report["Auth:SendOTP"] = test_endpoint("Send OTP", "POST", "/api/v1/auth/otp/send", {"phone_number": "+919999999999"})
    
    # 3. Worker (Get first worker from seed)
    # We'll fetch from analytics/dashboard to get some context if needed, but we'll try a dummy UUID first or skip id-specific for now
    report["Worker:Profile"] = test_endpoint("Create Profile", "POST", "/api/v1/workers/profile", {
        "user_id": str(uuid.uuid4()),
        "name": "Test User",
        "phone": "+1234567890",
        "zone": "Downtown"
    })
    
    # 4. Risk
    report["Risk:Health"] = test_endpoint("Risk Health", "GET", "/api/v1/risk/health")
    
    # 5. Pricing
    report["Pricing:Calculate"] = test_endpoint("Calculate", "POST", "/api/v1/pricing/calculate", {
        "user_id": str(uuid.uuid4()),
        "weekly_income": 10000.0,
        "risk_zone": "Downtown"
    })
    
    # 6. Trigger
    report["Trigger:Active"] = test_endpoint("Active Disruptions", "GET", "/api/v1/trigger/active")
    
    # 7. Analytics
    report["Analytics:Dashboard"] = test_endpoint("Dashboard", "GET", "/api/v1/analytics/dashboard")
    
    # 8. Pool
    report["Pool:Status"] = test_endpoint("Pool Status", "GET", "/api/v1/pool/status")

    # 9. Full cycle test (Mock Trigger)
    print("\nStarting Full Cycle Automation Test...")
    status, data = test_endpoint("Mock Trigger", "POST", "/api/v1/trigger/mock", {"event_type": "WEATHER", "duration": "1h"})
    report["Automation:MockTrigger"] = (status, data)
    
    # Wait for background processing (though our orchestrator is synced for now in the logic I wrote)
    time.sleep(2)
    
    # Check Analytics again to see if payout happened
    report["Automation:PostDisruptionAnalytics"] = test_endpoint("Post-Disruption Dashboard", "GET", "/api/v1/analytics/dashboard")
    
    return report

if __name__ == "__main__":
    results = run_all_tests()
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nTests completed. Results saved to test_results.json")
