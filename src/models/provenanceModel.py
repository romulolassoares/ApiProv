from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class agentModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    provType: str = Field(...)
    pki: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "userR01",
                "provType": "user",
                "pki": "97f3c717da19b4697ae9884e67aabce6",
            }
        }
        
class UpdateAgentModel(BaseModel): 
    name: Optional[str]
    provType: Optional[str]
    pki: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "userR02",
                "provType": "user",
                "pki": "97f3c717da19b4697ae9884e67aabce6",
            }
        }
        
class activityModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    provType: str = Field(...)
    info: dict = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "1": {
                    "name": "Transaction001",
                    "provType": "transaction",
                    "info": {
                        "pki": "09090",
                        "date": "date"
                    }
                },
                "2": {
                    "name": "DocGenerated001",
                    "provType": "docGenerated",
                    "info": {}
                }
            }
        }

class UpdateActivityModel(BaseModel): 
    name: Optional[str]
    provType: Optional[str]
    info: Optional[dict]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Transaction001",
                "provType": "transaction",
                "info": {
                    "pki": "09090",
                    "date": "date"
                }
            }
        }
        
class entityModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    provType: str = Field(...)
    info: dict = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "1": {
                    "name": "Print01",
                    "provType": "print",
                    "info": {
                        "destination": "iot01"
                    }
                },
                "2": {
                    "name": "DocGenerated001",
                    "provType": "docGenerated",
                    "info": {
                        "author": "Rômulo Soares",
                        "title": "Doc File",
                        "format": "pdf"
                    }
                }
            }
        }
        
class ProvModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    key: str = Field(...)
    data: dict = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "key": "8839c2e520b5977e8d719471fa8d3a75",
                "data": {
                    "name": "DocGenerated001",
                    "provType": "docGenerated",
                    "info": {}
                }
            }
        }
        
class UpdateProvModel(BaseModel):
    key: Optional[str]
    data: Optional[dict]
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "key": "",
                "data": {
                    "name": "DocGenerated001",
                    "provType": "docGenerated",
                    "info": {}
                }
            }
        }