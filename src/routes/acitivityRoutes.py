from fastapi import APIRouter, Body, HTTPException, status
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import src.models.provenanceModel as provenanceModel
import src.database.database as database

#APIRouter creates path operations for item module
router = APIRouter(
   prefix="/activity",
   tags=["Activity Router"],
   responses={404: {"description": "Not found"}},
)

@router.get("/", response_description="List all activities", response_model=List[provenanceModel.activityModel])
async def list_activities():
   provData = await database.db["activity"].find().to_list(1000)
   return provData

@router.get("/get/{idActivity}", response_description="Get a single activity", response_model=provenanceModel.activityModel)
async def show_activity(idActivity: str):
   if (activity := await database.db["activity"].find_one({"_id": idActivity})) is not None:
      return activity

   raise HTTPException(status_code=404, detail=f"Activity {idActivity} not found")

@router.get("/get/name/{nameActivity}", response_description="Get a single activity by name", response_model=provenanceModel.activityModel)
async def show_activity_name(nameActivity: str):
   if (activity := await database.db["activity"].find_one({"name": nameActivity})) is not None:
      return activity

   raise HTTPException(status_code=404, detail=f"Activity {nameActivity} not found")
 
@router.post("/post/", response_description="Add new activity", response_model=provenanceModel.activityModel)
async def create_activity(activity: provenanceModel.activityModel = Body(...)):
   activity = jsonable_encoder(activity)
   
   if (activity := await database.db["activity"].find_one({"_id": activity["name"]})) is not None:
      print("Already exists")
      return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"error": "Already exists"})
   else:
      new_activity = await database.db["activity"].insert_one(activity)
      created_activity = await database.db["activity"].find_one({"_id": new_activity.inserted_id})
      return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_activity)