import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Titre de l'application
st.title("Espace Inspecteur - Suivi IGPF")

# Connexion au Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Lecture des données
df = conn.read(ttl=600)

# Affichage du tableau (C'EST CETTE LIGNE QUI MANQUAIT)
st.write("Données de la base :")
st.dataframe(df, use_container_width=True)
