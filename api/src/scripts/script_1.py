import json
from math import ceil
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


def script_1(session, data_base, show_debug=True, ignorar_fracao_liquida=False):

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

            massa_total_trato = total_formula_trato.get((trato.id, formula.id), d(0))
            pct_seco_formula = (100 - d(formula.water_percentage)) / 100

            linhas_trato = []
            soma_agua_produtos = d(0)

            # =====================================================
            # 1️⃣ PRIMEIRO PASSO (SEM AJUSTE DE ÁGUA)
            # =====================================================
            for produto in todos_produtos.values():

                item_formula = next(
                    (i for i in formula.details if i.product_id == produto.id),
                    None
                )

                pct_produto = d(item_formula.product_percentage_without_moisture) if item_formula else d(0)

                pct_umid = d(getattr(produto, "moisture_percentage", 0))
                frac_seca = (100 - pct_umid) / 100

                # 🔥 MASSA SECA (BASE REAL DO EXCEL)
                massa_seca = (pct_produto / 100) * massa_total_trato

                if produto.id == 1:
                    # água calculada depois
                    p_trato = d(0)
                    massa_real = d(0)
                else:
                    # 🔥 IGUAL EXCEL
                    if frac_seca > 0:
                        p_trato = massa_seca / frac_seca
                    else:
                        p_trato = d(0)

                    p_trato = r(p_trato)

                    # massa real (natural)
                    massa_real = p_trato

                    # 🔥 água do produto = N - M
                    agua_prod = massa_real - massa_seca
                    soma_agua_produtos += agua_prod

                frac_h2o = 1 - frac_seca

                linhas_trato.append({
                    "produto": produto,
                    "pct_produto": pct_produto,
                    "massa_seca": massa_seca,
                    "p_trato": p_trato,
                    "pct_umid": pct_umid,
                    "frac_h2o": frac_h2o,
                    "frac_seca": frac_seca,
                })

            # =====================================================
            # 2️⃣ AJUSTE DA ÁGUA (SÓ SE NÃO IGNORAR)
            # =====================================================
            if not ignorar_fracao_liquida:
                # total da mistura (M209 do Excel)
                if pct_seco_formula > 0:
                    total_mistura = massa_total_trato / pct_seco_formula
                else:
                    total_mistura = d(0)

                # água = total mistura - soma(N - M)
                agua_total = total_mistura - soma_agua_produtos

                for l in linhas_trato:
                    if l["produto"].id == 1:
                        l["p_trato"] = r(max(d(0), agua_total))

            # =====================================================
            # 3️⃣ MONTAGEM FINAL
            # =====================================================
            for l in linhas_trato:

                produto = l["produto"]
                p_trato = r(l["p_trato"])

                if produto.density > 0:
                    v_trato = r(p_trato / (d(produto.density) / 1000))
                else:
                    v_trato = d(0)

                row = {
                    "GALPÃO": galpao.name,
                    "SALA": sala.name,
                    "ID_PR": produto.id,
                    "PRODUTO": produto.name,
                    "D_PR": produto.density,
                    "ID_FO": formula.id,
                    "TRATO": trato.id,
                    "PCT_H20_FO": float(formula.water_percentage),
                    "PCT_PR_100_PCT_S_H2O_FO": float(l["pct_produto"]),
                    "EH_AGUA": produto.id == 1,
                    "P_TRATO": p_trato,
                    "V_TRATO": v_trato,
                }

                # CAMPOS DINÂMICOS (SÓ QUANDO CONSIDERA FRAÇÃO)
                if not ignorar_fracao_liquida:
                    row.update({
                        "PCT_UMID_PR": float(l["pct_umid"]),
                        "FRAC_SECA_PR": float(l["frac_seca"]),
                        "FRAC_H2O_PR": float(l["frac_h2o"]),
                        "P_TRATO_S_CALC_UMID": float(r(l["massa_seca"])),
                    })

                matriz_producao_receita.append(row)

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

            if V_MAX_UTIL_CZ > 0:
                etapas = int(ceil(div))
            else:
                etapas = 0

            v_etapa = r(sum_v / etapas) if etapas > 0 else d(0)
            p_etapa = r(sum_p / etapas) if etapas > 0 else d(0)

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