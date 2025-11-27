from pydantic import BaseModel, field_validator

class QuestionCreate(BaseModel):
    subject: str
    content: str

    # (선택) 빈 문자열이 들어오지 않도록 검사
    @field_validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v