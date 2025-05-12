from src.model import db
from sqlalchemy.schema import Column, ForeignKey # Traz o recurso para o ORM entender que o atributo será uma coluna na tabela
# Traz o recurso para o ORM entender que o atributo será uma chave estrangeira na tabela
from sqlalchemy.types import Integer, String, DECIMAL, DATE
from sqlalchemy.sql import func # <- Importa uma função geradora para pegar date e hora atual

class Reembolso(db.Model):
    __tablename__ = "reembolso"
# --------------------------------------ATRIBUTOS--------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    company = Column(String(50), nullable=False)
    installment_number = Column(Integer, nullable=False)
    description = Column(String(255))
    date = Column(DATE, nullable=False, default=func.current_date())
    expense_type = Column(String(35), nullable=False)
    cost_center = Column(String(50), nullable=False)
    internal_order = Column(String(50))
    div = Column(String(50))
    pep = Column(String(50))
    currency = Column(String(20), nullable=False)
    distance_km = Column(String(50)) 
    value_km = Column(String(50)) 
    value_billed = Column(DECIMAL(10,2), nullable=False) 
    expense = Column(DECIMAL(10,2))
    id_colaborador = Column(Integer, ForeignKey(column='colaborador.id'), nullable=False)
    status = Column(String(25))
#-------------------------------------------------------------------------------------------------------------

    def __init__(self, name, company, installment_number,description, date, expense_type, cost_center, internal_order, div, pep, currency, distance_km, value_km, value_billed, expense, id_colaborador, status='Em analise'):
        self.name = name
        self.company = company
        self.installment_number = installment_number
        self.description = description
        self.date=date
        self.expense_type = expense_type
        self.cost_center = cost_center
        self.internal_order = internal_order
        self.div = div
        self.pep = pep
        self.currency = currency
        self.distance_km = distance_km
        self.value_km = value_km
        self.value_billed = value_billed
        self.expense = expense
        self.id_colaborador = id_colaborador
        self.status = status
        
#----------------------------------------------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'company': self.company,
            'installment_number': self.installment_number,
            'description': self.description,
            'date': self.date,
            'expense_type': self.expense_type,
            'cost_center': self.cost_center,
            'internal_order': self.internal_order,
            'div': self.div,
            'pep': self.pep,
            'currency': self.currency,
            'distance_km': self.distance_km,
            'value_km': self.value_km,
            'value_billed': self.value_billed,
            'expense': self.expense,
            'id_colaborador': self.id_colaborador,
            'status': self.status
        }