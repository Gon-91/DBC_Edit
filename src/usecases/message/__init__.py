from usecases.base import Usecase




class Select(Usecase):

    def __init__(self,  controller):
        self._controller = controller

    def execute(self,messageviewdata):

        self._controller.select_message(messageviewdata)

        #log 
        print("message Usecase : Open")
