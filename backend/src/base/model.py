import uuid
from typing import Callable

from sqlalchemy import ForeignKey, Select, and_
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)


class FilterableMixin:
    
    @staticmethod
    def eq(field, value): return field == value
    @staticmethod
    def neq(field, value): return field != value
    @staticmethod
    def contains(field, value): return field.ilike(f"%{value}%")
    @staticmethod
    def not_contains(field, value): return ~field.ilike(f"%{value}%")
    @staticmethod
    def gt(field, value): return field > value
    @staticmethod
    def lt(field, value): return field < value

    OPERATORS: dict[str, Callable] = {
        "eq": eq,
        "neq": neq,
        "contains": contains,
        "not_contains": not_contains,
        "gt": gt,
        "lt": lt,
    }

    @classmethod
    def apply_filters(cls, query: Select, filters: dict[str, dict[str, str]]) -> Select:
        conditions = []

        for field, rule in filters.items():
            if rule is None:
                continue
            if not hasattr(cls, field):
                raise AttributeError(f"Model {cls.__name__} has no attribute '{field}'")

            operator = rule.get("operator", "eq")
            value = rule.get("value")
            operator_func = cls.OPERATORS.get(operator)

            if operator_func is None:
                raise ValueError(f"Operador inválido: {operator}")

            column = getattr(cls, field)
            try:
                value = column.type.python_type(value)
            except Exception:
                raise ValueError(f"Valor inválido para {field}: {value!r}")

            conditions.append(operator_func(column, value))

        if conditions:
            query = query.where(and_(*conditions))
        return query
            
class BaseModel(DeclarativeBase, FilterableMixin):
    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self) -> str:
        attrs = ", ".join(f"{key}={value!r}" for key, value in self.__dict__.items() if not key.startswith('_'))
        return f"<{self.__class__.__name__}({attrs})>"

class ResourceModel(BaseModel):
    __abstract__ = True

    @declared_attr
    def owner_id(cls) -> Mapped[uuid.UUID]:
        return mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    @declared_attr
    def owner(cls):
        return relationship("User", backref="owned_resources")
    #TODO

