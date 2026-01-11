from app.app_context import AppContext

from views.main_window import MainWindow



# main_window 생성

def create_main_window() -> MainWindow:
    app_context = AppContext()

    window = MainWindow(
        model = app_context.model,
        usecase=app_context.usecases
    )

    return window