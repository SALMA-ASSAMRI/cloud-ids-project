import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib

df = pd.read_csv("model/dataset.csv")

FEATURES = ["heure","nb_requetes_min","nb_fichiers",
            "taille_totale_mb","ip_connue","pays_etranger","methode_delete"]

X = df[FEATURES]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

modele = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
modele.fit(X_train, y_train)

predictions = modele.predict(X_test)
print("=== Résultats du modèle ===")
print(classification_report(y_test, predictions,
      target_names=["Normal", "Suspect"]))
print("Matrice de confusion :")
print(confusion_matrix(y_test, predictions))

joblib.dump(modele, "model/ids_model.pkl")
print("Modèle sauvegardé : model/ids_model.pkl")