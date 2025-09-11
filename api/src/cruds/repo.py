from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, asc, desc, text, true
from src.domain import exceptions as exc
from src.domain.permissions import PermissionEnum

class Repository:
    def __init__(self, model, db_session: Session):
        self.model = model
        self.db_session = db_session

    def get_entity_name(self):
        return self.model.__table__.name

    def get(self, id: int, actor=None):
        return self.db_session.get(self.model, id)

    def check_exists(self, id: int, actor=None):
        db_item = self.get(id)
        if not db_item:
            raise exc.NotFound(f"{self.get_entity_name()} not found")
        return db_item

    def build_query(self):
        query = self.db_session.query(self.model)
        return query
    
    def apply_ordering(self, query, order_by: dict):
        """
        Aplica a ordenação no query baseado no dicionário order_by.
        Exemplo de order_by: {'field_name': 'asc', 'other_field': 'desc'}
        """
        if not order_by or not isinstance(order_by, dict):
            return query
        
        for field_name, direction in order_by.items():
            column = getattr(self.model, field_name, None)
            if column is not None:
                if direction.lower() == 'asc':
                    query = query.order_by(asc(column))
                else:
                    query = query.order_by(desc(column))
        return query
    
    def format_results(self, results: List):
        return results
    
    def get_list(self, skip: int = 0, limit: int = None, filters: dict = None, order_by: dict = {'id': 'asc'}, actor=None):
        query = self.build_query()
        query = self.build_filter(query, filters)
        query = self.apply_ordering(query, order_by)
        query = query.offset(skip)
        if limit is not None:
            query = query.limit(limit)
        return self.format_results(query.all())

    def get_count(self, filters: dict = None) -> int:
        query = self.build_query()
        query = self.build_filter(query, filters)
        return query.count()
    
    def get_list_and_count(self, skip: int = 0, limit: int = None, filters: dict = None, order_by: dict = {'id': 'asc'}, actor=None):
        return self.get_list(skip, limit, filters, order_by), self.get_count(filters)

    def get_one(self, filters: dict):
        query = self.db_session.query(self.model)
        query = self.build_filter(query, filters)
        return query.first()

    def build_filter(self, query, filters: dict):
        """
        Aplica filtros ao query com base nos atributos e operadores fornecidos.

        Os filtros podem ser passados no seguinte formato:
        {
            'attr': 'valor',  # Igualdade (eq)
            'attr': {'op': 'like', 'value': valor},  # LIKE
            'attr': {'op': 'in', 'value': [valor1, valor2]},  # IN
            'attr': {'op': 'ge', 'value': valor},  # >=
            'attr': {'op': 'le', 'value': valor},  # <=
            'attr': {'op': 'range', 'start': valor1, 'end': valor2},  # Intervalo de valores
            'or': [{'attr1': valor}, {'attr2': {'op': 'eq', 'value': valor}}]  # Condições OR
        }
        """
        conditions = []
        if filters:
            for key, value in filters.items():
                if key not in self.model.__table__.columns.keys():
                    continue
                if value in [None, '']:
                    continue
                if key == 'or':
                    # Filtros 'OR' para múltiplas condições
                    or_conditions = []
                    for or_filter in value:
                        or_conditions = [self._apply_condition(attr, cond) for attr, cond in or_filter.items()]
                    conditions.append(or_(*or_conditions))
                else:
                    # Se o valor for diretamente passado, assume-se igualdade (eq)
                    condition = value if isinstance(value, dict) else {'op': 'eq', 'value': value}
                    conditions.append(self._apply_condition(key, condition))
        return query.filter(and_(*conditions) if conditions else true())

    def _apply_condition(self, attr: str, condition: dict):
        """
        Aplica a condição para um atributo específico com base no operador.
        """
        column = getattr(self.model, attr)
        op = condition.get('op', 'eq')  # O padrão agora é 'eq'
        value = condition.get('value')

        if op == 'eq':
            return column == value
        elif op == 'like':
            return column.like(f"%{value}%")
        elif op == 'in':
            return column.in_(value)
        elif op == 'ge':
            return column >= value
        elif op == 'le':
            return column <= value
        elif op == 'range':
            start = condition.get('start')
            end = condition.get('end')
            conditions = []
            if start is not None:
                conditions.append(column >= start)
            if end is not None:
                conditions.append(column <= end)
            return and_(*conditions)


    def save(self, values: dict, actor=None):
        if actor:
            values['created_by'] = str(actor.id)
            values['updated_by'] = str(actor.id)
        obj = self.model(**values)
        self.db_session.add(obj)
        self.db_session.flush()
        return obj

    def update(self, id: int, values: dict, actor=None):
        obj = self.check_exists(id)
        if actor:
            values['updated_by'] = str(actor.id)
        if obj:
            for key, value in values.items():
                setattr(obj, key, value)
            self.db_session.flush()
        return obj

    def delete(self, id: int, actor=None):
        obj = self.check_exists(id)
        if obj:
            self.db_session.delete(obj)
            self.db_session.flush()
            return obj
        return None

    def get_columns(self):
        return self.model.__table__.columns.keys()

    def commit(self):
        self.db_session.commit()