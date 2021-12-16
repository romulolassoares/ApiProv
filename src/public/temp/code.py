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

# import routes
from src.routes.provRoutes import router as prov_router
from src.routes.acitivityRoutes import router as activity_router, show_activity
from src.routes.agentRoutes import router as agent_router, show_agent
from src.routes.entityRoutes import router as entity_router, show_entity
from src.routes.relationshipRoutes import router as relationship_routes

# Import files
import src.routes.provRoutes as provRoutes
import src.models.provenanceModel as provenanceModel
import src.controller.provenance as provenance
import src.controller.func as functions
import src.database.database as database


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
 
 
@app.post("/prov", response_description="Test prov data")
async def create_student():
    provData = testing()
    dataString = provData.serialize()
    data = json.loads(dataString)

    return(data["activity"]["transaction001"])

@app.get("/test", response_description="test")
async def list_test():
    provData = await provRoutes.show_provData("61abb860931f83749150a74f")
    document = functions.json2DocumentProvenance(provData["data"])
    
    document2 = prov.ProvDocument()
    document2.set_default_namespace('http://localhost:4444/')
           
    activityTransaction = provenance.generateTransactionActivity(document2, "transaction002", "e619269265072f5b3c9b3cce1ed0ebe2", "date")
    activityTransaction.wasAssociatedWith(document2.agent("useR01"))
    document.update(document2)
    
    provDataDoc = document.serialize()
    provDataDoc = json.loads(provDataDoc)
    
    
    return provDataDoc
    
    


@app.get("/relationships/{idActivity}&{idEntity}&{idAgent}", response_description="Generate Relationships")
async def generate_relationship(idActivity: str, idEntity: str, idAgent: str):
    dataAgent = await show_agent(idAgent)
    dataActivity = await show_activity(idActivity)
    dataEntity = await show_entity(idEntity)
    return {
        "activity": dataActivity,
        "entity": dataEntity,
        "agent": dataAgent    
    }
    
    
@app.get("/relationships2/{idActivityTransaction}&{idActivityGeneratedDoc}&{idEntityPrint}&{idEntityDoc}&{idAgent}", response_description="Generate Relationships")
async def generate_relationship(idActivityTransaction: str, idActivityGeneratedDoc: str, idEntityPrint: str, idEntityDoc: str, idAgent: str):
    dataActivityTransaction = await show_activity(idActivityTransaction)
    dataActivityGeneratedDoc = await show_activity(idActivityGeneratedDoc)
    dataEntityPrint = await show_entity(idEntityPrint)
    dataEntityDoc = await show_entity(idEntityDoc)
    dataAgent = await show_agent(idAgent)
    
    document = provenance.generateTransactionRelationship(dataAgent, dataActivityTransaction, dataActivityGeneratedDoc, dataEntityPrint, dataEntityDoc)
    
    provenance.generateImage(document)
       
    data = document.serialize()
    dataJson = json.loads(data)
    
    data2 = await provRoutes.create_provData(data)
    
    return data2