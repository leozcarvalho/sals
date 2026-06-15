import pytest
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from src.scripts.script_1 import script_1
from tests.conftest import session_with_seed

TOL = 0.1


def r1(value):
    """Arredonda para 1 casa decimal com ROUND_HALF_UP (igual Excel)."""
    return float(Decimal(str(value)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def almost(a, b):
    return round(abs(a - b), 10) <= TOL


def assert_rows(result_rows, expected_rows, *keys):
    """Compara duas listas de tuplas por chaves arbitrárias, com tolerância."""
    assert len(result_rows) == len(expected_rows), (
        f"Quantidade de linhas diferente: {len(result_rows)} != {len(expected_rows)}"
    )
    for idx, (row, exp) in enumerate(zip(result_rows, expected_rows)):
        exp = exp if isinstance(exp, (list, tuple)) else (exp,)
        for key, exp_val in zip(keys, exp):
            got = r1(row[key])
            exp_val = r1(exp_val)
            assert almost(got, exp_val), (
                f"Linha {idx}: {key}={got} (esperado {exp_val})"
            )


# ---------------------------------------------------------------------------
# Dados esperados (planilha)
# ---------------------------------------------------------------------------

EXPECTED_TOTAL_FORMULA_TRATO = [
    (1, 1, 228.8), (2, 1, 343.2), (4, 1, 343.2), (6, 1, 228.8),
    (1, 4, 417.12), (2, 4, 625.68), (4, 4, 625.68), (6, 4, 417.12),
]

# (P_TRATO, V_TRATO) por linha de CÁLCULO DE PRODUÇÃO E RECEITA
EXPECTED_P_V_SECO = [
    (953.3, 953.3), (171.6, 264),   (57.2, 72.4),   (0, 0), (0, 0),
    (1430,  1430),  (257.4, 396),   (85.8, 108.6),  (0, 0), (0, 0),
    (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
    (1430,  1430),  (257.4, 396),   (85.8, 108.6),  (0, 0), (0, 0),
    (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
    (953.3, 953.3), (171.6, 264),   (57.2, 72.4),   (0, 0), (0, 0),
    (1668.5, 1668.5), (271.1, 417.1), (75.1, 95.1), (70.9, 88.6), (0, 0),
    (2502.7, 2502.7), (406.7, 625.7), (112.6, 142.5), (106.4, 133), (0, 0),
    (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
    (2502.7, 2502.7), (406.7, 625.7), (112.6, 142.5), (106.4, 133), (0, 0),
    (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
    (1668.5, 1668.5), (271.1, 417.1), (75.1, 95.1), (70.9, 88.6), (0, 0),
]

# (ETAPAS_TRATO, P_ETAPA_TRATO) por linha de CÁLCULO DE DISTRIBUIÇÃO
EXPECTED_DISTRIBUICAO_SECO = [
    (2, 644.9, 591.1),
    (3, 644.9, 591.1),
    (0, 0.0,   0.0),
    (3, 644.9, 591.1),
    (0, 0.0,   0.0),
    (2, 644.9, 591.1),
    (3, 756.4, 695.2),
    (4, 851.0, 782.1),
    (0, 0.0,   0.0),
    (4, 851.0, 782.1),
    (0, 0.0,   0.0),
    (3, 756.4, 695.2),
]

# (T1, T2, T3, T4, T5, T6) por baia
EXPECTED_BAIA_TRATOS_SECO = [
    *((13.4, 13.4, 0.0, 13.4, 0.0, 13.4) for _ in range(44)),
    *((15.8, 17.8, 0.0, 14.062, 0.0, 15.8) for _ in range(44)),
]


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------

def test_script_1_seco(session_with_seed):
    result = script_1(session_with_seed, data_base=date(2026, 3, 20), considerar_fracao_liquida=False)

    assert result['LOCALIZAÇÃO DE DADOS RELEVANTES NA CURVA COM BASE NO DIA']

    # --- total formula/trato ---
    got = [(i['TRATO'], i['FORMULA'], i['VALOR']) for i in result['TOTAL FORMULA/TRATO']]
    assert got == EXPECTED_TOTAL_FORMULA_TRATO

    # --- producao/receita ---
    assert_rows(result['CÁLCULO DE PRODUÇÃO E RECEITA'], EXPECTED_P_V_SECO, 'P_TRATO', 'V_TRATO')

    # --- distribuição ---
    assert_rows(result['CALCULO DE RAÇÃO LIQUIDA POR TRATO E FORMULA TOTALIZADOS'], EXPECTED_DISTRIBUICAO_SECO, 'ETAPAS_TRATO', 'V_ETAPA_TRATO', 'P_ETAPA_TRATO')

    # --- distribuição por baia ---
    cols = ['T1-ETAPA-TRATO', 'T2-ETAPA-TRATO', 'T3-ETAPA-TRATO',
            'T4-ETAPA-TRATO', 'T5-ETAPA-TRATO', 'T6-ETAPA-TRATO']
    baias = result['RECEITA FINAL DE DISTRIBUIÇÃO POR BAIA']
    assert len(baias) == len(EXPECTED_BAIA_TRATOS_SECO)
    for idx, (row, exp) in enumerate(zip(baias, EXPECTED_BAIA_TRATOS_SECO)):
        for col_i, (col, e) in enumerate(zip(cols, exp)):
            assert almost(row[col], e), (
                f"Baia {idx}, {col}: {row[col]} != {e}"
            )


EXPECTED_P_V_UMIDO = [
    (924.9, 924.9), (195.0, 300.0), (62.2, 78.7), (0, 0), (0, 0),
    (1387.4, 1387.4), (292.5, 450.0), (93.3, 118.1), (0, 0), (0, 0),
    (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
    (1387.4, 1387.4), (292.5, 450.0), (93.3, 118.1), (0, 0), (0, 0),
    (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
    (924.9, 924.9), (195.0, 300.0), (62.2, 78.7), (0, 0), (0, 0),
    (1617.1, 1617.1), (308.1, 474.0), (81.6, 103.3), (78.8, 98.5), (0, 0),
    (2425.6, 2425.6), (462.2, 711.1), (122.4, 154.9), (118.2, 147.8), (0, 0),
    (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
    (2425.6, 2425.6), (462.2, 711.1), (122.4, 154.9), (118.2, 147.8), (0, 0),
    (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
    (1617.1, 1617.1), (308.1, 474.0), (81.6, 103.3), (78.8, 98.5), (0, 0),
]

EXPECTED_DISTRIBUICAO_UMIDO = [
    (2, 651.8, 591.1),
    (3, 651.8, 591.1),
    (0, 0.0,   0.0),
    (3, 651.8, 591.1),
    (0, 0.0,   0.0),
    (2, 651.8, 591.1),
    (3, 764.3, 695.2),
    (4, 859.9, 782.1),
    (0, 0.0,   0.0),
    (4, 859.9, 782.1),
    (0, 0.0,   0.0),
    (3, 764.3, 695.2),
]

def test_script_1_umido(session_with_seed):
    result = script_1(session_with_seed, data_base=date(2026, 3, 20), considerar_fracao_liquida=True)

    assert result['LOCALIZAÇÃO DE DADOS RELEVANTES NA CURVA COM BASE NO DIA']

    # --- total formula/trato ---
    got = [(i['TRATO'], i['FORMULA'], i['VALOR']) for i in result['TOTAL FORMULA/TRATO']]
    assert got == EXPECTED_TOTAL_FORMULA_TRATO

    # --- producao/receita ---
    assert_rows(result['CÁLCULO DE PRODUÇÃO E RECEITA'], EXPECTED_P_V_UMIDO, 'P_TRATO', 'V_TRATO')

    # --- distribuição ---
    assert_rows(result['CALCULO DE RAÇÃO LIQUIDA POR TRATO E FORMULA TOTALIZADOS'], EXPECTED_DISTRIBUICAO_UMIDO, 'ETAPAS_TRATO', 'V_ETAPA_TRATO', 'P_ETAPA_TRATO')

    # --- distribuição por baia ---
    cols = ['T1-ETAPA-TRATO', 'T2-ETAPA-TRATO', 'T3-ETAPA-TRATO',
            'T4-ETAPA-TRATO', 'T5-ETAPA-TRATO', 'T6-ETAPA-TRATO']
    baias = result['RECEITA FINAL DE DISTRIBUIÇÃO POR BAIA']
    assert len(baias) == len(EXPECTED_BAIA_TRATOS_SECO)
    for idx, (row, exp) in enumerate(zip(baias, EXPECTED_BAIA_TRATOS_SECO)):
        for col_i, (col, e) in enumerate(zip(cols, exp)):
            assert almost(row[col], e), (
                f"Baia {idx}, {col}: {row[col]} != {e}"
            )
