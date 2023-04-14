def presupuesto_cuotas(valor_producto, t_vida, fecha_inicio, t_int = 0.01):
    """
    Calcula valor cuota/ahorro y monto ahorrado al fin del período
    Args = valor_producto int,
           t_vida años int o float,
           fecha_inicio date,
           t_int tasa_interes float (valor por defecto 0.01)
    Return = lista zip (fecha, valor_cuota)
    """

    import numpy as np
    import pandas as pd
    import math
    from dateutil.relativedelta import relativedelta as rd

    fechas = np.array([], dtype='datetime64[D]')
    n_cuotas = np.array([], dtype='str')
    cuotas = np.array([], dtype='int32')
    meses = math.floor(t_vida * 12)
    cuota_anterior = math.ceil(valor_producto / meses)
    fecha_anterior = fecha_inicio

    for i in range(meses):
        fechas = np.append(fechas, fecha_anterior)
        n_cuotas = np.append(n_cuotas, str(i + 1) + " de " + str(meses))
        fecha_anterior = fecha_anterior + rd(months=+1)
        cuota_periodo = math.ceil(cuota_anterior * (1 + t_int))
        cuotas = np.append(cuotas, cuota_periodo)
        cuota_anterior = cuota_periodo
    
    datos = {
        'Cuota número' : n_cuotas,
        'Fecha' : fechas,
        'Valor cuota' : cuotas,
    }
    df = pd.DataFrame(datos)
    return df
