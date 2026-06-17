# ⚡ Modelo Predictivo de Consumo Eléctrico Industrial (Tecnomyl)

**[📺 Clic aquí para ver el Video de Presentación del Proyecto](https://drive.google.com/file/d/1E1FchPuKPWM3NLCDEJqIYSNI1MlBLMlN/view?usp=sharing)**

## 📌 Descripción del Proyecto
Este repositorio contiene el desarrollo de un modelo de Aprendizaje Automático diseñado para predecir el consumo mensual de energía eléctrica (en kWh) de la planta industrial Tecnomyl, ubicada en Río Grande, Tierra del Fuego. El objetivo es mitigar la incertidumbre operativa y optimizar la planificación de eficiencia energética.

---

## 📂 Estructura del Repositorio
* `data/`: Contiene el dataset original y el archivo `.csv` procesado (`features_energia_tecnomyl.csv`).
* `notebooks/`: Notebooks de Jupyter con el proceso de ETL, Análisis Exploratorio (EDA) y el modelado predictivo.
* `reports/figures/`: Gráficos generados durante el EDA y la evaluación del modelo.
* `documentacion/`: Documentación complementaria del proyecto.

---

## 📊 1. Orígenes de Datos
El dataset histórico abarca el período desde enero de 2023 hasta abril de 2026 (40 registros mensuales). Las variables extraídas de los sistemas de la planta incluyen:
* **Producción Física (`Produccion_lts_kg`):** Volumen total procesado.
* **Consumo de Gas Natural (`Consumo_Gas_m3`):** Demanda térmica.
* **Consumo Eléctrico (`kWh_Medidor_1` y `kWh_Medidor_2`):** Demanda energética sectorizada.

Se aplicó un proceso de limpieza (ETL) utilizando Pandas para imputar valores faltantes y corregir desfases estructurales.

## 📈 2. Análisis Exploratorio de Datos (EDA)
Las visualizaciones y análisis estadísticos revelaron factores críticos:
* **Quiebre Estructural (2025):** El Medidor 2 pasó de consumos marginales a operar a escala industrial (aprox. 150,000 kWh/mes) por la activación de maquinaria pesada (sopladoras).
* **Multicolinealidad:** Existe una alta correlación (0.83) entre el Gas y la Producción, lo que invalida el uso de modelos lineales simples.
* **Estacionalidad:** Se detectaron caídas drásticas y predecibles del consumo durante diciembre y enero por paradas técnicas.

## 🧠 3. Modelo de Aprendizaje Automático
Se implementó un modelo **Random Forest Regressor** utilizando un **enfoque de desacople** (Descomposición de la Variable Objetivo). 
En lugar de predecir el consumo global, el modelo de Machine Learning predice exclusivamente el Medidor 1 (dinámico), mientras que el Medidor 2 se trata como un costo determinista fijo. Además, se aplicó ingeniería de características para crear una variable binaria (`Parada_Fin_Anio`) que captura el freno estacional.

* **Validación:** Cronológica estricta (`shuffle=False`) dividiendo 80% Train y 20% Test.
* **Hiperparámetros:** `n_estimators=30`, `max_depth=3`, `min_samples_split=3`.

## ⚙️ 4. Métricas de Evaluación
Evaluando sobre el conjunto de Test con datos no vistos previamente por el algoritmo, se obtuvieron las siguientes métricas de regresión:
* **Mean Absolute Error (MAE):** 39,871 kWh
* **Root Mean Squared Error (RMSE):** 47,611 kWh
* **Coeficiente de Determinación (R²):** 0.4582

*(A modo comparativo, un modelo base de Regresión Lineal obtuvo un R² de apenas 0.1890, confirmando la superioridad del modelo de ensamble).*

## 🎯 5. Conclusiones
El análisis de importancia de variables (*Feature Importance*) confirmó que el Random Forest basó sus predicciones en la física real de la planta: Producción (63.9%), Gas (29.1%) y la estacionalidad de fin de año (6.9%). 

El modelo implementado logró superar el ruido del quiebre de infraestructura de 2025 y la multicolinealidad, explicando casi el 46% de la varianza en una serie temporal corta y compleja. Esta herramienta predictiva sienta las bases matemáticas para evitar penalizaciones por picos de demanda y mejorar la planificación financiera a largo plazo de la compañía.