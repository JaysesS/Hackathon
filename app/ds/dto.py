from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class TaskRawData:
    process_name: str
    task_name: str
    owner: str
    assigner: Optional[str]
    start_time: datetime
    end_time: Optional[datetime]
    due_time: datetime
    priority: int
    var_count: int
    
    def get_as_row(self, column_names):
        row = []
        for col in column_names:
            row.append(self.__getattribute__(col))
        return row
    
    @classmethod
    def collumn(cls):
        return tuple(cls.__dataclass_fields__.keys())
