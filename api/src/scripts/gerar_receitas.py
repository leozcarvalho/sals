from collections import defaultdict
from datetime import date, time
from decimal import Decimal
from sqlmodel import Session, select

from src.scripts.script_1 import script_1, calcular_dia_curva, r
from src.cruds.trato import TratoRepository
from src.cruds.batch import BatchRepository
from src.domain.receita import Receita, ReceitaStatus
from src.domain.receita_produzir import ReceitaProduzir, ReceitaProduzirStatus
from src.domain.receita_distribuicao import ReceitaDistribuicao, ReceitaDistribuicaoStatus
from src.domain import exceptions as exc


def _ingredientes_unicos(resultado: dict) -> dict[tuple, dict]:
    """
    Deduplica a matriz de produção por (cozinha_id, trato_id, formula_id, produto_id).
    A matriz repete o total da cozinha para cada lote — basta a primeira ocorrência.
    """
    mapa: dict[tuple, dict] = {}
    for row in resultado["CÁLCULO DE PRODUÇÃO E RECEITA"]:
        if row["ID_CZ"] is None:
            continue
        chave = (row["ID_CZ"], row["TRATO"], row["ID_FO"], row["ID_PR"])
        if chave not in mapa:
            mapa[chave] = {
                "p_trato": Decimal(str(row["P_TRATO"])),
                "v_trato": Decimal(str(row["V_TRATO"])),
                "e_agua":  row["EH_AGUA"],
            }
    return mapa


def gerar_receitas(session: Session, data_base: date) -> list[Receita]:
    """
    Gera RECEITAS, RECEITAS_PRODUZIR e RECEITAS_DISTRIBUICAO do dia.
    Lança erro se já existirem receitas para a data informada.
    """
    existente = session.exec(select(Receita).where(Receita.data == data_base)).first()
    if existente:
        raise exc.InvalidData(f"Receitas para {data_base} já foram geradas.")

    resultado_seco  = script_1(session, data_base=data_base, considerar_fracao_liquida=False)
    resultado_umido = script_1(session, data_base=data_base, considerar_fracao_liquida=True)

    trato_repo = TratoRepository(session)
    tratos_map = {t.id: t for t in trato_repo.get_list()}

    ing_seco  = _ingredientes_unicos(resultado_seco)
    ing_umido = _ingredientes_unicos(resultado_umido)

    etapas_map: dict[tuple, int] = {}
    for linha in resultado_seco["CALCULO DE RAÇÃO LIQUIDA POR TRATO E FORMULA TOTALIZADOS"]:
        chave = (linha["ID_CZ"], linha["TRATO"], linha["ID_FO"])
        etapas_map[chave] = linha["ETAPAS_TRATO"]

    # ── Metadados por baia: galpao, sala, cozinha, formula ───────────────────
    lotes = BatchRepository(session).get_list(filters={"is_active": True})
    baia_meta: dict[int, dict] = {}
    for lote in lotes:
        try:
            dia = calcular_dia_curva(lote, data_base)
        except ValueError:
            continue
        detalhes = lote.feeding_curve.details if lote.feeding_curve else []
        if dia >= len(detalhes) or not detalhes[dia] or not detalhes[dia].formula:
            continue
        cozinha = lote.sala.shed.kitchen
        if not cozinha:
            continue
        formula = detalhes[dia].formula
        for baia in lote.sala.baias:
            baia_meta[baia.id] = {
                "cozinha_id": cozinha.id,
                "galpao_id":  lote.sala.shed.id,
                "sala_id":    lote.sala.id,
                "formula_id": formula.id,
            }

    # ── Expande ração totalizada em N receitas (uma por etapa) ───────────────
    linhas = []
    for linha in resultado_seco["CALCULO DE RAÇÃO LIQUIDA POR TRATO E FORMULA TOTALIZADOS"]:
        etapas = linha["ETAPAS_TRATO"]
        if etapas == 0:
            continue
        trato      = tratos_map[linha["TRATO"]]
        hora_trato = time(trato.hour, trato.minute)
        for etapa in range(1, etapas + 1):
            linhas.append({
                "hora_trato":   hora_trato,
                "cozinha_id":   linha["ID_CZ"],
                "formula_id":   linha["ID_FO"],
                "trato_id":     trato.id,
                "etapa":        etapa,
                "etapas_total": etapas,
                "p_etapa_seco": Decimal(str(linha["P_ETAPA_TRATO"])),
            })

    linhas.sort(key=lambda x: (x["hora_trato"], x["cozinha_id"], x["etapa"]))

    # ── Índice de receitas criadas por (cozinha, trato) → {etapa → receita} ──
    receitas_idx: dict[tuple, dict[int, Receita]] = defaultdict(dict)

    # ── Cria RECEITAS + RECEITAS_PRODUZIR ─────────────────────────────────────
    receitas = []
    for seq_receita, dados in enumerate(linhas, start=1):
        receita = Receita(
            data=data_base,
            seq=seq_receita,
            id_cz=dados["cozinha_id"],
            id_fo=dados["formula_id"],
            trato=dados["trato_id"],
            etapa=dados["etapa"],
            p_etapa_s_frac=dados["p_etapa_seco"],
            hora_trato=dados["hora_trato"],
            status=ReceitaStatus.aguardando,
        )
        session.add(receita)
        session.flush()

        receitas_idx[(dados["cozinha_id"], dados["trato_id"])][dados["etapa"]] = receita

        etapas_total   = dados["etapas_total"]
        chave_cz_tr_fo = (dados["cozinha_id"], dados["trato_id"], dados["formula_id"])

        itens = [
            (chave, ing)
            for chave, ing in ing_seco.items()
            if chave[:3] == chave_cz_tr_fo and ing["p_trato"] > 0
        ]
        itens.sort(key=lambda x: (x[1]["e_agua"], x[0][3]))

        for seq_dosagem, (chave, ing_s) in enumerate(itens, start=1):
            produto_id = chave[3]
            ing_u      = ing_umido.get(chave, ing_s)
            session.add(ReceitaProduzir(
                receita_id=receita.id,
                cozinha_id=dados["cozinha_id"],
                formula_id=dados["formula_id"],
                trato_id=dados["trato_id"],
                etapa=dados["etapa"],
                produto_id=produto_id,
                seq_dosagem=seq_dosagem,
                peso_etapa_sem_fracao_liquida=r(ing_s["p_trato"] / etapas_total),
                peso_etapa_com_fracao_liquida=r(ing_u["p_trato"] / etapas_total),
                volume_etapa=r(ing_s["v_trato"] / etapas_total),
                produto_e_agua=ing_s["e_agua"],
                status=ReceitaProduzirStatus.aguardando,
            ))

        receitas.append(receita)

    # ── Cria RECEITAS_DISTRIBUICAO ─────────────────────────────────────────────
    for row in resultado_seco["RECEITA FINAL DE DISTRIBUIÇÃO POR BAIA"]:
        baia_id = row["ID"]
        meta    = baia_meta.get(baia_id)
        if not meta:
            continue

        cz_id      = row["ID_CZ"]
        sala_id    = row["ID_SA"]
        suinos     = row["SUINOS"]

        for (cz, trato_id), etapas_dict in receitas_idx.items():
            if cz != cz_id:
                continue

            col  = f"T{trato_id}-ETAPA-TRATO"
            pesf = Decimal(str(row.get(col, 0)))
            if pesf == 0:
                continue

            for etapa, receita in etapas_dict.items():
                if receita.id_fo != meta["formula_id"]:
                    continue
                session.add(ReceitaDistribuicao(
                    receita_id=receita.id,
                    cozinha_id=cz_id,
                    galpao_id=meta["galpao_id"],
                    sala_id=sala_id,
                    baia_id=baia_id,
                    quantidade_suinos=suinos,
                    formula_id=meta["formula_id"],
                    trato_id=trato_id,
                    etapa=etapa,
                    peso_sem_fracao_liquida=pesf,
                    status=ReceitaDistribuicaoStatus.aguardando,
                ))

    session.commit()
    for rec in receitas:
        session.refresh(rec)

    return receitas
