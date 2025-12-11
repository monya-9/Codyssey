import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Question
from domain.question import question_schema

router = APIRouter(
    prefix='/api/question',
)

# response_model에 Pydantic 스키마 적용
# db: Session = Depends(get_db)를 통해 contextlib로 만든 제너레이터 사용
@router.get('/list', response_model=List[question_schema.Question])
def question_list(db: Session = Depends(get_db)):
    _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return _question_list

@router.post('/create')
def question_create(_question_create: question_schema.QuestionCreate,
                    db: Session = Depends(get_db)):
    question = Question(subject=_question_create.subject,
                        content=_question_create.content,
                        create_date=datetime.datetime.now())
    db.add(question)
    db.commit()
    
    return {'message': '질문 등록 성공'}