import streamlit as st
import pandas as pd
import random
from collections import Counter

st.title("🧠 IA Lotofácil")

file = st.file_uploader("Envie histórico (.xlsx)")

if file:
    df = pd.read_excel(file, engine="openpyxl")
    numeros = df.iloc[:, 1:16].values
    flat = numeros.flatten()

    freq = Counter(flat)

    atraso = {}
    for n in range(1, 26):
        atraso[n] = 0
        for i in range(len(numeros)-1, -1, -1):
            if n in numeros[i]:
                break
            atraso[n] += 1

    peso_freq = st.slider("Peso Frequência", 0.5, 2.0, 1.2)
    peso_atraso = st.slider("Peso Atraso", 0.5, 2.0, 1.0)

    score = {}
    for n in range(1, 26):
        score[n] = freq[n]*peso_freq - atraso[n]*peso_atraso

    ranking = sorted(score, key=score.get, reverse=True)
    base21 = ranking[:21]

    st.write("🎯 Base21:", base21)

    def gerar_jogo():
        while True:
            jogo = sorted(random.sample(base21, 15))
            pares = sum(n % 2 == 0 for n in jogo)
            baixos = sum(n <= 13 for n in jogo)

            if 7 <= pares <= 8 and 8 <= baixos <= 9:
                return jogo

    if st.button("Gerar Jogos"):
        jogos = []
        while len(jogos) < 30:
            j = gerar_jogo()
            if j not in jogos:
                jogos.append(j)

        for i, j in enumerate(jogos, 1):
            st.write(f"Jogo {i}: {j}")
