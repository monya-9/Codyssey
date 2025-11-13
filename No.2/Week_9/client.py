import requests
import json
import sys
import os

API_BASE_URL = "http://127.0.0.1:8080/todo"

def call_api(method, endpoint, data=None):
    """
    API를 호출하고 결과를 출력합니다.
    """
    url = f"{API_BASE_URL}{endpoint}"
    
    print(f"\n--- {method} {url} ---")
    
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data)
        elif method == 'PUT':
            response = requests.put(url, json=data)
        elif method == 'DELETE':
            response = requests.delete(url)
        else:
            print("지원하지 않는 메서드입니다.")
            return

        # 응답 상태 코드 및 내용 출력
        print(f"Status Code: {response.status_code}")
        try:
            print(f"Response Body: {json.dumps(response.json(), indent=2)}")
        except requests.exceptions.JSONDecodeError:
            print(f"Response Body (Non-JSON): {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("오류: Fast API 서버가 8080 포트에서 실행 중인지 확인하십시오.")
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")

def run_tests():
    """
    모든 CRUD 기능을 순차적으로 테스트합니다.
    """
    print("FastAPI TO-DO API 클라이언트 테스트 시작")
    
    # 1. 항목 추가 (POST)
    call_api("POST", "/add_todo", data={"task": "1. 장비 진단 보고서 작성", "completed": False})
    call_api("POST", "/add_todo", data={"task": "2. 화성 기지 에너지 시스템 점검", "completed": False})

    # 2. 전체 조회 (GET)
    call_api("GET", "/retrieve_todo")
    
    # 3. 개별 조회 (GET by ID=1)
    call_api("GET", "/get_single_todo/1")
    
    # 4. 항목 수정 (PUT ID=1)
    # ID=1 항목의 completed 상태를 True로 변경
    call_api("PUT", "/update_todo/1", data={"completed": True})
    
    # 5. 수정된 항목 확인 (GET by ID=1)
    call_api("GET", "/get_single_todo/1")
    
    # 6. 항목 삭제 (DELETE ID=2)
    call_api("DELETE", "/delete_single_todo/2")
    
    # 7. 전체 조회 (삭제 확인)
    call_api("GET", "/retrieve_todo")
    
    # 8. 존재하지 않는 항목 삭제 시도 (404 테스트)
    call_api("DELETE", "/delete_single_todo/99")

if __name__ == '__main__':
    # 서버 실행 후 client.py 실행
    # (venv) uvicorn todo:app --reload --port 8080
    run_tests()

### **5. 실행 방법**

# 1.  **두 개의 터미널**을 열고 `venv` 가상 환경을 활성화합니다.
# 2.  **첫 번째 터미널 (서버)**: `todo.py` 파일이 있는 폴더에서 서버를 실행합니다.
#     ```bash
#     uvicorn todo:app --reload --port 8080