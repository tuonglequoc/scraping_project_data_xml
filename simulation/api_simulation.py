from sys import prefix
from typing import Optional
from uuid import UUID

from fastapi import FastAPI, Response, APIRouter

URL_PREFIX = "/_api/ProjectData"

app = FastAPI(prefix=URL_PREFIX)

project_router = APIRouter()


def get_data_from_file(filename: str):
    with open(filename, "r") as file:
        content = file.read()
    return content

@project_router.get("/")
def read_root():
    data = get_data_from_file("ProjectData_APIresponse.xml")
    return Response(content=data, media_type="application/xml")


@project_router.get("/Projects(guid'{project_id}')/Assignments")
def get_assignments(project_id: UUID):
    data = get_data_from_file("Assignments_APIresponse.xml")
    return Response(content=data, media_type="application/xml")



@project_router.get("/Projects(guid'{project_id}')/Tasks")
def get_tasks(project_id: UUID):
    data = get_data_from_file("Tasks_APIresponse.xml")
    return Response(content=data, media_type="application/xml")


app.include_router(project_router, prefix=URL_PREFIX)