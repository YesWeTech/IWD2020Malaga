#!/usr/bin/env python

import logging
from google.cloud import ndb
from typing import List

from cats import models

client = ndb.Client()
logger = logging.getLogger('app')


def _cat_to_ndb(cat: models.Cat) -> models.CatNDB:
    """Transforms an API object to a NDB object."""
    return models.CatNDB(name=cat.name, date_of_birth=cat.date_of_birth,
                         weight=cat.weight, species=cat.species)


def _ndb_to_cat(cat: models.CatNDB) -> models.Cat:
    """Transforms a NDB object to an API object."""
    return models.Cat(name=cat.name, date_of_birth=cat.date_of_birth,
                      weight=cat.weight, species=cat.species,
                      id=cat.key.urlsafe())


def store_cats(cats: List[models.Cat]):
    """Store a list of cats in datastore."""
    logger.info('Storing %d new cats.', len(cats))
    ndb_cats = [_cat_to_ndb(c) for c in cats]
    with client.context():
        ndb.put_multi(ndb_cats)


def retrieve_cats(limit: int = 2, cursor: str = None):
    """Retrieves cats from datastore."""
    logger.info('Retrieving all cats')
    with client.context():
        query = models.CatNDB.query()
        res, cursor, _ = query.fetch_page(
            limit=limit, start_cursor=ndb.Cursor(urlsafe=cursor))

    return ([_ndb_to_cat(c) for c in res],
            cursor.urlsafe() if cursor is not None else '')


def retrieve_cat_by_id(id: str) -> models.Cat:
    """Retrieves a cat by id from datastore."""
    with client.context():
        cat = ndb.Key(urlsafe=id).get()
        if cat is None:
            logger.warning('Cat with ID %s not found', id)
            return None
        else:
            return _ndb_to_cat(cat)


def delete_cat(cat: str):
    """Deletes a single cats by its datastore Key."""
    with client.context():
        logger.info('Removing cat %s', cat)
        ndb.Key(urlsafe=cat).delete()
