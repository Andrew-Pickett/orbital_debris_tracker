from pydantic import BaseModel


class DataModel(BaseModel):
    NORAD_CAT_ID: int
    OBJECT_NAME: str
    EPOCH: str
    MEAN_MOTION: float
    ECCENTRICITY: float
    INCLINATION: float
    RA_OF_ASC_NODE: float
    ARG_OF_PERICENTER: float
    MEAN_ANOMALY: float
    OBJECT_TYPE: str
    DECAY_DATE: str | None = None


from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Date, DateTime

from datetime import datetime, date


class Base(DeclarativeBase):
    pass


class SpaceTrackRecord(Base):
    __tablename__ = "space_track_records"

    NORAD_CAT_ID: Mapped[int] = mapped_column(primary_key=True)
    OBJECT_NAME: Mapped[str]
    EPOCH: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    MEAN_MOTION: Mapped[float]
    ECCENTRICITY: Mapped[float]
    INCLINATION: Mapped[float]
    RA_OF_ASC_NODE: Mapped[float]
    ARG_OF_PERICENTER: Mapped[float]
    MEAN_ANOMALY: Mapped[float]
    OBJECT_TYPE: Mapped[str]
    DECAY_DATE: Mapped[date | None] = mapped_column(Date, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
