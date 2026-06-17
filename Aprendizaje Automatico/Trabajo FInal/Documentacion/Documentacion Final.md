# Documentación Final: Modelo Predictivo de Consumo Eléctrico Industrial (Tecnomyl)

## 1. Orígenes de Datos
El presente proyecto utiliza un conjunto de datos históricos tabulares provenientes de la planta industrial Tecnomyl, ubicada en Río Grande, Tierra del Fuego. El dataset abarca el período mensual desde enero de 2023 hasta abril de 2026 (40 registros). 

Las variables extraídas de los sistemas de la planta incluyen:
* **Producción Física (`Produccion_lts_kg`):** Volumen total procesado.
* **Consumo de Gas Natural (`Consumo_Gas_m3`):** Demanda térmica de la planta.
* **Consumo Eléctrico (`kWh_Medidor_1` y `kWh_Medidor_2`):** Demanda energética sectorizada, que sumadas componen la variable objetivo (`kWh_Total`).

Se aplicó un proceso de limpieza (ETL) utilizando la librería Pandas, imputando valores faltantes y corrigiendo desfases estructurales en los registros originales.

---

## 2. Análisis Exploratorio de Datos (EDA)
Durante la fase exploratoria se generaron visualizaciones clave para entender el comportamiento físico y operativo de la planta:

1. **Evolución Temporal:** Se graficó la línea de tiempo del consumo total versus la producción, detectando que las curvas se acompañan, pero existen "saltos" en el consumo eléctrico que no responden linealmente al volumen fabricado.
2. **Matriz de Correlación (Heatmap):** Se identificó una altísima correlación (0.83) entre el Consumo de Gas y la Producción, alertando sobre posible multicolinealidad. Por el contrario, la variable genérica `Mes` mostró una correlación casi nula (-0.11) con el consumo total.
3. **Estacionalidad Mensual (Gráfico de Barras):** Se evidenció una caída drástica del consumo durante los meses de diciembre y enero.

### Conclusiones Clave del EDA
* **Quiebre Estructural (2025):** Se descubrió que el Medidor 2 pasó de consumos marginales a operar a escala industrial (aprox. 150,000 kWh mensuales) a principios de 2025 por la activación de nueva maquinaria (sopladoras). Este salto rompe cualquier tendencia histórica previa.
* **Multicolinealidad y Ruido:** Un modelo lineal clásico fallaría debido a la fuerte correlación entre las variables predictoras (Gas y Producción).
* **Estacionalidad Discreta:** La caída de consumo a fin de año responde a paradas técnicas programadas, un comportamiento que requiere reglas condicionales, no regresiones lineales continuas.

---

## 3. Modelo de Aprendizaje Automático Desarrollado
Para abordar la complejidad no lineal del problema, se descartó el modelo base (Regresión Lineal) y se desarrolló un modelo basado en ensambles de árboles: **Random Forest Regressor**.

### Arquitectura y Estrategia (Enfoque de Desacople)
En lugar de predecir el consumo global y confundir al algoritmo con el quiebre de infraestructura de 2025, se aplicó la técnica de *Descomposición de la Variable Objetivo*:
* El modelo de *Machine Learning* se entrenó exclusivamente para predecir el **Medidor 1**, el cual responde de manera dinámica a la producción y el gas.
* El **Medidor 2** se separó del entrenamiento y se trató como un costo determinista (constante a sumar post-predicción), limpiando el ruido del dataset.

### Ingeniería de Características
Se eliminó la variable `Mes` (que aportaba ruido algorítmico) y se creó una variable binaria temporal (`Parada_Fin_Anio` = 1 para diciembre y enero), logrando capturar el freno estacional.

### Hiperparámetros y Validación
* Se utilizó una validación cronológica estricta (`train_test_split` con `shuffle=False` y proporción 80/20) para evitar fuga de datos temporales (*Data Leakage*).
* Ajustes para evitar sobreajuste (*Overfitting*): `n_estimators=30`, `max_depth=3`, `min_samples_split=3`, `random_state=42`.

---

## 4. Métricas de Evaluación del Modelo
*Nota Metodológica: Al tratarse de un problema de predicción de una variable continua (kWh), se omiten métricas de clasificación (Precisión, Recall, F1-Score) y se utilizan estrictamente métricas de regresión.*

Evaluando el conjunto de prueba (Test) con datos nunca antes vistos por el algoritmo, se obtuvieron los siguientes resultados tras acoplar ambas líneas de consumo:

* **Mean Absolute Error (MAE):** 39,871 kWh
* **Root Mean Squared Error (RMSE):** 47,611 kWh
* **Coeficiente de Determinación (R²):** 0.4582

A modo comparativo, el modelo de Regresión Lineal base obtuvo un R² de apenas 0.1890 y un RMSE de 58,249 kWh, lo que demuestra la superioridad del modelo de ensamble elegido.

---

## 5. Interpretación de Resultados y Conclusión Final
El análisis de importancia de características (*Feature Importance*) reveló que el Random Forest basa sus decisiones en:
1. **Producción (63.91%):** Es el motor del consumo dinámico.
2. **Consumo de Gas (29.16%):** Aporta la variabilidad fina de la demanda energética.
3. **Parada Fin de Año (6.93%):** Actúa como un atenuador estacional exitoso.

### Conclusión Final
El modelo desarrollado cumplió con el objetivo original de mitigar la incertidumbre operativa en el consumo energético. Al implementar un enfoque de desacople y variables estacionales, el algoritmo superó las limitaciones paramétricas de una regresión lineal (la cual asignaba coeficientes negativos irreales al gas por multicolinealidad). Lograr explicar casi el 46% de la varianza en un escenario industrial con datos cortos y un quiebre de infraestructura masivo demuestra que el análisis predictivo es una herramienta viable para Tecnomyl. Este sistema no solo previene penalizaciones financieras por picos de demanda imprevistos, sino que sienta las bases para una planificación de eficiencia energética a largo plazo.