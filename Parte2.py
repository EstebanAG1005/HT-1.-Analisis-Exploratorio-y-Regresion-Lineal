import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Se carga la data
df = pd.read_csv("baseball.csv")

# Remove comma from 'attendance' column
df["attendance"] = (
    df["attendance"]
    .str.replace(",", "", regex=False)
    .str.replace("'", "", regex=False)
    .str.replace("]", "", regex=False)
)


df["attendance"] = pd.to_numeric(df["attendance"], errors="coerce")
df = df.dropna(subset=["attendance"])

# Remove quotes from 'other_info_string' column
df = df.drop("other_info_string", axis=1)

# Remove quotes from 'other_info_string' column
df["venue"] = df["venue"].str.replace(":", "")

df["game_duration"] = df["game_duration"].str.replace(":", "")

# Remove quotes from 'start_time' column
df["start_time"] = df["start_time"].str.replace('"', "")


print(df)

df.to_csv("New1.csv", index=False)

# Apply Label Encoder to all string features
df = df.apply(LabelEncoder().fit_transform)

# Importamos el conjunto de datos
X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

# Ajustar el modelo de regresión lineal a los datos que tenemos
reg = LinearRegression().fit(X, y)

# Calculo del parametro R2
y_pred = reg.predict(X)
r2 = r2_score(y, y_pred)
print("R2 score:", r2)

# Obtener las constantes del modelo
intercept = reg.intercept_
coeffs = reg.coef_

# Explresar la ecuacion como un string
equation = "y = "
equation += str(intercept) + " + "
for i, coeff in enumerate(coeffs):
    equation += str(coeff) + " * X" + str(i) + " + "
equation = equation[:-3]
print("Equation:", equation)

# Predict the number of attendees given X and Y teams, day of the week, time, and state
# Predecir el numero de personas que atenderan al partido en base a X y Y equipos, dia de la semana, tiempo, y estado
X_new = np.array([[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
attendance_prediction = reg.predict(X_new)
print("Attendance prediction:", attendance_prediction[0])
