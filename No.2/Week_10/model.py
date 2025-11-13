from pydantic import BaseModel, Field
import typing as t

# 제약조건: 클래스 이름은 CapWord 방식으로 작성합니다.

class TodoItem(BaseModel):
    """
    POST 요청 시 사용되는 모델: 새로운 TO-DO 항목을 생성합니다.
    """
    task: str = Field(..., description="The description of the task", example="지구 본부와 통신 설정 확인")
    completed: bool = Field(False, description="Completion status of the task")

class TodoItemUpdate(BaseModel):
    """
    PUT 요청 시 사용되는 모델: 기존 TO-DO 항목을 수정합니다. 
    모든 필드는 선택 사항(Optional)입니다.
    """
    task: t.Optional[str] = Field(None, description="The new description of the task")
    completed: t.Optional[bool] = Field(None, description="The new completion status of the task")