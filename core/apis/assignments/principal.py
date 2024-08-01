from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db

router = APIRouter()
@router.get("/assignments", response_model=List[schemas.Assignment])
def get_assignments(db: Session = Depends(get_db)):
    assignments = crud.get_all_assignments(db)
    return assignments
@router.get("/teachers", response_model=List[schemas.Teacher])
def get_teachers(db: Session = Depends(get_db)):
    teachers = crud.get_all_teachers(db)
    return teachers
@router.post("/assignments/grade", response_model=schemas.Assignment)
def grade_assignment(assignment_id: int, grade: float, db: Session = Depends(get_db)):
    assignment = crud.grade_assignment(db, assignment_id, grade)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment
