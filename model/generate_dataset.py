import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

def generer_acces_normal():
    return {
        "heure":               random.randint(8, 18),
        "nb_requetes_min":     random.randint(1, 20),
        "nb_fichiers":         random.randint(1, 10),
        "taille_totale_mb":    random.uniform(0.1, 50),
        "ip_connue":           1,
        "pays_etranger":       0,
        "methode_delete":      random.choices([0,1],[0.95,0.05])[0],
        "label":               0
    }

def generer_acces_suspect():
    return {
        "heure":               random.choice([0,1,2,3,4,22,23]),
        "nb_requetes_min":     random.randint(100, 1000),
        "nb_fichiers":         random.randint(50, 500),
        "taille_totale_mb":    random.uniform(500, 5000),
        "ip_connue":           0,
        "pays_etranger":       random.choices([0,1],[0.2,0.8])[0],
        "methode_delete":      random.choices([0,1],[0.3,0.7])[0],
        "label":               1
    }

data = []
for _ in range(1000):
    data.append(generer_acces_normal())
for _ in range(400):
    data.append(generer_acces_suspect())

df = pd.DataFrame(data)
df = df.sample(frac=1).reset_index(drop=True)
df.to_csv("model/dataset.csv", index=False)
print(f"Dataset créé : {len(df)} accès ({df['label'].sum()} suspects)")