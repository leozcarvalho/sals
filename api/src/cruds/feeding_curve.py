from sqlmodel import Session
from src.cruds.repo import Repository
from src.domain.feeding_curve import FeedingCurve
from src.cruds.feeding_curve_detail import FeedingCurveDetailRepository
from src.schemas.feeding_curve_detail import FeedingCurveDetailCreate
from typing import List

class FeedingCurveRepository(Repository):
    def __init__(self, db_session: Session):
        super().__init__(FeedingCurve, db_session)
        self.detail_repository = FeedingCurveDetailRepository(db_session)
    
    def save(self, values, actor=None):
        details = values.pop('details', None) or []
        feeding_curve = super().save(values, actor)
        self.__update_details(feeding_curve.id, details, actor)
        return feeding_curve
    
    def update(self, id, values, actor=None):
        details = values.pop('details', None) or []
        feeding_curve = super().update(id, values, actor)
        self.__update_details(feeding_curve.id, details, actor)
        return feeding_curve

    def __update_details(self, feeding_curve_id: int, details: List[FeedingCurveDetailCreate], actor=None):
        self.detail_repository.delete_by_feeding_curve_id(feeding_curve_id)
        for detail in details:
            values = dict(
                feeding_curve_id=feeding_curve_id,
                age_day=detail['age_day'],
                formula_id=detail['formula_id'],
                formula_mass_per_animal=detail['formula_mass_per_animal'],
                is_active=detail['is_active'],
                animal_weight=detail['animal_weight']
            )
            self.detail_repository.save(values, actor)
