# @title Ejecución

def proyeccion_ahorro_y_dp(valor_producto, t_vida, fecha_inicio, dias_ciclo, t_int_objetivo = 0.01, t_int_dp = 0.007, precision = 0.0001):
    """
    Args =  valor_producto int,
            t_vida años int o float,
            fecha_inicio date,
            t_int_objetivo float : por defecto 0.01,
            dias int : duración en días del ciclo de depósito a plazo,
            t_int_dp float : tasa de interés del depósito a plazo, por defecto 0.007,
            precision float : tasa de aumento en tasa_int_personal entre iteraciones en busca del valor objetivo

    """

    import pandas as pd
    from fn_presupuesto_cuotas import presupuesto_cuotas as pc
    from fn_inversion_a_plazo import inversion_a_plazo as ip

    presupuesto_inicio = pc(valor_producto, t_vida, fecha_inicio, t_int_objetivo)
    monto_objetivo = presupuesto_inicio['Valor cuota'].sum()

    tasa_int_personal = t_int_objetivo - 0.015
    rescate = 0
    saldo = -1

    while saldo < 0:
        df_presupuesto = pc(valor_producto, t_vida, fecha_inicio, tasa_int_personal)
        fecha_union_pc = []
        for fecha in df_presupuesto['Fecha']:
            if fecha.month < 10:
                fecha_union_pc.append(str(fecha.year) + '0' + str(fecha.month))
            else:
                fecha_union_pc.append(str(fecha.year) + str(fecha.month))
        df_presupuesto['fecha_union'] = fecha_union_pc


        fechas_union = []
        ganancias_union = []
        fecha_no_inversion = []
        plazo = t_vida - (1/12)

        for i in range(df_presupuesto['Valor cuota'].size):
            monto_inversion = df_presupuesto['Valor cuota'][i]
            fecha_inversion = df_presupuesto['Fecha'][i]

            df_inv = ip(monto_inversion, fecha_inversion, dias_ciclo, t_int_dp, rescate, plazo)
            fecha_union_ip = []
            for fecha in df_inv['Fecha rescate']:
                if fecha.month < 10:
                    fecha_union_ip.append(str(fecha.year) + '0' + str(fecha.month))
                else:
                    fecha_union_ip.append(str(fecha.year) + str(fecha.month))
            df_inv['fecha_union'] = fecha_union_ip
            
            for j in range(len(df_inv)):
                if df_inv['fecha_union'][j] in fechas_union:
                    ganancias_union[fechas_union.index(df_inv['fecha_union'][j])] += int(df_inv['Ganancia'][j])
                else:
                    fechas_union.append(df_inv['fecha_union'][j])
                    ganancias_union.append(int(df_inv['Ganancia'][j]))

            plazo = plazo - (1/12)
            fecha_no_inversion.append(fecha_inversion) if df_inv.empty else ''

        datos = {
            'fecha_union' : fechas_union,
            'Ganancia' : ganancias_union
        }

        df_inv = pd.DataFrame(datos)
        saldo = (df_presupuesto['Valor cuota'].sum() + df_inv['Ganancia'].sum() - presupuesto_inicio['Valor cuota'].sum())
        tasa_int_personal += precision

    df = pd.merge(
        df_presupuesto,
        df_inv[['fecha_union', 'Ganancia']],
        how='left',
        on=['fecha_union']
    )
    ganancia = []

    import math

    for g in df['Ganancia']:
        if math.isnan(g):
            ganancia.append(0)
        else:
            ganancia.append(int(g))

    df['Ganancia'] = ganancia

    cuota_invertida = [df['Fecha'][i] not in fecha_no_inversion for i in range(len(df))]
    df.insert(
        loc = 2,
        column = 'Cuota invertida',
        value = cuota_invertida
    )
    df = pd.DataFrame(
        df,
        columns=['Fecha', 'Valor cuota', 'Cuota invertida', 'Ganancia']
    )

    return df, monto_objetivo, tasa_int_personal