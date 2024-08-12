
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



# Grouper par académie et calculer les statistiques descriptives
stats = df.groupby('Académie')["Taux d'emploi"].describe()
print("Statistiques descriptives du taux d'emploi par académie:")
print(stats)

# Créer un box plot pour visualiser la répartition du Taux d'insertion par académie
plt.figure(figsize=(10, 6))
sns.boxplot(x='Académie', y="Taux d'emploi", data=df)
plt.title("Répartition du Taux d'insertion par académie")
plt.xlabel('Académie')
plt.ylabel("Taux d'emploi")
plt.show()

# Calculer la moyenne et l'écart-type par académie
mean_std = df.groupby('Académie')["Taux d'emploi"].agg(['mean', 'std'])
print("Moyenne et écart-type par académie:")
print(mean_std)
