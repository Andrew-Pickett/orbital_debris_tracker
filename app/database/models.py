
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
