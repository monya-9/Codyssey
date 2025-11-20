# 📝 게시판 API 프로젝트 (FastAPI + SQLAlchemy + SQLite)

## 📌 프로젝트 개요  
이 프로젝트는 메모리에만 데이터를 저장하던 기존 방식의 **휘발성 문제를 해결**하기 위해  
**SQLite 기반 영구 저장소**를 도입한 게시판 백엔드 시스템입니다.  
FastAPI를 기반으로 하며, **SQLAlchemy(ORM)** 와 **Alembic(마이그레이션)** 을 사용해  
안정적인 데이터 관리 환경을 구축했습니다.

---

## 📂 디렉터리 구조 (Directory Structure)

Codyssey/
├── main.py # FastAPI 애플리케이션 진입점
├── database.py # SQLite 연결 설정 및 세션 관리
├── models.py # SQLAlchemy 모델 정의 (Question 테이블)
├── alembic.ini # Alembic 설정 파일
├── migrations/
│ ├── env.py # Alembic 환경 설정
│ └── versions/ # 리비전 파일(.py) 저장 폴더
├── domain/
│ └── question/ # 도메인별 로직
└── frontend/ # 프론트엔드 리소스

yaml
코드 복사

---

## 🛠 개발 환경 및 기술 스택 (Tech Stack)

| 구성 요소 | 사용 기술 |
|-----------|-----------|
| Language  | Python 3.x |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Migration Tool | Alembic |
| Database | SQLite |

---

## ⚙️ 설치 및 실행 가이드 (Setup & Run)

> ※ 윈도우 환경 기준

### 1. 라이브러리 설치

```bash
pip install fastapi uvicorn sqlalchemy alembic
2. 데이터베이스 초기화 및 생성 (Migration)
2-1) 리비전 파일 생성
bash
코드 복사
python -m alembic revision --autogenerate -m "create question table"
2-2) 데이터베이스 업그레이드 (테이블 생성)
bash
코드 복사
python -m alembic upgrade head
3. 서버 실행
bash
코드 복사
uvicorn main:app --reload
📊 데이터베이스 모델 명세 (Database Schema)
Question 테이블 (models.py)
필드명	타입	설명	제약조건
id	Integer	고유 번호	Primary Key
subject	String	질문 제목	Not Null
content	Text	질문 내용	Not Null
create_date	DateTime	작성 일시	Not Null

📜 코딩 컨벤션 (Coding Conventions)
PEP 8 스타일 가이드 준수

문자열은 ' 작은따옴표 사용

예: subject = Column(String, nullable=False)

대입문 = 앞뒤에는 공백 사용

예: foo = (0,)

네이밍 규칙

변수/함수: snake_case

클래스: CapWords

기본 명령어 및 지정된 패키지 외 추가 라이브러리 사용 금지

✅ 과제 수행 결과
 ORM 적용: SQLAlchemy 기반 Question 모델 구현

 DB 설정 완료: SQLite 연결 및 autocommit=False 세션 구성

 마이그레이션 성공: Alembic revision 생성 및 upgrade head 실행

 테이블 생성 확인: question 테이블 정상 생성

 (Bonus) DB Browser for SQLite로 스키마 검증 완료