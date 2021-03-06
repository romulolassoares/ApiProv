from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import FileResponse
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import hashlib
import prov.model as prov
import prov.dot as provDot
from pathlib import Path
import os

import src.database.database as database
import json
import src.models.provenanceModel as provenanceModel
import src.controller.provenance as provenance

import src.controller.func as function


#APIRouter creates path operations for item module
router = APIRouter(
    prefix="/prov",
    tags=["Provenance Router"],
    responses={404: {"description": "Not found"}},
)

def testing():
    document = prov.ProvDocument()
    document.set_default_namespace('http://localhost:4444/')
    document.add_namespace('example', 'http://localhost:4444/example/')
    # generating provenance activities
    activityTransaction = provenance.generateTransactionActivity(document, "transaction001", "e619269265072f5b3c9b3cce1ed0ebe2", "date")
    activityGeneratePrint = provenance.generateDocGeneratedActivity(document, "generetedPrinting001")

    # generating provenance entities
    entityPrint = provenance.generateDocumentEntity(document, "doc", "Romulo", "Doc Title", "pdf")
    entityDoc = provenance.generatePrintEntity(document, "print", "iot1")

    # generating provenance agents
    agent = provenance.generateUserAgent(document, "userR01", "97f3c717da19b4697ae9884e67aabce6")

    # Defining relationships
    entityDoc.wasGeneratedBy(activityGeneratePrint)
    entityDoc.wasDerivedFrom(entityPrint)

    activityTransaction.used(entityPrint)
    activityTransaction.wasAssociatedWith(agent)

    activityGeneratePrint.wasInformedBy(activityTransaction)

    entityPrint.wasGeneratedBy(activityTransaction)
    
    return document

@router.post("/generate_prov_test/", response_description="Add new provenance data test", response_model=List[provenanceModel.ProvModel])
async def create_provDataTest(provData: provenanceModel.ProvModel = Body(...)):
    document = testing()
    provDataDoc = document.serialize()
    provDataDoc = json.loads(provDataDoc)
    provData = jsonable_encoder(provData)
    provData["data"] = provDataDoc
    key = json.dumps(provDataDoc)
    provData["key"] = hashlib.sha256(key.encode("utf-8")).hexdigest()
    new_provData = await database.db["provenanceData"].insert_one(provData)
    created_provData = await database.db["provenanceData"].find_one({"_id": new_provData.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_provData)

@router.get("/get/{id}", response_description="Get a single provenance data", response_model=provenanceModel.ProvModel)
async def show_provData(id: str):
    if (provData := await database.db["provenanceData"].find_one({"_id": id})) is not None:
        return provData
    raise HTTPException(status_code=404, detail=f"Provenance Data {id} not found")

@router.post("/generate_prov_data/", response_description="Add new provenance data on database", response_model=List[provenanceModel.ProvModel])
async def create_provData(data: dict):
    if data is None:
        data = {
        "key": "8839c2e520b5977e8d719471fa8d3a75",
        "data": {
                "name": "DocGenerated001",
                "provType": "docGenerated",
                "info": {}
            }
        }
    if type(data) is str:
        data = json.loads(data)
    provDataDoc = data

    key = hashlib.sha256(data["key"].encode("utf-8")).hexdigest()

    provData = provenanceModel.ProvModel(id=provenanceModel.ObjectId() ,key=key, data=provDataDoc["data"])
    
    provData = jsonable_encoder(provData)
    
    new_provData = await database.db["provenanceData"].insert_one(provData)
    created_provData = await database.db["provenanceData"].find_one({"_id": new_provData.inserted_id})
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_provData)

@router.put("/update/{id}", response_description="Update a Provenace Data")
async def update_provData(id: str, provData: dict):
    provData = {k: v for k, v in provData.items() if v is not None}
    
    if len(provData) >= 1:
        update_result = await database.db["provenanceData"].update_one({"_id": id}, {"$set": provData})
        
        if update_result.modified_count == 1:
            if ( updated_provData := await database.db["provenanceData"].find_one({"_id": id}) ) is not None:
                return updated_provData
    
    if ( existing_provData := await database.db["provenanceData"].find_one({"_id": id}) ) is not None:
        return existing_provData
        
    
    raise HTTPException(status_code=404, detail=f"Provenace Data {id} not found")

@router.post("/start_prov_data/", response_description="Start Provenance Data", response_model=List[provenanceModel.ProvModel])
async def start_prov_data(provData: provenanceModel.ProvModel = Body(...)):  
    key = hashlib.sha256(provData.key.encode("utf-8")).hexdigest()

    provData = provenanceModel.ProvModel(id=provenanceModel.ObjectId() ,key=key, data=provData.data)
    
    provData = jsonable_encoder(provData)
    
    new_provData = await database.db["provenanceData"].insert_one(provData)
    created_provData = await database.db["provenanceData"].find_one({"_id": new_provData.inserted_id})
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_provData)

@router.get("/create_png/{id}", response_description="Convert one prov document to a png")
async def create_png(id: str):
    # Get the last data on provenanceData database
    # provDocument = await database.db['provenanceData'].find().to_list(10000)
    lastProvDocument = await show_provData(id)
    # Convet a povData from json to provenance document
    
    file_name = "provData.png"
    
    provenance_filepath = Path("/home/romulo/www/bolsa/ApiFiles/" + file_name)
    file_path = str(provenance_filepath)
    
    provDocument = function.json2DocumentProvenance(lastProvDocument['data'])
    dot = provDot.prov_to_dot(provDocument)
    dot.write_png(provenance_filepath)
    
    return FileResponse(path=file_path, media_type='application/octet-stream', filename=file_name)


@router.get("/create_png_last", response_description="Convert the last prov document to a png")
async def create_png_last():
    # Get the last data on provenanceData database
    provDocument = await database.db['provenanceData'].find().to_list(10000)
    lastProvDocument = provDocument[len(provDocument)-1]
    # Convet a povData from json to provenance document
    
    file_name = "provData.png"
    
    provenance_filepath = Path("/home/romulo/www/bolsa/ApiFiles/" + file_name)
    file_path = str(provenance_filepath)
    
    provDocument = function.json2DocumentProvenance(lastProvDocument['data'])
    dot = provDot.prov_to_dot(provDocument)
    dot.write_png(provenance_filepath)
    
    return FileResponse(path=file_path, media_type='application/octet-stream', filename=file_name)

