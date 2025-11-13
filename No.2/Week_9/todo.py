import csv
import sys
import os
import typing as t

from fastapi import FastAPI, APIRouter, HTTPException, Body
from pydantic import BaseModel, Field

# --- 전역 상수 및 설정 ---
CSV_FILE = 'todo_data.csv'
CSV_HEADERS = ['id', 'task', 'completed']
router = APIRouter()

# Pydantic 모델 정의: API 입력 데이터의 구조와 타입을 정의합니다.
# 제약조건: 클래스의 이름은 CapWord 방식으로 작성합니다.
class TodoItem(BaseModel):
    # Field를 사용하여 데이터의 예시와 설명을 제공합니다.
    task: str = Field(..., description="The description of the task", example="지구 본부와 통신 설정 확인")
    completed: bool = Field(False, description="Completion status of the task")

def read_todos() -> t.List[dict]:
    """
    제약조건: CSV 파일을 읽어서 TO-DO 리스트를 가져옵니다.
    """
    if not os.path.exists(CSV_FILE):
        return []
    
    try:
        # 파일이 존재하고 헤더를 포함하고 있다고 가정합니다.
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            # 제약조건: CSV 파일을 다루기 위한 패키지는 사용 가능합니다.
            reader = csv.DictReader(file)
            return list(reader)
    except Exception as e:
        print(f"CSV 파일 읽기 오류 발생: {e}")
        return []

def write_todo(todo_item: dict):
    """
    제약조건: TO-DO 항목을 CSV 파일에 추가합니다.
    """
    is_new_file = not os.path.exists(CSV_FILE)
    
    try:
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            
            if is_new_file:
                writer.writeheader()
            
            writer.writerow(todo_item)
    except Exception as e:
        print(f"CSV 파일 쓰기 오류 발생: {e}")

# ==============================================================================
# APIRouter를 이용한 라우트 정의
# ==============================================================================

# 제약조건: 함수 이름은 소문자_언더라인을 사용합니다.
@router.post("/add_todo", response_model=dict, status_code=201)
def add_todo(item: TodoItem) -> dict:
    """
    POST 방식: todo_list에 새로운 항목을 추가하고 결과를 반환합니다.
    """
    
    # 보너스 과제: 입력되는 Dict 타입이 빈값이면 경고를 돌려줍니다.
    # Pydantic 모델을 사용하므로, 빈 객체{}가 들어오면 task 필드 때문에 자동으로 422 오류를 반환합니다.
    # 여기서는 Dict 타입이 비어있지 않더라도, 필수 필드가 비어있는지 확인합니다.
    if not item.task.strip():
        # 제약조건: Dict 타입으로 반환합니다.
        raise HTTPException(status_code=400, detail={"message": "Task description cannot be empty."})

    # 현재 시간을 기반으로 간단한 ID를 생성합니다.
    current_todos = read_todos()
    new_id = len(current_todos) + 1
    
    new_todo = {
        'id': str(new_id),
        'task': item.task,
        'completed': str(item.completed)
    }
    
    write_todo(new_todo)
    
    # 제약조건: Dict 타입으로 반환합니다.
    return {"message": "TO-DO item added successfully", "todo": new_todo}

# 제약조건: 함수 이름은 소문자_언더라인을 사용합니다.
@router.get("/retrieve_todo", response_model=dict)
def retrieve_todo() -> dict:
    """
    GET 방식: todo_list 전체를 가져와 반환합니다.
    """
    todo_list = read_todos()
    
    # 제약조건: Dict 타입으로 반환합니다.
    return {"todo_list": todo_list, "count": len(todo_list)}

# ==============================================================================
# Fast API 메인 애플리케이션
# ==============================================================================

app = FastAPI(title="Mars To-Do API")

# APIRouter를 메인 애플리케이션에 포함합니다.
app.include_router(router, prefix="/todo")


if __name__ == '__main__':
    print(f"TO-DO API가 실행될 준비가 되었습니다.")
    print(f"데이터는 '{CSV_FILE}'에 저장됩니다.")
    
    # 애플리케이션을 실행하려면 터미널에서 다음 명령어를 실행하십시오:
    # uvicorn todo:app --reload --port 8000
    
    # 파일 생성 확인을 위한 초기화 코드 (선택 사항)
    if not os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
                writer.writeheader()
            print(f"'{CSV_FILE}' 파일이 초기화되었습니다.")
        except Exception as e:
            print(f"CSV 파일 초기화 오류: {e}")

# ```
# eof

# ### **3. 서버 실행 및 `curl` 테스트 방법**

# **1. 서버 실행 (uvicorn)**

# 가상 환경이 활성화된 터미널에서 `todo.py` 파일이 있는 폴더로 이동한 후, 아래 명령어를 입력합니다.

# ```bash
# uvicorn todo:app --reload --port 8080
# ```
# * `todo:app`: `todo.py` 파일 내의 `app` 객체를 실행하라는 의미입니다.
# * `--port 8080`: 요구사항에 맞춰 8080 포트를 사용합니다.

# **2. `curl`을 이용한 테스트**

# 서버가 실행되면, 새로운 터미널을 열어 아래 `curl` 명령어로 API의 정상 작동 여부를 확인합니다.

# #### **A. TO-DO 항목 추가 (POST)**

# 새로운 TO-DO 항목을 추가합니다. POST 방식은 JSON 데이터를 전송해야 합니다.

# ```bash
# # 첫 번째 항목 추가
# curl -X POST "http://127.0.0.1:8080/todo/add_todo" -H "Content-Type: application/json" -d '{"task": "지구 본부 통신 데이터 정리", "completed": false}'

# # 두 번째 항목 추가
# curl -X POST "http://127.0.0.1:8080/todo/add_todo" -H "Content-Type: application/json" -d '{"task": "화성 이착륙 장치 점검"}'
# ```

# #### **B. TO-DO 리스트 가져오기 (GET)**

# 추가된 TO-DO 항목 리스트 전체를 가져옵니다.

# ```bash
# curl -X GET "http://127.0.0.1:8080/todo/retrieve_todo"