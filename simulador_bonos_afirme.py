import streamlit as st
from PIL import Image
import base64
from io import BytesIO

# Esta línea debe ir aquí inmediatamente
st.set_page_config(page_title="Simulador Bonos Afirme 2025", layout="centered")

# Función para aplicar formato de miles con pesos
def formatear_pesos(valor):
    try:
        valor = float(valor)
        return "$ {:,.2f}".format(valor)
    except:
        return "$ 0.00"

# Mostrar logo en esquina superior derecha con títulos centrados
logo = Image.open("link logo.jpg")  # Asegúrate que esté en la carpeta correcta
buffered = BytesIO()
logo.save(buffered, format="PNG")
img_base64 = base64.b64encode(buffered.getvalue()).decode()

st.markdown(
    f"""
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div style="flex-grow: 1; text-align: center;">
            <h1>Simulador de Bonos</h1>
            <h2>Afirme 2025</h2>
        </div>
        <div>
            <img src="data:image/png;base64,{img_base64}" alt="Logo" style="max-height: 80px;">
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# Títulos centrados
st.markdown("""
    <div style='text-align: center;'>
        <h1>Simulador de Bonos</h1>
        <h2>Afirme 2025</h2>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")
agente = st.text_input("Nombre del Agente")
tipo_bono = st.selectbox("Selecciona la sección a calcular:", [
    "Autos (Producción y Crecimiento)",
    "Daños (Producción y Crecimiento)",
    "Vida Grupo",
    "Bono Anual por Buena Siniestralidad Autos",
    "Bono de Siniestralidad en Ramos Especiales",
    "Nueva Recluta: Autos, Daños o Vida"
])
st.markdown("---")

# =========================
# Autos (Producción y Crecimiento)
# =========================
if tipo_bono == "Autos (Producción y Crecimiento)":
    produccion_2024 = st.number_input("Producción 2024 Autos ($)", min_value=0.0, format="%.2f")
    produccion_2025 = st.number_input("Producción 2025 Autos ($)", min_value=0.0, format="%.2f")
    siniestralidad = st.number_input("Siniestralidad Autos (%)", min_value=0.0, max_value=100.0, format="%.2f")

    calcular = st.button("Calcular Bono de Autos")

    if calcular:
        bono_produccion = 0
        bono_crecimiento = 0
        explicacion = []

        tramos_produccion = [
            (1400001, float('inf'), 6.5, 5.5, 4.5),
            (780001, 1400000, 5.5, 4.5, 3.5),
            (570001, 780000, 4.5, 3.5, 2.5),
            (380001, 570000, 4.0, 3.0, 2.0),
            (220001, 380000, 3.0, 2.0, 1.0),
            (110000, 220000, 2.0, 1.0, 0.0)
        ]

        for minimo, maximo, pct1, pct2, pct3 in tramos_produccion:
            if minimo <= produccion_2025 <= maximo:
                if siniestralidad < 60:
                    bono_produccion = pct1
                    explicacion.append(f"✅ Aplica bono de producción del {pct1}% por siniestralidad < 60%.")
                elif siniestralidad < 75:
                    bono_produccion = pct2
                    explicacion.append(f"✅ Aplica bono de producción del {pct2}% por siniestralidad entre 60% y 74.99%.")
                else:
                    bono_produccion = pct3
                    if pct3 > 0:
                        explicacion.append(f"✅ Aplica bono de producción del {pct3}% por siniestralidad ≥ 75%.")
                    else:
                        explicacion.append("❌ Siniestralidad ≥ 75%. No aplica bono de producción en este rango.")
                break
        else:
            explicacion.append("❌ No alcanza el mínimo de producción de $110,000 para aplicar a bono de producción.")

        if produccion_2024 > 0:
            crecimiento = ((produccion_2025 - produccion_2024) / produccion_2024) * 100
        else:
            crecimiento = 0

        if siniestralidad < 63 and crecimiento >= 10:
            for minimo, maximo, pct10, pct15, pct25 in [
                (1400001, float('inf'), 2.25, 3.25, 4.25),
                (780001, 1400000, 2.00, 3.00, 4.00),
                (570001, 780000, 1.75, 2.75, 3.75),
                (380001, 570000, 1.50, 2.50, 3.50),
                (220001, 380000, 1.25, 2.25, 3.25),
                (110000, 220000, 1.00, 2.00, 3.00)
            ]:
                if minimo <= produccion_2025 <= maximo:
                    if crecimiento >= 25:
                        bono_crecimiento = pct25
                    elif crecimiento >= 15:
                        bono_crecimiento = pct15
                    else:
                        bono_crecimiento = pct10
                    explicacion.append(f"✅ Aplica bono de crecimiento del {bono_crecimiento}% por crecimiento del {crecimiento:.2f}% y siniestralidad < 63%.")
                    break
        else:
            if siniestralidad >= 63:
                explicacion.append("❌ Siniestralidad ≥ 63%. No aplica bono de crecimiento.")
            if crecimiento < 10:
                explicacion.append(f"❌ Crecimiento del {crecimiento:.2f}% es menor al 10%. No aplica bono de crecimiento.")

        total_bono = (bono_produccion + bono_crecimiento) * produccion_2025 / 100

        # RESULTADOS
        st.markdown(f"### 🧾 Resultados para {agente.upper()}:")
        st.write("**Datos Ingresados:**")
        st.write(f"- Producción 2024 Autos: {formatear_pesos(produccion_2024)}")
        st.write(f"- Producción 2025 Autos: {formatear_pesos(produccion_2025)}")
        st.write(f"- Crecimiento: {crecimiento:.2f}%")
        st.write(f"- Siniestralidad: {siniestralidad:.2f}%")

        st.write("**Resultados del Bono:**")
        st.write(f"- Bono de Producción: {bono_produccion:.2f}% → {formatear_pesos(bono_produccion * produccion_2025 / 100)}")
        st.write(f"- Bono de Crecimiento: {bono_crecimiento:.2f}% → {formatear_pesos(bono_crecimiento * produccion_2025 / 100)}")

        st.success(f"💰 Total del Bono: {formatear_pesos(total_bono)}")

        st.markdown("---")
        st.subheader("📌 Explicación:")
        for e in explicacion:
            st.write(e)

# =========================
# Daños (Producción y Crecimiento)
# =========================
if tipo_bono == "Daños (Producción y Crecimiento)":
    st.subheader("🧾 Ingreso de Datos: Daños")
    produccion_2024 = st.number_input("Producción Daños 2024 ($)", min_value=0.0, format="%.2f")
    produccion_2025 = st.number_input("Producción Daños 2025 ($)", min_value=0.0, format="%.2f")
    siniestralidad = st.number_input("Siniestralidad Daños 2025 (%)", min_value=0.0, max_value=100.0, format="%.2f")

    calcular = st.button("Calcular Bono Daños")

    if calcular:
        explicacion = []
        bono_produccion = 0
        bono_crecimiento = 0
        crecimiento_real = 0

        # Cálculo de Producción
        tramos_produccion_danos = [
            (650001, float('inf'), 6.0, 5.0),
            (410001, 650000, 5.0, 4.0),
            (290001, 410000, 4.0, 3.0),
            (125001, 290000, 3.0, 2.0),
            (75000, 125000, 2.0, 1.0),
        ]

        for minimo, maximo, pct_bajo, pct_alto in tramos_produccion_danos:
            if minimo <= produccion_2025 <= maximo:
                if siniestralidad < 50:
                    bono_produccion = pct_bajo
                    explicacion.append(f"✅ Aplica bono de producción del {pct_bajo}% por siniestralidad menor al 50%.")
                else:
                    bono_produccion = pct_alto
                    explicacion.append(f"✅ Aplica bono de producción del {pct_alto}% por siniestralidad del 50% o más.")
                break
        else:
            explicacion.append("❌ No alcanza el mínimo de $75,000 de producción para aplicar a bono de producción.")

        # Cálculo de Crecimiento
        if produccion_2024 > 0:
            crecimiento_real = ((produccion_2025 - produccion_2024) / produccion_2024) * 100

            tramos_crecimiento_danos = [
                (650001, float('inf'), 3.0, 4.0, 5.0),
                (410001, 650000, 2.5, 3.5, 4.5),
                (290001, 410000, 2.0, 3.0, 4.0),
                (125001, 290000, 1.5, 2.5, 3.5),
                (75000, 125000, 1.0, 2.0, 3.0),
            ]

            for minimo, maximo, pct_10, pct_15, pct_20 in tramos_crecimiento_danos:
                if minimo <= produccion_2025 <= maximo:
                    if crecimiento_real >= 25:
                        bono_crecimiento = pct_20
                        explicacion.append(f"✅ Aplica bono de crecimiento del {pct_20}% por crecimiento ≥ 25%.")
                    elif crecimiento_real >= 15:
                        bono_crecimiento = pct_15
                        explicacion.append(f"✅ Aplica bono de crecimiento del {pct_15}% por crecimiento ≥ 15%.")
                    elif crecimiento_real >= 10:
                        bono_crecimiento = pct_10
                        explicacion.append(f"✅ Aplica bono de crecimiento del {pct_10}% por crecimiento ≥ 10%.")
                    else:
                        explicacion.append(f"❌ No aplica bono de crecimiento. Se requiere al menos 10% de crecimiento.")
                    break
        else:
            explicacion.append("❌ Producción 2024 no registrada. No se puede calcular crecimiento.")

        # Total
        total_bono = (bono_produccion + bono_crecimiento) * produccion_2025 / 100

        # Resultados
        st.markdown(f"### 🧾 Resultados para {agente}")
        st.write("**Datos Ingresados:**")
        st.write(f"- Producción 2024: {formatear_pesos(produccion_2024)}")
        st.write(f"- Producción 2025: {formatear_pesos(produccion_2025)}")
        st.write(f"- Siniestralidad: {siniestralidad:.2f}%")
        st.write(f"- Crecimiento Real: {crecimiento_real:.2f}%")

        st.write("**Resultado del Bono:**")
        st.write(f"- Bono Producción: {bono_produccion:.2f}%")
        st.write(f"- Bono Crecimiento: {bono_crecimiento:.2f}%")
        st.success(f"🟢 Total del Bono: {formatear_pesos(total_bono)}")

        st.markdown("---")
        st.subheader("Explicación del Cálculo:")
        for e in explicacion:
            st.write(e)

        st.markdown("---")
        st.markdown("<div style='text-align: center; color: gray;'>Aplican restricciones y condiciones conforme al cuaderno oficial de Afirme Seguros 2025.</div>", unsafe_allow_html=True)

# =========================
# Nueva Recluta: Autos, Daños o Vida
# =========================
if tipo_bono == "Nueva Recluta: Autos, Daños o Vida":
    st.subheader("Bono Nueva Recluta")
    st.markdown("Selecciona el ramo correspondiente e ingresa los datos para calcular el bono según el esquema de nueva recluta.")
    ramo_recluta = st.selectbox("Selecciona el ramo:", ["Autos", "Daños", "Vida"])
    prima = st.number_input("Prima neta pagada 2025 ($)", min_value=0.0, format="%.2f")
    resultado = ""
    siniestralidad = 0.0
    if ramo_recluta in ["Autos", "Daños"]:
        siniestralidad = st.number_input("Siniestralidad (%)", min_value=0.0, max_value=100.0, format="%.2f")
    calcular = st.button("Calcular Bono Nueva Recluta")

    if calcular:
        porcentaje_bono = 0
        explicacion = []

        if ramo_recluta == "Autos":
            tabla_autos = [
                (1120001, float('inf'), [6.5, 5.5, 4.5]),
                (624001, 1120000, [5.5, 4.5, 3.5]),
                (456001, 624000, [4.0, 3.0, 2.0]),
                (304001, 456000, [3.0, 2.0, 1.0]),
                (176001, 304000, [2.0, 1.0, 0.0]),
                (88000, 176000, [2.0, 1.0, 0.0])
            ]
            for minimo, maximo, porcentajes in tabla_autos:
                if minimo <= prima <= maximo:
                    if siniestralidad < 60:
                        porcentaje_bono = porcentajes[0]
                        explicacion.append("✅ Siniestralidad menor al 60%")
                    elif siniestralidad <= 75:
                        porcentaje_bono = porcentajes[1]
                        explicacion.append("✅ Siniestralidad entre 60% y 75%")
                    else:
                        porcentaje_bono = porcentajes[2]
                        explicacion.append("⚠️ Siniestralidad mayor al 75%")
                    break

        elif ramo_recluta == "Daños":
            tabla_danos = [
                (520001, float('inf'), [6.0, 5.0]),
                (328001, 520000, [5.0, 4.0]),
                (232001, 328000, [4.0, 3.0]),
                (100001, 232000, [3.0, 2.0]),
                (60000, 100000, [2.0, 1.0])
            ]
            for minimo, maximo, porcentajes in tabla_danos:
                if minimo <= prima <= maximo:
                    if siniestralidad < 50:
                        porcentaje_bono = porcentajes[0]
                        explicacion.append("✅ Siniestralidad menor al 50%")
                    else:
                        porcentaje_bono = porcentajes[1]
                        explicacion.append("⚠️ Siniestralidad mayor o igual al 50%")
                    break

        elif ramo_recluta == "Vida":
            tabla_vida = [
                (320001, float('inf'), 3.0),
                (240001, 320000, 2.5),
                (160001, 240000, 2.0),
                (80001, 160000, 1.5),
                (40000, 80000, 1.0)
            ]
            for minimo, maximo, pct in tabla_vida:
                if minimo <= prima <= maximo:
                    porcentaje_bono = pct
                    explicacion.append(f"✅ Prima dentro del rango para {pct}%")
                    break

        total_bono = porcentaje_bono * prima / 100

        st.markdown(f"### 🧾 Resultados para {agente.upper()}")
        st.write("**Datos Ingresados:**")
        st.write(f"- Ramo seleccionado: {ramo_recluta}")
        st.write(f"- Prima 2025: {formatear_pesos(prima)}")
        if ramo_recluta in ["Autos", "Daños"]:
            st.write(f"- Siniestralidad: {siniestralidad:.2f}%")

        st.write("**Resultado del Bono:**")
        if porcentaje_bono > 0:
            st.success(f"✅ Bono aplicado: {porcentaje_bono:.2f}%")
        else:
            st.error("❌ No aplica bono con los datos ingresados.")
        st.info(f"💰 Total del Bono: {formatear_pesos(total_bono)}")

        st.markdown("---")
        st.subheader("Explicaciones:")
        for e in explicacion:
            st.write(f"- {e}")

        st.markdown("---")
        st.markdown("<div style='text-align: center; color: gray;'>Aplican restricciones y condiciones conforme al cuaderno oficial de Afirme Seguros 2025.</div>", unsafe_allow_html=True)

# =========================
# Bono Anual por Buena Siniestralidad Autos
# =========================
if tipo_bono == "Bono Anual por Buena Siniestralidad Autos":
    st.subheader("Bono Anual por Buena Siniestralidad en Autos")

    prima_total = st.number_input("Prima neta total anual Autos ($)", min_value=0.0, format="%.2f")
    siniestralidad = st.number_input("Siniestralidad Autos (%)", min_value=0.0, max_value=100.0, format="%.2f")
    es_nueva_recluta = st.checkbox("¿Es nueva recluta?")

    calcular = st.button("Calcular Bono de Buena Siniestralidad")

    if calcular:
        porcentaje_bono = 0
        explicacion = []

        if es_nueva_recluta:
            if prima_total >= 1_360_000:
                explicacion.append("✅ Es nueva recluta y cumple con la prima mínima de $1,360,000.")
                if siniestralidad < 40:
                    porcentaje_bono = 5.0
                elif siniestralidad < 50:
                    porcentaje_bono = 4.0
                elif siniestralidad < 55:
                    porcentaje_bono = 3.0
                elif siniestralidad < 60:
                    porcentaje_bono = 2.5
                elif siniestralidad <= 63:
                    porcentaje_bono = 1.0
                else:
                    porcentaje_bono = 0
                    explicacion.append("❌ Siniestralidad mayor al 63%. No aplica bono.")
            else:
                explicacion.append("❌ No cumple con la prima mínima de $1,360,000 para nueva recluta.")
        else:
            if prima_total >= 1_700_000:
                explicacion.append("✅ Cumple con la prima mínima de $1,700,000.")
                bono = st.number_input("Número de pólizas Cobertura Amplia", min_value=0, step=1) * 100
                bono += st.number_input("Número de pólizas Cobertura Limitada", min_value=0, step=1) * 50
                porcentaje_bono = None  # bono directo, no porcentual
                explicacion.append("✅ Bono directo por número de pólizas.")
            else:
                explicacion.append("❌ No cumple con la prima mínima de $1,700,000 para bono anual tradicional.")

        st.markdown(f"### 🧾 Resultados para {agente.upper()}")
        st.write("**Datos Ingresados:**")
        st.write(f"- Prima total anual Autos: {formatear_pesos(prima_total)}")
        st.write(f"- Siniestralidad: {siniestralidad:.2f}%")
        st.write(f"- Tipo de agente: {'Nueva Recluta' if es_nueva_recluta else 'Agente Regular'}")

        st.write("**Resultado del Bono:**")
        if es_nueva_recluta:
            if porcentaje_bono > 0:
                total_bono = porcentaje_bono * prima_total / 100
                st.success(f"✅ Aplica bono del {porcentaje_bono:.2f}%")
                st.info(f"💰 Total del Bono: {formatear_pesos(total_bono)}")
            else:
                total_bono = 0
                st.error("❌ No aplica bono.")
        else:
            if prima_total >= 1_700_000:
                st.success("✅ Aplica bono directo por pólizas")
                st.info(f"💰 Total del Bono: {formatear_pesos(bono)}")
            else:
                st.error("❌ No aplica bono.")
                bono = 0

        st.markdown("---")
        st.subheader("Explicación:")
        for e in explicacion:
            st.write(f"- {e}")

        st.markdown("---")
        st.markdown("<div style='text-align: center; color: gray;'>Aplican restricciones y condiciones conforme al cuaderno oficial de Afirme Seguros 2025.</div>", unsafe_allow_html=True)

# =========================
# Bono de Siniestralidad en Ramos Especiales
# =========================
if tipo_bono == "Bono de Siniestralidad en Ramos Especiales":
    st.subheader("Bono de Siniestralidad en Ramos Especiales")

    ramo = st.selectbox("Selecciona el ramo:", [
        "Transporte de Carga",
        "Robo de Mercancía",
        "Equipo de Contratista",
        "Dinero y Valores"
    ])
    siniestralidad = st.number_input("Siniestralidad del ramo (%)", min_value=0.0, max_value=100.0, format="%.2f")

    calcular = st.button("Calcular Bono por Siniestralidad en Ramos Especiales")

    if calcular:
        porcentaje_bono = 0
        explicacion = []

        if siniestralidad < 30:
            porcentaje_bono = 100
            explicacion.append("✅ Siniestralidad menor a 30%. Aplica bono completo del 100%.")
        elif 30 <= siniestralidad <= 49.9:
            porcentaje_bono = 50
            explicacion.append("✅ Siniestralidad entre 30.1% y 49.9%. Aplica bono parcial del 50%.")
        else:
            porcentaje_bono = 0
            explicacion.append("❌ Siniestralidad igual o mayor a 50%. No aplica bono.")

        st.markdown(f"### 🧾 Resultados para {agente.upper()}")
        st.write("**Datos Ingresados:**")
        st.write(f"- Ramo: {ramo}")
        st.write(f"- Siniestralidad: {siniestralidad:.2f}%")

        st.write("**Resultado del Bono:**")
        st.write(f"- Porcentaje Bono Aplicado: {porcentaje_bono}%")

        st.markdown("---")
        st.subheader("Explicación:")
        for e in explicacion:
            st.write(f"- {e}")

        st.markdown("---")
        st.markdown("<div style='text-align: center; color: gray;'>Aplican restricciones y condiciones conforme al cuaderno oficial de Afirme Seguros 2025.</div>", unsafe_allow_html=True)

