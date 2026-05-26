from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime

from datetime import datetime

from backend.database.database import Base


class Review(Base):

    __tablename__ = "reviews"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    review_text = Column(String)

    sentiment = Column(String)

    confidence = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )