"""
유틸리티 헬퍼 함수들
"""
from datetime import datetime, date, time
from typing import Optional


def format_datetime(dt: Optional[datetime], format_str: str = "%Y-%m-%d %H:%M") -> str:
    """
    datetime 객체를 문자열로 포맷팅
    
    Args:
        dt: datetime 객체
        format_str: 포맷 문자열
        
    Returns:
        포맷된 문자열
    """
    if dt is None:
        return ""
    return dt.strftime(format_str)


def format_date_only(dt: Optional[datetime]) -> str:
    """
    날짜만 포맷팅
    
    Args:
        dt: datetime 객체
        
    Returns:
        날짜 문자열 (YYYY-MM-DD)
    """
    return format_datetime(dt, "%Y-%m-%d")


def format_time_only(dt: Optional[datetime]) -> str:
    """
    시간만 포맷팅
    
    Args:
        dt: datetime 객체
        
    Returns:
        시간 문자열 (HH:MM)
    """
    return format_datetime(dt, "%H:%M")


def format_relative_time(dt: Optional[datetime]) -> str:
    """
    상대적 시간 포맷팅 (예: 5분 전, 2시간 전)
    
    Args:
        dt: datetime 객체
        
    Returns:
        상대적 시간 문자열
    """
    if dt is None:
        return ""
    
    now = datetime.now()
    diff = now - dt
    
    if diff.days > 0:
        return f"{diff.days}일 전"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours}시간 전"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes}분 전"
    else:
        return "방금 전"


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    텍스트 자르기
    
    Args:
        text: 원본 텍스트
        max_length: 최대 길이
        suffix: 접미사
        
    Returns:
        자른 텍스트
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def validate_project_title(title: str) -> tuple[bool, str]:
    """
    프로젝트 제목 검증
    
    Args:
        title: 프로젝트 제목
        
    Returns:
        (유효성, 오류 메시지) 튜플
    """
    if not title or title.strip() == "":
        return False, "프로젝트 제목을 입력해주세요."
    
    if len(title.strip()) > 100:
        return False, "프로젝트 제목은 100자 이내로 입력해주세요."
    
    return True, ""


def validate_task_title(title: str) -> tuple[bool, str]:
    """
    할 일 제목 검증
    
    Args:
        title: 할 일 제목
        
    Returns:
        (유효성, 오류 메시지) 튜플
    """
    if not title or title.strip() == "":
        return False, "할 일 제목을 입력해주세요."
    
    if len(title.strip()) > 200:
        return False, "할 일 제목은 200자 이내로 입력해주세요."
    
    return True, ""


def safe_string_to_int(value: str, default: int = 0) -> int:
    """
    안전한 문자열을 정수로 변환
    
    Args:
        value: 변환할 문자열
        default: 기본값
        
    Returns:
        정수 값
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


# ---------------------------------------------------------------------------
# 공통 날짜 파싱 유틸리티 (SQLite 결과가 str 혹은 datetime 둘 다 가능)
# ---------------------------------------------------------------------------


def parse_datetime(value) -> Optional[datetime]:
    """DB에서 가져온 열 값을 안전하게 datetime 으로 변환

    SQLite 설정에 따라 같은 열이 str(ISO 문자열) 로 오거나 이미 datetime 객체로
    올 수 있다. 또한 None 일 수도 있으므로 모든 경우를 처리한다.

    Args:
        value: DB 로부터 읽은 값

    Returns:
        datetime 또는 None
    """
    if value is None:
        return None

    if isinstance(value, datetime):
        return value

    if isinstance(value, (date, time)):
        # date / time 타입은 그대로 반환 or 조합할 수도 있지만 여기선 str 에서 파싱 시도
        try:
            return datetime.combine(value, datetime.min.time())
        except Exception:
            return None

    if isinstance(value, (bytes, bytearray, memoryview)):
        try:
            value = value.decode()
        except Exception:
            value = str(value)

    if isinstance(value, str):
        # ISO 형식 파싱 시도 (공백 구분도 허용)
        try:
            return datetime.fromisoformat(value.replace("T", " "))
        except Exception:
            pass
        # SQLite 기본 포맷 "YYYY-MM-DD HH:MM:SS"
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f"):
            try:
                return datetime.strptime(value, fmt)
            except Exception:
                continue

    # 변환 실패
    return None 