from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base

class Question(Base):
    # 테이블 이름 지정
    __tablename__ = 'question'

    # 질문 데이터의 고유번호 (Primary Key)
    id = Column(Integer, primary_key=True)
    
    # 질문 제목
    subject = Column(String, nullable=False)
    
    # 질문 내용
    content = Column(Text, nullable=False)
    
    # 질문 작성일시
    create_date = Column(DateTime, nullable=False)