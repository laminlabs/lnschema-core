from sqlalchemy.sql import func
from sqlmodel import Field

CreatedAt = Field(index=True, sa_column_kwargs=dict(server_default=func.now()))
UpdatedAt = Field(default=None, index=True, sa_column_kwargs=dict(onupdate=func.now()))
