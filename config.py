# Armazenar as configurações do ambiente de desenvolvimento
from os import environ # Esse arquivo tem acesso as variaveis de ambiente
from dotenv import load_dotenv # Carregamento das variaveis de ambiente nesse arquivo do .env

load_dotenv() # Carrega as variaveis de ambiente do arquivo .env

class Config:
    SQLALCHEMY_DATABASE_URI = environ.get('URL_DATABASE_DEV') # Puxa a variavel de ambiente e utiliza para conexão com o banco de dados
<<<<<<< HEAD
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Desabilita o rastreamento de modificações do SQLAlchemy e evita carregamentos desnecessários e, principalmente, OTIMIZA as querys no banco de dados
=======
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Desabilita o rastreamento de modificações do SQLAlchemy e evita carregamentos desnecessários e OTIMIZA as querys no banco de dados
>>>>>>> 9646ef9c723e9148154edf715d33e5385596ccc2
