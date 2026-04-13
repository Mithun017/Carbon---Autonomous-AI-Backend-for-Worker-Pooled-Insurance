import random
import httpx
from datetime import datetime
from app.core.config import settings

class TriggerService:
    @staticmethod
    async def check_weather_disruption(lat: float, lon: float) -> dict:
        """
        Poll weather data and detect high rainfall/wind.
        """
        try:
            # For simulation, we randomly succeed or call the real API
            # For now, let's mock the detection
            is_disruption = random.choice([True, False, False, False]) # 25% chance
            
            if is_disruption:
                return {
                    "type": "WEATHER",
                    "severity": "HIGH",
                    "source": "OPEN_METEO",
                    "timestamp": datetime.utcnow().isoformat(),
                    "details": "Heavy rainfall detected (> 50mm/h)"
                }
            return None
        except Exception:
            return None

    @staticmethod
    def simulate_platform_outage() -> dict:
        """
        Simulate a platform signal (e.g., DoorDash/Uber outage).
        """
        return {
            "type": "PLATFORM",
            "severity": "CRITICAL",
            "source": "SIMULATOR",
            "timestamp": datetime.utcnow().isoformat(),
            "details": "Platform API response time > 5000ms"
        }

    @staticmethod
    def get_active_disruptions():
        # Mock active disruptions for the dashboard
        return [
            {"id": "d1", "type": "WEATHER", "zone": "San Francisco", "active": True},
            {"id": "d2", "type": "TRAFFIC", "zone": "London", "active": True}
        ]
