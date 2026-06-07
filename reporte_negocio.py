import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import datetime
import io

st.set_page_config(page_title="Reporte Financiero", page_icon="📊", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0f0f0f; }
    .block-container { padding-top: 2rem; }
    h1, h2, h3 { color: white; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Sistema de Análisis Financiero")
st.caption("Reporte semanal automático para tu negocio")

with st.sidebar:
    st.header("⚙️ Datos del Negocio")
    nombre = st.text_input("Nombre del negocio", "Mi Negocio")
    
    st.subheader("💰 Ventas por día")
    lunes     = st.number_input("Lunes",     value=850000, step=10000)
    martes    = st.number_input("Martes",    value=920000, step=10000)
    miercoles = st.number_input("Miércoles", value=780000, step=10000)
    jueves    = st.number_input("Jueves",    value=1100000, step=10000)
    viernes   = st.number_input("Viernes",   value=1450000, step=10000)
    sabado    = st.number_input("Sábado",    value=1800000, step=10000)
    domingo   = st.number_input("Domingo",   value=1200000, step=10000)

    st.subheader("💸 Gastos de la semana")
    insumos   = st.number_input("Insumos / Materias primas", value=2100000, step=10000)
    nomina    = st.number_input("Nómina / Empleados",        value=1500000, step=10000)
    arriendo  = st.number_input("Arriendo",                  value=600000,  step=10000)
    servicios = st.number_input("Servicios públicos",        value=200000,  step=10000)
    marketing = st.number_input("Marketing",                 value=150000,  step=10000)
    otros     = st.number_input("Otros",                     value=120000,  step=10000)

    st.subheader("📅 Semana anterior")
    ventas_ant = st.number_input("Ventas semana anterior", value=7500000, step=10000)
    gastos_ant = st.number_input("Gastos semana anterior", value=4500000, step=10000)

ventas_semana = {
    'Lunes': lunes, 'Martes': martes, 'Miércoles': miercoles,
    'Jueves': jueves, 'Viernes': viernes, 'Sábado': sabado, 'Domingo': domingo
}
gastos_semana = {
    'Insumos': insumos, 'Nómina': nomina, 'Arriendo': arriendo,
    'Servicios': servicios, 'Marketing': marketing, 'Otros': otros
}

ventas_totales  = sum(ventas_semana.values())
gastos_totales  = sum(gastos_semana.values())
ganancia_neta   = ventas_totales - gastos_totales
margen_neto     = (ganancia_neta / ventas_totales) * 100
promedio_diario = ventas_totales / 7
ganancia_ant    = ventas_ant - gastos_ant

var_ventas   = ((ventas_totales - ventas_ant) / ventas_ant) * 100
var_gastos   = ((gastos_totales - gastos_ant) / gastos_ant) * 100
var_ganancia = ((ganancia_neta - ganancia_ant) / abs(ganancia_ant)) * 100 if ganancia_ant != 0 else 0

dia_max     = max(ventas_semana, key=ventas_semana.get)
dia_min     = min(ventas_semana, key=ventas_semana.get)
gasto_mayor = max(gastos_semana, key=gastos_semana.get)

def fmt(n): return f"${n:,.0f}"

st.subheader(f"📋 Reporte Semanal — {nombre}")
st.caption(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Ventas Totales", fmt(ventas_totales),  f"{var_ventas:+.1f}% vs semana ant.")
col2.metric("💸 Gastos Totales", fmt(gastos_totales),  f"{var_gastos:+.1f}% vs semana ant.")
col3.metric("✅ Ganancia Neta",  fmt(ganancia_neta),   f"{var_ganancia:+.1f}% vs semana ant.")
col4.metric("📐 Margen Neto",    f"{margen_neto:.1f}%")

st.divider()

plt.rcParams.update({
    'figure.facecolor': '#0f0f0f', 'axes.facecolor': '#1a1a1a',
    'axes.edgecolor': '#333', 'text.color': 'white',
    'axes.labelcolor': 'white', 'xtick.color': '#aaa',
    'ytick.color': '#aaa', 'grid.color': '#2a2a2a', 'grid.linestyle': '--'
})

fig, axes = plt.subplots(2, 2, figsize=(14, 8))
fig.suptitle(f'Análisis Semanal — {nombre}', fontsize=15, color='white', fontweight='bold')

dias    = list(ventas_semana.keys())
ventas  = list(ventas_semana.values())
colores = ['#00c48c' if v >= promedio_diario else '#ff6b6b' for v in ventas]

ax1 = axes[0, 0]
bars = ax1.bar(dias, ventas, color=colores, edgecolor='none', width=0.6)
ax1.axhline(promedio_diario, color='#ffd166', linestyle='--', linewidth=1.5, label='Promedio')
ax1.set_title('Ventas por Día', color='white', fontsize=11)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x/1e6:.1f}M'))
ax1.legend(fontsize=8)
ax1.grid(axis='y')

ax2 = axes[0, 1]
colores_pie = ['#ff6b6b','#ffd166','#06d6a0','#118ab2','#a78bfa','#fb923c']
ax2.pie(gastos_semana.values(), labels=gastos_semana.keys(), autopct='%1.1f%%',
        colors=colores_pie, pctdistance=0.75, startangle=90)
ax2.set_title('Distribución de Gastos', color='white', fontsize=11)

ax3 = axes[1, 0]
cats = ['Ventas', 'Gastos', 'Ganancia']
vals = [ventas_totales, gastos_totales, ganancia_neta]
ax3.bar(cats, vals, color=['#00c48c','#ff6b6b','#ffd166'], width=0.5, edgecolor='none')
ax3.set_title('Resumen Financiero', color='white', fontsize=11)
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x/1e6:.1f}M'))
ax3.grid(axis='y')

ax4 = axes[1, 1]
x = range(3)
ax4.bar([i - 0.2 for i in x], [ventas_ant, gastos_ant, ganancia_ant], width=0.35, label='Semana anterior', color='#4b5563', edgecolor='none')
ax4.bar([i + 0.2 for i in x], [ventas_totales, gastos_totales, ganancia_neta], width=0.35, label='Esta semana', color='#00c48c', edgecolor='none')
ax4.set_xticks(list(x))
ax4.set_xticklabels(['Ventas', 'Gastos', 'Ganancia'])
ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x/1e6:.1f}M'))
ax4.set_title('Comparación Semanal', color='white', fontsize=11)
ax4.legend(fontsize=8)
ax4.grid(axis='y')

plt.tight_layout()
st.pyplot(fig)

st.divider()

st.subheader("💡 Recomendaciones Automáticas")
pct_gastos = (gastos_totales / ventas_totales) * 100

if margen_neto < 10:
    st.error(f"🔴 Margen neto bajo ({margen_neto:.1f}%). Revisa tus precios o reduce gastos.")
elif margen_neto < 20:
    st.warning(f"🟡 Margen neto moderado ({margen_neto:.1f}%). Busca reducir el rubro más alto.")
else:
    st.success(f"🟢 Buen margen neto ({margen_neto:.1f}%). Considera reinvertir en marketing.")

if pct_gastos > 80:
    st.error(f"🔴 Gastos representan el {pct_gastos:.0f}% de ventas. Nivel crítico.")
elif pct_gastos > 65:
    st.warning(f"🟡 Gastos en {pct_gastos:.0f}% de ventas. Controla '{gasto_mayor}'.")
else:
    st.success(f"🟢 Gastos controlados ({pct_gastos:.0f}% de ventas).")

if var_ventas > 5:
    st.success(f"🟢 Ventas subieron {var_ventas:.1f}% vs semana anterior. ¡Mantén el ritmo!")
elif var_ventas < -5:
    st.error(f"🔴 Ventas bajaron {abs(var_ventas):.1f}%. Activa promociones.")
else:
    st.info(f"🟡 Ventas estables ({var_ventas:+.1f}%). Busca estrategias para crecer.")

st.info(f"📌 '{dia_min}' es tu día más flojo ({fmt(ventas_semana[dia_min])}). Considera promociones ese día.")
st.success(f"🏆 '{dia_max}' es tu mejor día ({fmt(ventas_semana[dia_max])}). Aprovéchalo al máximo.")

st.divider()

st.subheader("📥 Exportar Reporte")
output = io.BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df_ventas = pd.DataFrame(list(ventas_semana.items()), columns=['Día', 'Ventas'])
    df_ventas.to_excel(writer, sheet_name='Ventas por Día', index=False)
    df_gastos = pd.DataFrame(list(gastos_semana.items()), columns=['Concepto', 'Monto'])
    df_gastos['% del total'] = [f"{(v/gastos_totales)*100:.1f}%" for v in gastos_semana.values()]
    df_gastos.to_excel(writer, sheet_name='Gastos', index=False)
    resumen = {
        'Métrica': ['Ventas Totales','Gastos Totales','Ganancia Neta','Margen Neto','Promedio Diario','Mejor Día','Peor Día'],
        'Valor': [fmt(ventas_totales), fmt(gastos_totales), fmt(ganancia_neta),
                  f'{margen_neto:.1f}%', fmt(promedio_diario), dia_max, dia_min]
    }
    pd.DataFrame(resumen).to_excel(writer, sheet_name='Resumen', index=False)

st.download_button(
    label="⬇️ Descargar Reporte Excel",
    data=output.getvalue(),
    file_name=f"reporte_{nombre.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
