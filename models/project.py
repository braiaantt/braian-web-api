from sqlmodel import SQLModel

class PortfolioProject(SQLModel):
    id: int
    name: str
    small_about: str
    cover_src: str