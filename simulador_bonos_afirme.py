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
st.title("Simulador de Bonos")
st.subheader("Afirme 2025")

st.markdown("---")
agente = st.text_input("Nombre del Agente")
tipo_bono = st.selectbox("Selecciona la sección a calcular:", [
    "Autos (Producción y Crecimiento)",
    "Daños (Producción y Crecimiento)",
    "Vida Grupo",
    "Bono Anual por Buena Siniestralidad Autos",
    "Bono de Siniestralidad en Ramos Especiales"
])

es_nueva_recluta = st.checkbox("¿Es nueva recluta?")
st.markdown("---")

if tipo_bono == "Daños (Producción y Crecimiento)":
    prima_danos = st.number_input("Prima participante Daños 2025", min_value=0.0, format="%.2f")
    produccion_2024 = st.number_input("Producción Daños 2024", min_value=0.0, format="%.2f")
    siniestralidad = st.number_input("Siniestralidad Daños (%)", min_value=0.0, max_value=100.0, format="%.2f")

    calcular = st.button("Calcular Bonos")

    if calcular:
        bono_produccion = 0
        bono_crecimiento = 0
        explicacion = []

        tramos_produccion = [
            (650001, 6.0, 5.0),
            (410001, 5.0, 4.0),
            (290001, 4.0, 3.0),
            (125001, 3.0, 2.0),
            (75001, 2.0, 1.0),
        ]

        for minimo, pct1, pct2 in tramos_produccion:
            if prima_danos >= minimo:
                if siniestralidad < 50:
                    bono_produccion = pct1
                else:
                    bono_produccion = pct2
                break

        if prima_danos < 75001:
            explicacion.append("❌ No alcanza prima mínima para bono de producción de daños.")
        else:
            explicacion.append(f"✅ Bono de producción daños aplicado: {bono_produccion}%")

        if produccion_2024 > 0:
            crecimiento = ((prima_danos - produccion_2024) / produccion_2024) * 100
            tramos_crecimiento = [
                (650001, 3.0, 4.0, 5.0),
                (410001, 2.5, 3.5, 4.5),
                (290001, 2.0, 3.0, 4.0),
                (125001, 1.5, 2.5, 3.5),
                (75001, 1.0, 2.0, 3.0),
            ]
            for minimo, pct10, pct15, pct20 in tramos_crecimiento:
                if prima_danos >= minimo:
                    if crecimiento >= 20:
                        bono_crecimiento = pct20
                    elif crecimiento >= 15:
                        bono_crecimiento = pct15
                    elif crecimiento >= 10:
                        bono_crecimiento = pct10
                    break
            if crecimiento >= 10:
                explicacion.append(f"✅ Bono de crecimiento daños aplicado: {bono_crecimiento}% (Crecimiento: {crecimiento:.2f}%)")
            else:
                explicacion.append(f"❌ No alcanza el mínimo de 10% de crecimiento (Actual: {crecimiento:.2f}%)")
        else:
            explicacion.append("❌ Producción 2024 no registrada. No se puede calcular crecimiento.")

        if es_nueva_recluta:
            bono_produccion *= 1.25
            bono_crecimiento *= 1.25
            explicacion.append("✨ Aplicado potenciador del 125% por ser nueva recluta.")

        total_bono = (bono_produccion + bono_crecimiento) * prima_danos / 100

        st.markdown("### Resultados")
        st.write(f"**Agente:** {agente}")
        st.write(f"**Bono Producción Daños:** {bono_produccion:.2f}%")
        st.write(f"**Bono Crecimiento Daños:** {bono_crecimiento:.2f}%")
        st.write(f"**Total bono ganado:** {formatear_pesos(total_bono)}")
        st.markdown("---")
        st.subheader("Explicación")
        for e in explicacion:
            st.write(e)

elif tipo_bono == "Vida Grupo":
    prima_vida = st.number_input("Prima neta 2025 Vida Grupo", min_value=0.0, format="%.2f")
    calcular = st.button("Calcular Bono Vida")

    if calcular:
        porcentaje_bono = 0
        explicacion = []

        tramos_vida = [
            (320001, 3.0),
            (240001, 2.5),
            (160001, 2.0),
            (80001, 1.5),
        ]

        for minimo, pct in tramos_vida:
            if prima_vida >= minimo:
                porcentaje_bono = pct
                break

        if prima_vida < 80001:
            explicacion.append("❌ No alcanza prima mínima para aplicar bono en Vida Grupo.")
        else:
            explicacion.append(f"✅ Bono de producción Vida Grupo aplicado: {porcentaje_bono}%")

        total_bono = porcentaje_bono * prima_vida / 100

        st.markdown("### Resultados")
        st.write(f"**Agente:** {agente}")
        st.write(f"**Bono Vida Grupo:** {porcentaje_bono:.2f}%")
        st.write(f"**Total bono ganado:** {formatear_pesos(total_bono)}")
        st.markdown("---")
        st.subheader("Explicación")
        for e in explicacion:
            st.write(e)

elif tipo_bono == "Bono Anual por Buena Siniestralidad Autos":
    prima_total = st.number_input("Prima neta total anual Autos", min_value=0.0, format="%.2f")
    polizas_amplia = st.number_input("Número de pólizas Cobertura Amplia", min_value=0, step=1)
    polizas_limitada = st.number_input("Número de pólizas Cobertura Limitada", min_value=0, step=1)
    calcular = st.button("Calcular Bono Anual")

    if calcular:
        explicacion = []
        aplica = False

        if es_nueva_recluta and prima_total >= 1360000:
            aplica = True
        elif not es_nueva_recluta and prima_total >= 1700000:
            aplica = True

        if aplica:
            bono = polizas_amplia * 100 + polizas_limitada * 50
            explicacion.append("✅ Aplica bono por buena siniestralidad autos.")
        else:
            bono = 0
            explicacion.append("❌ No cumple con la prima mínima anual para aplicar bono de siniestralidad.")

        st.markdown("### Resultados")
        st.write(f"**Agente:** {agente}")
        st.write(f"**Total bono ganado:** {formatear_pesos(bono)}")
        st.markdown("---")
        st.subheader("Explicación")
        for e in explicacion:
            st.write(e)

elif tipo_bono == "Bono de Siniestralidad en Ramos Especiales":
    ramo = st.selectbox("Selecciona el ramo:", ["Transporte de carga", "Robo de mercancía", "Equipo de contratista", "Dinero y Valores"])
    siniestralidad = st.number_input("Siniestralidad del ramo (%)", min_value=0.0, max_value=100.0, format="%.2f")
    calcular = st.button("Calcular Bono Especial")

    if calcular:
        porcentaje_bono = 0

        if siniestralidad < 30:
            porcentaje_bono = 100
        elif siniestralidad < 50:
            porcentaje_bono = 50
        else:
            porcentaje_bono = 0

        st.markdown("### Resultados")
        st.write(f"**Agente:** {agente}")
        st.write(f"**Ramo:** {ramo}")
        st.write(f"**Siniestralidad:** {siniestralidad}%")
        st.write(f"**% Bono aplicado:** {porcentaje_bono}%")
        st.markdown("---")
        if porcentaje_bono > 0:
            st.success("✅ Aplica bono anual por siniestralidad baja.")
        else:
            st.error("❌ Siniestralidad igual o mayor a 50%. No aplica bono.")
