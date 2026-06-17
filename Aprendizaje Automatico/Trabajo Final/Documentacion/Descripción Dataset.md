# Documentación del Dataset: Consumo Eléctrico - Tecnomyl

## 1. Descripción del Dataset
Este dataset contiene el histórico consolidado del consumo eléctrico mensual y las variables operativas de la planta de Tecnomyl, estructurado como una **Serie Temporal** con frecuencia mensual desde enero de 2023 hasta abril de 2026 inclusive. 

El objetivo final de este recurso es alimentar un modelo de Aprendizaje Automático Supervisado para predecir el consumo eléctrico global (medido en kWh), utilizando factores estacionales, registros de volumen físico de producción y consumo de gas natural.

## 2. Proceso de Ingeniería de Datos (ETL)
Los datos originales presentaban un alto nivel de dispersión y complejidad estructural (múltiples tablas anidadas vertical y horizontalmente en una sola hoja de Excel, inclusión de métricas financieras de costos en dólares, totales intermedios y desfasajes por cambios de formato entre años). 

Para lograr esta matriz limpia, se implementó un pipeline automatizado en Python que realizó las siguientes transformaciones quirúrgicas:
* **Segmentación Dinámica:** Localización de los bloques mensuales de datos mediante el mapeo de índices de palabras clave (`enero`), evitando fallas por filas en blanco o comentarios variables.
* **Aislamiento de Componentes:** Separación de los datos numéricos del Medidor 1 (Producción Principal) y el Medidor 2 (Sopladoras / Servicios).
* **Corrección de Desfasaje de Columnas (2025-2026):** Se corrigió mediante programación un desplazamiento horizontal en la estructura del Excel original para las planillas de 2025 y 2026, evitando la pérdida de datos y la generación de valores nulos (`NaN`) en el Medidor 2.
* **Normalización Temporal:** Conversión de los nombres de los meses en formato de texto plano (`enero`, `febrero`) a un índice cronológico estandarizado de tipo `datetime64` (`YYYY-MM-DD`).
* **Filtrado de Ruido Financiero:** Eliminación de variables de costos en dólares ($U\$S$), tipos de cambio, ratios internos calculados y filas de totales/promedios que provocarían sesgos o fuga de datos (*Data Leakage*) en el modelo de Machine Learning.

## 3. Diccionario de Datos Actual (`features_energia_tecnomyl.csv`)
La matriz cuenta actualmente con **40 instancias (filas)** compactas y continuas, compuestas por las siguientes variables:

| Nombre de Variable | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| `Fecha` | `object` (Datetime) | Índice temporal del registro en formato `AAAA-MM-DD` (primer día de cada mes). |
| `kWh_Medidor_1` | `float64` | Consumo eléctrico mensual registrado en el medidor principal del sector de Producción. |
| `kWh_Medidor_2` | `float64` | Consumo eléctrico mensual registrado en el medidor del sector Sopladoras/Servicios (Imputado en `0.0` para los meses previos a su conexión en 2023). |
| `Produccion_lts_kg`| `int64` | Volumen físico total de producción de la planta durante el mes, expresado en litros o kilogramos. |

## 4. Siguientes Pasos para el Modelado
Para cumplir estrictamente con los requisitos del modelo predictivo supervisado, el dataset se encuentra en una fase intermedia lista para:
1. **Definición del Target (`y`):** Calcular la columna objetivo final (`kWh_Total`) sumando de forma lineal el `kWh_Medidor_1` y `kWh_Medidor_2`.
2. **Extracción de Factores de Tiempo:** Descomponer la variable `Fecha` en una columna numérica discreta para el `Mes` (1 al 12) que permita al algoritmo mapear la estacionalidad energética de Río Grande.
3. **Fusión de Datos de Gas:** Integrar mediante un cruce horizontal (*left join*) los registros mensuales de consumo de gas natural ($m^3$) utilizando la columna `Fecha` como clave de unión.