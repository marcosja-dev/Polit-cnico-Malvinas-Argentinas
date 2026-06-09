import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Creación del DataFrame
data = {
    'Producto': ['A', 'B', 'C', 'D'],
    'Precio': [10, 20, 15, 25],
    'Cantidad_Vendida': [50, 30, 40, 20]
}
df = pd.DataFrame(data)

# --- Visualización ---

# Configuración de estilo (para que se vea pro)
sns.set_theme(style="whitegrid")

# Instrucción 1: Histograma de precios
plt.figure(figsize=(8, 5))
sns.histplot(df['Precio'], bins=4, kde=True, color='skyblue')
plt.title('Distribución de Precios de Productos')
plt.xlabel('Precio ($)')
plt.ylabel('Frecuencia')
plt.show()

# Instrucción 2: Gráfico de dispersión (Precio vs Cantidad_Vendida)
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='Precio', y='Cantidad_Vendida', hue='Producto', s=100)
plt.title('Relación: Precio vs Cantidad Vendida')
plt.xlabel('Precio ($)')
plt.ylabel('Unidades Vendidas')
plt.show()