import re

from services.dbc_loader import load_dbc_file

"""
    파일 관련 컨트롤러
    SRP : 파일 읽기 / 쓰기 담당  
    상세 내용은 service 레벨에서 처리
"""


class FileController:

    def __init__(self,data_model):
        self.data_model = data_model


    def open_file(self, file_path: str):
        self.data_model.add_file(load_dbc_file(file_path))

        print("File Controller : open_file_called")
        print("File opened : ", file_path)
        



#if __name__ == "__main__":
#    controller = filecontrooler()
#    controller.read_file("./src/control/sample.dbc")