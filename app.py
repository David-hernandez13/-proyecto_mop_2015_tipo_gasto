import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Contratos MOP 2015", layout="wide")
st.title("📊 Contratos del Ministerio de Obras Públicas - 2015")

# Cargar archivo Excel desde el usuario
archivo = st.file_uploader("Sube el archivo Excel del MOP", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)

    st.subheader("🔍 Vista previa de los datos")

    # Filtro por región
    regiones = df["Región"].dropna().unique().tolist()
    region_seleccionada = st.selectbox("Filtrar por región", ["Todas"] + sorted(regiones))

    if region_seleccionada != "Todas":
        df = df[df["Región"] == region_seleccionada]

    # Mostrar tabla completa con scroll
    st.dataframe(df, height=600)

    # Presupuesto por región
    df_region = df.groupby("Región")["Presupuesto Oficial"].sum().sort_values(ascending=False)
    st.subheader("🏗️ Presupuesto Oficial por Región")
    fig, ax = plt.subplots(figsize=(10, 6))
    df_region.plot(kind="bar", ax=ax, color='skyblue')
    ax.set_title("Presupuesto Oficial por Región (MOP - 2015)")
    ax.set_xlabel("Región")
    ax.set_ylabel("Presupuesto en pesos")
    ax.grid(axis='y')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    # Nuevo gráfico: Presupuesto por tipo de gasto
    df_tipo = df.groupby("Tipo de Gasto")["Presupuesto Oficial"].sum().sort_values(ascending=False)
    st.subheader("💰 Presupuesto por Tipo de Gasto")
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    df_tipo.plot(kind="bar", ax=ax2, color="orange")
    ax2.set_title("Presupuesto por Tipo de Gasto")
    ax2.set_xlabel("Tipo de Gasto")
    ax2.set_ylabel("Presupuesto en pesos")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    # Opcional: expandir por contrato
    with st.expander("📄 Ver contratos uno a uno"):
        for i, fila in df.iterrows():
            st.markdown(f"**{fila['Nombre Contrato']}**")
            st.write(fila.to_frame())
else:
    st.info("Por favor, sube el archivo Excel para comenzar.")