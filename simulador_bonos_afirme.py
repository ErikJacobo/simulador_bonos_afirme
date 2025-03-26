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

# =========================
# Sección Autos Producción y Crecimiento
# =========================
if tipo_bono == "Autos (Producción y Crecimiento)":
    produccion_2024 = st.number_input("Producción Autos 2024 ($)", min_value=0.0, format="%.2f")
    produccion_2025 = st.number_input("Producción Autos 2025 ($)", min_value=0.0, format="%.2f")
    siniestralidad = st.number_input("Siniestralidad Autos (%)", min_value=0.0, max_value=100.0, format="%.2f")

    calcular = st.button("Calcular Bonos")

    if calcular:
        bono_produccion = 0
        bono_crecimiento = 0
        explicacion = []

        # Bono producción autos
        tramos_produccion = [
            (1400001, 6.5, 5.5, 4.5),
            (780001, 5.5, 4.5, 3.5),
            (570001, 4.5, 3.5, 2.5),
            (380001, 4.0, 3.0, 2.0),
            (220001, 3.0, 2.0, 1.0),
            (110001, 2.0, 1.0, 0.0),
        ]

        for minimo, pct1, pct2, pct3 in tramos_produccion:
            if produccion_2025 >= minimo:
                if siniestralidad < 60:
                    bono_produccion = pct1
                    explicacion.append(f"✅ Aplica bono de producción del {pct1}% por producción ≥ ${minimo:,} y siniestralidad < 60%.")
                elif siniestralidad < 75:
                    bono_produccion = pct2
                    explicacion.append(f"✅ Aplica bono de producción del {pct2}% por producción ≥ ${minimo:,} y siniestralidad entre 60%-75%.")
                else:
                    bono_produccion = pct3
                    explicacion.append(f"✅ Aplica bono de producción del {pct3}% por producción ≥ ${minimo:,} y siniestralidad ≥ 75%.")
                break

        if produccion_2025 < 110001:
            explicacion.append("❌ No alcanza producción mínima de $110,001 para bono de producción.")

        # Bono crecimiento autos
        crecimiento = 0
        if produccion_2024 > 0:
            crecimiento = ((produccion_2025 - produccion_2024) / produccion_2024) * 100
            tramos_crecimiento = [
                (1400001, 2.25, 3.25, 4.25),
                (780001, 2.0, 3.0, 4.0),
                (570001, 1.75, 2.75, 3.75),
                (380001, 1.5, 2.5, 3.5),
                (220001, 1.25, 2.25, 3.25),
                (110001, 1.0, 2.0, 3.0),
            ]
            for minimo, pct10, pct15, pct25 in tramos_crecimiento:
                if produccion_2025 >= minimo:
                    if siniestralidad < 63:
                        if crecimiento >= 25:
                            bono_crecimiento = pct25
                            explicacion.append(f"✅ Aplica bono de crecimiento del {pct25}% por crecimiento ≥ 25% y producción ≥ ${minimo:,}.")
                        elif crecimiento >= 15:
                            bono_crecimiento = pct15
                            explicacion.append(f"✅ Aplica bono de crecimiento del {pct15}% por crecimiento ≥ 15% y producción ≥ ${minimo:,}.")
                        elif crecimiento >= 10:
                            bono_crecimiento = pct10
                            explicacion.append(f"✅ Aplica bono de crecimiento del {pct10}% por crecimiento ≥ 10% y producción ≥ ${minimo:,}.")
                        else:
                            explicacion.append(f"❌ Crecimiento de {crecimiento:.2f}%. No alcanza mínimo del 10% requerido.")
                    else:
                        explicacion.append(f"❌ Siniestralidad {siniestralidad:.2f}% excede el máximo del 63% para aplicar al bono de crecimiento.")
                    break
        else:
            explicacion.append("❌ Producción 2024 no registrada. No se puede calcular crecimiento.")

        total_bono = (bono_produccion + bono_crecimiento) * produccion_2025 / 100

        st.markdown(f"### 🧾 Resultados para {agente}:")
        st.write("**Datos Ingresados:**")
        st.write(f"- Producción 2024 Autos: {formatear_pesos(produccion_2024)}")
        st.write(f"- Producción 2025 Autos: {formatear_pesos(produccion_2025)}")
        st.write(f"- Crecimiento: {crecimiento:.2f}%")
        st.write(f"- Siniestralidad: {siniestralidad:.2f}%")

        st.write("**Resultados del Bono:**")
        st.write(f"- Bono Producción: {bono_produccion:.2f}%")
        st.write(f"- Bono Crecimiento: {bono_crecimiento:.2f}%")
        st.success(f"🟢 Total del Bono: {formatear_pesos(total_bono)}")

        st.markdown("---")
        st.subheader("Explicaciones:")
        for e in explicacion:
            st.write(e)

        st.markdown("---")
        st.markdown("<div style='text-align: center; color: gray;'>Aplican restricciones y condiciones conforme al cuaderno oficial de Afirme Seguros 2025.</div>", unsafe_allow_html=True)


# =========================
# Sección Daños Producción y Crecimiento
# =========================
if tipo_bono == "Daños (Producción y Crecimiento)":
    produccion_2024 = st.number_input("Producción Daños 2024 ($)", min_value=0.0, format="%.2f")
    produccion_2025 = st.number_input("Producción Daños 2025 ($)", min_value=0.0, format="%.2f")
    siniestralidad = st.number_input("Siniestralidad Daños (%)", min_value=0.0, max_value=100.0, format="%.2f")

    calcular = st.button("Calcular Bonos")

    if calcular:
        bono_produccion = 0
        bono_crecimiento = 0
        explicacion = []

        # Bono producción daños
        tramos_produccion = [
            (650001, 6.0, 5.0),
            (410001, 5.0, 4.0),
            (290001, 4.0, 3.0),
            (125001, 3.0, 2.0),
            (75001, 2.0, 1.0),
        ]
        for minimo, pct1, pct2 in tramos_produccion:
            if produccion_2025 >= minimo:
                if siniestralidad < 50:
                    bono_produccion = pct1
                    explicacion.append(f"✅ Aplica bono de producción del {pct1}% por producción ≥ ${minimo:,} y siniestralidad < 50%.")
                else:
                    bono_produccion = pct2
                    explicacion.append(f"✅ Aplica bono de producción del {pct2}% por producción ≥ ${minimo:,} y siniestralidad ≥ 50%.")
                break

        if produccion_2025 < 75001:
            explicacion.append("❌ No alcanza producción mínima de $75,001 para bono de producción.")

        # Bono crecimiento daños
        crecimiento = 0
        if produccion_2024 > 0:
            crecimiento = ((produccion_2025 - produccion_2024) / produccion_2024) * 100
            tramos_crecimiento = [
                (650001, 3.0, 4.0, 5.0),
                (410001, 2.5, 3.5, 4.5),
                (290001, 2.0, 3.0, 4.0),
                (125001, 1.5, 2.5, 3.5),
                (75001, 1.0, 2.0, 3.0),
            ]
            for minimo, pct10, pct15, pct20 in tramos_crecimiento:
                if produccion_2025 >= minimo:
                    if crecimiento >= 20:
                        bono_crecimiento = pct20
                        explicacion.append(f"✅ Aplica bono de crecimiento del {pct20}% por crecimiento ≥ 20% y producción ≥ ${minimo:,}.")
                    elif crecimiento >= 15:
                        bono_crecimiento = pct15
                        explicacion.append(f"✅ Aplica bono de crecimiento del {pct15}% por crecimiento ≥ 15% y producción ≥ ${minimo:,}.")
                    elif crecimiento >= 10:
                        bono_crecimiento = pct10
                        explicacion.append(f"✅ Aplica bono de crecimiento del {pct10}% por crecimiento ≥ 10% y producción ≥ ${minimo:,}.")
                    else:
                        explicacion.append(f"❌ Crecimiento de {crecimiento:.2f}%. No alcanza el mínimo del 10% requerido.")
                    break
        else:
            explicacion.append("❌ Producción 2024 no registrada. No se puede calcular crecimiento.")

        total_bono = (bono_produccion + bono_crecimiento) * produccion_2025 / 100

        st.markdown(f"### 🧾 Resultados para {agente}:")
        st.write("**Datos Ingresados:**")
        st.write(f"- Producción 2024 Daños: {formatear_pesos(produccion_2024)}")
        st.write(f"- Producción 2025 Daños: {formatear_pesos(produccion_2025)}")
        st.write(f"- Crecimiento: {crecimiento:.2f}%")
        st.write(f"- Siniestralidad: {siniestralidad:.2f}%")

        st.write("**Resultados del Bono:**")
        st.write(f"- Bono Producción: {bono_produccion:.2f}%")
        st.write(f"- Bono Crecimiento: {bono_crecimiento:.2f}%")
        st.success(f"🟢 Total del Bono: {formatear_pesos(total_bono)}")

        st.markdown("---")
        st.subheader("Explicaciones:")
        for e in explicacion:
            st.write(e)

        st.markdown("---")
        st.markdown("<div style='text-align: center; color: gray;'>Aplican restricciones y condiciones conforme al cuaderno oficial de Afirme Seguros 2025.</div>", unsafe_allow_html=True)

# =========================
# Bono Vida Grupo
# =========================
if tipo_bono == "Vida Grupo":
    prima_vida = st.number_input("Prima neta 2025 Vida Grupo ($)", min_value=0.0, format="%.2f")
    calcular = st.button("Calcular Bono Vida Grupo")

    if calcular:
        porcentaje_bono = 0
        explicacion = []

        tramos_vida = [
            (400001, float('inf'), 3.0),
            (300001, 400001, 2.5),
            (200001, 300001, 2.0),
            (100001, 200001, 1.5),
            (50000, 100001, 1.0)
        ]

        for minimo, maximo, pct in tramos_vida:
            if minimo <= prima_vida < maximo:
                porcentaje_bono = pct
                break

        if porcentaje_bono > 0:
            explicacion.append(f"✅ Aplica bono del {porcentaje_bono:.1f}% por estar en el rango de prima correspondiente.")
        else:
            explicacion.append("❌ No alcanza el rango mínimo de prima ($50,000) para aplicar al bono.")

        total_bono = porcentaje_bono * prima_vida / 100

        st.markdown(f"### 🧾 Resultados para {agente}")
        st.write("**Datos Ingresados:**")
        st.write(f"- Prima Vida Grupo: {formatear_pesos(prima_vida)}")

        st.write("**Resultado del Bono:**")
        st.write(f"- Porcentaje Bono Aplicado: {porcentaje_bono:.1f}%")
        st.success(f"🟢 Total del Bono: {formatear_pesos(total_bono)}")

        st.markdown("---")
        st.subheader("Explicación:")
        for e in explicacion:
            st.write(e)

        st.markdown("---")
        st.markdown("<div style='text-align: center; color: gray;'>Aplican restricciones y condiciones conforme al cuaderno oficial de Afirme Seguros 2025.</div>", unsafe_allow_html=True)

# =========================
# Bono Nueva Recluta: Autos, Daños o Vida
# =========================
if tipo_bono == "Nueva Recluta: Autos, Daños o Vida":
    ramo_recluta = st.selectbox("Selecciona el ramo:", ["Autos", "Daños", "Vida Grupo"], key="recluta_ramo")
    prima_recluta = st.number_input(f"Prima neta 2025 ({ramo_recluta})", min_value=0.0, format="%.2f", key="prima_recluta")

    if ramo_recluta in ["Autos", "Daños"]:
        siniestralidad_recluta = st.number_input("Siniestralidad (%)", min_value=0.0, max_value=100.0, format="%.2f")

    calcular_recluta = st.button("Calcular Bono Nueva Recluta")

    if calcular_recluta:
        bono_pct = 0
        explicacion = []

        if ramo_recluta == "Autos":
            tramos = [
                (1120001, float('inf'), 6.5, 5.5, 4.5),
                (624001, 1120000, 5.5, 4.5, 3.5),
                (456001, 624000, 4.5, 3.5, 2.5),
                (304001, 456000, 4.0, 3.0, 2.0),
                (176001, 304000, 3.0, 2.0, 1.0),
                (88000, 176000, 2.0, 1.0, 0.0)
            ]
            for minimo, maximo, pct1, pct2, pct3 in tramos:
                if minimo <= prima_recluta <= maximo:
                    if siniestralidad_recluta < 60:
                        bono_pct = pct1
                        explicacion.append(f"✅ Prima entre {formatear_pesos(minimo)} y {formatear_pesos(maximo)} con siniestralidad < 60%.")
                    elif siniestralidad_recluta <= 75:
                        bono_pct = pct2
                        explicacion.append(f"✅ Prima entre {formatear_pesos(minimo)} y {formatear_pesos(maximo)} con siniestralidad entre 60% y 75%.")
                    else:
                        bono_pct = pct3
                        explicacion.append(f"✅ Prima entre {formatear_pesos(minimo)} y {formatear_pesos(maximo)} con siniestralidad mayor al 75%.")
                    break

        elif ramo_recluta == "Daños":
            tramos = [
                (520001, float('inf'), 6.0, 5.0),
                (328001, 520000, 5.0, 4.0),
                (232001, 328000, 4.0, 3.0),
                (100001, 232000, 3.0, 2.0),
                (60000, 100000, 2.0, 1.0)
            ]
            for minimo, maximo, pct1, pct2 in tramos:
                if minimo <= prima_recluta <= maximo:
                    if siniestralidad_recluta < 50:
                        bono_pct = pct1
                        explicacion.append(f"✅ Prima entre {formatear_pesos(minimo)} y {formatear_pesos(maximo)} con siniestralidad < 50%.")
                    else:
                        bono_pct = pct2
                        explicacion.append(f"✅ Prima entre {formatear_pesos(minimo)} y {formatear_pesos(maximo)} con siniestralidad ≥ 50%.")
                    break

        elif ramo_recluta == "Vida Grupo":
            tramos = [
                (320001, float('inf'), 3.0),
                (240001, 320000, 2.5),
                (160001, 240000, 2.0),
                (80001, 160000, 1.5)
            ]
            for minimo, maximo, pct in tramos:
                if minimo <= prima_recluta <= maximo:
                    bono_pct = pct
                    explicacion.append(f"✅ Prima entre {formatear_pesos(minimo)} y {formatear_pesos(maximo)}.")
                    break

        if bono_pct == 0:
            explicacion.append("❌ No se alcanzó la prima mínima requerida para aplicar al bono en este ramo.")

        total_bono = prima_recluta * bono_pct / 100

        st.markdown(f"### 🧾 Resultados para {agente}")
        st.write("**Datos Ingresados:**")
        st.write(f"- Ramo: {ramo_recluta}")
        st.write(f"- Prima 2025: {formatear_pesos(prima_recluta)}")
        if ramo_recluta in ["Autos", "Daños"]:
            st.write(f"- Siniestralidad: {siniestralidad_recluta:.2f}%")

        st.write("**Resultado del Bono:**")
        st.write(f"- Bono Aplicado: {bono_pct:.2f}%")
        st.success(f"🟢 Total del Bono: {formatear_pesos(total_bono)}")

        st.markdown("---")
        st.subheader("Explicaciones:")
        for e in explicacion:
            st.write(e)

        st.markdown("---")
        st.markdown("<div style='text-align: center; color: gray;'>Aplican restricciones y condiciones conforme al cuaderno oficial de Afirme Seguros 2025.</div>", unsafe_allow_html=True)

# =========================
# Bono Anual por Buena Siniestralidad Autos
# =========================
if tipo_bono == "Bono Anual por Buena Siniestralidad Autos":
    prima_total = st.number_input("Prima neta total anual Autos ($)", min_value=0.0, format="%.2f")
    es_nueva_recluta = st.checkbox("¿Es nueva recluta?")
    siniestralidad = None
    polizas_amplia = 0
    polizas_limitada = 0

    if es_nueva_recluta:
        siniestralidad = st.number_input("Siniestralidad anual Autos (%)", min_value=0.0, max_value=100.0, format="%.2f")
    else:
        polizas_amplia = st.number_input("Número de pólizas Cobertura Amplia", min_value=0, step=1)
        polizas_limitada = st.number_input("Número de pólizas Cobertura Limitada", min_value=0, step=1)

    calcular = st.button("Calcular Bono de Buena Siniestralidad")

    if calcular:
        explicacion = []
        bono = 0

        if es_nueva_recluta:
            if prima_total >= 1360000:
                if siniestralidad < 40:
                    bono_pct = 5.0
                elif siniestralidad < 50:
                    bono_pct = 4.0
                elif siniestralidad < 55.1:
                    bono_pct = 3.0
                elif siniestralidad < 60:
                    bono_pct = 2.5
                elif siniestralidad <= 63:
                    bono_pct = 1.0
                else:
                    bono_pct = 0

                bono = prima_total * bono_pct / 100
                if bono_pct > 0:
                    explicacion.append(f"✅ Nueva recluta: Aplica bono del {bono_pct}% por siniestralidad de {siniestralidad:.2f}%.")
                else:
                    explicacion.append("❌ No aplica bono: Siniestralidad mayor al 63%.")
            else:
                explicacion.append("❌ No alcanza prima mínima de $1,360,000 como nueva recluta.")
        else:
            if prima_total >= 1700000:
                bono = polizas_amplia * 100 + polizas_limitada * 50
                explicacion.append(f"✅ Bono calculado: {polizas_amplia} x $100 + {polizas_limitada} x $50 = {formatear_pesos(bono)}")
            else:
                explicacion.append("❌ No alcanza prima mínima de $1,700,000.")

        st.markdown(f"### 🧾 Resultados para {agente}")
        st.write("**Datos Ingresados:**")
        st.write(f"- Prima total anual Autos: {formatear_pesos(prima_total)}")
        if es_nueva_recluta:
            st.write(f"- Siniestralidad: {siniestralidad:.2f}%")
        else:
            st.write(f"- Pólizas Amplia: {polizas_amplia}")
            st.write(f"- Pólizas Limitada: {polizas_limitada}")

        st.write("**Resultado del Bono:**")
        st.write(f"- Total Bono: {formatear_pesos(bono)}")

        st.markdown("---")
        st.subheader("Explicaciones:")
        for e in explicacion:
            st.write(e)

        st.markdown("---")
        st.markdown("<div style='text-align: center; color: gray;'>Aplican restricciones y condiciones conforme al cuaderno oficial de Afirme Seguros 2025.</div>", unsafe_allow_html=True)


# =========================
# Bono de Siniestralidad en Ramos Especiales
# =========================
if tipo_bono == "Bono de Siniestralidad en Ramos Especiales":
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
        if siniestralidad < 30:
            porcentaje_bono = 100
            mensaje = "✅ Aplica bono completo del 100% por siniestralidad < 30%."
        elif siniestralidad < 50:
            porcentaje_bono = 50
            mensaje = "✅ Aplica bono parcial del 50% por siniestralidad entre 30.1% y 49.9%."
        else:
            mensaje = "❌ No aplica bono por siniestralidad ≥ 50%."

        st.markdown(f"### 🧾 Resultados para {agente}")
        st.write("**Datos Ingresados:**")
        st.write(f"- Ramo: {ramo}")
        st.write(f"- Siniestralidad: {siniestralidad:.2f}%")

        st.write("**Resultado del Bono:**")
        st.write(f"- Porcentaje Bono Aplicado: {porcentaje_bono}%")

        st.markdown("---")
        st.subheader("Explicación:")
        st.write(mensaje)

        st.markdown("---")
        st.markdown("<div style='text-align: center; color: gray;'>Aplican restricciones y condiciones conforme al cuaderno oficial de Afirme Seguros 2025.</div>", unsafe_allow_html=True)
