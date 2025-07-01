"""
데이터베이스 모델 정의
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class Project:
    """프로젝트 모델"""
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None

    def __post_init__(self):
        if self.created_date is None:
            self.created_date = datetime.now()
        self.updated_date = datetime.now()


@dataclass
class Task:
    """할 일 모델"""
    id: Optional[int] = None
    project_id: int = 0
    title: str = ""
    description: str = ""
    completed: bool = False
    created_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None

    def __post_init__(self):
        if self.created_date is None:
            self.created_date = datetime.now()


@dataclass
class Note:
    """노트 모델"""
    id: Optional[int] = None
    project_id: int = 0
    content: str = ""
    created_date: Optional[datetime] = None

    def __post_init__(self):
        if self.created_date is None:
            self.created_date = datetime.now() 