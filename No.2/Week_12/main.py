from fastapi import FastAPI
from database import engine, Base
from domain.question import question_router

# 데이터베이스 테이블 생성 (Alembic을 사용하지 않고 바로 생성할 경우 사용되나,
# 이번 과제에서는 Alembic 사용이 목표이므로 앱 초기화 용도로 작성합니다)
# Base.metadata.create_all(bind=engine)

app = FastAPI()

# 라우터 등록
app.include_router(question_router.router)

@app.get('/')
def root():
    return {'message': 'Hello World'}