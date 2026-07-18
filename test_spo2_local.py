import asyncio
from backend.models.manager import ModelManager

async def main():
    mm = ModelManager()

    base = {
        "age": 45, "gender": "Male", "bmi": 24, "smoking": False,
        "hr": 70, "sbp": 120, "dbp": 80,
        "spo2": 98, "temp": 37.0, "respiratory_rate": 16, "glucose": 100,
        "symptoms": ["chest pain"], "symptom_duration_days": 5
    }

    base_pred = await mm.predict_async(base)
    print(f"Base: {base_pred['severity_score']}")

    p2 = base.copy()
    p2["spo2"] = 82
    p2_pred = await mm.predict_async(p2)
    print(f"SpO2 82: {p2_pred['severity_score']}")

asyncio.run(main())
