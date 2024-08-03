from pydantic import BaseModel

class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int
    name: str

    class Config: 
        orm_mode = True

