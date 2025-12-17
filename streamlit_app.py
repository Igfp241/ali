import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Connexion à Google Sheets via les Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# Lecture des données (ceci remplira votre tableau Inspecteur)
df = conn.read() 

# --- CONFIGURATION DE LA PAGE & DESIGN  ---
st.set_page_config(page_title="IGFP - SUIVI PEDAGOGIQUE", page_icon="🎓", layout="wide")

# Fonction pour charger le logo (assurez-vous d'avoir le fichier image dans le même dossier)
def afficher_logo():
    nom_fichier_logo = "logo_igfp.png" 
    
    # Vérification simple pour éviter que l'app plante si l'image manque
    if os.path.exists(nom_fichier_logo):
        st.sidebar.image(nom_fichier_logo, width=150)
    else:
        st.sidebar.warning(f"Image '{nom_fichier_logo}' introuvable.")
        
    # CETTE LIGNE EST LA CLÉ ! ELLE NE DOIT PAS AVOIR DE PARENTHÈSES SUPPLÉMENTAIRES.
    st.sidebar.markdown("### IGFP APPLICATION")
    # Placeholder pour le logo décrit 
    # Dans la pratique, mettez votre fichier 'logo.png' dans le dossier

# --- LISTES DE DONNÉES ---
ETABLISSEMENTS = [
    "CFPP Basile Ondimba", "CFPP Nkembo", "CIMFEP Nkok", "BTP Bois", 
    "CIMFEP Mvengué", "CFPP Franceville", "CIMFEP Ntchéngué", 
    "CFPP Porgentil", "CFPP Tchibanga", "CFPP Koulamoutou", 
    "CFPP Makokou", "CFPP Oyem"
] # 

DIPLOMES = [
    "CFP1", "CFP2", "CFP3", "CFP4", "CQP", "CAP", "BEP", "BPI", "DTS", "LICENCE", "BTS"
] # [cite: 7]

# --- GESTION DES DONNÉES (Simulation Base de données) ---
FILE_DB = "igfp_data.csv"

def save_data(data):
    df = pd.DataFrame([data])
    if not os.path.isfile(FILE_DB):
        df.to_csv(FILE_DB, index=False)
    else:
        df.to_csv(FILE_DB, mode='a', header=False, index=False)

def load_data():
    if os.path.isfile(FILE_DB):
        return pd.read_csv(FILE_DB)
    return pd.DataFrame()

# --- AUTHENTIFICATION  ---
def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] in ["INSPECTEUR2024", "FORMATEUR2024"]:
            st.session_state["password_correct"] = True
            # Déterminer le rôle basé sur le code (Simplifié pour l'exemple)
            if st.session_state["password"] == "INSPECTEUR2024":
                st.session_state["role"] = "Inspecteur"
            else:
                st.session_state["role"] = "Formateur"
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Veuillez entrer votre code d'accès :", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Veuillez entrer votre code d'accès :", type="password", on_change=password_entered, key="password")
        st.error("Code incorrect 😕")
        return False
    else:
        return True

# --- INTERFACE PRINCIPALE ---
if check_password():
    afficher_logo()
    
    # Menu de navigation
    menu = st.sidebar.radio("Navigation", ["Formulaire Formateur", "Espace Inspecteur", "Messagerie"])

    # ---------------- SECTION FORMATEUR ----------------
    if menu == "Formulaire Formateur":
        st.title("🎓 Espace Formateur")
        st.markdown("Veuillez renseigner les activités pédagogiques.")

        with st.form("form_activite", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            # Champs [cite: 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14]
            with col1:
                etablissement = st.selectbox("Nom de l'établissement", ETABLISSEMENTS) # [cite: 2, 4]
                filiere = st.text_input("Filière") # [cite: 5]
                niveau = st.text_input("Niveau de la classe") # [cite: 6]
                diplome = st.selectbox("Diplôme attendu", DIPLOMES) # [cite: 7]
                salle = st.text_input("Nom de la salle de classe") # [cite: 8]
                date_cours = st.date_input("Date du cours") # [cite: 14]

            with col2:
                formateur_nom = st.text_input("Nom du Formateur") # [cite: 12]
                contact = st.text_input("Contact du Formateur") # [cite: 13]
                effectif = st.number_input("Effectif de la classe", min_value=0) # [cite: 9]
                presents = st.number_input("Nombre de présents", min_value=0) # [cite: 10]
                absents = st.text_area("Les noms des absents") # [cite: 11]

            grandes_lignes = st.text_area("Les grandes lignes du cours") # [cite: 15]

            st.markdown("---")
            st.subheader("📂 Téléversement des fichiers") # [cite: 16]
            
            # Uploaders [cite: 17, 18, 19, 20, 21, 22]
            f1 = st.file_uploader("Le programme de formation", type=['pdf', 'docx', 'xlsx'])
            f2 = st.file_uploader("Préparation du cours")
            f3 = st.file_uploader("Calendrier prévisionnel")
            f4 = st.file_uploader("L'emploi du temps")
            f5 = st.file_uploader("La liste de présence cochée")
            f6 = st.file_uploader("Le cahier de texte")

            submitted = st.form_submit_button("Envoyer le rapport")
            
            if submitted:
                # Préparation des données pour Google Sheets
                # On inclut les champs texte et les emplacements pour les 6 fichiers [cite: 3-22]
                nouvelle_donnee = pd.DataFrame([{
                    "Date": str(date_cours),
                    "Etablissement": etablissement,
                    "Formateur": formateur_nom,
                    "Filiere": filiere,
                    "Niveau": niveau,
                    "Diplome": diplome,
                    "Salle": salle,
                    "Effectif": effectif,
                    "Presents": presents,
                    "Absents": absents,
                    "Contact": contact,
                    "Contenu": grandes_lignes,
                    "Lien_Programme": "Lien_Stockage_1", 
                    "Lien_Preparation": "Lien_Stockage_2",
                    "Lien_Calendrier": "Lien_Stockage_3",
                    "Lien_Emploi_Temps": "Lien_Stockage_4",
                    "Lien_Presence": "Lien_Stockage_5",
                    "Lien_Cahier_Texte": "Lien_Stockage_6"
                }])
                
                # Envoi effectif vers la feuille de calcul Google
                df_existant = conn.read()
                df_final = pd.concat([df_existant, nouvelle_donnee], ignore_index=True)
                conn.update(data=df_final)
                
                st.success("✅ Rapport et documents transmis avec succès à l'inspection !")

    # ---------------- SECTION INSPECTEUR ----------------
    elif menu == "Espace Inspecteur":
        if st.session_state["role"] == "Inspecteur":
            st.title("🔍 Tableau de Bord Inspection")
            
            # Lecture en temps réel sur Google Sheets
            df = conn.read()
            
            if not df.empty:
                st.subheader("Données consolidées")
                st.dataframe(df)

                st.markdown("---")
                st.subheader("📂 Téléchargement des documents par formateur")
                
                # Création d'un menu déroulant pour chaque formateur
                for index, row in df.iterrows():
                    with st.expander(f"Dossier : {row['Formateur']} - {row['Etablissement']}"):
                        st.write(f"Documents téléversés le : {row['Date']}")
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.markdown(f"📄 [Le programme de formation]({row['Lien_Programme']})")
                            st.markdown(f"📄 [Préparation du cours]({row['Lien_Preparation']})")
                            st.markdown(f"📄 [Son calendrier prévisionnel]({row['Lien_Calendrier']})")
                        with col_b:
                            st.markdown(f"📄 [L’emploi du temps]({row['Lien_Emploi_Temps']})")
                            st.markdown(f"📄 [La liste de présence cochée]({row['Lien_Presence']})")
                            st.markdown(f"📄 [Le cahier de texte]({row['Lien_Cahier_Texte']})")
                
                st.markdown("---")
                # Bouton pour le fichier Excel global requis
                st.download_button(
                    label="📊 Télécharger toutes les données (Excel)",
                    data=df.to_csv(index=False).encode('utf-8'),
                    file_name="rapport_inspecteur_IGFP.csv",
                    mime="text/csv"
                )
            else:
                st.info("Aucune donnée disponible pour le moment.")

    # ---------------- SECTION MESSAGERIE  ----------------
    elif menu == "Messagerie":
        st.title("💬 Messagerie Inspecteur - Formateur")
        
        # Interface de messagerie simulée
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Afficher les messages précédents
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Champ de saisie
        if prompt := st.chat_input("Écrivez votre message ici..."):
            # Ajouter le message utilisateur
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Réponse simulée (puisque c'est une démo locale)
            with st.chat_message("assistant"):
                reponse = "Message transmis."
                st.markdown(reponse)

            st.session_state.messages.append({"role": "assistant", "content": reponse})
