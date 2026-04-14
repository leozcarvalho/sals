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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =========================================================
# 🔥 HELPERS
# =========================================================
def d(v): return Decimal(str(v))
def r(v): return v.quantize(Decimal("0.01"))

# =========================================================
# 🔥 DIA CURVA
# =========================================================
def calcular_dia_curva(lote: Batch, data_base: date):
    dias_passados = (data_base - lote.created_at.date()).days

    if dias_passados < 0:
        raise Exception(f"Data base menor que início do lote {lote.id}")

    curva_inicio = lote.initial_curve_detail
    dia_curva = curva_inicio.age_day + dias_passados

    max_dia = max(c.age_day for c in lote.feeding_curve.details)

    return min(dia_curva, max_dia), dias_passados


def script_1(session, data_base, show_debug=True):
    batch_repo = BatchRepository(session)
    trato_repo = TratoRepository(session)

    lotes = batch_repo.get_list(filters={'is_active': True})
    tratos = trato_repo.get_list()

    trato_repo.validate_percent(tratos)

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
    # LOOP PRINCIPAL
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

        dia_curva, dias = calcular_dia_curva(lote, data_base)

        curva_dia = next(
            (c for c in lote.feeding_curve.details if c.age_day == dia_curva),
            None
        )

        if not curva_dia or not curva_dia.formula:
            continue

        consumo_animal = d(curva_dia.formula_mass_per_animal)
        formula = curva_dia.formula

        dados_curva.append({
            "LOTE": lote.id,
            "DIA_CURVA": dia_curva,
            "FORMULA": formula.id,
            "CONSUMO_ANIMAL": float(consumo_animal)
        })

        for baia in baias:

            qtd = d(baia.animals_quantity)
            consumo_baia = consumo_animal * qtd

            for trato in tratos:

                if trato.percent == 0:
                    continue

                consumo_trato = consumo_baia * d(trato.percent) / 100

                total_baia_trato.append({
                    "ID_BA": baia.id,
                    "TRATO": trato.id,
                    "P_SECO": float(r(consumo_trato))
                })

                total_formula_trato[(trato.id, formula.id)] += consumo_trato

                for item in formula.details:

                    perc = d(item.product_percentage_without_moisture) / 100
                    massa_seca = consumo_trato * perc

                    produto = item.product
                    umidade = d(getattr(produto, "moisture_percentage", 0)) / 100

                    # 🔥 converte para massa real
                    if umidade < 1:
                        massa_real = massa_seca / (1 - umidade)
                    else:
                        massa_real = massa_seca

                    matriz_detalhada.append({
                        "sala_id": sala.id,
                        "trato_id": trato.id,
                        "formula_id": formula.id,
                        "product": produto.name if produto else None,
                        "massa_seca": massa_seca,
                        "massa_real": massa_real
                    })

    # =========================================================
    # PRODUÇÃO SECA
    # =========================================================
    producao_seca = defaultdict(Decimal)
    for row in matriz_detalhada:
        producao_seca[row["product"]] += row["massa_seca"]

    # =========================================================
    # RAÇÃO LIQUIDA (COM ÁGUA)
    # =========================================================
    racao_liquida = defaultdict(Decimal)

    for (trato_id, formula_id), massa_seca_total in total_formula_trato.items():

        formula = map_formulas.get(formula_id)
        if not formula:
            continue

        water_pct = d(formula.water_percentage) / 100

        # 🔥 adiciona água
        if water_pct < 1:
            massa_total = massa_seca_total / (1 - water_pct)
        else:
            massa_total = massa_seca_total

        racao_liquida[(trato_id, formula_id)] += massa_total

    # =========================================================
    # PRODUÇÃO LIQUIDA (CORRIGIDA)
    # =========================================================
    producao_liquida = defaultdict(Decimal)

    for (trato_id, formula_id), massa_total in racao_liquida.items():

        formula = map_formulas.get(formula_id)
        if not formula:
            continue

        for item in formula.details:
            perc = d(item.product_percentage_without_moisture) / 100
            nome = item.product.name if item.product else f"PROD_{item.product_id}"

            producao_liquida[nome] += massa_total * perc

        # 🔥 adiciona água como produto separado
        producao_liquida["Água"] += massa_total * (d(formula.water_percentage) / 100)

    # =========================================================
    # DISTRIBUIÇÃO SECA
    # =========================================================
    distribuicao_seca = defaultdict(Decimal)
    for row in matriz_detalhada:
        chave = (row["sala_id"], row["trato_id"], row["product"])
        distribuicao_seca[chave] += row["massa_seca"]

    # =========================================================
    # ETAPAS
    # =========================================================
    distribuicao_etapa = []

    map_etapas = {
        1: 2,
        2: 3,
        3: 0,
        4: 3,
        5: 0,
        6: 2
    }

    for lote in lotes:

        sala = lote.sala
        baias = sala.baias

        dia_curva, _ = calcular_dia_curva(lote, data_base)

        curva_dia = next(
            (c for c in lote.feeding_curve.details if c.age_day == dia_curva),
            None
        )

        if not curva_dia or not curva_dia.formula:
            continue

        consumo_animal = d(curva_dia.formula_mass_per_animal)

        for baia in baias:

            qtd = d(baia.animals_quantity)
            consumo_baia = consumo_animal * qtd

            row = {
                "ID": baia.id,
                "DESC": baia.name,
                "ID_SA": sala.id,
                "SUINOS": int(qtd)
            }

            for trato in tratos:

                etapas = map_etapas.get(trato.id, 0)
                col = f"T{trato.id}-ETAPA-TRATO"

                if etapas == 0 or trato.percent == 0:
                    row[col] = 0
                    continue

                consumo_trato = consumo_baia * d(trato.percent) / 100
                valor_etapa = consumo_trato / etapas

                row[col] = float(r(valor_etapa))

            distribuicao_etapa.append(row)

    # =========================================================
    # OUTPUT FINAL
    # =========================================================
    resultado = {
        "CONSULTAS DE PREPARAÇÃO DE DADOS DA CURVA": consultas_curva,
        "LOCALIZAÇÃO NA CURVA": dados_curva,
        "TOTAL POR BAIA/TRATO": total_baia_trato,
        "TOTAL FORMULA/TRATO": [
            {"TRATO": k[0], "FORMULA": k[1], "VALOR": float(r(v))}
            for k, v in total_formula_trato.items()
        ],
        "MATRIZ MASSA SECA": matriz_detalhada,
        "PRODUÇÃO SECA": [
            {"PRODUTO": k, "VALOR": float(r(v))}
            for k, v in producao_seca.items()
        ],
        "RAÇÃO LIQUIDA": [
            {"TRATO": k[0], "FORMULA": k[1], "VALOR": float(r(v))}
            for k, v in racao_liquida.items()
        ],
        "PRODUÇÃO LIQUIDA": [
            {"PRODUTO": k, "VALOR": float(r(v))}
            for k, v in producao_liquida.items()
        ],
        "DISTRIBUIÇÃO SECA": [
            {"SALA": k[0], "TRATO": k[1], "PRODUTO": k[2], "VALOR": float(r(v))}
            for k, v in distribuicao_seca.items()
        ],
        "ETAPAS": distribuicao_etapa,
    }

    if show_debug:
        print(json.dumps(resultado, indent=2, ensure_ascii=False))

    return resultado


# =========================================================
# 🚀 MAIN
# =========================================================
def main():
    data_base = date(2026, 3, 16)

    with session_scope() as session:
        script_1(session, data_base=data_base, show_debug=True)


if __name__ == "__main__":
    main()