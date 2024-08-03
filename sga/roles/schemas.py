from pydantic import BaseModel

class RoleBase(BaseModel):
    name: str


class RoleCreateSchema(RoleBase):
    pass


class RoleSchema(RoleBase):
    id: int
    name: str

    class Config: 
        from_attributes = True