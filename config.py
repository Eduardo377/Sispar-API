from os import environ # Acesso as variaveis de ambiente
from dotenv import load_dotenv # Carrega as variaveis de ambiente do arquivo .env

load_dotenv() # Carrega as variaveis de ambiente do arquivo .env

class Config:
    SQLALCHEMY_DATABASE_URI = environ.get('URL_DATABASE_DEV') # URL do banco de dados
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Desabilita o rastreamento de modificações do SQLAlchemy e evita carregamentos desnecessários