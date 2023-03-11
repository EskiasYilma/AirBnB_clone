#!/usr/bin/python3
"""
Initialize storage

Defines the entry point of the command interpreter
"""
from models.engine import file_storage


storage = file_storage.FileStorage()
storage.reload()
