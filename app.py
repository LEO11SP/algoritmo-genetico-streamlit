import streamlit as st
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🧬 Algoritmo Genético Simple – Visual Paso a Paso")

# =========================
# SIDEBAR
# =========================
st.sidebar.header("Parámetros")
funcion_txt = st.sidebar.text_input("Función f(x)", "1 + x")
PROB_MUT = st.sidebar.slider("Prob. mutación", 0.0, 1.0, 0.1)
POB = st.sidebar.slider("Población", 4, 20, 8)
ELITE = st.sidebar.slider("Elitismo", 1, 2, 1)

# =========================
# ESTADO
# =========================
if "poblacion" not in st.session_state:
    st.session_state.poblacion = []
if "fitness" not in st.session_state:
    st.session_state.fitness = []
if "gen" not in st.session_state:
    st.session_state.gen = 0
if "seleccionados" not in st.session_state:
    st.session_state.seleccionados = []

# =========================
# FUNCIONES
# =========================
def f(x):
    return eval(funcion_txt)

def fitness(x):
    return abs(f(x))   # minimizar |f(x)| → buscar raíz

def binario(x):
    return format((x + 128) % 256, "08b")

# =========================
# BOTÓN 1 – POBLACIÓN
# =========================
if st.button("1️⃣ Generar población"):
    st.session_state.poblacion = [random.randint(-10, 10) for _ in range(POB)]
    st.session_state.fitness = []
    st.session_state.seleccionados = []

# =========================
# MOSTRAR POBLACIÓN
# =========================
if st.session_state.poblacion:
    st.subheader("Población")
    st.table(pd.DataFrame({
        "Decimal": st.session_state.poblacion,
        "Binario": [binario(x) for x in st.session_state.poblacion]
    }))

# =========================
# BOTÓN 2 – FITNESS
# =========================
if st.button("2️⃣ Evaluar fitness"):
    st.session_state.fitness = [fitness(x) for x in st.session_state.poblacion]

if st.session_state.fitness:
    st.subheader("Fitness")
    st.table(pd.DataFrame({
        "x": st.session_state.poblacion,
        "|f(x)|": st.session_state.fitness
    }))

# =========================
# BOTÓN 3 – SELECCIÓN ORDENADA
# =========================
if st.button("3️⃣ Selección (Ordenado + Sándwich)"):

    # Crear DataFrame conjunto
    df = pd.DataFrame({
        "x": st.session_state.poblacion,
        "fitness": st.session_state.fitness
    })

    # Ordenar de MEJOR a PEOR fitness
    df_ordenado = df.sort_values(by="fitness", ascending=True)

    st.subheader("Ordenados por Fitness (Mejor → Peor)")
    st.table(df_ordenado)

    # Selección sándwich
    elite = df_ordenado["x"].iloc[:ELITE].tolist()
    resto = df_ordenado["x"].iloc[ELITE:].tolist()

    st.session_state.seleccionados = elite + resto[::-1]

    st.subheader("Seleccionados (Sándwich)")
    st.write(st.session_state.seleccionados)

# =========================
# BOTÓN 4 – CRUZA
# =========================
if st.button("4️⃣ Cruza"):
    hijos = []
    sel = st.session_state.seleccionados

    for i in range(len(sel)//2):
        p1 = binario(sel[i])
        p2 = binario(sel[-(i+1)])
        corte = random.randint(1, 6)

        hijo = p1[:corte] + p2[corte:]
        hijos.append(int(hijo, 2) - 128)

        st.write(f"{p1} × {p2} → {hijo}")

    st.session_state.poblacion = hijos
    st.session_state.fitness = []

# =========================
# BOTÓN 5 – MUTACIÓN
# =========================
if st.button("5️⃣ Mutación"):
    nueva = []
    for x in st.session_state.poblacion:
        bits = binario(x)
        if random.random() < PROB_MUT:
            pos = random.randint(0, 7)
            bits = bits[:pos] + ('1' if bits[pos]=='0' else '0') + bits[pos+1:]
        nueva.append(int(bits, 2) - 128)

    st.session_state.poblacion = nueva
    st.session_state.fitness = []

# =========================
# BOTÓN 6 – GENERACIÓN
# =========================
if st.button("➡️ Siguiente generación"):
    st.session_state.gen += 1
    st.success(f"Generación {st.session_state.gen}")
