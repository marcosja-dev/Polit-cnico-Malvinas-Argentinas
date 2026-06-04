import pandas as pd

# 1. Cargar y consolidar datos de Energía Eléctrica (2023 - 2026)
hojas_elec = ['datos23', 'datos24', 'datos25', 'datos26']
lista_elec = []

for hoja in hojas_elec:
    # Se omiten las filas de encabezados decorativos de los Excel organizando las matrices limpias
    df = pd.read_excel('data/raw/Energia electrica.xlsx', sheet_name=hoja, skiprows=3)
    # Filtrar solo las filas que corresponden a meses reales (enero a diciembre)
    df = df[df.iloc[:, 1].str.lower().isin(['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'])]
    lista_elec.append(df)

df_elec_total = pd.concat(lista_elec, ignore_index=True)

# 2. Estructurar las columnas principales para el modelo
# Tomamos el consumo en kWh (Target), volumen de producción (lts-kg) y factor de tiempo
df_modelo = pd.DataFrame({
    'Mes': df_elec_total.iloc[:, 1],
    'Consumo_kWh': df_elec_total.iloc[:, 2],          # Variable Objetivo
    'Produccion_Volumen': df_elec_total.iloc[:, 7]     # Variable Predictora 1
})

# 3. Inspección técnica para el informe
print(f"Cantidad total de instancias (filas): {df_modelo.shape[0]}")
print("\nCaracterísticas y tipos de datos:")
print(df_modelo.dtypes)
print("\nVista previa del Dataset Consolidado:")
print(df_modelo.head())