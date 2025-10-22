from src.cruds.svg import SvgRepository
from src.schemas.svg import SVGCreate

SVG = SVGCreate(
    name="Test SVG",
    owner_type="shed",
    owner_id=1,
    content="<svg></svg>"
)

def create_svg(session, actor=None, **overrides):
    repo = SvgRepository(session)
    svg_dict = SVG.model_dump()
    svg_dict.update(overrides)
    svg = SVGCreate(**svg_dict)
    svg = repo.save(svg.model_dump(), actor=actor)
    return svg
