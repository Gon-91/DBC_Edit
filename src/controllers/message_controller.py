
class MessageController:

    def __init__(self,data_model):
        self.model = data_model

    def select_message(self, selected_message):
        self.model.select_message(selected_message)