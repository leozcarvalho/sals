from sqlmodel import Session
from src.cruds.repo import Repository
from src.domain.feeding_curve import FeedingCurve

class FeedingCurveRepository(Repository):
    def __init__(self, db_session: Session):
        super().__init__(FeedingCurve, db_session)