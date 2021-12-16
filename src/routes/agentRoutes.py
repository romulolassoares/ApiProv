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

    raise HTTPException(status_code=404, detail=f"Agent {id} not found")

@router.post("/post/", response_description="Add new agent", response_model=provenanceModel.agentModel)
async def create_agent(agent: provenanceModel.agentModel = Body(...)):
    agent = jsonable_encoder(agent)
    new_agent = await database.db["agent"].insert_one(agent)
    created_agent = await database.db["agent"].find_one({"_id": new_agent.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_agent)



