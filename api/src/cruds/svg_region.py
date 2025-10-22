from sqlalchemy.orm import Session
from src.domain.svg_region import SVGRegion
from src.cruds.repo import Repository

class SvgRegionRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(SVGRegion, session)
