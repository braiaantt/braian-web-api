from sqlmodel import SQLModel

class TechnologyUpdate(SQLModel):
    name: str
    icon_src: str