from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite 데이터베이스 파일 경로 설정
SQLALCHEMY_DATABASE_URL = 'sqlite:///./myapi.db'

# SQLite는 기본적으로 단일 스레드 통신만 허용하므로,
# 여러 스레드에서 접근할 수 있도록 check_same_thread 옵션을 False로 설정
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)

# 데이터베이스 세션 생성
# autocommit=False, autoflush=False로 설정
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델 클래스들이 상속받을 Base 클래스 생성
Base = declarative_base()