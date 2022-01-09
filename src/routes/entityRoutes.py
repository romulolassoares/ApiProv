from fastapi import APIRouter, Body, HTTPException, status
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import src.models.provenanceModel as provenanceModel
import src.database.database as database

#APIRouter creates path operations for item module
router = APIRouter(
   prefix="/entity",
   tags=["Entity Router"],
   responses={404: {"description": "Not found"}},
)

@router.get("/", response_description="List all entities", response_model=List[provenanceModel.activityModel])
async def list_entities():
   provData = await database.db["entity"].find().to_list(1000)
   return provData

@router.get("/get/{idEntity}", response_description="Get a single entity", response_model=provenanceModel.entityModel)
async def show_entity(idEntity: str):
    if (entity := await database.db["entity"].find_one({"_id": idEntity})) is not None:
        return entity

    raise HTTPException(status_code=404, detail=f"Entity {idEntity} not found")

@router.get("/get/name/{nameEntity}", response_description="Get a single entity", response_model=provenanceModel.entityModel)
async def show_entity_name(nameEntity: str):
    if (entity := await database.db["entity"].find_one({"name": nameEntity})) is not None:
        return entity

    raise HTTPException(status_code=404, detail=f"Entity {nameEntity} not found")


@router.post("/post/", response_description="Add new entity by name", response_model=provenanceModel.entityModel)
async def create_entity(entity: provenanceModel.entityModel = Body(...)):
    entity = jsonable_encoder(entity)
        
    if (entity := await database.db["entity"].find_one({"name": entity["name"]})) is not None:
        print("Already exists")
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"error": "Already exists"})
    else:
        new_entity = await database.db["entity"].insert_one(entity)
        created_entity = await database.db["entity"].find_one({"_id": new_entity.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_entity)