from typing import Any, Optional, Text, Union

from pydantic import BaseModel


class BasicResponse(BaseModel):
    success: bool = False
    message: Optional[Text] = None
    data: Any = None
    time_cost: Optional[Union[float, int]] = None


class TaskResponse(BasicResponse):
    task_id: Text
