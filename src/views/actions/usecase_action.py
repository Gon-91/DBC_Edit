from PySide6.QtGui import QAction

class UsecaseAction(QAction):
    def __init__(self, text,parent, uescase):
        super().__init__(text,parent)
        self._usecase = uescase
        self._parent = parent
        self.triggered.connect(self._on_triggered)

    def _on_triggered(self):
        self._usecase.execute(self._parent)