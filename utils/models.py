from sqlmodel import SQLModel, Field
from datetime import datetime
from sqlalchemy import text
import uuid


class IDTimeBasedModel(SQLModel):
    id : uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        sa_column_kwargs={"server_default" : text("gen_random_uuid()"), "unique" : True}
    )
    created_at : datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"server_default" : text("current_timestamp(0)")}
    )
    modified_at : datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={
            "server_default" : text("current_timestamp(0)"),
            "onupdate" : text("current_timestamp(0)"),
            }
    )