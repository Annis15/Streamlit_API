import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import make_msgid
from email.utils import formatdate
from email import encoders
import streamlit as st
from PIL import Image

# Initiate Variables
server = 'smtpecon' # os.environ['SERVER_SMTP'] # 
port = 25 #os.environ['PORT_SMTP'] # 
sender = 'annis.hajji@allianz.fr' #os.environ['MAIL_FROM'] #  | 'from@fromdomain.com'
receivers ='annis.hajji@allianz.fr' # os.environ['MAIL_TO'] # 

# Create Mail object
multipart = MIMEMultipart()
multipart['From'] = sender
multipart['To'] = receivers
multipart['Subject'] = 'RAAS : Automatisation des Contrôles de niveau 1'
multipart['Message-Id'] = make_msgid()


def send_email(body):
    multipart.attach(MIMEText(body, 'plain'))
    s = smtplib.SMTP(server, port)
    s.sendmail(sender, receivers.split(','), multipart.as_string())
    s.quit()

# Create Front
st.title('Automatisation des Contrôles de niveau 1 : Risk As a Service')
st.text('')
st.write("Bonjour, l'équipe Performance et Transformation de la Direction du Contrôle Interne a mis en place cet outil pour détecter les contrôles automatisables.")
st.text('')
st.markdown("En répondant à cette suite de questions, vous serez en mesure de définir si votre contrôle est :\n- Automatisable\n- Eligible pour une Simplification/Ciblage\n- Non Automatisable pour le moment")
st.markdown('***')

st.write("Avant de commencer, merci de renseigner les informations suivantes pour que l'on puisse revenir vers vous")
email = st.text_input("Adresse e-mail")
ctrl = st.text_input("Nom du contrôle à automatiser")
st.markdown('***')

# Create Form
with st.form('Contrôle Automatisable ?'):
    
    # Typologie
    st.subheader('Typologie des Données')
    st.write('Quelles types de données utilisez-vous lors du contrôle ? Cf Image ci-dessous')
    st.write('')
    st.write('Ne pas parler de données accessibles --> Aucun moyen de savoir pour le métier...')
    data_options = ['Données Objectives', 'Données Subjectives', 'Données Mixtes']
    datas = st.radio('Select an Option: ', data_options )
    
    # Images
    data_img = Image.open('process_niveau1.jpg')
    st.text('')
    st.image(data_img)
    st.markdown('***')
    
    # Règles
    st.subheader('Règles Métier')
    regles_options = ['Règles Claires & Définies', 'Règles Subjectives', 'Règles Mixtes']
    regles = st.radio('Select an Option: ', regles_options)
    
    # Images
    regle_img = Image.open('process_niveau1.jpg')
    st.text('')
    st.image(regle_img)
    st.markdown('***')
    
    # Fréquence Changement
    st.subheader('Fréquence Changement Processus')
    st.write('Votre Contrôle est-il amené à evoluer régulièrement ?')
    freq_options = ['Quelques fois par mois', 'Quelques fois par an', 'Rarement', 'Jamais']
    freqs = st.radio('Select an Option: ', freq_options)
    st.markdown('***')
    
    # Documentation
    st.subheader('Documentation de Contrôle')
    st.write('Votre Contrôle est-il documenté ? (Mode Opératoire, Procédure)')
    doc_options = ['Oui', 'Non']
    docs = st.radio('Select an Option: ', doc_options)
    st.markdown('***')
    
    # Délai Contrôle
    st.subheader('Délai réalisation du Contrôle')
    st.write('Quel est le temps nécessaire pour réaliser votre Contrôle ?')
    time_options = ['Moins de 1 jour', 'Environ 1 jour', 'Supérieur à 1 jour', 'Environ 1 semaine', 'Supérieur à 1 semaine']
    times = st.radio('Select an Option: ', time_options)

    # Every Form must have a submit Button
    submitted = st.form_submit_button('Submit')
    
    if submitted: 
        
        # Define the Information to insert in all mail
        items = [datas, regles, freqs, docs, times]
        bullet_points = '\n- '.join(items)
        
        if (datas == 'Données Subjectives') or (regles == 'Règles Subjectives') or (freqs == 'Quelques fois par mois') or (freqs == 'Quelques fois par an'):
            st.write('Contrôle Non Automatisable pour le moment')
            
        elif (datas == 'Données Mixtes') or ((regles == 'Règles Mixtes')):
            st.write('Automatisation à étudier --> Simplification de Contrôle / Ciblage')
            body = f"Hello,\n\nLe contrôle de niveau 1 étudié {ctrl} est apte pour une simplification et/ou ciblage.\nMerci de prendre contact avec le contrôle owner suivant : {email}\n\nVoici les éléments renseignés :\n- {bullet_points}\n\nCordialement,\nP&T"
            send_email(body)
            
        elif (datas == 'Données Objectives') and (regles == 'Règles Claires & Définies') and ((freqs == 'Rarement') or (freqs == 'Jamais')):
            
            if (docs == 'Non'):
                
                if (times == 'Moins de 1 jour'):
                    priority = 'Faible ROI'
                    
                elif (times == 'Environ 1 jour'):
                    priority = 'Priorité 5'
                   
                elif (times == 'Supérieur à 1 jour'):
                    priority = 'Priorité 4'
               
                elif (times == 'Environ 1 semaine'):
                    priority = 'Priorité 3'
                   
                elif (times == 'Supérieur à 1 semaine'):
                    priority = 'Priorité 2'
            
            else:
                if (times == 'Moins de 1 jour'):
                    priority = 'Priorité 5'
           
                elif (times == 'Environ 1 jour'):
                    priority = 'Priorité 4'
                   
                elif (times == 'Supérieur à 1 jour'):
                    priority = 'Priorité 3'
             
                elif (times == 'Environ 1 semaine'):
                    priority = 'Priorité 2'
                 
                elif (times == 'Supérieur à 1 semaine'):
                    priority = 'Priorité 1'
       
            st.write(f'Contrôle Automatisable ({priority})')
            body = f"Hello, \r\r Le contrôle de niveau 1 étudié ({ctrl}) est apte pour une automatisation ({priority}). \rMerci de prendre contact avec le contrôle owner suivant : {email}\n\nVoici les éléments renseignés :\n- {bullet_points}\n\nCordialement,\nP&T"
            send_email(body)        
        
        else:
            st.write('ELSE')
            body = f"Hello, \r\r Le contrôle de niveau 1 étudié ({ctrl}) dispose d'erreurs dans les éléments renseignés\n\nCordialement,\nP&T"
            send_email(body)
        