from fastapi import APIRouter

import json

import src.controller.func as function
import src.database.database as database
import src.controller.provenance as provenance
import src.routes.provRoutes as provRoutes
import src.routes.agentRoutes as agentRoutes
import src.routes.acitivityRoutes as activityRoutes
import src.routes.entityRoutes as entityRoutes

router = APIRouter(
   prefix="/relationship",
   tags=["Relationship Router"],
   responses={404: {"description": "Not found"}},
)

async def sendToDatabase(provID, document):
   await provRoutes.update_provData(provID, document)

def generateNewProvDocument(provDocument, lastProvDocument):
   dataSTR = provDocument.serialize(None, 'json')
   dataJSON = json.loads(dataSTR)
   newProvDocument = lastProvDocument
   newProvDocument["data"] = dataJSON
   return newProvDocument

@router.post("/was_used/{idActivity}&{idEntity}", response_description="Was Used")
async def was_used(idActivity: str, idEntity: str):
   provDocument = await database.db['provenanceData'].find().to_list(1000)
   lastProvDocument = provDocument[len(provDocument)-1]

   provDocument = function.json2DocumentProvenance(lastProvDocument['data'])
   
   activityDB = await activityRoutes.show_activity(idActivity)
   entityDB = await entityRoutes.show_entity(idEntity)
   
   activity = provenance.generateActivity(provDocument, activityDB['name'], activityDB['_id'])
   entity = provenance.generateEntity(provDocument, entityDB['name'], entityDB['_id'])
   
   activity.used(entity)
   
   # dictData = json.loads(provDocument.serialize())
   # await sendToDatabase(lastProvDocument["_id"], dictData)
   
   newProvDocument = generateNewProvDocument(provDocument, lastProvDocument)
   await provRoutes.create_provData(newProvDocument)
   
   return newProvDocument

@router.post("/was_generated_by/{idActivity}&{idEntity}", response_description="Was Used")
async def was_generated_by(idActivity: str, idEntity: str):
   provDocument = await database.db['provenanceData'].find().to_list(1000)
   lastProvDocument = provDocument[len(provDocument)-1]

   provDocument = function.json2DocumentProvenance(lastProvDocument['data'])
   
   activityDB = await activityRoutes.show_activity(idActivity)
   entityDB = await entityRoutes.show_entity(idEntity)
   
   activity = provenance.generateActivity(provDocument, activityDB['name'], activityDB['_id'])
   entity = provenance.generateEntity(provDocument, entityDB['name'], entityDB['_id'])
   
   entity.wasGeneratedBy(activity)
   newProvDocument = generateNewProvDocument(provDocument, lastProvDocument)
   await provRoutes.create_provData(newProvDocument)
   
   return newProvDocument

@router.post("/was_attribuited_to/{idAgent}&{idEntity}", response_description="Was Used")
async def was_attribuited_to(idAgent: str, idEntity: str):
   provDocument = await database.db['provenanceData'].find().to_list(10000)
   lastProvDocument = provDocument[len(provDocument)-1]
   
   provDocument = function.json2DocumentProvenance(lastProvDocument['data'])
   
   agentDB = await agentRoutes.show_agent(idAgent)
   entityDB = await entityRoutes.show_entity(idEntity)
   
   agent = provenance.generateActivity(provDocument, agentDB['name'], agentDB['_id'])
   entity = provenance.generateEntity(provDocument, entityDB['name'], entityDB['_id'])
   
   entity.wasAttributedTo(agent)
   
   newProvDocument = generateNewProvDocument(provDocument, lastProvDocument)
   await provRoutes.create_provData(newProvDocument)
   
   return newProvDocument

@router.post("/was_associated_with/{idAgent}&{idActivity}", response_description="Was Used")
async def was_associated_with(idAgent: str, idActivity: str):
   provDocument = await database.db['provenanceData'].find().to_list(10000)
   lastProvDocument = provDocument[len(provDocument)-1]

   provDocument = function.json2DocumentProvenance(lastProvDocument['data'])
   agentDB = await agentRoutes.show_agent(idAgent)

   activityDB = await activityRoutes.show_activity(idActivity)
   agent = provenance.generateActivity(provDocument, agentDB['name'], agentDB['_id'])
   activity = provenance.generateEntity(provDocument, activityDB['name'], activityDB['_id'])
   
   # activity.wasAssociatedWith(agent)
   agent.wasAssociatedWith(activity)
   
   newProvDocument = generateNewProvDocument(provDocument, lastProvDocument)
   await provRoutes.create_provData(newProvDocument)
   
   return newProvDocument

@router.post("/was_derived_from/{idEntity1}&{idEntity2}", response_description="Was Used")
async def was_derived_from(idEntity1: str, idEntity2: str):
   provDocument = await database.db['provenanceData'].find().to_list(10000)
   lastProvDocument = provDocument[len(provDocument)-1]

   provDocument = function.json2DocumentProvenance(lastProvDocument['data'])
   entity1DB = await entityRoutes.show_entity(idEntity1)

   entity2DB = await entityRoutes.show_entity(idEntity2)
   entity1 = provenance.generateEntity(provDocument, entity1DB['name'], entity1DB['_id'])
   entity2 = provenance.generateEntity(provDocument, entity2DB['name'], entity2DB['_id'])
   
   entity1.wasDerivedFrom(entity2)
   
   newProvDocument = generateNewProvDocument(provDocument, lastProvDocument)
   await provRoutes.create_provData(newProvDocument)
   
   return newProvDocument

@router.post("/acted_on_behalf_of/{idAgent1}&{idAgent2}", response_description="Was Used")
async def acted_on_behalf_of(idAgent1: str, idAgent2: str):
   provDocument = await database.db['provenanceData'].find().to_list(10000)
   lastProvDocument = provDocument[len(provDocument)-1]

   provDocument = function.json2DocumentProvenance(lastProvDocument['data'])
   
   agent1DB = await agentRoutes.show_agent(idAgent1)
   agent2DB = await agentRoutes.show_agent(idAgent2)
   
   agent1 = provenance.generateAgent(provDocument, agent1DB['name'], agent1DB['_id'])
   agent2 = provenance.generateAgent(provDocument, agent2DB['name'], agent2DB['_id'])
   
   agent1.actedOnBehalfOf(agent2)
   
   newProvDocument = generateNewProvDocument(provDocument, lastProvDocument)
   await provRoutes.create_provData(newProvDocument)
   
   return newProvDocument

@router.post("/was_informed_by/{idActivity1}&{idActivity2}", response_description="Was Used")
async def was_informed_by(idActivity1: str, idActivity2: str):
   provDocument = await database.db['provenanceData'].find().to_list(1000)
   lastProvDocument = provDocument[len(provDocument)-1]

   provDocument = function.json2DocumentProvenance(lastProvDocument['data'])
   
   activity1DB = await activityRoutes.show_activity(idActivity1)
   activity2DB = await activityRoutes.show_activity(idActivity2)
   
   activity1 = provenance.generateActivity(provDocument, activity1DB['name'], activity1DB['_id'])
   activity2 = provenance.generateactivity(provDocument, activity2DB['name'], activity2DB['_id'])
   
   activity1.wasInformedBy(activity2)
   
   newProvDocument = generateNewProvDocument(provDocument, lastProvDocument)
   await provRoutes.create_provData(newProvDocument)
   
   return newProvDocument