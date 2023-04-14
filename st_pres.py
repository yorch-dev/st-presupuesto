import streamlit as st
import pandas as pd
from fn_proyeccion_ahorro_y_dp import proyeccion_ahorro_y_dp as padp
from fn_formato import formatNumber
from datetime import date
import numpy as np
import matplotlib.pyplot as plt

st.write(
    """
        # Ahorro con inversión

        Muestra el resultado del ahorro para un producto con inversión de sus cuotas
    """
)

nombre_producto = st.text_input(
    "Nombre del producto",
    placeholder='Ejemplo: "Notebook"'
)

valor_producto = st.number_input(
        "Valor del producto",
        min_value=0,
        max_value=10000000,
)

t_vida_slider = np.array([x for x in range(1, 21)])
t_vida = st.select_slider(
    "Tiempo de vida",
    options=t_vida_slider
)

fecha_inicio = st.date_input(
    "Fecha inicio",
)

dias_ciclos_inversion = st.number_input(
    "Días ciclo de inversión",
    min_value=7,
    max_value=180
)

tasa_interes_objetivo = st.number_input(
    "Tasa de interés objetivo (aplica para costo futuro del producto)",
    help="Ejemplo: 1.00 si se quiere un 1%",
    value = 1.00
)

tasa_interes_objetivo = tasa_interes_objetivo / 100

tasa_interes_inversion = st.number_input(
    "Tasa de interés inversión (aplica para interés negociado)",
    help="Ejemplo: 1.00 si se quiere un 1%",
    value = 0.75
)
tasa_interes_inversion = tasa_interes_inversion / 100

precision_radio = st.radio(
    "Precisión del cálculo (afecta tiempo de ejecución)",
    options=['Baja', 'Normal', 'Alta', 'Muy alta']
)

precision = 0.0001
if precision_radio == 'Baja':
    precision = 0.001
elif precision_radio == 'Alta':
    precision = 0.00005
elif precision_radio == 'Muy alta':
    precision = 0.00001

boton = st.button(
    'Ver resultados',
)


def make_grid(cols,rows):
    grid = [0]*cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid

def func(pct, allvals):
    absolute = int(round((pct/100.*np.sum(allvals)), 0))
    return "{:.1f}%\n${}".format(pct, formatNumber(absolute, 0))

@st.experimental_memo
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

if boton:
    df_padp, monto_objetivo, tasa_int_personal = padp(valor_producto, t_vida, fecha_inicio, dias_ciclos_inversion, tasa_interes_objetivo, tasa_interes_inversion, precision)
    st.dataframe(df_padp, use_container_width=True)
    csv = convert_df(df_padp)
    st.download_button(
        "Descargar tabla con proyección",
        csv,
        f"Proyecto_{nombre_producto}.csv",
        "text/csv",
        key='download-csv'
    )
    df_padp['% Cuota'] = df_padp['Valor cuota'] / (df_padp['Valor cuota'] + df_padp['Ganancia'])
    df_padp['% Ganancia'] = df_padp['Ganancia'] / (df_padp['Valor cuota'] + df_padp['Ganancia'])
    st.bar_chart(
        df_padp,
        x='Fecha',
        y=['% Ganancia', '% Cuota']
    )
    st.write(f'# *Resumen proyecto {nombre_producto}*')
    mygrid = make_grid(2, 2)

    mygrid[1][0].write(f" El objetivo es: ${formatNumber(int(monto_objetivo), 0)}")
    mygrid[1][0].write(f" El resultado es: ${formatNumber(int(df_padp['Valor cuota'].sum() + df_padp['Ganancia'].sum()), 0)}")
    mygrid[1][0].write("\tAcumulado con cuota personal: ${}".format(formatNumber(int(df_padp['Valor cuota'].sum()), 0)))
    mygrid[1][0].write("\tTasa de interés ahorro personal {}%".format(round(tasa_int_personal * 100, 2)))
    mygrid[1][0].write("\tGanancia inversión: ${}".format(formatNumber(int(df_padp['Ganancia'].sum()), 0)))
    mygrid[1][0].write(f" El saldo: ${formatNumber(int((df_padp['Valor cuota'].sum() + df_padp['Ganancia'].sum()) - monto_objetivo), 0)}")

    fig, ax = plt.subplots()
    data = [df_padp['Valor cuota'].sum(), df_padp['Ganancia'].sum()]
    ax.pie(data,
        labels=['Cuotas ahorro', 'Ganancia'],
        explode=[0, 0.2],
        shadow=True,
        startangle=120,
        autopct=lambda pct: func(pct, data),
        textprops={'color':"w"},
        wedgeprops={'linewidth': 3.0, 'edgecolor': 'black'}
    )
    fig.set_facecolor('black')
    mygrid[1][1].write(fig)
