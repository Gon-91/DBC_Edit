
from models.appmodel import AppModel

from controllers.file_controller import FileController




class AppContext:
    def __init__(self):
        self.model = AppModel()
        self.controllers = ControllerContext(self.model)
        self.usecases = UsecaseContext(self.controllers)




class ControllerContext:
    def __init__(self,model) :
        self.file_controller = FileController(model)
        # ...



import usecases.file as UseCaseFile


class UsecaseContext:
    def __init__(self,controllers) :

        self._regstry = {}
        self._regstry["file.open"]= UseCaseFile.Open(controllers.file_controller)
        self._regstry["file_close"] = UseCaseFile.Close(controllers.file_controller)


    def get(self,key) :
        return self._regstry[key]
