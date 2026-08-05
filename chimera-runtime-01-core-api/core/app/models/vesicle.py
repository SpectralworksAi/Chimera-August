from pydantic import BaseModel
class Vesicle(BaseModel):
    id:str
    payload:dict
