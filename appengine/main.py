#!/usr/bin/env python

from cats import models, backend
from fastapi import FastAPI, HTTPException
import grpc
from google.protobuf.message import DecodeError
from typing import List

app = FastAPI()


@app.post('/cats')
async def store_cats(cats: List[models.Cat]):
    """Store new cats in the database."""
    backend.store_cats(cats)


@app.get('/cats', response_model=models.APIResponse)
async def retrieve_cats(limit: int = 5, cursor: str = None):
    """Retrieve cats from database."""
    try:
        res, cursor = backend.retrieve_cats(limit, cursor)
    except grpc._channel._MultiThreadedRendezvous:
        raise HTTPException(status_code=400, detail='Invalid cursor')
    return {'data': res, 'meta': {'cursor': cursor}}


@app.get('/cat/{id}', response_model=models.Cat)
async def retrieve_cat_by_id(id: str):
    """Retrieve a single cat from database."""
    try:
        cat = backend.retrieve_cat_by_id(id)
        if cat is None:
            raise HTTPException(status_code=404, detail='Cat not found')
    except DecodeError:
        raise HTTPException(status_code=400, detail='Invalid Cat ID')


@app.delete('/cat/{id}')
async def delete_cat(id: str):
    """Delete a cat from datastore by ID."""
    try:
        backend.delete_cat(id)
    except DecodeError:
        raise HTTPException(status_code=400, detail='Invalid Cat ID')
