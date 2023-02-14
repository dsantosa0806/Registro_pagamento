import sys
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException

## Oh Lord, forgive me for what i'm about to Code !


def acessa_sior(navegador):
    try:
        #Acesso a tela de login
        url_login = 'http://servicos.dnit.gov.br/sior/Account/Login/?ReturnUrl=%2Fsior%2F'
        navegador.get(url_login)
    except ValueError:
        print('Erro', 'O SIOR apresentou instabilidade, '
                      'por favor reinicie a aplicação e tente novamente T:acessa_sior ')
        sys.exit()


def login(navegador,usuario,senha):
    username = usuario
    userpass = senha
    cpfpath = '// *[ @ id = "UserName"]'
    senhapath = '//*[@id="Password"]'
    clickpath = '//*[@id="FormLogin"]/div[4]/div[2]/button'
    err = True
    while err:
        try:
            WebDriverWait(navegador, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, cpfpath))).send_keys(username)
            WebDriverWait(navegador, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, senhapath))).send_keys(userpass)
            WebDriverWait(navegador, 15).until(
                EC.element_to_be_clickable(
                    (By.XPATH, clickpath))).click()

            time.sleep(2)

            err = False

        except TimeoutException:
            print('Erro', 'O SIOR apresentou instabilidade, '
                          'por favor reinicie a aplicação e tente novamente T:Login')
            sys.exit()


def validate_login_error(navegador):
    cpfpath = '// *[ @ id = "UserName"]'
    senhapath = '//*[@id="Password"]'
    login_error = '//*[@id="placeholder"]/div[3]/div/div/div/div'
    try:
        navegador.find_element(By.XPATH,login_error).is_displayed()
        navegador.find_element(By.XPATH,cpfpath).clear()
        navegador.find_element(By.XPATH,senhapath).clear()
        return True
    except NoSuchElementException:
        return False


def validate_logado(navegador):
    logado = '//*[@id="center-pane"]/div/div/div[1]/div[2]'
    try:
        WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, logado))).is_displayed()
        valor = navegador.find_element(By.XPATH, logado).text
        print('Sucesso !', f'Bem-vindo(a)\n'
                           '\n'
                           f' {valor}')
        return True

    except TimeoutException:
        print('Opss', 'O SIOR apresentou instabilidade, a aplicação será encerrada.'
                      ' Por favor reinicie a aplicação e tente novamente T:validate_logado')
        return 0


def acessa_tela_incial_auto(navegador):
    # Acessa a tela da notificação da autuação
    url_base = 'https://servicos.dnit.gov.br/sior/Infracao/ConsultaAutoInfracao/?SituacoesInfracaoSelecionadas=1'
    try:
        navegador.get(url_base)
    except ValueError:
        print('Erro', 'O SIOR apresentou instabilidade, '
                      'por favor reinicie a aplicação e tente novamente T:acessa_tela_incial_auto')
        sys.exit()


def acessa_tela_incial_auto_pagamento(navegador):
    # Acessa a tela da notificação da autuação
    url_base = 'https://servicos.dnit.gov.br/sior/Cobranca/ENACPagamento'
    try:
        navegador.get(url_base)
    except ValueError:
        print('Erro', 'O SIOR apresentou instabilidade, '
                      'por favor reinicie a aplicação e tente novamente T:acessa_tela_incial_auto')
        sys.exit()


def registra(navegador, auto, data_pag, num_arrecadacao, obs):
    btn_consultar_inicial = '//*[@id="placeholder"]/div[1]/div/div[1]/button'
    btn_novo = '//*[@id="placeholder"]/div[1]/div/div[2]/button[2]'
    btn_salvar = '//*[@id="placeholder"]/div[1]/div/div/button[1]'
    input_data = '//*[@id="DataPagamento"]'
    input_num_arrec = '//*[@id="NumeroDocumentoArrecadacao"]'
    input_obs = '//*[@id="Observacao"]'
    btn_pesquisa_ait = '//*[@id="formENACPagamento"]/fieldset/div[1]/div[1]/div[2]/button'
    input_ait = '//*[@id="NumeroAutoPesquisa"]'
    btn_consultar = '/html/body/div[13]/div[2]/div[1]/div/div[1]/button'
    ait_visivel = '//*[@id="gridInfracao"]/table/tbody/tr/td[1]/a'
    master_row = '//*[@id="gridInfracao"]/table/tbody/tr'
    devedor = '//*[@id="devedorView"]'

    data_pagf = datetime.strftime(data_pag, "%d/%m/%Y")
    num_arrecadacaof = "%017d" % num_arrecadacao
    obsf = "%017d" % obs


    # Clique BTN novo
    try:
        WebDriverWait(navegador, 25).until(
            EC.element_to_be_clickable((By.XPATH, btn_novo))).click()
    except TimeoutException:
        print(f'Erro {auto}', 'Btn Novo')
        return 1

    # Pesquisa Ait
    try:
        WebDriverWait(navegador, 25).until(
            EC.element_to_be_clickable((By.XPATH, btn_pesquisa_ait))).click()
    except TimeoutException:
        print(f'Erro {auto}', 'Btn Ait')
        return 1

    # Input Ait
    try:
        WebDriverWait(navegador, 25).until(
            EC.element_to_be_clickable((By.XPATH, input_ait))).send_keys(auto)
    except TimeoutException:
        print(f'Erro {auto}', 'Input Ait')
        return 1

    # Consultar Ait
    try:
        WebDriverWait(navegador, 25).until(
            EC.element_to_be_clickable((By.XPATH, btn_consultar))).click()
    except TimeoutException:
        print(f'Erro {auto}', 'Btn Consultar')
        return 1

    #  Ait Visible
    try:

        if WebDriverWait(navegador, 25).until(
                EC.element_to_be_clickable((By.XPATH, ait_visivel))).is_displayed():
            WebDriverWait(navegador, 25).until(
                EC.element_to_be_clickable((By.XPATH, master_row))).click()
    except TimeoutException:
        print(f'Erro {auto}', 'Master Row')
        return 1

    #  Devedor Visible e input elements
    try:
        if WebDriverWait(navegador, 25).until(
                EC.element_to_be_clickable((By.XPATH, devedor))).is_displayed():
            WebDriverWait(navegador, 25).until(
                EC.element_to_be_clickable((By.XPATH, input_data))).send_keys(data_pagf)
            WebDriverWait(navegador, 25).until(
                EC.element_to_be_clickable((By.XPATH, input_num_arrec))).send_keys(num_arrecadacaof)
            WebDriverWait(navegador, 25).until(
                EC.element_to_be_clickable((By.XPATH, input_obs))).send_keys(obsf)
    except TimeoutException:
        print(f'Erro {auto}', 'Input elementos')
        return 1

    #  Devedor Visible e input elements
    try:
        WebDriverWait(navegador, 25).until(
            EC.element_to_be_clickable((By.XPATH, btn_salvar))).click()
    except ElementClickInterceptedException:
        print(f'Erro {auto}', 'Btn Salvar')
        return 1

    # Clique Consultar
    try:
        time.sleep(3)
        WebDriverWait(navegador, 25).until(
            EC.element_to_be_clickable((By.XPATH, btn_consultar_inicial))).is_displayed()
    except TimeoutException:
        print(f'Erro {auto}', 'Btn Consultar')
        return 1

