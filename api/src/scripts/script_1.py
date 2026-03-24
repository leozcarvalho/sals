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


def calcular_dia_curva(lote: Batch, data_base: date):
    start_date = lote.created_at.date()

    dias_passados = (data_base - start_date).days

    if dias_passados < 0:
        raise Exception(f"Data base menor que início do lote {lote.id}")

    curva_inicio: FeedingCurveDetail = lote.initial_curve_detail

    if not curva_inicio:
        raise Exception(f"Lote {lote.id} sem initial_curve_detail")

    dia_inicial = curva_inicio.age_day

    dia_curva = dia_inicial + dias_passados

    max_dia = max(c.age_day for c in lote.feeding_curve.details)

    if dia_curva > max_dia:
        dia_curva = max_dia

    return dia_curva, dias_passados


def script_1(session, data_base: date, show_debug: bool = True):
    '''
    DATA → DIA CURVA
    → CONSUMO ANIMAL
    → CONSUMO BAIA
    → DIVISÃO POR TRATO
    → DIVISÃO POR FÓRMULA
    → SOMA FINAL
    '''
    logger.info("Iniciando script_1")
    logger.info(f"Data base: {data_base}")

    batch_repo = BatchRepository(session)
    trato_repo = TratoRepository(session)

    lotes: List[Batch] = batch_repo.get_list(filters={'is_active': True})
    tratos: List[Trato] = trato_repo.get_list()

    trato_repo.validate_percent(tratos)

    debug_curva = []
    debug_baia = []
    matriz_detalhada = []

    for lote in lotes:
        logger.info(f"Processando lote {lote.id}")

        sala = lote.sala
        galpao = sala.shed
        baias: List[Baia] = sala.baias
        curva: FeedingCurve = lote.feeding_curve

        #data_base = date(2026, 3, 16)
        dia_curva, dias_passados = calcular_dia_curva(lote, data_base)
        logger.info(f"Lote {lote.id} - Dia curva: {dia_curva} Data base: {data_base} (dias passados: {dias_passados})")

        # 🔥 pega detalhe da curva
        curva_dia: FeedingCurveDetail = next(
            (c for c in curva.details if c.age_day == dia_curva),
            None
        )

        if not curva_dia:
            logger.warning(
                f"Curva não encontrada | lote={lote.id} | dia={dia_curva}"
            )
            continue

        consumo_animal = Decimal(curva_dia.formula_mass_per_animal)
        formula: Formula = curva_dia.formula


        debug_curva.append({
            "LOTE": lote.id,
            "ID_SA": sala.id,
            "GALPAO": galpao.name,
            "SALA": sala.name,
            "DATA_BASE": str(data_base),
            "DIAS_PASSADOS": dias_passados,
            "DIA_INICIAL": lote.initial_curve_detail.age_day,
            "DIA_CURVA": dia_curva,
            "PESO_SUINO": float(curva_dia.animal_weight),
            "P_SECO_ANIMAL": float(consumo_animal),
            "FORMULA_ID": formula.id if formula else None,
            "FORMULA": formula.name if formula else None,
        })

        if not formula:
            continue

        formula_itens: List[FormulaDetail] = formula.details

        # 🔥 valida fórmula
        total_formula = sum(
            Decimal(i.product_percentage_without_moisture)
            for i in formula_itens
        )

        if total_formula != Decimal("100"):
            raise Exception(f"Fórmula {formula.id} não fecha 100%")


        for baia in baias:

            qtd_animais = Decimal(baia.animals_quantity)
            consumo_total_baia = consumo_animal * qtd_animais

            row_baia = {
                "ID_BA": baia.id,
                "ID_SA": sala.id,
                "SUINOS": int(qtd_animais)
            }

            total_dia = Decimal(0)

            for trato in tratos:

                percentual = Decimal(trato.percent) / Decimal(100)
                consumo_trato = consumo_total_baia * percentual

                row_baia[f"P_SECO_T{trato.id}"] = float(round(consumo_trato, 2))

                total_dia += consumo_trato

                # 🔥 explode fórmula
                for item in formula_itens:

                    percentual_item = Decimal(
                        item.product_percentage_without_moisture
                    ) / Decimal(100)

                    massa = consumo_trato * percentual_item

                    matriz_detalhada.append({
                        "sala_id": sala.id,
                        "galpao": galpao.name,
                        "sala": sala.name,
                        "trato_id": trato.id,
                        "formula_id": formula.id,
                        "formula": formula.name,
                        "massa": massa
                    })

            row_baia["P_SECO_TOTAL"] = float(round(total_dia, 2))
            debug_baia.append(row_baia)

    # =========================================================
    # 🔥 AGRUPAMENTO FINAL
    # =========================================================
    matriz_agrupada = defaultdict(Decimal)

    for row in matriz_detalhada:
        chave = (
            row["sala_id"],
            row["galpao"],
            row["sala"],
            row["trato_id"],
            row["formula_id"],
            row["formula"]
        )
        matriz_agrupada[chave] += row["massa"]

    resultado_final = []

    for (
        sala_id,
        galpao,
        sala,
        trato_id,
        formula_id,
        formula_nome
    ), massa in matriz_agrupada.items():

        resultado_final.append({
            "ID_SA": sala_id,
            "GALPAO": galpao,
            "SALA": sala,
            "TRATO": trato_id,
            "ID_FO": formula_id,
            "FORMULA": formula_nome,
            "P_SECO": float(round(massa, 2))
        })

    resultado_final.sort(key=lambda x: (x["ID_SA"], x["TRATO"]))

    if show_debug:
        print("\n===== DEBUG CURVA =====")
        print(json.dumps(debug_curva, indent=2, ensure_ascii=False))

        print("\n===== DEBUG BAIA =====")
        print(json.dumps(debug_baia[:20], indent=2, ensure_ascii=False))

        print("\n===== RESULTADO FINAL =====")
        print(json.dumps(resultado_final, indent=2, ensure_ascii=False))

    return [
        {"curva": debug_curva},
        {"baia": debug_baia},
        {"final": resultado_final}
    ]

def main():
    data_base = date(2026, 3, 16)  # 🔥 igual planilha
    with session_scope() as session:
        script_1(session, data_base=data_base, show_debug=True)


if __name__ == "__main__":
    main()