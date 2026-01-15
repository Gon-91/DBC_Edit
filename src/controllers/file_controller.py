import re

from services.dbc_loader import load_dbc_file

"""
    파일 관련 컨트롤러
    SRP : 파일 읽기 / 쓰기 담당  
    상세 내용은 service 레벨에서 처리
"""


class FileController:

    def __init__(self,data_model):
        self.model = data_model


    def open_file(self, file_path: str):
        self.model.add_file(load_dbc_file(file_path))

        #log 
        print("File Controller : open_file_called")
    

    def close_file(self, file_name : str) :
        self.model.remove_file(file_name)

        #log 
        print("File Controller : close_file_called")
        
    def select_file(self, file_name : str) :
        self.model.select_file(file_name)

        #log 
        print("File Controller : select_file_called")