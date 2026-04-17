"""
Run: python seed_demo.py
Creates demo users (admin, doctor, nurse, patient) for testing.
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import settings
from app.database import Base
from app.models import User, Patient, Provider, MedicalHistory, UserRole
from app.auth import hash_password

engine = create_async_engine(settings.DATABASE_URL)
Session = async_sessionmaker(engine)


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with Session() as db:
        users = [
            {"email": "admin@hospital.com", "full_name": "Admin User", "role": UserRole.admin},
            {"email": "doctor@hospital.com", "full_name": "Dr. Sarah Johnson", "role": UserRole.doctor},
            {"email": "nurse@hospital.com", "full_name": "Nurse Mike Chen", "role": UserRole.nurse},
            {"email": "patient@example.com", "full_name": "John Doe", "role": UserRole.patient},
        ]

        for u_data in users:
            user = User(
                email=u_data["email"],
                hashed_password=hash_password("demo123"),
                full_name=u_data["full_name"],
                role=u_data["role"],
            )
            db.add(user)
            await db.flush()

            if u_data["role"] in (UserRole.doctor, UserRole.nurse):
                provider = Provider(
                    user_id=user.id,
                    specialty="Emergency Medicine" if u_data["role"] == UserRole.doctor else "Emergency Nursing",
                    department="Emergency Department",
                    years_experience=10,
                    max_cases=15,
                    available_care_levels=["Emergency Room", "Urgent Care"],
                )
                db.add(provider)
            elif u_data["role"] == UserRole.patient:
                patient = Patient(user_id=user.id, gender="Male", blood_type="O+", height_cm=178, weight_kg=75)
                db.add(patient)
                await db.flush()
                history = MedicalHistory(
                    patient_id=patient.id,
                    chronic_conditions=["Hypertension", "Type 2 Diabetes"],
                    allergies=["Penicillin"],
                    current_medications=[{"name": "Metformin", "dose": "500mg"}, {"name": "Lisinopril", "dose": "10mg"}],
                    smoking_status="Former",
                )
                db.add(history)

        await db.commit()
        print("Demo data seeded successfully!")
        print("Login credentials: email / demo123")
        for u in users:
            print(f"  {u['role'].value}: {u['email']}")


asyncio.run(seed())
