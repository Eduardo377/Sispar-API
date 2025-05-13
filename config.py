# Armazenar as configurações do ambiente de desenvolvimento
from os import environ # Esse arquivo tem acesso as variaveis de ambiente
from dotenv import load_dotenv # Carregamento das variaveis de ambiente nesse arquivo do .env

load_dotenv() # Carrega as variaveis de ambiente do arquivo .env

class Config:
    SQLALCHEMY_DATABASE_URI = environ.get('URL_DATABASE_PROD') # Puxa a variavel de ambiente e utiliza para conexão com o banco de dados
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Desabilita o rastreamento de modificações do SQLAlchemy e evita carregamentos desnecessários e OTIMIZA as querys no banco de dados