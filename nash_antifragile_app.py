import streamlit as st
import pandas as pd
# 🗣️ Dizionario traduzioni completo
testi = {
    "🇮🇹": {
        "titolo": "Distribuzione Meritocratica Nash-Antifragile",
        "partecipanti": "Numero di partecipanti",
        "criteri": "Numero di criteri di valutazione",
        "soglia": "Soglia minima (s)",
        "premio": "Montepremi totale (P)",
        "pesi": "⚖️ Pesi dei criteri",
        "punteggi": "Punteggi dei partecipanti",
        "risultati": "📊 Distribuzione Premi",
        "somma_pesi": "🔢 Somma totale dei pesi inseriti",
        "normalizzazione": "✅ I pesi sono stati normalizzati automaticamente.",
        "idoneo_sì": "✅ Sì",
        "idoneo_no": "❌ No",
        "tabella": {
            "nome": "Nome",
            "punteggio": "Punteggio",
            "idoneo": "Idoneo",
            "premio": "Premio"
        }
    },
    "🇺🇸": {
        "titolo": "Nash-Antifragile Meritocratic Distribution",
        "partecipanti": "Number of participants",
        "criteri": "Number of evaluation criteria",
        "soglia": "Minimum threshold (s)",
        "premio": "Total prize pool (P)",
        "pesi": "⚖️ Criteria weights",
        "punteggi": "Participants' scores",
        "risultati": "📊 Prize Distribution",
        "somma_pesi": "🔢 Total sum of weights entered",
        "normalizzazione": "✅ Weights have been automatically normalized.",
        "idoneo_sì": "✅ Yes",
        "idoneo_no": "❌ No",
        "tabella": {
            "nome": "Name",
            "punteggio": "Score",
            "idoneo": "Eligible",
            "premio": "Prize"
        }
    },
    "🇪🇸": {
        "titolo": "Distribución Meritocrática Nash-Antifrágil",
        "partecipanti": "Número de participantes",
        "criteri": "Número de criterios de evaluación",
        "soglia": "Umbral mínimo (s)",
        "premio": "Monto total del premio (P)",
        "pesi": "⚖️ Pesos de los criterios",
        "punteggi": "Puntajes de los participantes",
        "risultati": "📊 Distribución de Premios",
        "somma_pesi": "🔢 Suma total de los pesos ingresados",
        "normalizzazione": "✅ Los pesos se han normalizado automáticamente.",
        "idoneo_sì": "✅ Sí",
        "idoneo_no": "❌ No",
        "tabella": {
            "nome": "Nombre",
            "punteggio": "Puntuación",
            "idoneo": "Elegible",
            "premio": "Premio"
        }
    }
}
lingua = st.selectbox("🌍 Lingua / Language / Idioma", ["🇮🇹 Italiano", "🇺🇸 English", "🇪🇸 Español"])
codice = lingua.split()[0]  # Estrae l'emoji come chiave
t = testi[codice]           # Riferimento al blocco di testo tradotto


st.set_page_config(page_title=t["titolo"], layout="centered")
st.title(f"💎 {t['titolo']}")

st.markdown(f"{t['punteggi']}")  # O inserisci una nuova chiave tipo "introduzione"

# Parametri con etichette localizzate
n = st.number_input(t["partecipanti"], min_value=1, value=5)
m = st.number_input(t["criteri"], min_value=1, value=3)
soglia = st.number_input(t["soglia"], min_value=0.0, value=5.0)
premio_totale = st.number_input(t["premio"], min_value=0.0, value=10000.0)

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

# 🗣️ Recupera dizionario lingua corrente (solo una volta)
t = testi[codice]
colonne = t["tabella"]
id_sì = t["idoneo_sì"]
id_no = t["idoneo_no"]

# 🔁 Costruzione tabella premi
risultati = []
for d in dati:
    premio = (d["vi"] / somma_vi * premio_totale) if d in idonei and somma_vi > 0 else 0
    risultati.append({
        colonne["nome"]: d["nome"],
        colonne["punteggio"]: round(d["vi"], 2),
        colonne["idoneo"]: id_sì if d in idonei else id_no,
        colonne["premio"]: round(premio, 2)
    })

# 🧾 Visualizzazione
st.subheader(t["risultati"])
df = pd.DataFrame(risultati)
st.dataframe(df)
