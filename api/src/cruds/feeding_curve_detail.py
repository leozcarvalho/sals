from sqlmodel import Session
from src.cruds.repo import Repository
from src.domain.feeding_curve_detail import FeedingCurveDetail

class FeedingCurveDetRepository(Repository):
    def __init__(self, db_session: Session):
        super().__init__(FeedingCurveDetail, db_session)
