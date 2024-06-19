import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
import streamlit as st
import pandas as pd
import joblib

st.write('''
# Application pour la prévision de fraude
''')

st.sidebar.header("Les caractéristiques de la transaction")

def user_input():
    step = st.sidebar.number_input('Saisir le step', min_value=1, value=45)
    age = st.sidebar.number_input('Saisir l\'âge', min_value=1, value=45)
    zipcodeori = st.sidebar.number_input('Saisir votre code postal', min_value=1, value=345)
    zipmerchant = st.sidebar.number_input('Saisir zipmerchant', min_value=1, value=556)
    # Utilisation d'une liste déroulante pour la catégorie avec des options de 1 à 15
    category = st.sidebar.selectbox('Saisir catégorie', list(range(1, 16)), index=0)
    amount = st.sidebar.number_input('Saisir le montant', min_value=1.0, value=566.0)

    data = {
        'step': step,
        'age': age,
        'zipcodeOri': zipcodeori,
        'zipMerchant': zipmerchant,
        'category': category,
        'amount': amount
    }

    features = pd.DataFrame(data, index=[0])
    return features

df = user_input()

st.subheader('Paramètres saisis')
st.write(df)

# Charger le modèle préalablement entraîné
try:
    modele_fraude = joblib.load('fraud_detection_model.joblib')
except FileNotFoundError:
    st.error("Le fichier modèle 'fraud_detection_model.joblib' est introuvable. Assurez-vous qu'il est dans le même répertoire que le script Streamlit.")
except ValueError as e:
    st.error(f"Erreur lors du chargement du modèle : {e}")
else:
    # Supprimer les colonnes non nécessaires pour la prédiction
    # Assurez-vous que df ne contient que les colonnes utilisées pour l'entraînement du modèle
    features_used_for_training = ['step', 'age', 'zipcodeOri', 'zipMerchant', 'category', 'amount']
    df = df[features_used_for_training]

    # Prédire la fraude
    if st.button('Prédire'):
        prediction = modele_fraude.predict(df)
        if prediction[0] == 1:
            st.write("Cette transaction est frauduleuse.")
        else:
            st.write("Cette transaction est acceptable.")
