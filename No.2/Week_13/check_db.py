import sqlite3

# 1. 데이터베이스 파일에 연결
conn = sqlite3.connect('myapi.db')
cursor = conn.cursor()

# 2. 현재 데이터베이스에 있는 모든 테이블 이름 조회 쿼리
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("=== 생성된 테이블 목록 ===")
for table in tables:
    print(table[0])

# 3. question 테이블의 구조(컬럼) 확인
print("\n=== question 테이블 구조 ===")
# 테이블이 존재하는지 먼저 확인
if ('question',) in tables:
    cursor.execute("PRAGMA table_info(question);")
    columns = cursor.fetchall()
    for col in columns:
        # col[1]은 컬럼명, col[2]는 데이터 타입
        print(f"컬럼명: {col[1]} | 타입: {col[2]}")
else:
    print("question 테이블이 발견되지 않았습니다.")

conn.close()