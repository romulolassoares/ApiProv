import json
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr

from src.models.provenanceModel import provenanceModel as provenanceModel

class wasDerivedFromModel(BaseModel):
    id: provenanceModel.PyObjectId = Field(default_factory=provenanceModel.PyObjectId, alias="_id")
    entity: str = Field(...)
    activity: str = Field(...)
    agent: str = Field(...)
    gpa: float = Field(..., le=4.0)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
               "enity": "",
               "activity": "",
               "agent": "",
               "relationship": {
                  ""
               },
            }
        }