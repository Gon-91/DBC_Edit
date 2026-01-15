
from models.appmodel import AppModel

class AppContext:
    def __init__(self):
        self.model = AppModel()
        self.controllers = ControllerContext(self.model)
        self.usecases = UsecaseContext(self.controllers)


from controllers.file_controller import FileController
from controllers.message_controller import MessageController

class ControllerContext:
    def __init__(self,model) :
        self.file_controller = FileController(model)
        self.message_controller = MessageController(model)
        # ...



import usecases.file as UseCaseFile
import usecases.message as UseCaseMessage


class UsecaseContext:
    def __init__(self,controllers) :

        self._regstry = {}
        self._regstry["file.open"]= UseCaseFile.Open(controllers.file_controller)
        self._regstry["file.close"] = UseCaseFile.Close(controllers.file_controller)
        self._regstry["file.select"] = UseCaseFile.Select(controllers.file_controller)

        self._regstry["message.select"] = UseCaseMessage.Select(controllers.message_controller)


    def get(self,key) :
        return self._regstry[key]
