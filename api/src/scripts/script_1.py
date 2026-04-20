import json
from math import ceil
from decimal import Decimal
from collections import defaultdict
from datetime import date

import logging
from src.core.db import session_scope

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
def calcular_dia_curva(lote, data_base: date):
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
    produtos = product_repo.get_list()

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

        dia_curva = calcular_dia_curva(lote, data_base)
        curva_dia = lote.feeding_curve.details[dia_curva]

        if not curva_dia or not curva_dia.formula:
            continue

        consumo_animal = d(curva_dia.formula_mass_per_animal)
        formula = curva_dia.formula

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

        dia_curva = calcular_dia_curva(lote, data_base)
        curva_dia = lote.feeding_curve.details[dia_curva]

        if not curva_dia or not curva_dia.formula:
            continue

        formula = curva_dia.formula

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

                if product_id == 1:
                    p_trato = d(0)
                else:
                    p_trato = massa_seca / frac_seca if frac_seca > 0 else d(0)
                    p_trato = r(p_trato)

                    # N - M
                    soma_agua += (p_trato - massa_seca)

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

            # Água (igual Excel)
            if not ignorar_fracao_liquida:
                total_mistura = massa_total / pct_seco_formula if pct_seco_formula > 0 else d(0)
                agua = total_mistura - soma_agua

                for l in linhas:
                    if l["produto"].id == 1:
                        l["p_trato"] = r(max(d(0), agua))

            # Montagem final
            for l in linhas:
                p_trato = r(l["p_trato"])
                dens = l["dens"]

                v_trato = r(p_trato / (dens / 1000)) if dens > 0 else d(0)

                row = {
                    "GALPÃO": galpao.name,
                    "SALA": sala.name,
                    "ID_PR": l["produto"].id,
                    "PRODUTO": l["produto"].name,
                    "D_PR": l["dens"],
                    "ID_FO": formula.id,
                    "TRATO": trato.id,
                    "PCT_H20_FO": float(formula.water_percentage),
                    "PCT_PR_100_PCT_S_H2O_FO": float(l["pct_produto"]),
                    "EH_AGUA": l["produto"].id == 1,
                    "P_TRATO": p_trato,
                    "V_TRATO": v_trato,
                }

                if not ignorar_fracao_liquida:
                    row.update({
                        "PCT_UMID_PR": float(l["umid"]),
                        "FRAC_SECA_PR": float(l["frac_seca"]),
                        "FRAC_H2O_PR": float(l["frac_h2o"]),
                        "P_TRATO_S_CALC_UMID": float(r(l["massa_seca"])),
                    })

                matriz_producao_receita.append(row)

    # =========================================================
    # 🔥 AGRUPAMENTO (remove O(n²))
    # =========================================================
    agrupado = defaultdict(lambda: {"sum_p": d(0), "sum_v": d(0)})

    for linha in matriz_producao_receita:
        chave = (linha["SALA"], linha["TRATO"], linha["ID_FO"])
        agrupado[chave]["sum_p"] += d(linha["P_TRATO"])
        agrupado[chave]["sum_v"] += d(linha["V_TRATO"])

    # =========================================================
    # RAÇÃO LIQUIDA
    # =========================================================
    matriz_racao_totalizada = []

    for lote in lotes:

        sala = lote.sala
        galpao = sala.shed
        cozinha = getattr(galpao, "kitchen", None)

        if not cozinha:
            continue

        V_MAX_CZ = d(cozinha.volume_misturador)
        PCT = d(cozinha.fracao_volume_misturador) / 100
        V_MAX_UTIL = V_MAX_CZ * PCT

        formula = lote.feeding_curve.details[
            calcular_dia_curva(lote, data_base)
        ].formula

        for trato in tratos:

            chave = (sala.name, trato.id, formula.id)
            sum_p = agrupado[chave]["sum_p"]
            sum_v = agrupado[chave]["sum_v"]

            div = sum_v / V_MAX_UTIL if V_MAX_UTIL > 0 else d(0)
            etapas = int(ceil(div)) if V_MAX_UTIL > 0 else 0

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
                "ID_CZ": getattr(cozinha, "id", 1),
                "V_MAX_CZ": float(V_MAX_CZ),
                "PCT_P_MAX_CZ": float(PCT * 100),
                "V_MAX_UTIL_CZ": float(r(V_MAX_UTIL)),
                "SUM_V_DIV_V_MAX_UTIL_CZ": float(r(div)),
                "ETAPAS_TRATO": etapas,
                "V_ETAPA_TRATO": float(r(v_etapa)),
                "P_ETAPA_TRATO": float(r(p_etapa)),
            })

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