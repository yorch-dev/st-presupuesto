# @title Función inversión a plazo
def inversion_a_plazo(monto_invertido, fecha_inicial, dias, t_int = 0.007, capitalizacion = 0.5, plazo = 5):
    """
    Calcula resultado de inversión
    Args
        monto_invertido int : monto inicial invertido
        fecha_inicial date : fecha de la inversión
        dias int : duración en días del ciclo del depósito
        t_int float : tasa de interés (aplica cada 30 días), 0.007 default
        capitalizacion float : porcentaje de rescate sobre los intereses generados en el período, 0.5 default
        plazo int o float : plazo en años, 5 default
    Return
        df_proyectado
    """

    import numpy as np
    import pandas as pd
    import math
    import datetime as dt
    from datetime import timedelta
    from dateutil.relativedelta import relativedelta

    fecha_ingreso = np.array([], dtype='datetime64[D]')
    fecha_rescate = np.array([], dtype='datetime64[D]')
    inversion = np.array([], dtype='int32')
    ganancia_periodo = np.array([], dtype='int32')
    monto_reinversion = np.array([], dtype='int32')
    monto_rescate = np.array([], dtype='int32')
    
    inversion_periodo = monto_invertido
    fecha_inversion = fecha_inicial
    fin_periodo = fecha_inversion + timedelta(dias)
    meses = int(plazo * 12)
    fecha_final = fecha_inicial + relativedelta(months=+meses)


    while fecha_final >= fin_periodo:
        #Revisión de fechas
        fecha_ingreso = np.append(fecha_ingreso, fecha_inversion)
        fecha_rescate = np.append(fecha_rescate, fin_periodo)
        fecha_inversion = fin_periodo + dt.timedelta(1)
        fin_periodo = fecha_inversion + dt.timedelta(dias)

        #Revisión de montos
        inversion = np.append(inversion, round(inversion_periodo))
        ganancia = round((inversion_periodo * t_int) * (dias / 30))
        ganancia_periodo = np.append(ganancia_periodo, ganancia)
        reinversion = math.ceil((1 - capitalizacion) * ganancia)
        monto_reinversion = np.append(monto_reinversion, reinversion)
        inversion_periodo += reinversion
        monto_rescate = np.append(monto_rescate ,ganancia - reinversion)
    
    datos = {
        'Fecha ingreso' :fecha_ingreso,
        'Fecha rescate' :fecha_rescate,
        'Inversión' : inversion,
        'Ganancia' : ganancia_periodo,
        'Reinversión' : monto_reinversion,
        'Rescate' : monto_rescate
    }
    
    return pd.DataFrame(datos)