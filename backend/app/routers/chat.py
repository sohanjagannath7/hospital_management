from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List
import json
import google.generativeai as genai
from app.database import get_db, AsyncSessionLocal
from app.models import ChatSession, ChatMessage, Patient, User
from app.schemas import ChatMessageCreate, ChatMessageOut, ChatSessionOut
from app.auth import get_current_user
from app.config import settings

router = APIRouter(prefix="/chat", tags=["AI Chat"])

TRIAGE_CHAT_SYSTEM = """You are MedAssist, a compassionate and professional AI healthcare triage assistant.
Your role is to:
1. Listen carefully to patient symptoms and concerns
2. Ask clarifying questions about symptoms (duration, severity, associated symptoms)
3. Provide initial guidance on urgency and care-seeking behavior
4. NEVER provide a definitive diagnosis — always encourage professional medical evaluation
5. Be empathetic and reassuring while being honest about when emergency care is needed
6. If symptoms suggest a life-threatening emergency (chest pain, difficulty breathing, stroke signs, etc.),
   immediately advise calling 911 or going to the nearest emergency room

Important: You are a triage assistant, not a doctor. Always recommend professional medical evaluation."""


@router.post("/sessions", response_model=ChatSessionOut, status_code=201)
async def create_session(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Patient).where(Patient.user_id == current_user.id))
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    session = ChatSession(patient_id=patient.id)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    result = await db.execute(
        select(ChatSession).where(ChatSession.id == session.id)
        .options(selectinload(ChatSession.messages))
    )
    return result.scalar_one()


@router.post("/sessions/{session_id}/messages", response_model=ChatMessageOut)
async def send_message(
    session_id: int,
    data: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ChatSession).where(ChatSession.id == session_id)
        .options(selectinload(ChatSession.messages))
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")

    user_msg = ChatMessage(session_id=session_id, role="user", content=data.content)
    db.add(user_msg)
    await db.flush()

    # Build conversation history for Gemini (user/model roles only)
    gemini_history = []
    for m in session.messages:
        role = "model" if m.role == "assistant" else "user"
        gemini_history.append({"role": role, "parts": [m.content]})

    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=TRIAGE_CHAT_SYSTEM)
    chat = model.start_chat(history=gemini_history)
    response = chat.send_message(data.content)
    ai_content = response.text

    ai_msg = ChatMessage(session_id=session_id, role="assistant", content=ai_content)
    db.add(ai_msg)
    await db.commit()
    await db.refresh(ai_msg)
    return ai_msg


@router.get("/sessions/{session_id}", response_model=ChatSessionOut)
async def get_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ChatSession).where(ChatSession.id == session_id)
        .options(selectinload(ChatSession.messages))
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.get("/sessions", response_model=List[ChatSessionOut])
async def list_my_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Patient).where(Patient.user_id == current_user.id))
    patient = result.scalar_one_or_none()
    if not patient:
        return []
    result = await db.execute(
        select(ChatSession).where(ChatSession.patient_id == patient.id)
        .options(selectinload(ChatSession.messages))
        .order_by(ChatSession.created_at.desc())
    )
    return result.scalars().all()
