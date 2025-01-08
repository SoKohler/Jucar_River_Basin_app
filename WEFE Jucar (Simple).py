"""
Python model 'WEFE Jucar (Simple).py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.functions import if_then_else
from pysd.py_backend.statefuls import DelayFixed, Integ
from pysd.py_backend.external import ExtData
from pysd import Component

__pysd_version__ = "3.11.0"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 1,
    "final_time": lambda: 120,
    "time_step": lambda: 1,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Month",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP",
    units="Month",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="DéfQecolAlar",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"qecolalar": 1, "sal_jucar": 1},
)
def defqecolalar():
    return np.maximum(0, qecolalar() - sal_jucar())


@component.add(
    name="SueltasAlarcón",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"qecolalar": 1, "alarcon": 1, "demanda_total_tous": 1},
)
def sueltasalarcon():
    return np.maximum(qecolalar(), alarcon() * demanda_total_tous() / 100)


@component.add(
    name="SueltasTous",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demanda_total_aguas_abajo_tous": 1},
)
def sueltastous():
    """
    IF THEN ELSE(Time<97:AND:Time>80, 0.6, 1) 3 IF THEN ELSE(Time<96:AND:Time>80, 0.5, 1) 4 IF THEN ELSE(Time<96:AND:Time>72, 0.6, 1) 5
    """
    return demanda_total_aguas_abajo_tous()


@component.add(
    name="Estado Alarcón",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"volumen_esperado_alarcon": 1},
)
def estado_alarcon():
    return (volumen_esperado_alarcon() / (1112.5 - 30)) * 100


@component.add(
    name="Estado Contreras",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"volumen_esperado_contreras": 1},
)
def estado_contreras():
    return (volumen_esperado_contreras() / (464 - 15)) * 100


@component.add(
    name="SueltasContreras",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"contreras": 1, "demanda_total_tous": 1},
)
def sueltascontreras():
    return contreras() * demanda_total_tous() / 100


@component.add(
    name="Demanda Total Tous",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "demanda_total_ribera": 1,
        "total_demanda_urbana": 1,
        "perdidas_t": 1,
        "minimotous": 1,
        "inflow_ds_tous": 1,
        "inflow_tous": 1,
    },
)
def demanda_total_tous():
    return np.maximum(
        0,
        demanda_total_ribera()
        + total_demanda_urbana()
        + perdidas_t()
        + minimotous()
        - inflow_ds_tous()
        - inflow_tous(),
    )


@component.add(
    name="Demanda otros cultivos",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"necesidad_hidrica_otros_cultivos": 1, "supotros_cultivos_ra": 1},
)
def demanda_otros_cultivos():
    return necesidad_hidrica_otros_cultivos() * supotros_cultivos_ra()


@component.add(
    name="Demanda otros cultivos RB",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"supotros_cultivos_rb": 1, "necesidad_hidrica_otros_cultivos": 1},
)
def demanda_otros_cultivos_rb():
    return supotros_cultivos_rb() * necesidad_hidrica_otros_cultivos()


@component.add(
    name="Demanda Ribera alta",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demanda_bruta_anual": 1, "distribucion_mensual": 1},
)
def demanda_ribera_alta():
    return demanda_bruta_anual() * distribucion_mensual()


@component.add(
    name="Demanda Ribera Baja",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demanda_bruta_anual_rb": 1, "distribucion_mensual_rb": 1},
)
def demanda_ribera_baja():
    return demanda_bruta_anual_rb() * distribucion_mensual_rb()


@component.add(name="Eficiencia global RB", comp_type="Constant", comp_subtype="Normal")
def eficiencia_global_rb():
    return 0.254


@component.add(
    name="Demanda caqui RB",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"necesidad_hidrica_caqui": 1, "sup_caqui_rb": 1},
)
def demanda_caqui_rb():
    return necesidad_hidrica_caqui() * sup_caqui_rb()


@component.add(
    name="Demanda cítricos",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sup_citricos_ra": 1, "necesidad_hidrica_citricos": 1},
)
def demanda_citricos():
    return sup_citricos_ra() * necesidad_hidrica_citricos()


@component.add(
    name="Demanda arroz",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"suparroz_ra": 1, "necesidad_hidrica_arroz": 1},
)
def demanda_arroz():
    return suparroz_ra() * necesidad_hidrica_arroz()


@component.add(
    name="Demanda arroz RB",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"necesidad_hidrica_arroz": 1, "sup_arroz_rb": 1},
)
def demanda_arroz_rb():
    return necesidad_hidrica_arroz() * sup_arroz_rb()


@component.add(
    name="Demanda bruta anual",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demanda_total_neta_anual": 1, "eficiencia_global_ra": 1},
)
def demanda_bruta_anual():
    return demanda_total_neta_anual() / eficiencia_global_ra()


@component.add(
    name="Demanda bruta anual RB",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demanda_total_neta_rb_anual": 1, "eficiencia_global_rb": 1},
)
def demanda_bruta_anual_rb():
    return demanda_total_neta_rb_anual() / eficiencia_global_rb()


@component.add(
    name="Demanda Caqui",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sup_caqui_ra": 1, "necesidad_hidrica_caqui": 1},
)
def demanda_caqui():
    return sup_caqui_ra() * necesidad_hidrica_caqui()


@component.add(name="Eficiencia global RA", comp_type="Constant", comp_subtype="Normal")
def eficiencia_global_ra():
    return 0.5227


@component.add(
    name="Necesidad hídrica Otros cultivos", comp_type="Constant", comp_subtype="Normal"
)
def necesidad_hidrica_otros_cultivos():
    return 0.003


@component.add(
    name="Demanda cítricos RB",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"necesidad_hidrica_citricos": 1, "sup_citricos_rb": 1},
)
def demanda_citricos_rb():
    return necesidad_hidrica_citricos() * sup_citricos_rb()


@component.add(
    name="DéficitRB",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demanda_ribera_baja": 1, "suminriberabaja": 1},
)
def deficitrb():
    return demanda_ribera_baja() - suminriberabaja()


@component.add(name="Sup caqui RB", comp_type="Constant", comp_subtype="Normal")
def sup_caqui_rb():
    return 0.02


@component.add(
    name="Distribución mensual",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_distribucion_mensual",
        "__data__": "_ext_data_distribucion_mensual",
        "time": 1,
    },
)
def distribucion_mensual():
    return _ext_data_distribucion_mensual(time())


_ext_data_distribucion_mensual = ExtData(
    "data.xlsx",
    "Distribucion Mensual Cultivos",
    "a",
    "b3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_distribucion_mensual",
)


@component.add(
    name="Distribución mensual RB",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_distribucion_mensual_rb",
        "__data__": "_ext_data_distribucion_mensual_rb",
        "time": 1,
    },
)
def distribucion_mensual_rb():
    return _ext_data_distribucion_mensual_rb(time())


_ext_data_distribucion_mensual_rb = ExtData(
    "data.xlsx",
    "Distribucion Mensual Cultivos",
    "a",
    "c3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_distribucion_mensual_rb",
)


@component.add(
    name="Necesidad Hídrica Cítricos", comp_type="Constant", comp_subtype="Normal"
)
def necesidad_hidrica_citricos():
    return 0.003975


@component.add(
    name="Demanda Total Ribera original",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demanda_ribera_alta": 1, "demanda_ribera_baja": 1},
)
def demanda_total_ribera_original():
    return demanda_ribera_alta() + demanda_ribera_baja()


@component.add(
    name="RIBERA BAJA mod",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demanda_ribera_baja": 1, "sequia_demanda_agricola": 1},
)
def ribera_baja_mod():
    return demanda_ribera_baja() * sequia_demanda_agricola()


@component.add(
    name='"Demanda total neta (anual)"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "demanda_arroz": 1,
        "demanda_caqui": 1,
        "demanda_citricos": 1,
        "demanda_otros_cultivos": 1,
    },
)
def demanda_total_neta_anual():
    return (
        demanda_arroz()
        + demanda_caqui()
        + demanda_citricos()
        + demanda_otros_cultivos()
    )


@component.add(
    name='"Demanda total neta RB (anual)"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "demanda_arroz_rb": 1,
        "demanda_caqui_rb": 1,
        "demanda_citricos_rb": 1,
        "demanda_otros_cultivos_rb": 1,
    },
)
def demanda_total_neta_rb_anual():
    return (
        demanda_arroz_rb()
        + demanda_caqui_rb()
        + demanda_citricos_rb()
        + demanda_otros_cultivos_rb()
    )


@component.add(
    name="Necesidad hídrica arroz", comp_type="Constant", comp_subtype="Normal"
)
def necesidad_hidrica_arroz():
    return 0.00814


@component.add(
    name="Necesidad hídrica caqui", comp_type="Constant", comp_subtype="Normal"
)
def necesidad_hidrica_caqui():
    return 0.004073


@component.add(name="Sup Cítricos RB", comp_type="Constant", comp_subtype="Normal")
def sup_citricos_rb():
    return 3288.48


@component.add(name="Sup Arroz RB", comp_type="Constant", comp_subtype="Normal")
def sup_arroz_rb():
    return 8818.6


@component.add(
    name="RIBERA ALTA mod",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sequia_demanda_agricola": 1, "demanda_ribera_alta": 1},
)
def ribera_alta_mod():
    return sequia_demanda_agricola() * demanda_ribera_alta()


@component.add(
    name="DéficitRA",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demanda_ribera_alta": 1, "suminriberaalta": 1},
)
def deficitra():
    return demanda_ribera_alta() - suminriberaalta()


@component.add(name="SupOtros cultivos RB", comp_type="Constant", comp_subtype="Normal")
def supotros_cultivos_rb():
    return 279.07


@component.add(
    name="SupOtros cultivos RA", units="Ha", comp_type="Constant", comp_subtype="Normal"
)
def supotros_cultivos_ra():
    return 1288.69


@component.add(name="Sup caqui RA", comp_type="Constant", comp_subtype="Normal")
def sup_caqui_ra():
    return 4236.49


@component.add(name="Sup Cítricos RA", comp_type="Constant", comp_subtype="Normal")
def sup_citricos_ra():
    return 13032


@component.add(name="SupArroz RA", comp_type="Constant", comp_subtype="Normal")
def suparroz_ra():
    return 3992.94


@component.add(
    name="N2",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sal_contreras": 1, "filtraciones_contreras": 1},
)
def n2():
    return sal_contreras() + 0.5 * filtraciones_contreras()


@component.add(
    name="Sal Tous",
    units="Hm3/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"reservatous": 1, "aliviadero_tous": 1, "sueltastous": 1},
)
def sal_tous():
    """
    MIN(ReservaTous, IF THEN ELSE( Demanda Total Aguas Abajo Tous - Inflow DS Tous - Total Demanda Urbana >0 , Demanda Total Aguas Abajo Tous - Inflow DS Tous + Aliviadero Tous , SueltasTous + Aliviadero Tous ))
    """
    return np.minimum(reservatous(), sueltastous() + aliviadero_tous())


@component.add(
    name='"Suministro por Júcar-Turia"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sal_tous": 2, "total_demanda_urbana": 2},
)
def suministro_por_jucarturia():
    return if_then_else(
        sal_tous() >= total_demanda_urbana(),
        lambda: total_demanda_urbana(),
        lambda: sal_tous(),
    )


@component.add(
    name="Recurso AA Tous",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "sal_tous": 1,
        "inflow_ds_tous": 1,
        "sequia_reutilizacion": 1,
        "suministro_por_jucarturia": 1,
    },
)
def recurso_aa_tous():
    return (
        sal_tous()
        + inflow_ds_tous()
        + sequia_reutilizacion()
        - suministro_por_jucarturia()
    )


@component.add(
    name="Sumin Sagunto",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "suministro_por_jucarturia": 3,
        "total_demanda_urbana": 1,
        "demanda_sagunto": 3,
        "suminvalencia": 2,
    },
)
def sumin_sagunto():
    return if_then_else(
        suministro_por_jucarturia() >= total_demanda_urbana(),
        lambda: demanda_sagunto(),
        lambda: if_then_else(
            suministro_por_jucarturia() - suminvalencia() >= demanda_sagunto(),
            lambda: demanda_sagunto(),
            lambda: suministro_por_jucarturia() - suminvalencia(),
        ),
    )


@component.add(
    name="SuminValencia",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "suministro_por_jucarturia": 2,
        "total_demanda_urbana": 1,
        "demanda_valencia": 1,
    },
)
def suminvalencia():
    return if_then_else(
        suministro_por_jucarturia() >= total_demanda_urbana(),
        lambda: demanda_valencia(),
        lambda: suministro_por_jucarturia(),
    )


@component.add(
    name="Sumin CJT",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "suministro_por_jucarturia": 3,
        "acuifero_auxiliar": 1,
        "total_demanda_urbana": 1,
        "cjtreal": 3,
        "suminvalencia": 2,
        "sumin_sagunto": 2,
    },
)
def sumin_cjt():
    return if_then_else(
        suministro_por_jucarturia() + acuifero_auxiliar() >= total_demanda_urbana(),
        lambda: cjtreal(),
        lambda: if_then_else(
            suministro_por_jucarturia() - suminvalencia() - sumin_sagunto()
            >= cjtreal(),
            lambda: cjtreal(),
            lambda: suministro_por_jucarturia() - suminvalencia() - sumin_sagunto(),
        ),
    )


@component.add(
    name="Total Storage Historico",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alarcon_historico": 1, "contreras_historico": 1, "tous_historico": 1},
)
def total_storage_historico():
    return alarcon_historico() + contreras_historico() + tous_historico()


@component.add(
    name="Supplied",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "sumin_cjt": 1,
        "sumin_sagunto": 1,
        "suminriberaalta": 1,
        "suminriberabaja": 1,
        "suminvalencia": 1,
    },
)
def supplied():
    return (
        sumin_cjt()
        + sumin_sagunto()
        + suminriberaalta()
        + suminriberabaja()
        + suminvalencia()
    )


@component.add(
    name="Total Recurso Disponible Ribera",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "recurso_aa_tous": 1,
        "suminvalencia": 1,
        "sumin_sagunto": 1,
        "sumin_cjt": 1,
    },
)
def total_recurso_disponible_ribera():
    return recurso_aa_tous() - suminvalencia() - sumin_sagunto() - sumin_cjt()


@component.add(
    name="SueltasCabeceraHistórico",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sueltasjucarhistorico": 1, "sueltascontrerashistorico": 1},
)
def sueltascabecerahistorico():
    return sueltasjucarhistorico() + sueltascontrerashistorico()


@component.add(
    name="SumaSueltascabecera",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sal_contreras": 1, "sal_jucar": 1},
)
def sumasueltascabecera():
    return sal_contreras() + sal_jucar()


@component.add(
    name='"%Alarcón"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alarcon_1": 1, "alarc_cont_tous": 1},
)
def alarcon():
    return (alarcon_1() / alarc_cont_tous()) * 100


@component.add(
    name='"%Contreras"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"contreras_1": 1, "alarc_cont_tous": 1},
)
def contreras():
    return (contreras_1() / alarc_cont_tous()) * 100


@component.add(
    name='"%Tous"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tous_1": 1, "alarc_cont_tous": 1},
)
def tous():
    return (tous_1() / alarc_cont_tous()) * 100


@component.add(
    name='"Alarc + Cont + Tous"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alarcon_1": 1, "contreras_1": 1, "tous_1": 1},
)
def alarc_cont_tous():
    return alarcon_1() + contreras_1() + tous_1()


@component.add(
    name="Volumen esperado Contreras",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"contreras_1": 1, "ent_con": 1, "time_step": 1, "sueltascontreras": 1},
)
def volumen_esperado_contreras():
    return contreras_1() + ent_con() * time_step() - sueltascontreras()


@component.add(
    name="Demanda Total Aguas abajo de Tous original",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_demanda_urbana": 1, "demanda_total_ribera_original": 1},
)
def demanda_total_aguas_abajo_de_tous_original():
    return total_demanda_urbana() + demanda_total_ribera_original()


@component.add(
    name="Déficit",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demanda_total_aguas_abajo_de_tous_original": 1, "recurso_aa_tous": 1},
)
def deficit():
    return np.maximum(
        0, demanda_total_aguas_abajo_de_tous_original() - recurso_aa_tous()
    )


@component.add(
    name="Déficit histórico",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_deficit_historico",
        "__data__": "_ext_data_deficit_historico",
        "time": 1,
    },
)
def deficit_historico():
    return _ext_data_deficit_historico(time())


_ext_data_deficit_historico = ExtData(
    "data.xlsx",
    "Demandas",
    "b",
    "AJ3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_deficit_historico",
)


@component.add(
    name="Mar histórico",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_mar_historico",
        "__data__": "_ext_data_mar_historico",
        "time": 1,
    },
)
def mar_historico():
    return _ext_data_mar_historico(time())


_ext_data_mar_historico = ExtData(
    "data.xlsx",
    "Demandas",
    "b",
    "AK3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_mar_historico",
)


@component.add(
    name="Sea",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"recurso_aa_tous": 1, "demanda_total_aguas_abajo_tous": 1},
)
def sea():
    return np.maximum(0, recurso_aa_tous() - demanda_total_aguas_abajo_tous())


@component.add(
    name="Demanda Total Aguas Abajo Tous",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demanda_total_ribera": 1, "total_demanda_urbana": 1},
)
def demanda_total_aguas_abajo_tous():
    return demanda_total_ribera() + total_demanda_urbana()


@component.add(
    name="Total Demanda Urbana",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demanda_valencia": 1, "demanda_sagunto": 1, "cjtreal": 1},
)
def total_demanda_urbana():
    return demanda_valencia() + demanda_sagunto() + cjtreal()


@component.add(
    name="CJTreal",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alarcon_1": 1, "convenio_alarcon": 1, "cjt": 1},
)
def cjtreal():
    return if_then_else(alarcon_1() > convenio_alarcon(), lambda: cjt(), lambda: 0)


@component.add(
    name="SueltasTousHistórico",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_sueltastoushistorico",
        "__data__": "_ext_data_sueltastoushistorico",
        "time": 1,
    },
)
def sueltastoushistorico():
    return _ext_data_sueltastoushistorico(time())


_ext_data_sueltastoushistorico = ExtData(
    "data.xlsx",
    "Demandas",
    "b",
    "S3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_sueltastoushistorico",
)


@component.add(
    name="SueltasJúcarHistórico",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_sueltasjucarhistorico",
        "__data__": "_ext_data_sueltasjucarhistorico",
        "time": 1,
    },
)
def sueltasjucarhistorico():
    return _ext_data_sueltasjucarhistorico(time())


_ext_data_sueltasjucarhistorico = ExtData(
    "data.xlsx",
    "Demandas",
    "b",
    "AA3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_sueltasjucarhistorico",
)


@component.add(
    name="EntradasAlarcónHistórico",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_entradasalarconhistorico",
        "__data__": "_ext_data_entradasalarconhistorico",
        "time": 1,
    },
)
def entradasalarconhistorico():
    return _ext_data_entradasalarconhistorico(time())


_ext_data_entradasalarconhistorico = ExtData(
    "data.xlsx",
    "Demandas",
    "b",
    "X3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_entradasalarconhistorico",
)


@component.add(
    name="SueltasContrerasHistórico",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_sueltascontrerashistorico",
        "__data__": "_ext_data_sueltascontrerashistorico",
        "time": 1,
    },
)
def sueltascontrerashistorico():
    return _ext_data_sueltascontrerashistorico(time())


_ext_data_sueltascontrerashistorico = ExtData(
    "data.xlsx",
    "Demandas",
    "b",
    "Y3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_sueltascontrerashistorico",
)


@component.add(
    name="EntradasTousHistórico",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_entradastoushistorico",
        "__data__": "_ext_data_entradastoushistorico",
        "time": 1,
    },
)
def entradastoushistorico():
    return _ext_data_entradastoushistorico(time())


_ext_data_entradastoushistorico = ExtData(
    "data.xlsx",
    "Demandas",
    "b",
    "W3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_entradastoushistorico",
)


@component.add(
    name="Tous Histórico",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_tous_historico",
        "__data__": "_ext_data_tous_historico",
        "time": 1,
    },
)
def tous_historico():
    return _ext_data_tous_historico(time())


_ext_data_tous_historico = ExtData(
    "data.xlsx",
    "Demandas",
    "b",
    "V3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_tous_historico",
)


@component.add(
    name="EntradasContrerasHistórico",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_entradascontrerashistorico",
        "__data__": "_ext_data_entradascontrerashistorico",
        "time": 1,
    },
)
def entradascontrerashistorico():
    return _ext_data_entradascontrerashistorico(time())


_ext_data_entradascontrerashistorico = ExtData(
    "data.xlsx",
    "Demandas",
    "b",
    "V3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_entradascontrerashistorico",
)


@component.add(
    name="Alarcón Histórico",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_alarcon_historico",
        "__data__": "_ext_data_alarcon_historico",
        "time": 1,
    },
)
def alarcon_historico():
    """
    De oct 99 a sept 09
    """
    return _ext_data_alarcon_historico(time())


_ext_data_alarcon_historico = ExtData(
    "data.xlsx",
    "Demandas",
    "b",
    "T3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_alarcon_historico",
)


@component.add(
    name="Contreras Histórico",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_contreras_historico",
        "__data__": "_ext_data_contreras_historico",
        "time": 1,
    },
)
def contreras_historico():
    return _ext_data_contreras_historico(time())


_ext_data_contreras_historico = ExtData(
    "data.xlsx",
    "Demandas",
    "b",
    "U3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_contreras_historico",
)


@component.add(
    name="Demanda total Ribera",
    units="Hm3/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "trasvase_jucarvinalopo": 1,
        "ribera_baja_mod": 1,
        "ribera_alta_mod": 1,
    },
)
def demanda_total_ribera():
    return trasvase_jucarvinalopo() + ribera_baja_mod() + ribera_alta_mod()


@component.add(
    name="Déficit Total Ribera",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"deficitjucvinal": 1, "deficitra": 1, "deficitrb": 1},
)
def deficit_total_ribera():
    return np.maximum(0, deficitjucvinal() + deficitra() + deficitrb())


@component.add(
    name="DéficitJucVinal",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"trasvase_jucarvinalopo": 1, "suminjucvinalop": 1},
)
def deficitjucvinal():
    return trasvase_jucarvinalopo() - suminjucvinalop()


@component.add(name="MinimoContreras", comp_type="Constant", comp_subtype="Normal")
def minimocontreras():
    return 15


@component.add(
    name="Aliviadero Contreras",
    units="Hm3/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"volumen_esperado_contreras": 2, "max_contreras": 2, "time_step": 1},
)
def aliviadero_contreras():
    return if_then_else(
        volumen_esperado_contreras() > max_contreras(),
        lambda: (volumen_esperado_contreras() - max_contreras()) / time_step(),
        lambda: 0,
    )


@component.add(
    name='"Alarc+Contr"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alarcon_1": 1, "contreras_1": 1},
)
def alarccontr():
    return alarcon_1() + contreras_1()


@component.add(
    name="Sal Contreras",
    units="Hm3/Month",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reservacontreras": 1,
        "sueltascontreras": 1,
        "aliviadero_contreras": 1,
    },
)
def sal_contreras():
    return np.minimum(reservacontreras(), sueltascontreras() + aliviadero_contreras())


@component.add(
    name="Tous",
    units="Hm3",
    limits=(29.0, 379.0),
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_tous_1": 1},
    other_deps={
        "_integ_tous_1": {
            "initial": {},
            "step": {"ent_tous": 1, "perdidas_t": 1, "sal_tous": 1},
        }
    },
)
def tous_1():
    """
    Para delay 1 mes : DELAY FIXED(Tous, 1, Tous) 44.3
    """
    return _integ_tous_1()


_integ_tous_1 = Integ(
    lambda: ent_tous() - (sal_tous() + perdidas_t()), lambda: 37.11, "_integ_tous_1"
)


@component.add(
    name="ReservaContreras",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "contreras_1": 1,
        "time_step": 1,
        "ent_con": 1,
        "minimocontreras": 1,
        "perdidas_c": 1,
    },
)
def reservacontreras():
    return np.maximum(
        0, contreras_1() / time_step() + ent_con() - minimocontreras() - perdidas_c()
    )


@component.add(
    name="VolEsperadoTous",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "tous_1": 1,
        "perdidas_t": 1,
        "time_step": 1,
        "ent_tous": 1,
        "sueltastous": 1,
    },
)
def volesperadotous():
    """
    max(35, Tous + TIME STEP*(Ent Tous-Pérdidas T) - MIN(SueltasTous , IF THEN ELSE( Demanda Total Aguas Abajo Tous - Inflow DS Tous >0 , Demanda Total Aguas Abajo Tous - Inflow DS Tous , 0)))
    """
    return np.maximum(
        35, tous_1() + time_step() * (ent_tous() - perdidas_t()) - sueltastous()
    )


@component.add(
    name="Convenio Alarcón",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_convenio_alarcon",
        "__data__": "_ext_data_convenio_alarcon",
        "time": 1,
    },
)
def convenio_alarcon():
    return _ext_data_convenio_alarcon(time())


_ext_data_convenio_alarcon = ExtData(
    "data.xlsx",
    "Embalses",
    "b",
    "M3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_convenio_alarcon",
)


@component.add(
    name='"Sal. ATS"',
    units="Hm3/Month",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "alarcon_1": 2,
        "convenio_alarcon": 1,
        "sustitumancha": 1,
        "albacete": 2,
        "minimo_alarcon": 1,
        "time_step": 1,
        "ent_alar": 1,
        "perdidas_a": 1,
    },
)
def sal_ats():
    return np.minimum(
        if_then_else(
            alarcon_1() > convenio_alarcon(),
            lambda: sustitumancha() + albacete(),
            lambda: albacete(),
        ),
        alarcon_1() / time_step() + ent_alar() - perdidas_a() - minimo_alarcon(),
    )


@component.add(
    name="AliviaderosAlarcón",
    units="Hm3/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"volumen_esperado_alarcon": 2, "max_alarcon": 2, "time_step": 1},
)
def aliviaderosalarcon():
    return if_then_else(
        volumen_esperado_alarcon() > max_alarcon(),
        lambda: (volumen_esperado_alarcon() - max_alarcon()) / time_step(),
        lambda: 0,
    )


@component.add(
    name="Volumen esperado Alarcón",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "alarcon_1": 1,
        "time_step": 1,
        "sueltasalarcon": 1,
        "sal_ats": 1,
        "ent_alar": 1,
    },
)
def volumen_esperado_alarcon():
    return alarcon_1() + (ent_alar() - sal_ats() - sueltasalarcon()) * time_step()


@component.add(
    name="Sal Jucar",
    units="Hm3/Month",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"reservaalarcon": 1, "sueltasalarcon": 1, "aliviaderosalarcon": 1},
)
def sal_jucar():
    return np.minimum(reservaalarcon(), sueltasalarcon() + aliviaderosalarcon())


@component.add(
    name='"Trasvase Jucar-Vinalopó"', comp_type="Constant", comp_subtype="Normal"
)
def trasvase_jucarvinalopo():
    return 0


@component.add(
    name="Inflow DS Tous",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_inflow_ds_tous",
        "__data__": "_ext_data_inflow_ds_tous",
        "time": 1,
    },
)
def inflow_ds_tous():
    """
    GET XLS DATA('data.xlsx', 'Aportaciones', 'b' , 'H3' ) 2003-2013 GET XLS DATA('data.xlsx', 'Aportaciones', 'b' , 'Q3' ) 1970-2008 GET XLS DATA('data.xlsx', 'ApoRCP4.5corto', 'b', 'H3') RCP4.5CP GET XLS DATA('data.xlsx', 'ApoRCP8.5corto', 'b', 'H3')
    """
    return _ext_data_inflow_ds_tous(time())


_ext_data_inflow_ds_tous = ExtData(
    "data.xlsx",
    "Aportaciones",
    "b",
    "H3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_inflow_ds_tous",
)


@component.add(
    name="Inflow Alarcón",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_inflow_alarcon",
        "__data__": "_ext_data_inflow_alarcon",
        "time": 1,
    },
)
def inflow_alarcon():
    """
    GET XLS DATA('data.xlsx', 'Aportaciones', 'b' , 'D3') histórico 2003-2013 GET XLS DATA('data.xlsx', 'Aportaciones', 'b' , 'M3' ) histórico 1971-2008 GET XLS DATA('data.xls', 'ApoRCP4.5corto', 'b' , 'D3' ) GET XLS DATA('data.xls', 'ApoRCP8.5corto', 'b' , 'D3' )
    """
    return _ext_data_inflow_alarcon(time())


_ext_data_inflow_alarcon = ExtData(
    "data.xlsx",
    "Aportaciones",
    "b",
    "D3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_inflow_alarcon",
)


@component.add(
    name='"Inflow Alarcón-Molinar"',
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_inflow_alarconmolinar",
        "__data__": "_ext_data_inflow_alarconmolinar",
        "time": 1,
    },
)
def inflow_alarconmolinar():
    """
    GET XLS DATA('data.xlsx', 'Aportaciones', 'b' , 'D3' ) 2003-2013 GET XLS DATA('data.xlsx', 'Aportaciones', 'b' , 'N3' ) 1970-2008 GET XLS DATA('data.xlsx', 'ApoRCP4.5corto', 'b' , 'E3' ) GET XLS DATA('data.xlsx', 'ApoRCP8.5corto', 'b' , 'E3' )
    """
    return _ext_data_inflow_alarconmolinar(time())


_ext_data_inflow_alarconmolinar = ExtData(
    "data.xlsx",
    "Aportaciones",
    "b",
    "D3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_inflow_alarconmolinar",
)


@component.add(
    name="Inflow Contreras",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_inflow_contreras",
        "__data__": "_ext_data_inflow_contreras",
        "time": 1,
    },
)
def inflow_contreras():
    """
    GET XLS DATA('data.xlsx', 'Aportaciones', 'b' , 'F3' ) 2003-2013 GET XLS DATA('data.xlsx', 'Aportaciones', 'b' , 'O3' ) 1970-2008 GET XLS DATA('data.xlsx', 'ApoRCP4.5corto', 'b' , 'F3') GET XLS DATA('data.xlsx', 'ApoRCP8.5corto', 'b' , 'F3')
    """
    return _ext_data_inflow_contreras(time())


_ext_data_inflow_contreras = ExtData(
    "data.xlsx",
    "Aportaciones",
    "b",
    "F3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_inflow_contreras",
)


@component.add(
    name="Inflow Tous",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_inflow_tous",
        "__data__": "_ext_data_inflow_tous",
        "time": 1,
    },
)
def inflow_tous():
    """
    GET XLS DATA('data.xlsx', 'Aportaciones', 'b' , 'G3' ) 2003-2013 GET XLS DATA('data.xlsx', 'Aportaciones', 'b' , 'P3' ) 1970-2008 GET XLS DATA('data.xlsx', 'ApoRCP4.5corto', 'b' , 'G3') RCP4.5CP GET XLS DATA('data.xlsx', 'ApoRCP8.5corto', 'b' , 'G3')
    """
    return _ext_data_inflow_tous(time())


_ext_data_inflow_tous = ExtData(
    "data.xlsx",
    "Aportaciones",
    "b",
    "G3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_inflow_tous",
)


@component.add(
    name="ContrerasTEvapo",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_contrerastevapo",
        "__data__": "_ext_data_contrerastevapo",
        "time": 1,
    },
)
def contrerastevapo():
    return _ext_data_contrerastevapo(time())


_ext_data_contrerastevapo = ExtData(
    "data.xlsx",
    "Evapotrans",
    "b",
    "D3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_contrerastevapo",
)


@component.add(
    name="Máx Contreras",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"perdidas_c": 1},
)
def max_contreras():
    return 463 + perdidas_c()


@component.add(
    name="Pérdidas A",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alarconevapo": 1},
)
def perdidas_a():
    return alarconevapo()


@component.add(
    name="Pérdidas C",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"contrerasevapo": 1, "filtraciones_contreras": 1},
)
def perdidas_c():
    return contrerasevapo() + filtraciones_contreras()


@component.add(
    name="TousEvapo",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"superficie_tous": 1, "toustevapo": 1},
)
def tousevapo():
    return superficie_tous() * toustevapo() * 10000


@component.add(
    name="Embalses mes",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alarcon_1": 1, "contreras_1": 1, "tous_1": 1},
)
def embalses_mes():
    return alarcon_1() + contreras_1() + tous_1()


@component.add(
    name="AlarconTEvapo",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_alarcontevapo",
        "__data__": "_ext_data_alarcontevapo",
        "time": 1,
    },
)
def alarcontevapo():
    return _ext_data_alarcontevapo(time())


_ext_data_alarcontevapo = ExtData(
    "data.xlsx",
    "Evapotrans",
    "b",
    "C3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_alarcontevapo",
)


@component.add(
    name="TousTEvapo",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_toustevapo",
        "__data__": "_ext_data_toustevapo",
        "time": 1,
    },
)
def toustevapo():
    return _ext_data_toustevapo(time())


_ext_data_toustevapo = ExtData(
    "data.xlsx",
    "Evapotrans",
    "b",
    "E3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_toustevapo",
)


@component.add(
    name="AlarcónEvapo",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alarcontevapo": 1, "superficie_alarcon": 1},
)
def alarconevapo():
    return alarcontevapo() * superficie_alarcon() * 10000


@component.add(
    name="ReservaTous",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "tous_1": 1,
        "time_step": 1,
        "ent_tous": 1,
        "perdidas_t": 1,
        "minimotous": 1,
    },
)
def reservatous():
    return np.maximum(
        0, tous_1() / time_step() + ent_tous() - perdidas_t() - minimotous()
    )


@component.add(
    name="Superficie Alarcón",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alarcon_1": 1},
)
def superficie_alarcon():
    return 0 + 54.9594 * alarcon_1() ** 0.680283


@component.add(
    name="Superficie Contreras",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"contreras_1": 1},
)
def superficie_contreras():
    return 0 + 31.8494 * contreras_1() ** 0.651389


@component.add(
    name="Pérdidas Tous",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tousevapo": 1, "filtraciones_tous": 1},
)
def perdidas_tous():
    return tousevapo() + filtraciones_tous()


@component.add(
    name="Filtraciones Tous",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tous_1": 1},
)
def filtraciones_tous():
    """
    a = 0 b = 0.065 c = 0.8
    """
    return 0 + 0.065 * tous_1() ** 0.8


@component.add(
    name="ContrerasEvapo",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"contrerastevapo": 1, "superficie_contreras": 1},
)
def contrerasevapo():
    return contrerastevapo() * superficie_contreras() * 10000


@component.add(
    name="Filtraciones Contreras",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"contreras_1": 1},
)
def filtraciones_contreras():
    """
    a = 3 b = 8E-5 c = 1.95
    """
    return 3 + 8e-05 * contreras_1() ** 1.95


@component.add(
    name="Superficie Tous",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tous_1": 1},
)
def superficie_tous():
    return 0 + 19.1324 * tous_1() ** 0.666315


@component.add(
    name="Demanda Sagunto",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "sequia_demanda_urbana": 1,
        "sagunto": 1,
        "usuarios_sagunto": 1,
        "usuariosinicialess": 1,
    },
)
def demanda_sagunto():
    return (
        sequia_demanda_urbana() * sagunto() * usuarios_sagunto() / usuariosinicialess()
    )


@component.add(
    name="Demanda Valencia",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "sequia_demanda_urbana": 1,
        "valencia": 1,
        "usuariosvalencia": 1,
        "usuariosinicialesv": 1,
    },
)
def demanda_valencia():
    return (
        sequia_demanda_urbana() * valencia() * usuariosvalencia() / usuariosinicialesv()
    )


@component.add(
    name="SuminRiberaBaja",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_recurso_disponible_ribera": 2,
        "demanda_total_ribera": 1,
        "sequia_bombeos_adicionales": 3,
        "ribera_baja_mod": 2,
        "pesorbb": 1,
    },
)
def suminriberabaja():
    return if_then_else(
        total_recurso_disponible_ribera() >= demanda_total_ribera(),
        lambda: ribera_baja_mod() + sequia_bombeos_adicionales(),
        lambda: np.minimum(
            pesorbb() * total_recurso_disponible_ribera()
            + sequia_bombeos_adicionales(),
            ribera_baja_mod() + sequia_bombeos_adicionales(),
        ),
    )


@component.add(
    name="SuminRiberaalta",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_recurso_disponible_ribera": 2,
        "demanda_total_ribera": 1,
        "sequia_bombeos_adicionales": 3,
        "ribera_alta_mod": 2,
        "pesoraa": 2,
    },
)
def suminriberaalta():
    """
    Para marcar la prioridad de Valencia y Sagunto debería restar al total recurso disponible aguas abajo de Tous el agua ya suministrada a Valencia y Sagunto
    """
    return if_then_else(
        total_recurso_disponible_ribera() >= demanda_total_ribera(),
        lambda: ribera_alta_mod() * pesoraa() + sequia_bombeos_adicionales(),
        lambda: np.minimum(
            pesoraa() * total_recurso_disponible_ribera()
            + sequia_bombeos_adicionales(),
            ribera_alta_mod() + sequia_bombeos_adicionales(),
        ),
    )


@component.add(
    name="Sequía extrema",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"deficit_urbano_1_delay": 1, "time": 1, "reservatous": 1},
)
def sequia_extrema():
    return if_then_else(
        np.logical_and(deficit_urbano_1_delay() > 0, time() > 1),
        lambda: 0,
        lambda: reservatous(),
    )


@component.add(
    name="N1",
    units="Hm3/Month",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"inflow_alarconmolinar": 1, "sal_jucar": 1},
)
def n1():
    return inflow_alarconmolinar() + sal_jucar()


@component.add(
    name="Ent Con",
    units="Hm3/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"inflow_contreras": 1},
)
def ent_con():
    return inflow_contreras()


@component.add(
    name='"Déf.Mancha"',
    units="Hm3/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "sustitumancha": 1,
        "defalbacete": 1,
        "senal_de_estado": 1,
        "sal_ats": 1,
        "albacete": 1,
    },
)
def defmancha():
    return np.maximum(
        0,
        sustitumancha()
        - (
            sal_ats()
            - (
                albacete()
                * if_then_else(senal_de_estado() == 0.5, lambda: 0.7, lambda: 1)
                - defalbacete()
            )
        ),
    )


@component.add(
    name="Ent Tous",
    units="Hm3/Month",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"inflow_tous": 1, "caudal_tous": 1, "n2": 1},
)
def ent_tous():
    return inflow_tous() + caudal_tous() + n2()


@component.add(
    name="Déficit urbano",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"deficit_sagunto": 1, "deficit_valencia": 1},
)
def deficit_urbano():
    return deficit_sagunto() + deficit_valencia()


@component.add(
    name="Ent Alar",
    units="Hm3/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"inflow_alarcon": 1},
)
def ent_alar():
    return inflow_alarcon()


@component.add(
    name="Déficit urbano 1 delay",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_deficit_urbano_1_delay": 1},
    other_deps={
        "_delayfixed_deficit_urbano_1_delay": {
            "initial": {},
            "step": {"deficit_urbano": 1},
        }
    },
)
def deficit_urbano_1_delay():
    return _delayfixed_deficit_urbano_1_delay()


_delayfixed_deficit_urbano_1_delay = DelayFixed(
    lambda: deficit_urbano(),
    lambda: 1,
    lambda: 1,
    time_step,
    "_delayfixed_deficit_urbano_1_delay",
)


@component.add(
    name="PesoRAA",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ribera_alta_mod": 1, "demanda_total_ribera": 1},
)
def pesoraa():
    return ribera_alta_mod() / demanda_total_ribera()


@component.add(
    name="PesoRBB",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ribera_baja_mod": 1, "demanda_total_ribera": 1},
)
def pesorbb():
    return ribera_baja_mod() / demanda_total_ribera()


@component.add(
    name="DemandaRA",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ribera_alta_mod": 1, "ribera_baja_mod": 1},
)
def demandara():
    return ribera_alta_mod() + ribera_baja_mod()


@component.add(
    name="Sequía bombeos adicionales",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"senal_de_estado": 2},
)
def sequia_bombeos_adicionales():
    """
    Son bombeos máximos mensuales, teniendo en cuenta que le máximo anual es el valore de 48 y 98 en el sistema Júcar. Se colocaría como shadow variable de apoyo a las demandas urbanas de Valencia y sagunto (View 3). Para desactivar cambiar 1.5 por 0
    """
    return if_then_else(
        senal_de_estado() >= 1.5,
        lambda: 0,
        lambda: if_then_else(senal_de_estado() > 0.5, lambda: 48 / 12, lambda: 98 / 12),
    )


@component.add(
    name="Sequía demanda agrícola",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"senal_de_estado": 2},
)
def sequia_demanda_agricola():
    """
    Para desactivar cambiar 1.5 por 0
    """
    return if_then_else(
        senal_de_estado() >= 1.5,
        lambda: 1,
        lambda: if_then_else(senal_de_estado() > 0.5, lambda: 0.8, lambda: 0.6),
    )


@component.add(
    name='"Déf.Albacete"',
    units="Hm3/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"albacete": 1, "senal_de_estado": 1, "sal_ats": 1},
)
def defalbacete():
    return np.maximum(
        0,
        albacete() * if_then_else(senal_de_estado() == 0.5, lambda: 0.7, lambda: 1)
        - sal_ats(),
    )


@component.add(
    name="Sequía demanda urbana",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"senal_de_estado": 1},
)
def sequia_demanda_urbana():
    """
    Para desactivar cambiar 1.8 por 0
    """
    return if_then_else(senal_de_estado() < 1.8, lambda: 0.95, lambda: 1)


@component.add(
    name="Sequía reutilización",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"senal_de_estado": 2},
)
def sequia_reutilizacion():
    """
    Valores son Hm³/año por eso divido entre 12 La colocamos como shadow variable aguas abajo de Tous en la salida a la Ribera Para desactivar cambiar 1.5 por 0
    """
    return if_then_else(
        senal_de_estado() >= 1.5,
        lambda: 0,
        lambda: if_then_else(
            senal_de_estado() > 0.5, lambda: 1.2 / 12, lambda: 13.5 / 12
        ),
    )


@component.add(
    name='"Total Demanda Alba-Mancha"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sustitumancha": 1, "senal_de_estado": 1, "albacete": 1},
)
def total_demanda_albamancha():
    return sustitumancha() + albacete() * if_then_else(
        senal_de_estado() == 0.5, lambda: 0.7, lambda: 1
    )


@component.add(
    name="EmbalsesMáx",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alarconmax": 1, "contrerasmax": 1, "tousmax": 1},
)
def embalsesmax():
    return alarconmax() + contrerasmax() + tousmax()


@component.add(
    name="EmbalsesMed",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alarconmed": 1, "contrerasmed": 1, "tousmed": 1},
)
def embalsesmed():
    return alarconmed() + contrerasmed() + tousmed()


@component.add(
    name="EmbalsesMín",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alarconmin": 1, "contrerasmin": 1, "tousmin": 1},
)
def embalsesmin():
    return alarconmin() + contrerasmin() + tousmin()


@component.add(
    name="TousMax",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_tousmax",
        "__data__": "_ext_data_tousmax",
        "time": 1,
    },
)
def tousmax():
    return _ext_data_tousmax(time())


_ext_data_tousmax = ExtData(
    "data.xlsx",
    "Embalses",
    "b",
    "J3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_tousmax",
)


@component.add(
    name="TousMed",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_tousmed",
        "__data__": "_ext_data_tousmed",
        "time": 1,
    },
)
def tousmed():
    return _ext_data_tousmed(time())


_ext_data_tousmed = ExtData(
    "data.xlsx",
    "Embalses",
    "b",
    "K3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_tousmed",
)


@component.add(
    name="TousMin",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_tousmin",
        "__data__": "_ext_data_tousmin",
        "time": 1,
    },
)
def tousmin():
    return _ext_data_tousmin(time())


_ext_data_tousmin = ExtData(
    "data.xlsx",
    "Embalses",
    "b",
    "L3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_tousmin",
)


@component.add(
    name="AlarconMax",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_alarconmax",
        "__data__": "_ext_data_alarconmax",
        "time": 1,
    },
)
def alarconmax():
    return _ext_data_alarconmax(time())


_ext_data_alarconmax = ExtData(
    "data.xlsx",
    "Embalses",
    "b",
    "D3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_alarconmax",
)


@component.add(
    name="AlarconMed",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_alarconmed",
        "__data__": "_ext_data_alarconmed",
        "time": 1,
    },
)
def alarconmed():
    return _ext_data_alarconmed(time())


_ext_data_alarconmed = ExtData(
    "data.xlsx",
    "Embalses",
    "b",
    "E3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_alarconmed",
)


@component.add(
    name="AlarconMin",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_alarconmin",
        "__data__": "_ext_data_alarconmin",
        "time": 1,
    },
)
def alarconmin():
    return _ext_data_alarconmin(time())


_ext_data_alarconmin = ExtData(
    "data.xlsx",
    "Embalses",
    "b",
    "F3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_alarconmin",
)


@component.add(
    name="ContrerasMin",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_contrerasmin",
        "__data__": "_ext_data_contrerasmin",
        "time": 1,
    },
)
def contrerasmin():
    return _ext_data_contrerasmin(time())


_ext_data_contrerasmin = ExtData(
    "data.xlsx",
    "Embalses",
    "b",
    "I3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_contrerasmin",
)


@component.add(
    name="ContrerasMed",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_contrerasmed",
        "__data__": "_ext_data_contrerasmed",
        "time": 1,
    },
)
def contrerasmed():
    return _ext_data_contrerasmed(time())


_ext_data_contrerasmed = ExtData(
    "data.xlsx",
    "Embalses",
    "b",
    "H3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_contrerasmed",
)


@component.add(
    name="Indice de estado",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "embalses_mes": 3,
        "embalsesmed": 4,
        "embalsesmax": 1,
        "embalsesmin": 2,
    },
)
def indice_de_estado():
    """
    Ie > 0.5 Normalidad 0.3 < Ie < 0.5 Prealerta 0.15 < Ie < 0.3 Alerta Ie < 0.15 Emergencia
    """
    return if_then_else(
        embalses_mes() >= embalsesmed(),
        lambda: 0.5
        * (1 + (embalses_mes() - embalsesmed()) / (embalsesmax() - embalsesmed())),
        lambda: np.maximum(
            0, (embalses_mes() - embalsesmin()) / (2 * (embalsesmed() - embalsesmin()))
        ),
    )


@component.add(
    name="Señal de estado",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"indice_de_estado": 3},
)
def senal_de_estado():
    """
    2 Normalidad; 1.5 Prealerta; 1 Alerta; 0.5 Emergencia Para desactivar medidas de actuación para sequía, sustituye 0.5 por -9
    """
    return if_then_else(
        indice_de_estado() >= 0.5,
        lambda: 2,
        lambda: if_then_else(
            indice_de_estado() >= 0.3,
            lambda: 1.5,
            lambda: if_then_else(indice_de_estado() >= 0.15, lambda: 1, lambda: 0.5),
        ),
    )


@component.add(
    name="ContrerasMax",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_contrerasmax",
        "__data__": "_ext_data_contrerasmax",
        "time": 1,
    },
)
def contrerasmax():
    return _ext_data_contrerasmax(time())


_ext_data_contrerasmax = ExtData(
    "data.xlsx",
    "Embalses",
    "b",
    "G3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_contrerasmax",
)


@component.add(
    name="Descarga 2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alfa_2": 3, "acuifero_mo_2": 1, "time_step": 2, "recarga_neta_2": 1},
)
def descarga_2():
    return alfa_2() * acuifero_mo_2() * np.exp(
        -alfa_2() * time_step()
    ) + recarga_neta_2() * (1 - np.exp(-alfa_2() * time_step()))


@component.add(
    name="Descarga",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alfa": 3, "acuifero_mo": 1, "time_step": 2, "recarga_neta": 1},
)
def descarga():
    return alfa() * acuifero_mo() * np.exp(-alfa() * time_step()) + recarga_neta() * (
        1 - np.exp(-alfa() * time_step())
    )


@component.add(
    name="Caudal Tous",
    units="Hm3/Month",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n1": 1, "aquifer_infiltration": 1},
)
def caudal_tous():
    return n1() + aquifer_infiltration()


@component.add(name="Alfa 2", comp_type="Constant", comp_subtype="Normal")
def alfa_2():
    return 0.4


@component.add(name='"Activar/Desactivar"', comp_type="Constant", comp_subtype="Normal")
def activardesactivar():
    """
    Activado = 1 Desactivado = 0
    """
    return 0


@component.add(name="Coef de reparto 2", comp_type="Constant", comp_subtype="Normal")
def coef_de_reparto_2():
    return 0.2


@component.add(
    name="Entradas 2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"recarga_neta_2": 1},
)
def entradas_2():
    return recarga_neta_2()


@component.add(
    name="Acuífero MO 2",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_acuifero_mo_2": 1},
    other_deps={
        "_integ_acuifero_mo_2": {
            "initial": {},
            "step": {"entradas_2": 1, "salidas_2": 1},
        }
    },
)
def acuifero_mo_2():
    return _integ_acuifero_mo_2()


_integ_acuifero_mo_2 = Integ(
    lambda: entradas_2() - salidas_2(), lambda: -3.5, "_integ_acuifero_mo_2"
)


@component.add(
    name="Recarga Neta",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"coef_de_reparto": 1, "mancha_oriental": 1},
)
def recarga_neta():
    return -coef_de_reparto() * mancha_oriental()


@component.add(
    name="Recarga Neta 2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"coef_de_reparto_2": 1, "mancha_oriental": 1},
)
def recarga_neta_2():
    return -coef_de_reparto_2() * mancha_oriental()


@component.add(
    name="Descarga teórica total",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"descarga": 1, "descarga_2": 1},
)
def descarga_teorica_total():
    return descarga() + descarga_2()


@component.add(name="Coef de reparto", comp_type="Constant", comp_subtype="Normal")
def coef_de_reparto():
    return 0.8


@component.add(
    name="Aquifer infiltration",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n1": 1, "descarga_teorica_total": 1},
)
def aquifer_infiltration():
    """
    max(-N1 , Descarga teórica total)
    """
    return np.maximum(-n1(), descarga_teorica_total())


@component.add(
    name="VariationS",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"usuarios_sagunto": 1, "variation_rate": 1, "activardesactivar": 1},
)
def variations():
    return usuarios_sagunto() * variation_rate() * activardesactivar()


@component.add(
    name="Salidas 2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"descarga_2": 1},
)
def salidas_2():
    return descarga_2()


@component.add(
    name="Salidas",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"descarga": 1},
)
def salidas():
    return descarga()


@component.add(
    name="VariationV",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"variation_rate": 1, "usuariosvalencia": 1, "activardesactivar": 1},
)
def variationv():
    return variation_rate() * usuariosvalencia() * activardesactivar()


@component.add(
    name="Acuífero Auxiliar",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "sal_tous": 2,
        "total_demanda_urbana": 1,
        "sumsubt": 2,
        "cjt": 1,
        "suminvalencia": 1,
        "sumin_sagunto": 1,
    },
)
def acuifero_auxiliar():
    return if_then_else(
        sal_tous() >= total_demanda_urbana() - sumsubt(),
        lambda: sumsubt(),
        lambda: np.minimum(
            10, cjt() - (sal_tous() - suminvalencia() - sumin_sagunto())
        ),
    )


@component.add(
    name="Déficit Sagunto",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demanda_sagunto": 1, "sumin_sagunto": 1},
)
def deficit_sagunto():
    return demanda_sagunto() - sumin_sagunto()


@component.add(
    name="Déficit Valencia",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demanda_valencia": 1, "suminvalencia": 1},
)
def deficit_valencia():
    return demanda_valencia() - suminvalencia()


@component.add(
    name="UsuariosValencia",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_usuariosvalencia": 1},
    other_deps={
        "_integ_usuariosvalencia": {
            "initial": {"usuariosinicialesv": 1},
            "step": {"variationv": 1},
        }
    },
)
def usuariosvalencia():
    return _integ_usuariosvalencia()


_integ_usuariosvalencia = Integ(
    lambda: -variationv(), lambda: usuariosinicialesv(), "_integ_usuariosvalencia"
)


@component.add(name="Variation Rate", comp_type="Constant", comp_subtype="Normal")
def variation_rate():
    return 0.00018728


@component.add(
    name="Usuarios Sagunto",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_usuarios_sagunto": 1},
    other_deps={
        "_integ_usuarios_sagunto": {
            "initial": {"usuariosinicialess": 1},
            "step": {"variations": 1},
        }
    },
)
def usuarios_sagunto():
    return _integ_usuarios_sagunto()


_integ_usuarios_sagunto = Integ(
    lambda: -variations(), lambda: usuariosinicialess(), "_integ_usuarios_sagunto"
)


@component.add(
    name="SuminJucVinalop",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_recurso_disponible_ribera": 2,
        "demanda_total_ribera": 1,
        "trasvase_jucarvinalopo": 2,
        "pesojvina": 1,
    },
)
def suminjucvinalop():
    return if_then_else(
        total_recurso_disponible_ribera() >= demanda_total_ribera(),
        lambda: trasvase_jucarvinalopo(),
        lambda: np.minimum(
            pesojvina() * total_recurso_disponible_ribera(), trasvase_jucarvinalopo()
        ),
    )


@component.add(name="UsuariosinicialesV", comp_type="Constant", comp_subtype="Normal")
def usuariosinicialesv():
    return 1272460.0


@component.add(
    name="PesoJVina",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"trasvase_jucarvinalopo": 1, "demanda_total_ribera": 1},
)
def pesojvina():
    return trasvase_jucarvinalopo() / demanda_total_ribera()


@component.add(name="UsuariosinicialesS", comp_type="Constant", comp_subtype="Normal")
def usuariosinicialess():
    return 106204


@component.add(
    name="ReservaAlarcón",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "alarcon_1": 1,
        "time_step": 1,
        "ent_alar": 1,
        "perdidas_a": 1,
        "sal_ats": 1,
        "minimo_alarcon": 1,
    },
)
def reservaalarcon():
    return np.maximum(
        0,
        alarcon_1() / time_step()
        + ent_alar()
        - perdidas_a()
        - sal_ats()
        - minimo_alarcon(),
    )


@component.add(
    name="Máx Alarcón",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"perdidas_a": 1},
)
def max_alarcon():
    return 1112 + perdidas_a()


@component.add(
    name="Alarcón",
    units="Hm3",
    limits=(0.0, 1112.5),
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_alarcon_1": 1},
    other_deps={
        "_integ_alarcon_1": {
            "initial": {},
            "step": {"ent_alar": 1, "perdidas_a": 1, "sal_jucar": 1, "sal_ats": 1},
        }
    },
)
def alarcon_1():
    return _integ_alarcon_1()


_integ_alarcon_1 = Integ(
    lambda: ent_alar() - perdidas_a() - sal_jucar() - sal_ats(),
    lambda: 262.21,
    "_integ_alarcon_1",
)


@component.add(
    name="Contreras",
    units="Hm3",
    limits=(14.95, 464.0),
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_contreras_1": 1},
    other_deps={
        "_integ_contreras_1": {
            "initial": {},
            "step": {"ent_con": 1, "perdidas_c": 1, "sal_contreras": 1},
        }
    },
)
def contreras_1():
    return _integ_contreras_1()


_integ_contreras_1 = Integ(
    lambda: ent_con() - perdidas_c() - sal_contreras(),
    lambda: 119.12,
    "_integ_contreras_1",
)


@component.add(
    name="Pérdidas T",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"perdidas_tous": 1},
)
def perdidas_t():
    return perdidas_tous()


@component.add(
    name="Acuífero MO",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_acuifero_mo": 1},
    other_deps={
        "_integ_acuifero_mo": {"initial": {}, "step": {"entradas": 1, "salidas": 1}}
    },
)
def acuifero_mo():
    return _integ_acuifero_mo()


_integ_acuifero_mo = Integ(
    lambda: entradas() - salidas(), lambda: -3500, "_integ_acuifero_mo"
)


@component.add(name="Alfa", comp_type="Constant", comp_subtype="Normal")
def alfa():
    """
    0.0035 original, tomaba demasiada agua, no quedaba en el río
    """
    return 0.0025


@component.add(
    name="Entradas",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"recarga_neta": 1},
)
def entradas():
    return recarga_neta()


@component.add(name="Mínimo Alarcón", comp_type="Constant", comp_subtype="Normal")
def minimo_alarcon():
    return 30


@component.add(
    name="Aliviadero Tous",
    units="Hm3/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"volesperadotous": 2, "max_tous": 2, "time_step": 1},
)
def aliviadero_tous():
    return if_then_else(
        volesperadotous() > max_tous(),
        lambda: np.maximum(0, (volesperadotous() - max_tous()) / time_step()),
        lambda: 0,
    )


@component.add(name="MinimoTous", comp_type="Constant", comp_subtype="Normal")
def minimotous():
    return 35


@component.add(
    name="SumSubt",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_sumsubt",
        "__data__": "_ext_data_sumsubt",
        "time": 1,
    },
)
def sumsubt():
    return _ext_data_sumsubt(time())


_ext_data_sumsubt = ExtData(
    "data.xlsx",
    "Demandas",
    "b",
    "O3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_sumsubt",
)


@component.add(
    name="SustituMancha",
    units="Hm3/Month",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_sustitumancha",
        "__data__": "_ext_data_sustitumancha",
        "time": 1,
    },
)
def sustitumancha():
    return _ext_data_sustitumancha(time())


_ext_data_sustitumancha = ExtData(
    "data.xlsx",
    "Demandas",
    "b",
    "E3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_sustitumancha",
)


@component.add(
    name="Albacete",
    units="Hm3/Month",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_albacete",
        "__data__": "_ext_data_albacete",
        "time": 1,
    },
)
def albacete():
    """
    el abastecimiento a esta demanda se verá sufragado por recursos subterráneos en un 30% en situación de emergencia
    """
    return _ext_data_albacete(time())


_ext_data_albacete = ExtData(
    "data.xlsx",
    "Demandas",
    "b",
    "D3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_albacete",
)


@component.add(
    name='"Suma Déficits Alba-Mancha"',
    units="Hm3/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"defmancha": 1, "defalbacete": 1},
)
def suma_deficits_albamancha():
    return defmancha() + defalbacete()


@component.add(
    name="Máx Tous",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_max_tous",
        "__data__": "_ext_data_max_tous",
        "time": 1,
    },
)
def max_tous():
    """
    El máximo está adelantado un mes para que no se supere el Vol Máximo a inicios del mes siguiente. Si el maximo de septiembre es 195 Hm3, queremos que en agosto se produzcan las sueltas que garanticen que a inicios de septiembre no tendremos más de 195 Hm3 (ejemplo)
    """
    return _ext_data_max_tous(time())


_ext_data_max_tous = ExtData(
    "data.xlsx",
    "Embalses",
    "b",
    "C3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_max_tous",
)


@component.add(
    name="Sagunto",
    units="Hm3/Month",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_sagunto",
        "__data__": "_ext_data_sagunto",
        "time": 1,
    },
)
def sagunto():
    return _ext_data_sagunto(time())


_ext_data_sagunto = ExtData(
    "data.xlsx",
    "Demandas",
    "b",
    "H3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_sagunto",
)


@component.add(
    name="CJT",
    units="Hm3/Month",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_cjt",
        "__data__": "_ext_data_cjt",
        "time": 1,
    },
)
def cjt():
    """
    NOT REALLY UNA DEMANDA URBANA Canal Jucar Turia
    """
    return _ext_data_cjt(time())


_ext_data_cjt = ExtData(
    "data.xlsx", "Demandas", "b", "I3", "interpolate", {}, _root, {}, "_ext_data_cjt"
)


@component.add(
    name="Déficit CJT",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cjt": 1, "sumin_cjt": 1},
)
def deficit_cjt():
    return np.maximum(0, cjt() - sumin_cjt())


@component.add(
    name="Déficit Total Ribera Comprobación",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demanda_total_ribera": 1, "total_recurso_disponible_ribera": 1},
)
def deficit_total_ribera_comprobacion():
    return np.maximum(0, demanda_total_ribera() - total_recurso_disponible_ribera())


@component.add(
    name="Valencia",
    units="Hm3/Month",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_valencia",
        "__data__": "_ext_data_valencia",
        "time": 1,
    },
)
def valencia():
    return _ext_data_valencia(time())


_ext_data_valencia = ExtData(
    "data.xlsx",
    "Demandas",
    "b",
    "G3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_valencia",
)


@component.add(
    name="Mancha Oriental",
    units="Hm3/Month",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_mancha_oriental",
        "__data__": "_ext_data_mancha_oriental",
        "time": 1,
    },
)
def mancha_oriental():
    """
    Zona albacete
    """
    return _ext_data_mancha_oriental(time())


_ext_data_mancha_oriental = ExtData(
    "data.xlsx",
    "Demandas",
    "b",
    "F3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_mancha_oriental",
)


@component.add(
    name="QEcolAlar",
    units="Hm3/Month",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_qecolalar",
        "__data__": "_ext_data_qecolalar",
        "time": 1,
    },
)
def qecolalar():
    return _ext_data_qecolalar(time())


_ext_data_qecolalar = ExtData(
    "data.xlsx",
    "Demandas",
    "b",
    "C3",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_qecolalar",
)
