import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Perceptrón Interactivo", page_icon="🧠", layout="wide")

st.title("🧠 Máquina Perceptrón Interactiva")
st.markdown("### Inspirada en la máquina física de Rosenblatt (1957)")
st.markdown("---")

st.markdown("""
**¿Cómo funciona?**
- Activa o desactiva las entradas con los botones ON/OFF
- Define si quieres que cada combinación sea ✅ Positiva o ❌ Negativa
- Ajusta las perillas (sliders) de los pesos w₁, w₂ y el Bias
- Observa en tiempo real cómo cambia la frontera de decisión
- ¡Tu objetivo es clasificar correctamente los 4 patrones!
""")

st.markdown("---")

# ============================================================
# SECCIÓN 1: CONFIGURACIÓN DE PATRONES
# ============================================================
st.header("🔘 Paso 1: Configura los 4 patrones de entrada")
st.markdown("Cada fila es una combinación posible de las dos entradas. Actívalas y define su etiqueta deseada.")

patrones = [
    {"nombre": "Patrón 1", "x1_default": False, "x2_default": False},
    {"nombre": "Patrón 2", "x1_default": True,  "x2_default": False},
    {"nombre": "Patrón 3", "x1_default": False,  "x2_default": True},
    {"nombre": "Patrón 4", "x1_default": True,  "x2_default": True},
]

entradas = []
etiquetas = []

for i, p in enumerate(patrones):
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    with col1:
        st.markdown(f"**{p['nombre']}**")
    with col2:
        x1 = st.checkbox(f"Entrada 1 (x₁)", value=p["x1_default"], key=f"x1_{i}")
    with col3:
        x2 = st.checkbox(f"Entrada 2 (x₂)", value=p["x2_default"], key=f"x2_{i}")
    with col4:
        etiqueta = st.radio(
            f"Etiqueta deseada",
            options=["✅ Positiva (+1)", "❌ Negativa (-1)"],
            key=f"etiqueta_{i}",
            horizontal=True
        )

    x1_val = 1.0 if x1 else -1.0
    x2_val = 1.0 if x2 else -1.0
    etiqueta_val = 1 if "Positiva" in etiqueta else -1

    entradas.append((x1_val, x2_val))
    etiquetas.append(etiqueta_val)

st.markdown("---")

# ============================================================
# SECCIÓN 2: PERILLAS (SLIDERS)
# ============================================================
st.header("🎛️ Paso 2: Ajusta las perillas manualmente")
st.markdown("Mueve los sliders para cambiar los pesos. ¡Tú eres el algoritmo de aprendizaje!")

col1, col2, col3 = st.columns(3)
with col1:
    w1 = st.slider("⚙️ Peso w₁", min_value=-5.0, max_value=5.0, value=0.0, step=0.1)
with col2:
    w2 = st.slider("⚙️ Peso w₂", min_value=-5.0, max_value=5.0, value=0.0, step=0.1)
with col3:
    bias = st.slider("⚙️ Bias (b)", min_value=-5.0, max_value=5.0, value=0.0, step=0.1)

st.markdown("---")

# ============================================================
# SECCIÓN 3: RESULTADOS EN TIEMPO REAL
# ============================================================
st.header("📊 Paso 3: Resultados en tiempo real")

correctos = 0
resultados = []

for i, ((x1_val, x2_val), etiqueta_val) in enumerate(zip(entradas, etiquetas)):
    suma = w1 * x1_val + w2 * x2_val + bias
    salida = 1 if suma >= 0 else -1
    correcto = salida == etiqueta_val
    if correcto:
        correctos += 1
    resultados.append({
        "patron": i + 1,
        "x1": x1_val,
        "x2": x2_val,
        "suma": suma,
        "salida": salida,
        "etiqueta": etiqueta_val,
        "correcto": correcto
    })

col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Tabla de resultados")
    for r in resultados:
        estado = "✅" if r["correcto"] else "❌"
        salida_texto = "POSITIVO (+1)" if r["salida"] == 1 else "NEGATIVO (-1)"
        etiqueta_texto = "POSITIVO (+1)" if r["etiqueta"] == 1 else "NEGATIVO (-1)"
        st.markdown(f"""
        **Patrón {r['patron']}** {estado}
        - x₁ = {r['x1']} | x₂ = {r['x2']}
        - Suma ponderada: `{r['suma']:.2f}`
        - Salida del perceptrón: **{salida_texto}**
        - Etiqueta deseada: **{etiqueta_texto}**
        ---
        """)

with col2:
    st.subheader("🎯 Marcador")
    porcentaje = (correctos / 4) * 100
    st.metric(label="Patrones correctos", value=f"{correctos} / 4")
    st.progress(correctos / 4)

    if correctos == 4:
        st.success("🏆 ¡Felicitaciones! ¡Clasificaste todos los patrones correctamente!")
        st.balloons()
    elif correctos == 3:
        st.warning("😊 ¡Casi! Solo te falta 1 patrón. Sigue ajustando las perillas.")
    elif correctos == 2:
        st.warning("💪 Vas por la mitad. Sigue intentando.")
    else:
        st.error("🔧 Sigue ajustando las perillas. ¡Tú puedes!")

    st.markdown("---")
    st.subheader("🔢 Pesos actuales")
    st.markdown(f"""
    - **w₁** = {w1}
    - **w₂** = {w2}
    - **Bias** = {bias}
    - **Fórmula:** salida = {w1}·x₁ + {w2}·x₂ + {bias}
    """)

st.markdown("---")

# ============================================================
# SECCIÓN 4: GRÁFICA FRONTERA DE DECISIÓN
# ============================================================
st.header("📈 Frontera de decisión en tiempo real")
st.markdown("La línea azul separa la región POSITIVA (arriba) de la región NEGATIVA (abajo).")

fig, ax = plt.subplots(figsize=(7, 7))
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_xlabel("Entrada x₁", fontsize=12)
ax.set_ylabel("Entrada x₂", fontsize=12)
ax.set_title("Frontera de Decisión del Perceptrón", fontsize=14)
ax.axhline(0, color='gray', linewidth=0.5)
ax.axvline(0, color='gray', linewidth=0.5)
ax.grid(True, linestyle='--', alpha=0.4)

# Dibujar frontera de decisión
x_line = np.linspace(-2, 2, 300)
if abs(w2) > 0.001:
    y_line = (-w1 * x_line - bias) / w2
    ax.plot(x_line, y_line, 'b-', linewidth=2.5, label="Frontera de decisión")
else:
    if abs(w1) > 0.001:
        x_frontera = -bias / w1
        ax.axvline(x=x_frontera, color='blue', linewidth=2.5, label="Frontera de decisión")
    else:
        ax.text(0, 0, "⚠️ Ajusta los pesos", ha='center', fontsize=12, color='red')

# Colorear regiones
xx, yy = np.meshgrid(np.linspace(-2, 2, 200), np.linspace(-2, 2, 200))
Z = w1 * xx + w2 * yy + bias
ax.contourf(xx, yy, Z, levels=[-1000, 0, 1000],
            colors=['#ffcccc', '#ccffcc'], alpha=0.3)

# Dibujar puntos
for r in resultados:
    color = 'green' if r['etiqueta'] == 1 else 'red'
    marker = 'o' if r['etiqueta'] == 1 else 's'
    borde = 'black' if r['correcto'] else 'orange'
    grosor = 2 if r['correcto'] else 3
    ax.scatter(r['x1'], r['x2'], c=color, marker=marker,
               s=200, zorder=5, edgecolors=borde, linewidths=grosor)
    ax.annotate(f"P{r['patron']}", (r['x1'], r['x2']),
                textcoords="offset points", xytext=(10, 10), fontsize=11)

from matplotlib.patches import Patch
from matplotlib.lines import Line2D
leyenda = [
    Patch(facecolor='green', label='Etiqueta Positiva (+1)'),
    Patch(facecolor='red', label='Etiqueta Negativa (-1)'),
    Line2D([0], [0], color='blue', linewidth=2, label='Frontera de decisión'),
    Patch(facecolor='#ccffcc', alpha=0.5, label='Región positiva'),
    Patch(facecolor='#ffcccc', alpha=0.5, label='Región negativa'),
]
ax.legend(handles=leyenda, loc='upper right', fontsize=9)

st.pyplot(fig)

st.markdown("---")
st.markdown("🎓 **Aplicación desarrollada para la asignatura: Autómatas, Gramáticas y Lenguaje - IU Digital de Antioquia**")
