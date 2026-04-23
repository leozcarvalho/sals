import json
from math import ceil
from decimal import Decimal
from collections import defaultdict
from datetime import date
from typing import TYPE_CHECKING
import logging

from src.core.db import session_scope
from src.cruds.batch import BatchRepository
from src.cruds.trato import TratoRepository
from src.cruds.product import ProductRepository

if TYPE_CHECKING:
    from src.domain import (
        Batch,
        Trato,
        Product,
        Formula,
        FormulaDetail,
        FeedingCurve,
        FeedingCurveDetail,
        Kitchen,
        Shed,
        Sala,
        Baia,
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =========================================================
# HELPERS
# =========================================================
def d(v): return Decimal(str(v))
def r(v): return v.quantize(Decimal("0.01"))

WATER_PRODUCT_ID = 1  # ID do produto Água — nunca pode ser apagado


# =========================================================
# DIA CURVA
# =========================================================
def calcular_dia_curva(lote: "Batch", data_base: date) -> int:
    if not lote.created_at:
        raise ValueError(f"Lote {lote.id} não possui data de criação.")
    dias_passados = (data_base - lote.created_at.date()).days
    if dias_passados < 0:
        raise ValueError(f"Data base {data_base} é anterior ao início do lote {lote.id}.")
    return dias_passados


def script_1(session, data_base: date, considerar_fracao_liquida: bool = False) -> dict:
    """
    Calcula o plano de alimentação diário por lote/sala/baia/trato.

    Args:
        session: Sessão do banco de dados.
        data_base: Data de referência para o cálculo.
        considerar_fracao_liquida: Se True, calcula a água proporcionalmente ao pct_agua
            da fórmula sem corrigir a umidade dos sólidos (método simplificado).

    Returns:
        dict com todas as matrizes de resultado.
    """

    batch_repo = BatchRepository(session)
    trato_repo = TratoRepository(session)
    product_repo = ProductRepository(session)

    lotes: list["Batch"] = batch_repo.get_list(filters={'is_active': True})
    tratos: list["Trato"] = trato_repo.get_list()
    produtos: list["Product"] = product_repo.get_list()

    trato_repo.validate_percent(tratos)

    # =========================================================
    # CACHE PRODUTOS (evita getattr + conversões repetidas)
    # =========================================================
    cache_produtos = {
        p.id: {
            "obj": p,
            "umid": d(p.moisture_percentage or 0),
            "dens": d(p.density or 0)
        }
        for p in produtos
    }

    # =========================================================
    # 1 LOTE POR SALA
    # =========================================================
    lotes_por_sala = {}
    for lote in lotes:
        if lote.sala.id not in lotes_por_sala:
            lotes_por_sala[lote.sala.id] = lote

    lotes = list(lotes_por_sala.values())

    consultas_curva = []
    dados_curva = []
    total_baia_trato = []
    total_formula_trato = defaultdict(Decimal)

    # cache de dia_curva e curva_dia/formula por lote — evita recalcular em múltiplos loops
    cache_dia_curva: dict[int, int] = {}
    cache_curva_dia: dict[int, object] = {}   # FeedingCurveDetail | None
    cache_formula: dict[int, object] = {}     # Formula | None

    for lote in lotes:
        dia = calcular_dia_curva(lote, data_base)
        cache_dia_curva[lote.id] = dia
        detalhes: list[FeedingCurveDetail] = lote.feeding_curve.details if lote.feeding_curve else []
        if dia < len(detalhes) and detalhes[dia] and detalhes[dia].formula:
            cache_curva_dia[lote.id] = detalhes[dia]
            cache_formula[lote.id] = detalhes[dia].formula
        else:
            cache_curva_dia[lote.id] = None
            cache_formula[lote.id] = None

    # =========================================================
    # LOOP PRINCIPAL
    # =========================================================
    for lote in lotes:

        sala: Sala = lote.sala
        galpao: Shed = sala.shed
        baias: list[Baia] = sala.baias

        consultas_curva.append({
            "LOTE": lote.id,
            "ID_SA": sala.id,
            "GALPAO": galpao.name
        })

        dia_curva = cache_dia_curva[lote.id]
        curva_dia = cache_curva_dia[lote.id]

        if not curva_dia:
            logger.warning("Lote %s: dia_curva %s fora do range ou sem fórmula. Ignorando.", lote.id, dia_curva)
            continue

        consumo_animal = d(curva_dia.formula_mass_per_animal)
        formula : Formula = cache_formula[lote.id]

        dados_curva.append({
            "GALPÃO": galpao.name,
            "SALA": sala.name,
            "ID_DIA_HOJE_NA_CURVA": dia_curva + 1,
            "DIA_HOJE_NA_CURVA": curva_dia.age_day,
            "P_SUINO_DIA": curva_dia.animal_weight,
            "P_ALIM_SECO_SUINO_DIA_HOJE": consumo_animal,
            "ID_FORMULA": formula.id,
            "FORMULA": formula.name,
            "MASSA_SECA_FORMULA": formula.water_percentage,
        })

        for baia in baias:
            qtd = d(baia.animals_quantity)
            consumo_baia = consumo_animal * qtd

            total_dia = d(0)

            for trato in tratos:
                if trato.percent == 0:
                    continue

                consumo_trato = r(consumo_baia * d(trato.percent) / 100)

                total_dia += consumo_trato
                total_formula_trato[(trato.id, formula.id, sala.name)] += consumo_trato

            total_baia_trato.append({
                "ID_BA": baia.id,
                "ID_SA": sala.id,
                "SUINOS": int(qtd),
                "P_SECO_DIA": float(r(total_dia))
            })

    # =========================================================
    # CACHE FORMULAS
    # =========================================================
    cache_formulas = {}

    matriz_producao_receita = []

    for lote in lotes:

        sala = lote.sala
        galpao = sala.shed

        dia_curva = cache_dia_curva[lote.id]
        curva_dia = cache_curva_dia[lote.id]

        if not curva_dia:
            logger.warning("Lote %s: dia_curva %s fora do range na receita. Ignorando.", lote.id, dia_curva)
            continue

        formula = cache_formula[lote.id]

        if formula.id not in cache_formulas:
            cache_formulas[formula.id] = {
                item.product_id: item
                for item in formula.details
            }

        map_formula = cache_formulas[formula.id]

        for trato in tratos:

            massa_total = total_formula_trato.get((trato.id, formula.id, sala.name), d(0))
            pct_seco_formula = (100 - d(formula.water_percentage)) / 100

            linhas = []
            soma_agua = d(0)

            for product_id, pdata in cache_produtos.items():
                produto = pdata["obj"]
                umid = pdata["umid"]
                dens = pdata["dens"]

                item = map_formula.get(product_id)
                pct_produto = d(item.product_percentage_without_moisture) if item else d(0)

                frac_seca = (100 - umid) / 100

                # M (Excel)
                massa_seca = (pct_produto / 100) * massa_total

                if product_id == WATER_PRODUCT_ID:
                    # Água é calculada depois como complemento — placeholder aqui
                    p_trato = d(0)
                elif considerar_fracao_liquida:
                    # Corrige a umidade do produto: divide pela fração seca
                    # para obter a massa úmida real que deve ser pesada.
                    # A diferença (P_TRATO − massa_seca) é a água interna,
                    # acumulada para calcular a água complementar.
                    p_trato_exato = massa_seca / frac_seca if frac_seca > 0 else d(0)
                    soma_agua += (p_trato_exato - massa_seca)
                    p_trato = r(p_trato_exato)
                else:
                    # Sem correção de umidade: replica a planilha
                    #   SE(EH_AGUA; massa_total/pct_seco; pct_produto/100*massa_total)
                    # → para não-água: pct_produto/100 * massa_total = massa_seca
                    p_trato = r(massa_seca)

                linhas.append({
                    "produto": produto,
                    "p_trato": p_trato,
                    "massa_seca": massa_seca,
                    "frac_seca": frac_seca,
                    "frac_h2o": 1 - frac_seca,
                    "umid": umid,
                    "dens": dens,
                    "pct_produto": pct_produto
                })

            # Água
            # considerar_fracao_liquida=True : sólidos corrigidos pela umidade;
            #   agua = (massa_total / pct_seco) − soma_agua  (complemento à mistura úmida)
            # considerar_fracao_liquida=False: sólidos usam massa_seca diretamente;
            #   agua = massa_total / pct_seco  — replica a planilha:
            #   SE(EH_AGUA; PROCX_massa_total / ((100−pct_agua)/100); massa_seca)
            if considerar_fracao_liquida:
                agua = (massa_total / pct_seco_formula if pct_seco_formula > 0 else d(0)) - soma_agua
            else:
                agua = massa_total / pct_seco_formula if pct_seco_formula > 0 else d(0)

            for linha_prod in linhas:
                if linha_prod["produto"].id == WATER_PRODUCT_ID:
                    linha_prod["p_trato"] = r(max(d(0), agua))

            # Montagem final
            for linha_prod in linhas:
                p_trato = r(linha_prod["p_trato"])
                dens = linha_prod["dens"]

                v_trato = r(p_trato / (dens / 1000)) if dens > 0 else d(0)

                row = {
                    "GALPÃO": galpao.name,
                    "SALA": sala.name,
                    "ID_PR": linha_prod["produto"].id,
                    "PRODUTO": linha_prod["produto"].name,
                    "D_PR": linha_prod["dens"],
                    "ID_FO": formula.id,
                    "TRATO": trato.id,
                    "PCT_H20_FO": float(formula.water_percentage),
                    "PCT_PR_100_PCT_S_H2O_FO": float(linha_prod["pct_produto"]),
                    "EH_AGUA": linha_prod["produto"].id == WATER_PRODUCT_ID,
                    "P_TRATO_S_CALC_UMID": float(r(linha_prod["massa_seca"])),
                    "P_TRATO": p_trato,
                    "V_TRATO": v_trato,
                    "PCT_UMID_PR": float(linha_prod["umid"]),
                    "FRAC_SECA_PR": float(linha_prod["frac_seca"]),
                    "FRAC_H2O_PR": float(linha_prod["frac_h2o"]),
                }

                if not considerar_fracao_liquida:
                    row.pop("P_TRATO_S_CALC_UMID", None)
                    row.pop("PCT_UMID_PR", None)
                    row.pop("FRAC_SECA_PR", None)
                    row.pop("FRAC_H2O_PR", None)

                matriz_producao_receita.append(row)

    # =========================================================
    # 🔥 AGRUPAMENTO (remove O(n²))
    # =========================================================
    agrupado = defaultdict(lambda: {"sum_p": d(0), "sum_v": d(0)})

    for linha in matriz_producao_receita:
        chave = (linha["SALA"], linha["TRATO"], linha["ID_FO"])
        agrupado[chave]["sum_p"] += linha["P_TRATO"]
        agrupado[chave]["sum_v"] += linha["V_TRATO"]

    # =========================================================
    # RAÇÃO LIQUIDA
    # =========================================================
    matriz_racao_totalizada = []

    for lote in lotes:

        sala : Sala = lote.sala
        galpao : Shed = sala.shed
        cozinha : Kitchen = galpao.kitchen

        if not cozinha:
            continue

        v_max_cz = d(cozinha.volume_misturador)
        pct_util = d(cozinha.fracao_volume_misturador) / 100
        v_max_util = v_max_cz * pct_util

        dia_curva_racao = cache_dia_curva[lote.id]
        curva_dia_racao = cache_curva_dia[lote.id]

        if not curva_dia_racao:
            logger.warning("Lote %s: dia_curva %s fora do range na ração líquida. Ignorando.", lote.id, dia_curva_racao)
            continue

        formula = cache_formula[lote.id]

        for trato in tratos:

            chave = (sala.name, trato.id, formula.id)
            sum_p = agrupado[chave]["sum_p"]
            sum_v = agrupado[chave]["sum_v"]

            div = sum_v / v_max_util if v_max_util > 0 else d(0)
            etapas = int(ceil(div)) if v_max_util > 0 else 0

            v_etapa = r(sum_v / etapas) if etapas else d(0)
            p_etapa = r(sum_p / etapas) if etapas else d(0)

            matriz_racao_totalizada.append({
                "ID_SA": sala.id,
                "GALPÃO": galpao.name,
                "SALA": sala.name,
                "ID_FO": formula.id,
                "TRATO": trato.id,
                "SUM_P": float(r(sum_p)),
                "SUM_V": float(r(sum_v)),
                "ID_GA": galpao.id,
                "ID_CZ": cozinha.id,
                "V_MAX_CZ": float(v_max_cz),
                "PCT_P_MAX_CZ": float(pct_util * 100),
                "V_MAX_UTIL_CZ": float(r(v_max_util)),
                "SUM_V_DIV_V_MAX_UTIL_CZ": float(r(div)),
                "ETAPAS_TRATO": etapas,
                "V_ETAPA_TRATO": float(r(v_etapa)),
                "P_ETAPA_TRATO": float(r(p_etapa)),
            })
    
    # =========================================================
    # 🔥 PREPARAÇÃO DE DADOS PARA CÁLCULO
    # =========================================================
    matriz_preparacao = []

    for lote in lotes:

        sala = lote.sala
        galpao = sala.shed
        baias = sala.baias

        dia_curva = cache_dia_curva[lote.id]
        curva_dia = cache_curva_dia[lote.id]

        if not curva_dia:
            continue

        formula = cache_formula[lote.id]

        total_suinos = sum(d(b.animals_quantity) for b in baias)

        for trato in tratos:

            linha_racao = next(
                (
                    l for l in matriz_racao_totalizada
                    if l["SALA"] == sala.name
                    and l["TRATO"] == trato.id
                    and l["ID_FO"] == formula.id
                ),
                None
            )

            if not linha_racao:
                continue

            etapas = linha_racao["ETAPAS_TRATO"]
            p_etapa = d(linha_racao["P_ETAPA_TRATO"])

            p_suino_etapa = (
                r(p_etapa / total_suinos)
                if total_suinos > 0 else d(0)
            )

            matriz_preparacao.append({
                "ID_SA": sala.id,
                "GALPÃO": galpao.name,
                "SALA": sala.name,
                "ID_FO": formula.id,
                "FORMULA": formula.name,
                "TRATO": trato.id,
                "ETAPAS_TRATO": etapas,
                "P_ETAPA_TRATO": float(r(p_etapa)),
                "TOTAL_SUINOS": int(total_suinos),
                "P_SUINO_ETAPA_TRATO": float(r(p_suino_etapa)),
            })
    
    # =========================================================
    # 🔥 CÁLCULO POR ETAPA (RECEITA FINAL DE DISTRIBUIÇÃO)
    # =========================================================
    matriz_final = []

    for lote in lotes:

        sala = lote.sala
        baias = sala.baias

        dia_curva = cache_dia_curva[lote.id]
        curva_dia = cache_curva_dia[lote.id]

        if not curva_dia:
            continue

        for baia in baias:

            qtd = d(baia.animals_quantity)

            row = {
                "ID": baia.id,
                "DESC": f"BA{baia.id}",
                "ID_SA": sala.id,
                "SUINOS": int(qtd),
                "T1-ETAPA-TRATO": 0,
                "T2-ETAPA-TRATO": 0,
                "T3-ETAPA-TRATO": 0,
                "T4-ETAPA-TRATO": 0,
                "T5-ETAPA-TRATO": 0,
                "T6-ETAPA-TRATO": 0,
            }

            for prep in matriz_preparacao:

                if prep["ID_SA"] != sala.id:
                    continue

                trato = prep["TRATO"]
                p_suino = d(prep["P_SUINO_ETAPA_TRATO"])

                valor = r(p_suino * qtd)

                col = f"T{trato}-ETAPA-TRATO"
                row[col] = float(valor)

            matriz_final.append(row)

    resultado = {
        "CONSULTAS DE PREPARAÇÃO DE DADOS DA CURVA": consultas_curva,
        "LOCALIZAÇÃO DE DADOS RELEVANTES NA CURVA COM BASE NO DIA": dados_curva,
        "CÁLCULO DO TOTAL POR BAIA POR TRATO E POR DIA": total_baia_trato,
        "TOTAL FORMULA/TRATO": [
            {"TRATO": k[0], "FORMULA": k[1], "VALOR": float(r(v))}
            for k, v in total_formula_trato.items()
        ],
        "CÁLCULO DE PRODUÇÃO E RECEITA": matriz_producao_receita,
        "CALCULO DE RAÇÃO LIQUIDA POR TRATO E FORMULA TOTALIZADOS": matriz_racao_totalizada,
        "CÁLCULO DE DISTRIBUIÇÃO": matriz_preparacao,
        "RECEITA FINAL DE DISTRIBUIÇÃO POR BAIA": matriz_final,
    }

    return resultado


def main():
    data_base = date(2026, 3, 20)
    with session_scope() as session:
        script_1(
            session,
            data_base=data_base,
            considerar_fracao_liquida=False
        )


if __name__ == "__main__":
    main()