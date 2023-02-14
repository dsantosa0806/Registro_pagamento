
import pandas as pd
table = pd.read_excel('tables/registros.xlsx')
print(table.columns)
# Atribuindo dados para variáveis
for i, auto in enumerate(table['Auto']):
    data_pagamento = table.loc[i,'Data']
    num_arrec = table.loc[i,'NumeroDocArrecadacao']
    observacao = table.loc[i,'Observacao']

    print("%017d" % num_arrec)
