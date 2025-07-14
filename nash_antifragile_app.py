import streamlit as st
import pandas as pd

st.set_page_config(page_title="Distribuzione Nash-Antifragile", layout="centered")
st.title("💎 Distribuzione Meritocratica Nash-Antifragile")

st.markdown("Inserisci i dati dei partecipanti e parametri della distribuzione:")

# Parametri
n = st.number_input("Numero di partecipanti", min_value=1, value=5)
m = st.number_input("Numero di criteri", min_value=1, value=3)
soglia = st.number_input("Soglia minima (s)", min_value=0.0, value=50.0)
premio_totale = st.number_input("Montepremi (P)", min_value=0.0, value=100.0)

# Recupera i testi localizzati per la lingua scelta
t = testi[codice]

st.subheader(t["pesi"])

# Slider per ogni criterio, con etichetta dinamica
pesi = [st.slider(f"{t['pesi']} {k+1}", 0.0, 1.0, 1.0/m, key=f"peso_{k}") for k in range(m)]

# Calcola la somma totale dei pesi prima della normalizzazione
peso_tot = sum(pesi)

# Mostra la somma grezza all'utente
st.markdown(f"{t['somma_pesi']}: **{round(peso_tot, 3)}**")

# Normalizza i pesi
pesi = [p / peso_tot for p in pesi]

# Conferma che sono stati normalizzati
st.markdown(t["normalizzazione"])

# Inserimento punteggi
dati = []
for i in range(n):
    st.markdown(f"**Partecipante {i+1}**")
    nome = st.text_input(f"Nome", value=f"Partecipante {i+1}", key=f"nome_{i}")
    punteggi = [st.number_input(f"Punteggio Criterio {k+1}", key=f"{i}_{k}") for k in range(m)]
    dati.append({"nome": nome, "punteggi": punteggi})

# Calcolo punteggio aggregato
for d in dati:
    d["vi"] = sum(p * w for p, w in zip(d["punteggi"], pesi))

# Identifica idonei
idonei = [d for d in dati if d["vi"] > soglia]
somma_vi = sum(d["vi"] for d in idonei)

# Calcolo premi
risultati = []
for d in dati:
    premio = (d["vi"] / somma_vi * premio_totale) if d in idonei and somma_vi > 0 else 0
    risultati.append({
        "Nome": d["nome"],
        "Punteggio": round(d["vi"], 2),
        "Idoneo": "✅" if d in idonei else "❌",
        "Premio": round(premio, 2)
    })

st.subheader("📊 Distribuzione Premi")
df = pd.DataFrame(risultati)
st.dataframe(df)
