"""
SQLite 데이터베이스 관리
"""
import sqlite3
import os
from datetime import datetime
from typing import List, Optional
from database.models import Project, Task, Note


class Database:
    def __init__(self, db_path: str = "data/progress.db"):
        self.db_path = db_path
        # data 디렉토리가 없으면 생성
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()

    def get_connection(self):
        """데이터베이스 연결 반환"""
        return sqlite3.connect(self.db_path)

    def init_database(self):
        """데이터베이스 테이블 초기화"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 프로젝트 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 할 일 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    completed BOOLEAN DEFAULT FALSE,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_date TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
                )
            """)
            
            # 노트 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
                )
            """)
            
            conn.commit()

    # 프로젝트 CRUD
    def create_project(self, project: Project) -> int:
        """프로젝트 생성"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO projects (title, description, created_date, updated_date)
                VALUES (?, ?, ?, ?)
            """, (project.title, project.description, project.created_date, project.updated_date))
            conn.commit()
            return cursor.lastrowid

    def get_all_projects(self) -> List[Project]:
        """모든 프로젝트 조회"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects ORDER BY updated_date DESC")
            rows = cursor.fetchall()
            
            projects = []
            for row in rows:
                project = Project(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    created_date=datetime.fromisoformat(row[3]) if row[3] else None,
                    updated_date=datetime.fromisoformat(row[4]) if row[4] else None
                )
                projects.append(project)
            return projects

    def get_project(self, project_id: int) -> Optional[Project]:
        """특정 프로젝트 조회"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
            row = cursor.fetchone()
            
            if row:
                return Project(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    created_date=datetime.fromisoformat(row[3]) if row[3] else None,
                    updated_date=datetime.fromisoformat(row[4]) if row[4] else None
                )
            return None

    def update_project(self, project: Project):
        """프로젝트 업데이트"""
        project.updated_date = datetime.now()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE projects 
                SET title = ?, description = ?, updated_date = ?
                WHERE id = ?
            """, (project.title, project.description, project.updated_date, project.id))
            conn.commit()

    def delete_project(self, project_id: int):
        """프로젝트 삭제"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            conn.commit()

    # 할 일 CRUD
    def create_task(self, task: Task) -> int:
        """할 일 생성"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tasks (project_id, title, description, completed, created_date)
                VALUES (?, ?, ?, ?, ?)
            """, (task.project_id, task.title, task.description, task.completed, task.created_date))
            conn.commit()
            return cursor.lastrowid

    def get_tasks_by_project(self, project_id: int) -> List[Task]:
        """프로젝트별 할 일 조회"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM tasks 
                WHERE project_id = ? 
                ORDER BY completed ASC, created_date ASC
            """, (project_id,))
            rows = cursor.fetchall()
            
            tasks = []
            for row in rows:
                task = Task(
                    id=row[0],
                    project_id=row[1],
                    title=row[2],
                    description=row[3],
                    completed=bool(row[4]),
                    created_date=datetime.fromisoformat(row[5]) if row[5] else None,
                    completed_date=datetime.fromisoformat(row[6]) if row[6] else None
                )
                tasks.append(task)
            return tasks

    def update_task(self, task: Task):
        """할 일 업데이트"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tasks 
                SET title = ?, description = ?, completed = ?, completed_date = ?
                WHERE id = ?
            """, (task.title, task.description, task.completed, task.completed_date, task.id))
            conn.commit()

    def delete_task(self, task_id: int):
        """할 일 삭제"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()

    def toggle_task_completion(self, task_id: int) -> bool:
        """할 일 완료 상태 토글"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # 현재 상태 조회
            cursor.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,))
            result = cursor.fetchone()
            if not result:
                return False
            
            new_completed = not bool(result[0])
            completed_date = datetime.now() if new_completed else None
            
            cursor.execute("""
                UPDATE tasks 
                SET completed = ?, completed_date = ?
                WHERE id = ?
            """, (new_completed, completed_date, task_id))
            conn.commit()
            return new_completed

    # 노트 CRUD
    def create_note(self, note: Note) -> int:
        """노트 생성"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO notes (project_id, content, created_date)
                VALUES (?, ?, ?)
            """, (note.project_id, note.content, note.created_date))
            conn.commit()
            return cursor.lastrowid

    def get_notes_by_project(self, project_id: int) -> List[Note]:
        """프로젝트별 노트 조회"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM notes 
                WHERE project_id = ? 
                ORDER BY created_date DESC
            """, (project_id,))
            rows = cursor.fetchall()
            
            notes = []
            for row in rows:
                note = Note(
                    id=row[0],
                    project_id=row[1],
                    content=row[2],
                    created_date=datetime.fromisoformat(row[3]) if row[3] else None
                )
                notes.append(note)
            return notes

    def update_note(self, note: Note):
        """노트 업데이트"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE notes 
                SET content = ?
                WHERE id = ?
            """, (note.content, note.id))
            conn.commit()

    def delete_note(self, note_id: int):
        """노트 삭제"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            conn.commit() 