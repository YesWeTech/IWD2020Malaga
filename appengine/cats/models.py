#!/usr/bin/env python

from datetime import date
from enum import Enum
from google.cloud import ndb
from pydantic import BaseModel
from typing import List, Dict


class SpeciesEnum(str, Enum):
    """Defines all allowed species in our system."""
    european = 'european'
    british = 'british'
    persian = 'persian'
    norweian_forest_cat = 'norweian forest cat'


class Cat(BaseModel):
    """Defines what a Cat is at API level."""
    name: str
    date_of_birth: date
    weight: float
    species: SpeciesEnum = SpeciesEnum.european
    id: str = ''


class CatNDB(ndb.Model):
    """Defines what a Cat is at database level."""
    name = ndb.StringProperty()
    date_of_birth = ndb.DateProperty()
    weight = ndb.FloatProperty()
    species = ndb.StringProperty()


class Meta(BaseModel):
    """Defines meta properties in a API list response."""
    cursor: str


class APIResponse(BaseModel):
    """Defines response structure following jsonapi specification."""
    data: List[Cat]
    meta: Meta
