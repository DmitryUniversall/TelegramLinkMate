from .model import FilelikeModel
from teleapi.core.http.request import method_request
from typing import TYPE_CHECKING
from teleapi.core.http.request.api_method import APIMethod

if TYPE_CHECKING:
    from teleapi.types.file import File


class Filelike(FilelikeModel):
    def __eq__(self, other) -> bool:
        return isinstance(other, Filelike) and other.file_id == self.file_id

    @classmethod
    async def fetch_file(cls, file_id: str) -> 'File':
        from teleapi.types.file import FileSerializer

        response, data = await method_request("GET", APIMethod.GET_FILE, data={'file_id': file_id})
        return FileSerializer().serialize(data=data['result'])

    async def get_file(self) -> 'File':
        return await self.fetch_file(file_id=self.file_id)

    async def download(self, path: str = None) -> None:
        file = await self.get_file()
        return await file.download(path=path)
