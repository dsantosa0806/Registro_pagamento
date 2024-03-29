from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as webdriver
import pandas as pd
from Navegador.selenium_execution import acessa_sior, login, acessa_tela_incial_auto_pagamento, registra


def option_navegador():

    options = webdriver.ChromeOptions()
    options.add_argument("enable-automation")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--use_subprocess")
    return options


def service_navegador():
    serv = Service()
    return serv


navegador = webdriver.Chrome(options=option_navegador())

acessa_sior(navegador)
login(navegador)
acessa_tela_incial_auto_pagamento(navegador)

table = pd.read_excel('tables/registros.xlsx')

# Atribuindo dados para variáveis
for i, auto in enumerate(table['Auto']):
    data_pagamento = table.loc[i,'Data']
    num_arrec = table.loc[i,'NumeroDocArrecadacao']
    observacao = table.loc[i,'Observacao']

    if registra(navegador, auto, data_pagamento, num_arrec, observacao) == 1:
        acessa_tela_incial_auto_pagamento(navegador)
        continue
    else:
        print(f'{i+1} {auto} Finalizado')

    # Finaliza o Loop
    acessa_tela_incial_auto_pagamento(navegador)

