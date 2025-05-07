# teste unitario vai testar 1 por 1 
# teste de integração vai testar um conjunto de coisas
# E2e é ponta a ponta. Pode ter vários fluxos no site e cada e2e testa um deles. Senão o código fica mto grande
# 1 e2e: cadastro
# Outro: login
# Outro: algum fluxo dentro do site, tipo administrar usuário 
# Etc
# Para que a biblioteca encontre o arquivo de teste, é necessário que o nome do arquivo comece com "test_" ou termine com "_test".
# Colocar o arquivo __init__.py para o pytest reconhecer a pasta como um pacote Python.
# Colocar o arquivo __init__.py para no src 
# pip install pytest-flask
# import pytest # Traz a biblioteca pytest para o arquivo de teste
# import time #  manipula o tempo

# from src.
#from src.app import create_app # Importa a função create_app do arquivo app.py


#-----------------------------Configuração para teste-----------------------------------
# @pytest.fixture # Vai identificar que a função é um fixture do pytest
# def app():
#     app = create_app() # Cria a aplicação Flask
#     yeild app # Retorna a aplicação para o pytest
# @pytest.fixture # Identifica que a função é um fixture do pytest
# def client(app):
#     return app.test_client() # Retorna o cliente de teste da aplicação Flask

#----------------------------------------------------------------

# funções de teste precisam começar com test_ ou terminar com _test

# def test_desempenho_requisição_get(client):
#     # Testa o desempenho da requisição GET