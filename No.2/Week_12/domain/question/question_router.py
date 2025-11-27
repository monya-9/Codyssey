import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Question
from domain.question import question_schema

router = APIRouter(
    prefix='/api/question',
)

# 목록 조회
@router.get('/list')
def question_list(db: Session = Depends(get_db)):
    _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return _question_list

# 질문 등록 (POST 메소드 사용)
@router.post('/create')
def question_create(_question_create: question_schema.QuestionCreate,
                    db: Session = Depends(get_db)):
    question = Question(subject=_question_create.subject,
                        content=_question_create.content,
                        create_date=datetime.datetime.now())
    db.add(question)
    db.commit()
    
    return {'message': '질문 등록 성공'}