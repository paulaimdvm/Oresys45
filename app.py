import streamlit as st
import pandas as pd

# Charger les données Excel
@st.cache_data
def load_data():
    df = pd.read_excel("planning.xlsx")
    # Nettoyage pour éviter les erreurs de recherche
    df["Prénom"] = df["Prénom"].astype(str).str.strip().str.lower()
    return df

df = load_data()


col1, col2 = st.columns([4, 1])

with col2:
    st.image("logo.png", width=200)


# 🎉 Titre
st.title("Ton Programme des 45 ")

st.write("Entre ton trigramme pour voir ton planning 👇")

# 🔍 Barre de recherche
user_input = st.text_input("Ton trigramme")

if user_input:
    user_input_clean = user_input.strip().lower()
    
    # Recherche dans le dataframe
    result = df[df["Prénom"] == user_input_clean]

    if not result.empty:
        st.success(f"Voici ton programme, {user_input.capitalize()} 👇")

        # Affichage stylé
        row = result.iloc[0]

        for col in df.columns:
            if col != "Prénom":
                st.markdown(f"**{col} :** {row[col]}")

    else:
        st.error("Aucun résultat trouvé 😕 Vérifie le trigramme.")
