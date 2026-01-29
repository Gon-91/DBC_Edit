"""
base.py
유스케이스 계층: 업무 로직 실행을 위한 추상 베이스 클래스 정의
"""
from abc import ABC, abstractmethod

class Usecase(ABC):
    """
    모든 유스케이스의 기본 인터페이스를 제공하는 추상 클래스입니다.
    execute() 메서드는 반드시 구현해야 합니다.
    """
    @abstractmethod
    def execute(self, *args, **kwargs) -> None:
        """
        유스케이스 실행 메서드 (구현 필수)
        """
        pass

    def can_execute(self) -> bool:
        """
        유스케이스 실행 가능 여부를 반환합니다.
        Returns:
            bool: 실행 가능 여부
        """
        return True