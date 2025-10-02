from sqlmodel import Session
from src.cruds.repo import Repository
from src.domain.feeding_curve_detail import FeedingCurveDetail

class FeedingCurveDetailRepository(Repository):
    def __init__(self, db_session: Session):
        super().__init__(FeedingCurveDetail, db_session)
    
    def delete_by_feeding_curve_id(self, feeding_curve_id: int):
        self.db_session.query(FeedingCurveDetail).filter(FeedingCurveDetail.feeding_curve_id == feeding_curve_id).delete()
        self.db_session.commit()
