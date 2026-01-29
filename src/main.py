"""
main.py
-------
애플리케이션 진입점. QApplication을 생성하고 메인 윈도우를 실행한다.
"""
import sys
from PySide6.QtWidgets import QApplication
from app.app_initializer import create_main_window

def main():
    """
    애플리케이션 실행 함수
    - QApplication 인스턴스 생성
    - 메인 윈도우 생성 및 표시
    - 이벤트 루프 진입
    """
    app = QApplication(sys.argv)  # Qt 애플리케이션 객체 생성
    window = create_main_window() # 메인 윈도우 생성
    window.show()                 # 윈도우 표시
    sys.exit(app.exec())          # 이벤트 루프 실행 및 종료 코드 반환

if __name__ == "__main__":
    main()  # 진입점에서 main 함수 실행

