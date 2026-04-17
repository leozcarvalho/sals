import json
from typing import List
from decimal import Decimal
from collections import defaultdict
from datetime import date

import logging
from src.core.db import session_scope

from src.domain import (
    Baia, Batch, FeedingCurve, FeedingCurveDetail,
    Formula, FormulaDetail, Trato
)

from src.cruds.batch import BatchRepository
from src.cruds.trato import TratoRepository
from src.cruds.product import ProductRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =========================================================
# HELPERS
# =========================================================
def d(v): return Decimal(str(v))
def r(v): return v.quantize(Decimal("0.01"))


# =========================================================
# DIA CURVA
# =========================================================
def calcular_dia_curva(lote: Batch, data_base: date):
    dias_passados = (data_base - lote.created_at.date()).days
    if dias_passados < 0:
        raise Exception(f"Data base menor que início do lote {lote.id}")
    return dias_passados


def script_1(session, data_base, show_debug=True, ignorar_fracao_liquida=True):

    batch_repo = BatchRepository(session)
    trato_repo = TratoRepository(session)
    product_repo = ProductRepository(session)

    lotes = batch_repo.get_list(filters={'is_active': True})
    tratos = trato_repo.get_list()

    trato_repo.validate_percent(tratos)

    # =========================================================
    # 1 LOTE POR SALA
    # =========================================================
    lotes_por_sala = {}
    for lote in lotes:
        if lote.sala.id not in lotes_por_sala:
            lotes_por_sala[lote.sala.id] = lote

    lotes = list(lotes_por_sala.values())

    # =========================================================
    # MAPA FORMULAS
    # =========================================================
    map_formulas = {}
    for lote in lotes:
        for c in lote.feeding_curve.details:
            if c.formula:
                map_formulas[c.formula.id] = c.formula

    consultas_curva = []
    dados_curva = []
    total_baia_trato = []
    total_formula_trato = defaultdict(Decimal)
    matriz_detalhada = []

    # =========================================================
    # LOOP PRINCIPAL (INALTERADO)
    # =========================================================
    for lote in lotes:

        sala = lote.sala
        galpao = sala.shed
        baias = sala.baias

        consultas_curva.append({
            "LOTE": lote.id,
            "ID_SA": sala.id,
            "GALPAO": galpao.name
        })

        dia_curva = calcular_dia_curva(lote, data_base)

        curva_dia = lote.feeding_curve.details[dia_curva]
        if not curva_dia or not curva_dia.formula:
            continue

        consumo_animal = d(curva_dia.formula_mass_per_animal)
        formula = curva_dia.formula

        dados_curva.append({
            "GALPÃO": galpao.name,
            "SALA": sala.name,
            "ID_DIA_HOJE_NA_CURVA": dia_curva - 1,
            "DIA_HOJE_NA_CURVA": curva_dia.age_day,
            "P_ALIM_SECO_SUINO_DIA_HOJE": consumo_animal,
            "ID_FORMULA": formula.id,
            "FORMULA": formula.name,
            "MASSA_SECA_FORMULA": formula.water_percentage,
        })

        for baia in baias:
            qtd = d(baia.animals_quantity)
            consumo_baia = consumo_animal * qtd

            row = {
                "ID_BA": baia.id,
                "ID_SA": sala.id,
                "SUINOS": int(qtd),
                "P_SECO_DIA_T1": 0,
                "P_SECO_DIA_T2": 0,
                "P_SECO_DIA_T3": 0,
                "P_SECO_DIA_T4": 0,
                "P_SECO_DIA_T5": 0,
                "P_SECO_DIA_T6": 0,
                "P_SECO_DIA": 0,
            }

            total_dia = d(0)

            for trato in tratos:

                if trato.percent == 0:
                    continue

                consumo_trato = r(consumo_baia * d(trato.percent) / 100)

                col = f"P_SECO_DIA_T{trato.id}"
                row[col] = float(consumo_trato)

                total_dia += consumo_trato
                total_formula_trato[(trato.id, formula.id)] += consumo_trato

                for item in formula.details:

                    perc = d(item.product_percentage_without_moisture) / 100
                    massa_seca = consumo_trato * perc

                    produto = item.product
                    umidade = d(getattr(produto, "moisture_percentage", 0)) / 100

                    massa_real = massa_seca if umidade >= 1 else massa_seca / (1 - umidade)

                    matriz_detalhada.append({
                        "sala_id": sala.id,
                        "trato_id": trato.id,
                        "formula_id": formula.id,
                        "product": produto.name if produto else None,
                        "massa_seca": massa_seca,
                        "massa_real": massa_real
                    })

            row["P_SECO_DIA"] = float(r(total_dia))
            total_baia_trato.append(row)

    # =========================================================
    # PRODUTOS
    # =========================================================
    todos_produtos = {p.id: p for p in product_repo.get_list()}

    # =========================================================
    # BASE AGRUPADA
    # =========================================================
    base = defaultdict(lambda: {"massa_seca": d(0), "massa_real": d(0)})

    for row in matriz_detalhada:
        chave = (
            row["sala_id"],
            row["trato_id"],
            row["formula_id"],
            row["product"]
        )
        base[chave]["massa_seca"] += row["massa_seca"]
        base[chave]["massa_real"] += row["massa_real"]

    # =========================================================
    # 🔥 PRODUÇÃO E RECEITA (NOVO)
    # =========================================================
    matriz_producao_receita = []

    for lote in lotes:

        sala = lote.sala
        galpao = sala.shed

        dia_curva = calcular_dia_curva(lote, data_base)
        curva_dia = lote.feeding_curve.details[dia_curva]

        if not curva_dia or not curva_dia.formula:
            continue

        formula = curva_dia.formula

        for trato in tratos:
            for produto in todos_produtos.values():
                item_formula = next(
                    (i for i in formula.details if i.product_id == produto.id),
                    None
                )
                pct_produto = d(item_formula.product_percentage_without_moisture) if item_formula else d(0)

                massa_total_trato = total_formula_trato.get((trato.id, formula.id), d(0))

                pct_seco_formula = (100 - d(formula.water_percentage)) / 100

                if produto.id == 1:
                    # água
                    if pct_seco_formula > 0:
                        p_trato = massa_total_trato / pct_seco_formula
                    else:
                        p_trato = d(0)
                else:
                    p_trato = (pct_produto / 100) * massa_total_trato

                p_trato = r(p_trato)

                if produto.density > 0:
                    v_trato = p_trato / (d(produto.density) / 1000)
                else:
                    v_trato = d(0)

                matriz_producao_receita.append({
                    "GALPÃO": galpao.name,
                    "SALA": sala.name,
                    "ID_PR": produto.id,
                    "PRODUTO": produto.name,
                    "D_PR": produto.density,
                    "ID_FO": formula.id,
                    "TRATO": trato.id,
                    "PCT_H20_FO": float(formula.water_percentage),
                    "PCT_PR_100_PCT_S_H2O_FO": float(pct_produto),
                    "EH_AGUA": produto.id == 1,
                    "P_TRATO": p_trato,
                    "V_TRATO": v_trato,
                })

    # =========================================================
    # 🔥 RAÇÃO LIQUIDA (NOVO COM COZINHA)
    # =========================================================
    matriz_racao_totalizada = []

    map_etapas = {1: 2, 2: 3, 3: 0, 4: 3, 5: 0, 6: 2}

    for lote in lotes:

        sala = lote.sala
        galpao = sala.shed
        cozinha = getattr(galpao, "kitchen", None)

        if not cozinha:
            continue

        V_MAX_CZ = d(cozinha.volume_misturador)
        PCT_P_MAX_CZ = d(cozinha.fracao_volume_misturador)
        V_MAX_UTIL_CZ = V_MAX_CZ * PCT_P_MAX_CZ

        dia_curva = calcular_dia_curva(lote, data_base)
        curva_dia = lote.feeding_curve.details[dia_curva]

        if not curva_dia or not curva_dia.formula:
            continue

        formula = curva_dia.formula

        for trato in tratos:

            chave = (trato.id, formula.id)

            sum_p = sum(
                d(linha["P_TRATO"])
                for linha in matriz_producao_receita
                if linha["TRATO"] == trato.id and linha["ID_FO"] == formula.id
            )

            water_pct = d(formula.water_percentage) / 100
            etapas = map_etapas.get(trato.id, 0)

            # SUM_V correto vindo da matriz
            sum_v = sum(
                d(linha["V_TRATO"])
                for linha in matriz_producao_receita
                if linha["TRATO"] == trato.id and linha["ID_FO"] == formula.id
            )

            # capacidade
            PCT_P_MAX_CZ = d(cozinha.fracao_volume_misturador) / 100
            V_MAX_UTIL_CZ = V_MAX_CZ * PCT_P_MAX_CZ

            div = sum_v / V_MAX_UTIL_CZ if V_MAX_UTIL_CZ > 0 else d(0)

            v_etapa = r(sum_v / etapas) if etapas > 0 else d(0)
            p_etapa = r(sum_p / etapas) if etapas > 0 else d(0)
            
            # SUM_P =SOMASES($J$131:$J$190;$F$131:$F$190;E194;$E$131:$E$190;D194)
            # SUM_V =SOMASES($K$131:$K$190;$F$131:$F$190;E194;$E$131:$E$190;D194)
            # V_MAX_UTIL_CZ =J194*K194/100
            # SUM_V_DIV_V_MAX_UTIL_CZ= =G194/L194
            # V_ETAPA_TRATO =ARRED(SE(ÉERRO(G194/N194);0;G194/N194);1)
            # P_ETAPA_TRATO =ARRED(SE(ÉERRO(F194/N194);0;F194/N194);1)
            matriz_racao_totalizada.append({
                "ID_SA": sala.id,
                "GALPÃO": galpao.name,
                "SALA": sala.name,
                "ID_FO": formula.id,
                "TRATO": trato.id,
                "SUM_P": float(r(sum_p)),
                "SUM_V": float(r(sum_v)),
                "ID_GA": galpao.id,
                "ID_CZ": getattr(cozinha, "id", 1),
                "V_MAX_CZ": float(V_MAX_CZ),
                "PCT_P_MAX_CZ": float(PCT_P_MAX_CZ * 100),
                "V_MAX_UTIL_CZ": float(r(V_MAX_UTIL_CZ)),
                "SUM_V_DIV_V_MAX_UTIL_CZ": float(r(div)),
                "ETAPAS_TRATO": etapas,
                "V_ETAPA_TRATO": float(r(v_etapa)),
                "P_ETAPA_TRATO": float(r(p_etapa)),
            })

    # =========================================================
    # OUTPUT FINAL
    # =========================================================
    resultado = {
        "CONSULTAS DE PREPARAÇÃO DE DADOS DA CURVA": consultas_curva,
        "LOCALIZAÇÃO DE DADOS RELEVANTES NA CURVA COM BASE NO DIA": dados_curva,
        "CÁLCULO DO TOTAL POR BAIA POR TRATO E POR DIA": total_baia_trato,
        "TOTAL FORMULA/TRATO": [
            {"TRATO": k[0], "FORMULA": k[1], "VALOR": float(r(v))}
            for k, v in total_formula_trato.items()
        ],
        "CÁLCULO DE PRODUÇÃO E RECEITA- MÉTODO IGNORANDO FRAÇÃO LÍQUIDA NOS PRODUTOS": matriz_producao_receita,
        "CALCULO DE RAÇÃO LIQUIDA POR TRATO E FORMULA TOTALIZADOS": matriz_racao_totalizada,
    }

    if show_debug:
        print(json.dumps(resultado, indent=2, ensure_ascii=False))

    return resultado


def main():
    data_base = date(2026, 3, 20)

    with session_scope() as session:
        script_1(
            session,
            data_base=data_base,
            ignorar_fracao_liquida=True
        )


if __name__ == "__main__":
    main()