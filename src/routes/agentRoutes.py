from fastapi import APIRouter, Body, HTTPException, status
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import src.models.provenanceModel as provenanceModel
import src.database.database as database

#APIRouter creates path operations for item module
router = APIRouter(
   prefix="/agent",
   tags=["Agent Router"],
   responses={404: {"description": "Not found"}},
)

@router.get("/", response_description="List all agents", response_model=List[provenanceModel.agentModel])
async def list_agents():
   provData = await database.db["agent"].find().to_list(1000)
   return provData

@router.get("/get/{idAgent}}", response_description="Get a single agent", response_model=provenanceModel.agentModel)
async def show_agent(idAgent: str):
    if (agent := await database.db["agent"].find_one({"_id": idAgent})) is not None:
        return agent

    raise HTTPException(status_code=404, detail=f"Agent {idAgent} not found")

@router.get("/get/name/{nameAgent}}", response_description="Get a single agent by name", response_model=provenanceModel.agentModel)
async def show_agent_name(nameAgent: str):
    if (agent := await database.db["agent"].find_one({"name": nameAgent})) is not None:
        return agent

    raise HTTPException(status_code=404, detail=f"Agent {nameAgent} not found")

@router.post("/post/", response_description="Add new agent", response_model=provenanceModel.agentModel)
async def create_agent(agent: provenanceModel.agentModel = Body(...)):
    agent = jsonable_encoder(agent)
    
    if (agent := await database.db["agent"].find_one({"name": agent["name"]})) is not None:
        print("Already exists")
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"error": "Already exists"})
    else:
        new_agent = await database.db["agent"].insert_one(agent)
        created_agent = await database.db["agent"].find_one({"_id": new_agent.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_agent)



