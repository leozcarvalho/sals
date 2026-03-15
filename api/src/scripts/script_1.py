import json
from decimal import Decimal
from collections import defaultdict

import asyncio
import logging
from src.core.db import session_scope

from src.cruds.batch import BatchRepository
from src.cruds.trato import TratoRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def script_1(session, initial_day):
    batch_repo = BatchRepository(session)
    trato_repo = TratoRepository(session)

    lotes = batch_repo.get_list(filters={'is_active': True, 'initial_day': initial_day})
    tratos = trato_repo.get_list()

    result = defaultdict(lambda: defaultdict(Decimal))

    for lote in lotes:
        
        curva_details = lote.feeding_curve.details
        dia = lote.initial_day
        logger.info("Processing lote: %s", f'{lote.name} (ID: {lote.id}) with initial day {dia}')
        for trato in tratos:
            percent = Decimal(trato.percent) / Decimal(100)
            formula_dia = [d for d in curva_details if d.age_day == dia]
            if not formula_dia:
                logger.warning("No feeding curve details found for lote %s on day %s", lote.name, dia)
                continue
            formula_dia = formula_dia[0]
            mass_per_animal = formula_dia.formula_mass_per_animal
            used_mass = mass_per_animal * percent
            result[trato.id][formula_dia.formula.name] += used_mass

    output = []

    for trato_id, formulas in result.items():
        output.append({
            "trato": trato_id,
            "formulas": [
                {
                    "formula": formula,
                    "massa_total": float(mass)
                }
                for formula, mass in formulas.items()
            ]
        })

    result = json.dumps(output, indent=4, ensure_ascii=False)
    #logger.info("Script 1 result:\n%s", result)
    return result


def main():
    with session_scope() as session:
        script_1(session, initial_day=1)

if __name__ == "__main__":
    main()

 