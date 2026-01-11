
from models.appmodel import AppModel

from controllers.file_controller import FileController

from usecases.file import *



class AppContext:
    def __init__(self):
        self.model = AppModel()
        self.controllers = ControllerContext(self.model)
        self.usecases = UsecaseContext(self.controllers)




class ControllerContext:
    def __init__(self,model) :
        self.file_controller = FileController(model)
        # ...




class UsecaseContext:
    def __init__(self,controllers) :
        self.open_file = OpenFileCommand(controllers.file_controller)



