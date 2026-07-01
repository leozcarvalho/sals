from datetime import date
from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.receita import ReceitaRead, ReceitaFilter
from src.schemas.receita_produzir import ReceitaProduzirRead
from src.schemas.receita_distribuicao import ReceitaDistribuicaoRead
from src.cruds.receita import ReceitaRepository
from src.cruds.receita_produzir import ReceitaProduzirRepository
from src.cruds.receita_distribuicao import ReceitaDistribuicaoRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.schemas.api_response import ApiResponse
from src.schemas.users import UserBase
from src.scripts.gerar_receitas import gerar_receitas


def get_receita_service(session=Depends(get_session)):
    return ReceitaRepository(session)


router_receitas = BaseRouter(
    prefix="/receitas",
    read_schema=ReceitaRead,
    create_schema=ReceitaRead,
    update_schema=ReceitaRead,
    filter_schema=ReceitaFilter,
    get_service=get_receita_service,
    get_current_user=get_current_user,
    tags=["Receitas"],
    exclude_routes=["create", "update", "delete"],
)


@router_receitas.router.get("/{receita_id}/produzir")
def get_produzir(
    receita_id: int,
    session=Depends(get_session),
    current_user: UserBase = Depends(get_current_user),
):
    itens = ReceitaProduzirRepository(session).get_by_receita(receita_id)
    return ApiResponse(success=True, data=itens, error=None)


@router_receitas.router.get("/{receita_id}/distribuicao")
def get_distribuicao(
    receita_id: int,
    session=Depends(get_session),
    current_user: UserBase = Depends(get_current_user),
):
    itens = ReceitaDistribuicaoRepository(session).get_by_receita(receita_id)
    return ApiResponse(success=True, data=itens, error=None)


@router_receitas.router.post("/gerar")
def gerar(
    data_base: date,
    considerar_fracao_liquida: bool = False,
    session=Depends(get_session),
    current_user: UserBase = Depends(get_current_user),
):
    receitas = gerar_receitas(session, data_base=data_base, considerar_fracao_liquida=considerar_fracao_liquida)
    return ApiResponse(success=True, data={"total": len(receitas)}, error=None)
