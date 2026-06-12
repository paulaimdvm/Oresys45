import streamlit as st
from supabase import create_client

# 🔑 CONFIG SUPABASE

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Shotgun Activités", layout="centered")

st.title(" Inscription aux activités")

# ==============================
# 🔍 AFFICHAGE DES PLACES
# ==============================
st.subheader("Places restantes")

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
st.info("⚠️ Une fois inscrit, tu ne pourras plus modifier ton choix d'activité.")
trigramme = st.text_input("Ton trigramme (ex: ABC)").upper()


if activites_dict:
    activite = st.selectbox(
        "Choix activité",
        list(activites_dict.keys()),index=None,
        placeholder="Choisis une activité"
    )
else:
    st.error("⚠️ Aucune activité disponible")
    st.stop()

if st.button(" Valider mon inscription"):

    if trigramme == "":
        st.warning("Veuillez entrer un trigramme")

    elif activite is None:
        st.warning("Veuillez choisir une activité")

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
            elif resultat == "TRIGRAMME_INCONNU":
                st.error("❌ Trigramme inconnu")

            elif resultat == "DEJA_INSCRIT":
                st.warning("⚠️ Tu es déjà inscrit, modification impossible")


            else:
                st.error(f"⚠️ Réponse inconnue : {resultat}")

        except Exception as e:
            st.error(f" Erreur : {e}")
st.write("DEBUG trigramme:", trigramme)
st.write("DEBUG activite:", activite)
st.divider()


