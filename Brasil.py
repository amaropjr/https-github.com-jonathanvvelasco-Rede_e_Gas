import pandas as pd
import ixmp
import message_ix
from matplotlib.pyplot import *
import matplotlib.pyplot as plt

from message_ix.utils import make_df

import inicio
import link


mp = ixmp.Platform()

scenario = message_ix.Scenario(mp, model="Brazil Electrified", scenario="baseline", version="new")
country = "Brazil"

scenario, history, model_horizon                    = inicio.definicoes(pd,scenario)
vintage_years, act_years,base_input, base_output    = link.base(make_df,scenario,"Brazil")
scenario, grid_efficiency                           = link.tecnologias(scenario,base_input, base_output)


capacity_factor = {
    "oil_ppl": 0.2,
    "pch_ppl": 0.5,
    "nuclear_g_ppl":0.85,
    "biogas_ppl":0.5,
    "solar_fotovoltaic_ppl":0.4,
    "solar_csp_ppl":0.2,
    "onshore_wind_ppl":0.3,
    "offshore_wind_ppl":0.3,
    "biomass_retrofit_ppl":0.67,
    "biomass_greenfield_ppl":0.67,
    "GN_open_cycle_ppl":0.4,
    "GN_combined_cycle_ppl":0.6,
    "national_coal_ppl":0.4,
    "imported_coal_ppl":0.5,
    "large_hydroelectric_ppl":0.5,
    "medium_hydroelectric_ppl":0.55,
    "bulb": 1,
}

for tec, val in capacity_factor.items():
    df = make_df(
        "capacity_factor",
        node_loc=country,
        year_vtg=vintage_years,
        year_act=act_years,
        time="year",
        unit="-",
        technology=tec,
        value=val,
    )
    scenario.add_par("capacity_factor", df)

    lifetime = {
    "oil_ppl": 20,
    "pch_ppl": 20,
    "nuclear_g_ppl":20,
    "biogas_ppl":20,
    "solar_fotovoltaic_ppl":20,
    "solar_csp_ppl":20,
    "onshore_wind_ppl":20,
    "offshore_wind_ppl":20,
    "biomass_retrofit_ppl":40,
    "biomass_greenfield_ppl":20,
    "GN_open_cycle_ppl":20,
    "GN_combined_cycle_ppl":20,
    "national_coal_ppl":35,
    "imported_coal_ppl":35,
    "large_hydroelectric_ppl":50,
    "medium_hydroelectric_ppl":50,
    "bulb": 1,
}

for tec, val in lifetime.items():
    df = make_df(
        "technical_lifetime",
        node_loc=country,
        year_vtg=model_horizon,
        unit="y",
        technology=tec,
        value=val,
    )
    scenario.add_par("technical_lifetime", df)


growth_technologies = [
    "pch_ppl",
    "nuclear_g_ppl",
    "biogas_ppl",
    "solar_fotovoltaic_ppl",
    "solar_csp_ppl",
    "onshore_wind_ppl",
    "offshore_wind_ppl",
    "biomass_retrofit_ppl",
    "biomass_greenfield_ppl",
    "GN_open_cycle_ppl",
    "GN_combined_cycle_ppl",
    "national_coal_ppl",
    "imported_coal_ppl",
    "large_hydroelectric_ppl",
    "medium_hydroelectric_ppl",
]

for tec in growth_technologies:
    df = make_df(
        "growth_activity_up",
        node_loc=country,
        year_act=model_horizon,
        time="year",
        unit="-",
        technology=tec,
        value=1.0,
    )
    scenario.add_par("growth_activity_up", df)


historic_demand =  60194
historic_generation = historic_demand / grid_efficiency
large_hydroelectric_fraction = 0.73532
pch_fraction = 0.04153
national_coal_fraction = 0.01339
gn_fraction = 0.07709
biomass_fraction = 0.05899
wind_fraction = 0.03887
nuclear_fraction  = 0.02834
oil_fraction = 0.00645



old_activity = {
    "large_hydroelectric_ppl":(large_hydroelectric_fraction) * historic_generation,
    "oil_ppl": oil_fraction * historic_generation,
    "nuclear_g_ppl": nuclear_fraction*historic_generation,
    "national_coal_ppl": national_coal_fraction* historic_generation,
    "biomass_retrofit_ppl": biomass_fraction * historic_generation,
    "onshore_wind_ppl": wind_fraction* historic_generation,
    "GN_open_cycle_ppl": gn_fraction * historic_generation,
    "pch_ppl": pch_fraction * historic_generation,

}
nomes_energias = []
uso_energias = []


for i in old_activity.items():
    nomes_energias.append(i[0])
    uso_energias.append(i[1])


capacity = {"biomass_retrofit_ppl": 20,
       }

base_capacity = {
    'node_loc': country,
    'year_vtg': [2015, 2020, 2025],
    'unit': 'GW',
}

##cf = pd.Series(capacity_factor)
##act = pd.Series(activity)
#capacity = (act / 8760 / cf).dropna().to_dict()

for tec, val in capacity.items():
    df = make_df(base_capacity, technology=tec, value=val)
    scenario.add_par('bound_new_capacity_up', df)


for tec, val in old_activity.items():
    df = make_df(
        "historical_activity",
        node_loc=country,
        year_act=history,
        mode="standard",
        time="year",
        unit="GWa",
        technology=tec,
        value=val,
    )
    scenario.add_par("historical_activity", df)


for tec in old_activity:
    value = old_activity[tec] / (1 * 10 * capacity_factor[tec])
    df = make_df(
        "historical_new_capacity",
        node_loc=country,
        year_vtg=history,
        unit="GWa",
        technology=tec,
        value=value,
    )
    scenario.add_par("historical_new_capacity", df)


scenario.add_par("interestrate", model_horizon, value=0.05, unit="-")


mp.add_unit("USD/kW")

costs = {
    "oil_ppl": 10000,
    "pch_ppl": 2600,
    "nuclear_g_ppl":3500,
    "biogas_ppl":2400,
    "solar_fotovoltaic_ppl":5900,
    "solar_csp_ppl":4800,
    "onshore_wind_ppl":2500,
    "offshore_wind_ppl":3500,
    "biomass_retrofit_ppl":1500,
    "biomass_greenfield_ppl":1900,
    "GN_open_cycle_ppl":850,
    "GN_combined_cycle_ppl":1200,
    "national_coal_ppl":2100,
    "imported_coal_ppl":2100,
    "large_hydroelectric_ppl":1800,
    "medium_hydroelectric_ppl":2100,
    "bulb": 1,
    
}
energias = []
custos =[]
for j in costs.items():
    if j[0] != 'bulb':
        energias.append(j[0])
        custos.append(j[1])

plt.pie(custos, shadow = True, startangle = 0, textprops={'fontsize': 9}, labels = custos)
plt.title("Investment Costs (USD/kW)")
plt.legend(energias, loc='upper right', bbox_to_anchor=(1.68,0.85))
plt.gcf().set_size_inches(10, 5)
plt.figure().clear()

for tec, val in costs.items():
    df = make_df(
        "inv_cost",
        node_loc=country,
        year_vtg=model_horizon,
        unit="USD/kW",
        technology=tec,
        value=val,
    )
    scenario.add_par("inv_cost", df)

costs = {
    "oil_ppl": 20,
    "pch_ppl": 29,
    "nuclear_g_ppl":92,
    "biogas_ppl":169,
    "solar_fotovoltaic_ppl":12,
    "solar_csp_ppl":58,
    "onshore_wind_ppl":31,
    "offshore_wind_ppl":87,
    "biomass_retrofit_ppl":10,
    "biomass_greenfield_ppl":65,
    "GN_open_cycle_ppl":12,
    "GN_combined_cycle_ppl":18,
    "national_coal_ppl":28,
    "imported_coal_ppl":28,
    "large_hydroelectric_ppl":29,
    "medium_hydroelectric_ppl":29,
    "bulb": 1,
}

for tec, val in costs.items():
    df = make_df(
        "fix_cost",
        node_loc=country,
        year_vtg=vintage_years,
        year_act=act_years,
        unit="USD/kWa",
        technology=tec,
        value=val,
    )
    scenario.add_par("fix_cost", df)



#O&M + Fuel
costs = {
    "biogas_ppl": 4.0,
    "nuclear_g_ppl":5.7 + 16,
    "national_coal_ppl":4.7 + 36.62,
    "imported_coal_ppl":7.0 + 19.12,
    "GN_open_cycle_ppl":4.0 + 75.60,
    "GN_combined_cycle_ppl":2.3 + 61.60,
    "biomass_retrofit_ppl":14.0,
    "biomass_greenfield_ppl":7.0,
   
}




for tec, val in costs.items():
    df = make_df(
        "var_cost",
        node_loc=country,
        year_vtg=vintage_years,
        year_act=act_years,
        mode="standard",
        time="year",
        unit="USD/kWa",
        technology=tec,
        value=val,
    )
    scenario.add_par("var_cost", df)


from message_ix import log

log.info(f"version number before commit(): {scenario.version}")

scenario.commit(comment="basic model of Brazil electrification")

log.info(f"version number after commit(): {scenario.version}")

scenario.set_as_default()


scenario.solve()

scenario.var("OBJ")["lvl"]

from message_ix.report import Reporter

rep = Reporter.from_scenario(scenario)


from message_ix.util.tutorial import prepare_plots

prepare_plots(rep)

'''
b = pd.DataFrame(scenario.var("CAP"))
b.to_excel("Capacidade.xlsx")
c = pd.DataFrame(scenario.var("CAP_NEW"))
c.to_excel("Nova Capacidade das Instalações.xlsx")
d = pd.DataFrame(scenario.var("ACT"))
d.to_excel("Atividade.xlsx")
'''




mp.close_db()

