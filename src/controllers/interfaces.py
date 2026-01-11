from typing import Protocol

class FileControllerProtocol(Protocol):

    def open_file(self, file_path: str) :
        ...