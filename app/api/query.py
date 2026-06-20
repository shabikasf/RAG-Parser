from fastapi import APIRouter, Request
from app.models.models import QueryRequest

app = APIRouter()

@app.post("/query")
def query(request: Request,  query: QueryRequest):

    query_service = request.app.state.container.query_service

    return query_service.query(
        query.query
    )