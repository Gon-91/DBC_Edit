"""
interfaces.py
-------------
컨트롤러 계층의 인터페이스(프로토콜) 정의. 타입 힌트 및 다형성 지원을 위함.
"""
from typing import Protocol

class FileControllerProtocol(Protocol):
    """
    FileControllerProtocol
    ----------------------
    파일 컨트롤러의 인터페이스(프로토콜) 정의
    """
    def open_file(self, file_path: str):
        """
        파일 열기 인터페이스
        """
        ...