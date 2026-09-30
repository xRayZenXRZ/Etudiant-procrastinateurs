import streamlit as st
import uuid
import random
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# 1. Authenticate with Google Sheets using Streamlit Secrets
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
client = gspread.authorize(creds)

# 2. Open the specific Google Sheet (make sure the name matches exactly)
sheet = client.open("Experiment_Data").sheet1

# 3. Initialize the SID and Form assignment
if 'sid' not in st.session_state:
    st.session_state.sid = str(uuid.uuid4())[:8].upper()
    st.session_state.condition = random.choice(["Form A", "Form B"])


# 1. Échelles de réponses (Échelle de 6)
echelle_accord = [
    "1 - Pas du tout d'accord", 
    "", 
    "", 
    "", 
    "",
    "6 - Tout à fait d'accord"
]

echelle_frequence = [
    "1 - Jamais", 
    "", 
    "", 
    "", 
    "", 
    "6 - Très souvent"
]

# 2. Listes des questions
questions_procrastination = [
    "Mes performances ont tendance à en pâtir lorsque je dois faire la course contre les délais.",
    "Je ne réussis pas bien si je dois me précipiter pour accomplir une tâche.",
    "Si je remets les choses à la dernière minute, je ne suis pas satisfait de leurs résultats.",
    "J'obtiens de meilleurs résultats si j'accomplis une tâche à un rythme plus lent, bien avant la date limite.",
    "C'est vraiment une souffrance pour moi de travailler avec des délais imminents.",
    "Je suis contrarié et réticent à agir lorsque je suis forcé de travailler sous pression.",
    "Je me sens tendu et je n'arrive pas à me concentrer lorsqu'il y a trop de pression temporelle sur moi.",
    "Je suis frustré quand je dois me précipiter pour respecter des délais.",
    "Pour utiliser mon temps plus efficacement, je repousse délibérément certaines tâches.",
    "Je repousse intentionnellement le travail pour maximiser ma motivation.",
    "Afin de faire un meilleur usage de mon temps, je repousse intentionnellement certaines tâches.",
    "Je termine la plupart de mes devoirs juste avant la date limite parce que je choisis de le faire.",
    "Je commence souvent les choses à la dernière minute et je trouve difficile de les terminer à temps.",
    "J'échoue souvent à accomplir les objectifs que je me suis fixés.",
    "Je suis souvent en retard pour faire les choses.",
    "J'ai des difficultés à terminer les activités une fois que je les ai commencées.",
    "Même après avoir pris une décision, je retarde le passage à l'acte."
]

questions_attention = [
    "Je fais souvent des fautes d'étourderie dans mes activités.",
    "J'ai des difficultés à rester concentré lors de mes activités (domestiques, professionnelles).",
    "Il m'est difficile d'attendre mon tour dans une file d'attente.",
    "J'ai du mal à maintenir mon attention au travail.",
    "Je ne prête pas vraiment attention aux détails.",
    "Je quitte souvent ma place sans nécessité lors d'une réunion.",
    "Il m'arrive souvent de remuer les mains ou les pieds sur ma chaise.",
    "Je suis souvent sujet à des oublis dans ma vie quotidienne (tâches ménagères, courses).",
    "Il m'est difficile d'organiser des tâches nécessitant plusieurs étapes.",
    "Mes proches me reprochent de ne pas les écouter quand ils parlent."
]

# 3. Construction du formulaire unique
with st.form("formulaire_complet"):
    reponses_procrastination = []
    reponses_attention = []

    # --- PARTIE 1 : PROCRASTINATION ---
    st.header("Partie 1 : Habitudes de travail")
    st.write("Veuillez indiquer à quel point vous êtes d'accord avec les affirmations suivantes :")
    
    for index, question in enumerate(questions_procrastination):
        st.write(f"**P{index + 1}.** {question}")
        reponse = st.radio(
            label="Choix caché",
            options=echelle_accord,
            horizontal=True,
            label_visibility="collapsed",
            key=f"proc_{index}" 
        )
        reponses_procrastination.append(reponse)
        st.write("") 

    st.divider()

    # --- PARTIE 2 : ATTENTION ---
    st.header("Partie 2 : Attention et Concentration")
    st.write("À quelle fréquence rencontrez-vous les situations suivantes ?")
    
    for index, question in enumerate(questions_attention):
        st.write(f"**A{index + 1}.** {question}")
        reponse = st.radio(
            label="Choix caché",
            options=echelle_frequence,
            horizontal=True,
            label_visibility="collapsed",
            key=f"att_{index}" 
        )
        reponses_attention.append(reponse)
        st.write("")

    # --- SOUMISSION ---
    if st.form_submit_button("Envoyer mes réponses"):
        
        # --- LIGNE AJOUTÉE : Extraction des chiffres uniquement pour faciliter l'analyse ---
        # Ex: "3 - plutôt d'accord" devient l'entier 3
        scores_procrastination = [int(rep[0]) for rep in reponses_procrastination]
        scores_attention = [int(rep[0]) for rep in reponses_attention]
        
        # Concaténation de toutes les données (SID + Cond + 17 Nombres + 10 Nombres + Date)
        ligne_google_sheet = [
            st.session_state.sid, 
            st.session_state.condition
        ] + scores_procrastination + scores_attention + [str(datetime.now())]
        
        # Envoi direct vers Google Sheets
        sheet.append_row(ligne_google_sheet)
        
        st.success("Merci ! Vos réponses ont été enregistrées avec succès.")