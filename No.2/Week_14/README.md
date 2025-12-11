# 📝 게시판 API 프로젝트 (FastAPI + SQLAlchemy + SQLite)

## 📌 프로젝트 개요

이 프로젝트는 기존 메모리 기반 휘발성 게시판의 한계를 극복하기 위해 **SQLite 영구 저장소**를 도입한 백엔드 시스템입니다.

FastAPI를 기반으로 하며, SQLAlchemy ORM과 Alembic 마이그레이션을 활용해 안정적이고 유지보수하기 좋은 데이터 관리 환경을 구축했습니다.  
APIRouter를 사용한 깔끔한 라우팅 구조로 확장성도 고려했습니다.

## 📂 디렉터리 구조

```
Codyssey/
├── main.py                  # FastAPI 앱 진입점 (Router 등록)
├── database.py              # SQLite 연결, SessionLocal, get_db 의존성
├── models.py                # SQLAlchemy 모델 정의 (Question)
├── alembic.ini              # Alembic 설정 파일
├── migrations/              # 마이그레이션 스크립트
│   ├── env.py
│   └── versions/            # 리비전 파일들
├── domain/
│   └── question/
│       ├── question_router.py   # 질문 관련 API 라우터
│       └── question_schema.py   # Pydantic 요청/응답 스키마
└── frontend/                # 정적 리소스 (현재 미사용)
```

## 🛠 기술 스택

| 구성 요소       | 사용 기술              |
|----------------|-------------------------|
| Language       | Python 3.x             |
| Framework      | FastAPI                |
| ORM            | SQLAlchemy             |
| Migration      | Alembic                |
| Database       | SQLite                 |
| Validation     | Pydantic               |

## ⚙️ 설치 및 실행 방법 (Windows 기준)

### 1. 필수 라이브러리 설치
```bash
pip install fastapi uvicorn sqlalchemy alembic
```

### 2. 데이터베이스 초기화 (마이그레이션)

```bash
# 2-1. 리비전 파일 자동 생성
python -m alembic revision --autogenerate -m "create question table"

# 2-2. DB에 테이블 적용
python -m alembic upgrade head
```

### 3. 서버 실행
```bash
python -m uvicorn main:app --reload
```

### 4. API 문서 및 테스트
→ http://127.0.0.1:8000/docs (FastAPI UI)  
→ http://127.0.0.1:8000/redoc (ReDoc)

## 📡 API 명세

**Base URL**: `/api/question`

| Method | URI         | 설명           | Request Body            | Response                  |
|--------|-------------|------------------------|-------------------------|---------------------------|
| GET    | `/list`     | 질문 목록 조회         | 없음                    | `List[Question]`          |
| POST   | `/create`   | 질문 등록              | `subject`, `content`    | 성공 메시지 + 생성된 질문 |

## 📊 데이터베이스 스키마 (Question 테이블)

| 필드명       | 타입         | 설명           | 제약 조건          |
|--------------|--------------|----------------|---------------------|
| id           | Integer      | 고유 번호      | Primary Key         |
| subject      | String       | 질문 제목      | Not Null            |
| content      | Text         | 질문 내용      | Not Null            |
| create_date  | DateTime     | 작성 일시      | Not Null            |

## 📜 코딩 컨벤션

- PEP 8 준수
- 문자열은 **작은따옴표** 사용 (`'string'`)
- 대입 연산자(`=`) 앞뒤 공백 필수
- 네이밍
  - 변수/함수: `snake_case`
  - 클래스: `CapWords`
- 추가 외부 라이브러리 사용 금지 (과제 지정 패키지 외)

## ✅ 과제 수행 결과

- [x] SQLAlchemy ORM 기반 Question 모델 구현  
- [x] SQLite 연결 및 `autocommit=False` 세션 설정  
- [x] Alembic 마이그레이션 성공 (revision 생성 → upgrade head)  
- [x] `question` 테이블 정상 생성 확인  
- [x] APIRouter를 활용한 `/api/question` 라우팅 구현  
- [x] 질문 목록 조회 (GET) - ORM 쿼리 사용  
- [x] 질문 등록 (POST) - Pydantic 스키마 검증 및 DB 저장  
- [x] **Bonus**: Swagger UI 및 DB Browser for SQLite로 정상 동작 검증 완료

**완료!** 🚀