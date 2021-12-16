import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
import motor.motor_asyncio
from pydantic import BaseModel, Field, EmailStr
from pathlib import Path
import prov.model as prov
from prov.dot import prov_to_dot
import json

def json2DocumentProvenance(data):
    documentAux = prov.ProvDocument()
    data = json.dumps(data)
    document = documentAux.deserialize(None, data,"json")
    return document