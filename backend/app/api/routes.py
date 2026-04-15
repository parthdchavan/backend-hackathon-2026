from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Objection
from ..schemas import ObjectionCreate, ObjectionResponse
from ..services.LLM_service.llm_client import response as llm_response

router = APIRouter(prefix="/objections", tags=["objections"])

@router.post("/", response_model=ObjectionResponse)
def create_objection(objection: ObjectionCreate, db: Session = Depends(get_db)):
    result = llm_response(objection.objection_text)
    
    db_objection = Objection(
        objection_text=objection.objection_text,
        response=result["response"],
        category=result["category"],
        severity=result["severity"],
        embedding=result["embedding"]
    )
    
    db.add(db_objection)
    db.commit()
    db.refresh(db_objection)
    
    return db_objection

@router.get("/", response_model=List[ObjectionResponse])
def get_objections(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    objections = db.query(Objection).offset(skip).limit(limit).all()
    return objections

@router.get("/{objection_id}", response_model=ObjectionResponse)
def get_objection(objection_id: int, db: Session = Depends(get_db)):
    objection = db.query(Objection).filter(Objection.id == objection_id).first()
    if not objection:
        raise HTTPException(status_code=404, detail="Objection not found")
    return objection
