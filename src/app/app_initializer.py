"""
app_initializer.py
-----------------
앱의 전역 컨텍스트(AppContext)를 초기화하고, 메인 윈도우(MainWindow)를 생성하는 모듈.
"""
from app.app_context import AppContext
from views.main_window import MainWindow

# 메인 윈도우 생성 함수
def create_main_window() -> MainWindow:
    """
    앱 컨텍스트를 초기화하고 메인 윈도우를 생성하여 반환
    - 모델, 유스케이스 등 전역 객체를 MainWindow에 주입
    """
    app_context = AppContext()  # 앱 전역 컨텍스트 생성
    window = MainWindow(
        model=app_context.model,
        usecase=app_context.usecases
    )
    return window