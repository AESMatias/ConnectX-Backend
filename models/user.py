from sqlalchemy import Table, Column, DateTime
from sqlalchemy.sql.sqltypes import Integer, String, TIMESTAMP, Boolean
from sqlalchemy.sql.expression import text

from config.db import meta, engine

users = Table("users", meta, 
    Column("id", Integer, primary_key=True),
    Column("nickName", String(255)), 
    Column("password", String(255)),
    Column("creationDate", DateTime, server_default=text('CURRENT_TIMESTAMP')),
    Column("sessionState", Boolean)
    )

meta.create_all(engine)