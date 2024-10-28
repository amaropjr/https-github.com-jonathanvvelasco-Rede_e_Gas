import pandas as pd
import ixmp
import message_ix
from matplotlib.pyplot import *
import matplotlib.pyplot as plt

from message_ix.utils import make_df

import inicio
import link
import descreve
import limites
import saidas


mp = ixmp.Platform()


scenario = message_ix.Scenario(mp, model="Brazil Electrified", scenario="baseline", version="new")


scenario, history, model_horizon, country, nodes    = inicio.definicoes (pd,scenario)

for local in nodes:
    scenario                                            = inicio.demanda    (pd,scenario,model_horizon,local)
    vintage_years, act_years,base_input, base_output    = link.base         (make_df,scenario,local)
    scenario, grid_efficiency                           = link.tecnologias  (scenario,base_input, base_output,local)
    scenario, capacity_factor               = descreve.fator_capacidade     (make_df,scenario,local,vintage_years, act_years)
    scenario                                = descreve.vida_util            (make_df,scenario,local,model_horizon)
    scenario                                = descreve.expande_tecnologias  (make_df,scenario,local,model_horizon)
    scenario                                = descreve.historico_geracao    (make_df,scenario,grid_efficiency,local,history,capacity_factor)
    scenario                                = descreve.custo_investimento   (make_df,scenario,local,model_horizon)
    scenario                                = descreve.custo_fixo           (make_df,scenario,local,vintage_years, act_years)
    scenario                                = descreve.custo_variavel       (make_df,scenario,local,vintage_years, act_years)
    scenario                                = limites.expansao_up           (make_df,scenario,local)

scenario = link.transmissao_S_SE(make_df,scenario)
scenario = link.transmissao_SE_S(make_df,scenario)

scenario.solve()


#saidas.gera_excel(pd,scenario)

print("O modelo foi rodado com sucesso.")


mp.close_db()



"""
# Tarefas
[x] 1. Região SE/CE (aprender a subdividir)
    [x] Trocar country por subsystem
[x] 2. Colocar 4 regiões
[x] 3. Conectar 2 regiões (SE/CE e Sul) (ambos os sentidos)
[] 4. Conectar todas as rgiões (respeitando geografia)
[] 5. Calibrar características das regiões
    [] Acrescentar ifs em cada modulo, para customizar dados de entrada por subsystem
[] 6. Revisar unidades no programa (USD, MW e MWa)
[] 7. Acrescentar tecnologia household para depois virar serviço energético
Obs: os dados inseridos devem contemplar todas as regioes.
"""