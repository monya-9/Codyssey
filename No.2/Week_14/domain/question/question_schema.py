import datetime
from pydantic import BaseModel, field_validator

# 질문 등록 시 사용하는 입력 스키마
class QuestionCreate(BaseModel):
    subject: str
    content: str

    @field_validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

# 질문 목록 조회 시 사용하는 출력 스키마
class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime

    # 보너스 과제: ORM 모드 설정
    # True일 경우: 객체의 속성(obj.id)으로 데이터에 접근 가능
    # False일 경우: 딕셔너리 키(obj['id'])로만 접근 시도 (SQLAlchemy 객체 변환 실패)
    class Config:
        orm_mode = True