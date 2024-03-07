from .model import FileModel
from teleapi.core.http.request import file_request
from typing import Union
from teleapi.types.filelike import Filelike


class File(Filelike, FileModel):
    async def download(self, path: str = None) -> Union[bytes, None]:
        response, bytes_ = await file_request("GET", self.file_path)

        if path is None:
            return bytes_

        with open(path, "wb") as f:
            f.write(bytes_)
