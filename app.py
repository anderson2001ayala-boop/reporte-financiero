import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Sistema de Gestión", page_icon="🏪", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

* { font-family: 'Poppins', sans-serif; }
.stApp { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); }
h1, h2, h3, p, label { color: white !important; }

.titulo-principal {
    font-size: 48px;
    font-weight: 800;
    background: linear-gradient(90deg, #e94560, #0f3460);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    padding: 20px 0;
}

.subtitulo {
    text-align: center;
    color: #aaa !important;
    font-size: 16px;
    letter-spacing: 3px;
    margin-bottom: 30px;
}

div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 15px;
    padding: 20px;
    backdrop-filter: blur(10px);
}

div[data-testid="metric-container"] label {
    color: #aaa !important;
    font-size: 14px !important;
}

div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #e94560 !important;
    font-size: 28px !important;
    font-weight: 800 !important;
}

.stButton > button {
    background: linear-gradient(90deg, #e94560, #c23152) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    padding: 12px !important;
    width: 100% !important;
    transition: all 0.3s !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 20px rgba(233,69,96,0.4) !important;
}

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: white !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 5px;
}

.stTabs [data-baseweb="tab"] {
    color: white !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #e94560, #c23152) !important;
}

.stDataFrame { border-radius: 10px; overflow: hidden; }

.alerta-box {
    background: rgba(233,69,96,0.2);
    border: 1px solid #e94560;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    color: white;
}

.success-box {
    background: rgba(0,200,100,0.2);
    border: 1px solid #00c864;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    color: white;
}

div[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.3) !important;
    backdrop-filter: blur(10px) !important;
}
</style>
""", unsafe_allow_html=True)

def init_db():
    conn = sqlite3.connect('tienda.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        categoria TEXT,
        precio_compra REAL,
        precio_venta REAL,
        stock INTEGER,
        stock_minimo INTEGER,
        fecha_registro TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_id INTEGER,
        producto_nombre TEXT,
        cantidad INTEGER,
        precio_unitario REAL,
        total REAL,
        cliente TEXT,
        fecha TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT,
        email TEXT,
        direccion TEXT,
        fecha_registro TEXT
    )''')
    conn.commit()
    conn.close()

def get_productos():
    conn = sqlite3.connect('tienda.db')
    df = pd.read_sql_query('SELECT * FROM productos', conn)
    conn.close()
    return df

def get_ventas():
    conn = sqlite3.connect('tienda.db')
    df = pd.read_sql_query('SELECT * FROM ventas', conn)
    conn.close()
    return df

def get_clientes():
    conn = sqlite3.connect('tienda.db')
    df = pd.read_sql_query('SELECT * FROM clientes', conn)
    conn.close()
    return df

def agregar_producto(nombre, categoria, precio_compra, precio_venta, stock, stock_minimo):
    conn = sqlite3.connect('tienda.db')
    c = conn.cursor()
    c.execute('INSERT INTO productos VALUES (NULL,?,?,?,?,?,?,?)',
              (nombre, categoria, precio_compra, precio_venta, stock, stock_minimo, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def registrar_venta(producto_id, producto_nombre, cantidad, precio_unitario, cliente):
    conn = sqlite3.connect('tienda.db')
    c = conn.cursor()
    total = cantidad * precio_unitario
    c.execute('INSERT INTO ventas VALUES (NULL,?,?,?,?,?,?,?)',
              (producto_id, producto_nombre, cantidad, precio_unitario, total, cliente, datetime.now().strftime("%Y-%m-%d %H:%M")))
    c.execute('UPDATE productos SET stock = stock - ? WHERE id = ?', (cantidad, producto_id))
    conn.commit()
    conn.close()

def agregar_cliente(nombre, telefono, email, direccion):
    conn = sqlite3.connect('tienda.db')
    c = conn.cursor()
    c.execute('INSERT INTO clientes VALUES (NULL,?,?,?,?,?)',
              (nombre, telefono, email, direccion, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def eliminar_producto(producto_id):
    conn = sqlite3.connect('tienda.db')
    c = conn.cursor()
    c.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
    conn.commit()
    conn.close()

init_db()

st.markdown('<p class="titulo-principal">🏪 Sistema de Gestión de Tienda</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo">CONTROL TOTAL DE TU NEGOCIO</p>', unsafe_allow_html=True)
st.markdown('<hr style="border-color: rgba(233,69,96,0.3);">', unsafe_allow_html=True)

df_productos = get_productos()
df_ventas = get_ventas()
df_clientes = get_clientes()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📦 Productos", len(df_productos))
with col2:
    total_ventas = df_ventas['total'].sum() if len(df_ventas) > 0 else 0
    st.metric("💰 Total Ventas", f"${total_ventas:,.0f}")
with col3:
    st.metric("👥 Clientes", len(df_clientes))
with col4:
    alertas = len(df_productos[df_productos['stock'] <= df_productos['stock_minimo']]) if len(df_productos) > 0 else 0
    st.metric("⚠️ Alertas Stock", alertas)

st.markdown('<hr style="border-color: rgba(233,69,96,0.3);">', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📦 Inventario", "💰 Ventas", "👥 Clientes", "📊 Reportes", "⚠️ Alertas"])

with tab1:
    st.subheader("📦 Gestión de Inventario")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("#### ➕ Agregar Producto")
        nombre = st.text_input("Nombre del producto")
        categoria = st.selectbox("Categoría", ["Ropa", "Calzado", "Accesorios", "Electrónica", "Alimentos", "Otro"])
        precio_compra = st.number_input("Precio de compra", min_value=0.0, step=1000.0)
        precio_venta = st.number_input("Precio de venta", min_value=0.0, step=1000.0)
        stock = st.number_input("Stock inicial", min_value=0, step=1)
        stock_minimo = st.number_input("Stock mínimo alerta", min_value=0, step=1)
        if st.button("➕ Agregar Producto"):
            if nombre:
                agregar_producto(nombre, categoria, precio_compra, precio_venta, stock, stock_minimo)
                st.success(f"✅ {nombre} agregado correctamente")
                st.rerun()
            else:
                st.error("❌ Escribe el nombre del producto")
    with col2:
        st.markdown("#### 📋 Lista de Productos")
        if len(df_productos) > 0:
            st.dataframe(df_productos, use_container_width=True, height=300)
            producto_eliminar = st.selectbox("Selecciona producto a eliminar", df_productos['id'].tolist(), format_func=lambda x: df_productos[df_productos['id']==x]['nombre'].values[0])
            if st.button("🗑️ Eliminar Producto"):
                eliminar_producto(producto_eliminar)
                st.success("✅ Producto eliminado")
                st.rerun()
        else:
            st.info("📭 No hay productos registrados aún")

with tab2:
    st.subheader("💰 Registrar Venta")
    col1, col2 = st.columns([1, 2])
    with col1:
        if len(df_productos) > 0:
            producto_sel = st.selectbox("Producto", df_productos['id'].tolist(), format_func=lambda x: df_productos[df_productos['id']==x]['nombre'].values[0])
            producto_info = df_productos[df_productos['id']==producto_sel].iloc[0]
            st.info(f"📦 Stock: {producto_info['stock']} | 💰 Precio: ${producto_info['precio_venta']:,.0f}")
            cantidad = st.number_input("Cantidad", min_value=1, max_value=int(producto_info['stock']) if producto_info['stock'] > 0 else 1)
            cliente = st.text_input("Cliente (opcional)")
            total_preview = cantidad * producto_info['precio_venta']
            st.metric("💵 Total a cobrar", f"${total_preview:,.0f}")
            if st.button("💰 Registrar Venta"):
                if producto_info['stock'] >= cantidad:
                    registrar_venta(producto_sel, producto_info['nombre'], cantidad, producto_info['precio_venta'], cliente)
                    st.success(f"✅ Venta registrada: ${total_preview:,.0f}")
                    st.rerun()
                else:
                    st.error("❌ Stock insuficiente")
        else:
            st.warning("⚠️ Agrega productos primero")
    with col2:
        st.markdown("#### 📋 Historial de Ventas")
        if len(df_ventas) > 0:
            st.dataframe(df_ventas, use_container_width=True, height=300)
        else:
            st.info("📭 No hay ventas registradas aún")

with tab3:
    st.subheader("👥 Gestión de Clientes")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("#### ➕ Agregar Cliente")
        nombre_c = st.text_input("Nombre completo")
        telefono_c = st.text_input("Teléfono")
        email_c = st.text_input("Email")
        direccion_c = st.text_input("Dirección")
        if st.button("➕ Agregar Cliente"):
            if nombre_c:
                agregar_cliente(nombre_c, telefono_c, email_c, direccion_c)
                st.success(f"✅ {nombre_c} agregado")
                st.rerun()
            else:
                st.error("❌ Escribe el nombre del cliente")
    with col2:
        st.markdown("#### 📋 Lista de Clientes")
        if len(df_clientes) > 0:
            st.dataframe(df_clientes, use_container_width=True, height=300)
        else:
            st.info("📭 No hay clientes registrados aún")

with tab4:
    st.subheader("📊 Reportes de Ventas")
    if len(df_ventas) > 0:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Ventas por Producto")
            ventas_producto = df_ventas.groupby('producto_nombre')['total'].sum()
            fig, ax = plt.subplots(facecolor='#16213e')
            ax.set_facecolor('#16213e')
            ventas_producto.plot(kind='bar', ax=ax, color='#e94560')
            ax.set_xlabel("Producto", color='white')
            ax.set_ylabel("Total $", color='white')
            ax.tick_params(colors='white')
            plt.xticks(rotation=45, color='white')
            st.pyplot(fig)
        with col2:
            st.markdown("#### Resumen")
            st.metric("💰 Total vendido", f"${df_ventas['total'].sum():,.0f}")
            st.metric("🛒 Número de ventas", len(df_ventas))
            st.metric("📊 Ticket promedio", f"${df_ventas['total'].mean():,.0f}")
    else:
        st.info("📭 Registra ventas para ver reportes")

with tab5:
    st.subheader("⚠️ Alertas de Stock Bajo")
    if len(df_productos) > 0:
        alertas_df = df_productos[df_productos['stock'] <= df_productos['stock_minimo']]
        if len(alertas_df) > 0:
            st.error(f"⚠️ {len(alertas_df)} productos con stock bajo")
            st.dataframe(alertas_df[['nombre', 'categoria', 'stock', 'stock_minimo']], use_container_width=True)
        else:
            st.success("✅ Todo el inventario está en niveles normales")
    else:
        st.info("📭 Agrega productos para ver alertas")

st.markdown('<hr style="border-color: rgba(233,69,96,0.3);">', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>Sistema de Gestión de Tienda | Desarrollado por Anderson Ayala | 2026</p>", unsafe_allow_html=True)