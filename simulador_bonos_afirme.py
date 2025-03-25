# Simulador de Bonos Afirme 2025 en Streamlit
import streamlit as st

# Función para aplicar formato de miles con pesos
def formatear_pesos(valor):
    try:
        valor = float(valor)
        return "$ {:,.2f}".format(valor)
    except:
        return "$ 0.00"

st.set_page_config(page_title="Simulador Bonos Afirme 2025", layout="centered")

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

if tipo_bono == "Autos (Producción y Crecimiento)":
    prima_neta = st.number_input("Prima neta 2025 de Autos", min_value=0.0, format="%.2f")
    produccion_2024 = st.number_input("Producción Autos 2024", min_value=0.0, format="%.2f")
    produccion_2025 = st.number_input("Producción Autos 2025", min_value=0.0, format="%.2f")
    siniestralidad = st.number_input("Siniestralidad Autos (%)", min_value=0.0, max_value=100.0, format="%.2f")
    calcular = st.button("Calcular Bonos")

    if calcular:
        crecimiento = 0 if produccion_2024 == 0 else ((produccion_2025 - produccion_2024) / produccion_2024) * 100
        crecimiento = max(0, crecimiento)
        produccion_real = prima_neta

        # Bono de producción Autos
        bono_prod = 0
        tabla_prod = [
            (1400001, 6.5, 5.5, 4.5),
            (780001, 5.5, 4.5, 3.5),
            (570001, 4.5, 3.5, 2.5),
            (380001, 4.0, 3.0, 2.0),
            (220001, 3.0, 2.0, 1.0),
            (110001, 2.0, 1.0, 0.0)
        ]
        for minimo, b1, b2, b3 in tabla_prod:
            if produccion_real >= minimo:
                if siniestralidad < 60:
                    bono_prod = b1
                elif siniestralidad <= 75:
                    bono_prod = b2
                else:
                    bono_prod = b3
                break

        # Bono de crecimiento Autos (solo aplica si siniestralidad < 63%)
        bono_cre = 0
        if siniestralidad < 63:
            tabla_cre = [
                (1400001, 2.25, 3.25, 4.25),
                (780001, 2.0, 3.0, 4.0),
                (570001, 1.75, 2.75, 3.75),
                (380001, 1.5, 2.5, 3.5),
                (220001, 1.25, 2.25, 3.25),
                (110001, 1.0, 2.0, 3.0)
            ]
            for minimo, c1, c2, c3 in tabla_cre:
                if produccion_real >= minimo:
                    if crecimiento < 15:
                        bono_cre = c1
                    elif crecimiento < 25:
                        bono_cre = c2
                    else:
                        bono_cre = c3
                    break

        total_bono_prod = produccion_real * bono_prod / 100
        total_bono_cre = (produccion_2025 - produccion_2024) * bono_cre / 100
        total_bono = total_bono_prod + total_bono_cre

        st.markdown(f"## Resultado para {agente}")
        st.markdown("### 📊 Datos Ingresados:")
        st.markdown(f"- Producción 2024: {formatear_pesos(produccion_2024)}")
        st.markdown(f"- Producción 2025: {formatear_pesos(produccion_2025)}")
        st.markdown(f"- Crecimiento Real: {crecimiento:.2f}%")
        st.markdown(f"- Siniestralidad: {siniestralidad:.2f}%")

        st.markdown("### 💲 Resultados de Bono:")
        st.markdown(f"- Bono de Producción: {bono_prod:.2f}% → {formatear_pesos(total_bono_prod)} ✅")
        if siniestralidad < 63:
            st.markdown(f"- Bono de Crecimiento: {bono_cre:.2f}% → {formatear_pesos(total_bono_cre)} ✅")
        else:
            st.markdown("- ❌ No aplica Bono de Crecimiento (Siniestralidad ≥ 63%)")

        st.markdown(f"### 🧾 Total del Bono: **{formatear_pesos(total_bono)}**")

# Pie de página centrado
st.markdown("""
    <hr style='margin-top: 50px;'>
    <div style='text-align: center; color: gray;'>
        Aplican restricciones y condiciones conforme al cuaderno oficial de Afirme Seguros 2025.
    </div>
""", unsafe_allow_html=True)
