import prov.model as prov
import datetime

from prov.dot import prov_to_dot
from pathlib import Path

import json




def generateDocument():
    document = prov.ProvDocument()
    document.set_default_namespace('')
    return document


def generateDocGeneratedActivity(document, name):
    activity = document.activity(
        name,
        datetime.datetime.now(),
        None,
        {
            prov.PROV_TYPE: "docGenerated",
        }
    ) 
    return activity

def generateTransactionActivity(document, name, pki, date):
    activity = document.activity(
        name,
        datetime.datetime.now(),
        None,
        {
            prov.PROV_TYPE: "transaction",
            "transactionKey": pki,
            "createdAt": date,
        }
    )
    return activity

def generatePrintEntity(document, name, destination):
    entity = document.entity(
        name,
        {
            prov.PROV_TYPE: "print",
            "destination": destination
        }
    )
    return entity

def generateDocumentEntity(document, name, author, title, format):
    entity = document.entity(
        name,
        {
            prov.PROV_TYPE: "doc",
            "author": author,
            "title": title,
            "format": format
        }
    )
    return entity

def generateUserAgent(document, name, pki):
    agent = document.agent(
        name,
        {
            prov.PROV_TYPE: "user",
            "pki": pki,
        }
    )
    return agent


def generateTransactionRelationship(dataAgent, dataActivityTransaction, dataActivityGeneratedDoc, dataEntityPrint, dataEntityDoc):
    document = prov.ProvDocument()
    document.set_default_namespace('http://localhost:4444/')
    document.add_namespace('example', 'http://localhost:4444/example/')
    # generating provenance activities
    activityTransaction = generateTransactionActivity(document, dataActivityTransaction["name"], dataActivityTransaction["info"]["pki"], dataActivityTransaction["info"]["date"])
    activityGeneratePrint = generateDocGeneratedActivity(document, dataActivityGeneratedDoc["name"])

    # generating provenance entities
    entityDoc = generateDocumentEntity(document, dataEntityDoc["name"], dataEntityDoc["info"]["author"], dataEntityDoc["info"]["title"], dataEntityDoc["info"]["format"])
    entityPrint = generatePrintEntity(document, dataEntityPrint["name"], dataEntityPrint["info"]["destination"])

    # generating provenance agents
    agent = generateUserAgent(document, dataAgent["name"], dataAgent["pki"])

    # Defining relationships
    entityDoc.wasGeneratedBy(activityGeneratePrint)
    entityDoc.wasDerivedFrom(entityPrint)

    activityTransaction.used(entityPrint)
    activityTransaction.wasAssociatedWith(agent)

    activityGeneratePrint.wasInformedBy(activityTransaction)

    entityPrint.wasGeneratedBy(activityTransaction)
    
    return document


def generateImage(document):
    provenance_filepath = Path("files/provDataTest.provn")
    print('Writing provenance to:', provenance_filepath)

    with provenance_filepath.open('w') as f:
        f.write(document.get_provn())

    # Visualise the provenance in a graphical representation
    dot = prov_to_dot(document)

    dot.write_png(provenance_filepath.with_suffix('.png'))
    
    
        # "Transaction",
        # "2012-03-31T09:21:00",
        # "2012-04-01T15:21:00",
        # {
        #     prov.PROV_TYPE: "transaction",
        #     "transactionKey": "e619269265072f5b3c9b3cce1ed0ebe2",
        #     "from": "Empresa A",
        #     "destination": "Empresa B",
        # }
    
def generateActivity(document, name, id, startTime, endTime, provType):
    activity = document.activity(
        name,
        startTime,
        endTime,
        {
            prov.PROV_TYPE: provType,
            "id": id,
        }
    ) 
    return activity

def generateEntity(document, name, id):
    entity = document.entity(
        name,
        {
            prov.PROV_TYPE: "doc",
            "id": id
        }
    )
    return entity

def generateAgent(document, name, id):
    agent = document.agent(
        name,
        {
            prov.PROV_TYPE: "user",
            "id": id,
        }
    )
    return agent