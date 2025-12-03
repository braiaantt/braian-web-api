from pydantic import BaseModel

class ImageRead(BaseModel):
    id: int
    id_project: int
    src: str

class ImageDelete(BaseModel):
    id_project: int
    src: str