import streamlit as st
from supabase import create_client

# 🔑 CONFIG SUPABASE

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Shotgun Activités", layout="centered")

st.title("🎯 Inscription aux activités")

# ==============================
# 🔍 AFFICHAGE DES PLACES
# ==============================
st.subheader("📊 Places restantes")

data = supabase.table("activites").select("*").execute()

activites_dict = {}
for act in data.data:
    restant = act["capacite"] - act["nb_inscrits"]
    activites_dict[act["nom"]] = restant
    st.write(f"👉 Activité {act['nom']} : {restant} places restantes")

st.divider()

# ==============================
# 📝 FORMULAIRE INSCRIPTION
# ==============================
st.subheader("📝 S'inscrire")

trigramme = st.text_input("Ton trigramme (ex: ABC)").upper()


if activites_dict:
    activite = st.selectbox(
        "Choix activité",
        list(activites_dict.keys())
    )
else:
    st.error("⚠️ Aucune activité disponible")
    st.stop()

if st.button("🚀 Valider mon inscription"):

    if trigramme == "":
        st.warning("Veuillez entrer un trigramme")
    else:
        try:
            res = supabase.rpc(
                "inscrire_user",
                {
                    "p_trigramme": trigramme,
                    "p_activite": activite
                }
            ).execute()

            resultat = res.data

            if resultat == "OK":
                st.success(f"✅ Inscription confirmée pour {activite}")
            elif resultat == "COMPLET":
                st.error("❌ Activité complète")
            elif resultat == "ACTIVITE INTROUVABLE":
                st.error("⚠️ Activité non reconnue")
            else:
                st.error(f"⚠️ Réponse inconnue : {resultat}")

        except Exception as e:
            st.error(f"🔥 Erreur : {e}")

st.divider()

# ==============================
# 🔎 VOIR SON INSCRIPTION
# ==============================
st.subheader("🔎 Voir mon inscription")

tri_check = st.text_input("Entrer ton trigramme pour vérifier")

if st.button("Voir mon activité"):

    if tri_check == "":
        st.warning("Veuillez entrer un trigramme")
    else:
        try:
            data = supabase.table("inscriptions") \
                .select("*") \
                .eq("trigramme", tri_check.upper()) \
                .execute()

            if data.data:
                activite_user = data.data[0]["activite"]

                st.success(f"✅ Tu es inscrit à l'activité : {activite_user}")

                # 🎯 Exemple de planning (à adapter)
                planning = {
                    "A": "Lundi 10h - Salle 1",
                    "B": "Mardi 14h - Salle 2",
                    "C": "Mercredi 9h - Salle 3"
                }

                if activite_user in planning:
                    st.info(f"📅 Planning : {planning[activite_user]}")
                else:
                    st.info("📅 Planning non défini")

            else:
                st.warning("❌ Aucun enregistrement trouvé")

        except Exception as e:
            st.error(f"🔥 Erreur : {e}")
