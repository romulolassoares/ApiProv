from fastapi import FastAPI

# import routes
from src.routes.provRoutes import router as prov_router
from src.routes.acitivityRoutes import router as activity_router
from src.routes.agentRoutes import router as agent_router
from src.routes.entityRoutes import router as entity_router
from src.routes.relationshipRoutes import router as relationship_routes
# from src.routes.newRelationShipsRoutes import router as new_relationship_routes


app = FastAPI()

app.include_router(prov_router)
app.include_router(activity_router)
app.include_router(agent_router)
app.include_router(entity_router)
app.include_router(relationship_routes)
# app.include_router(new_relationship_routes)


@app.get("/", response_description="Home")
async def home():
    data = {
        "Connect": "You are connected with api-prov",
        "Documents": "http://github.com",
        "Status": "200"
    }
    return data