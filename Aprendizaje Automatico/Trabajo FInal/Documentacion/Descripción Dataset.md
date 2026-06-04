# INFORME DE PROYECTO: APRENDIZAJE AUTOMÁTICO (ENTREGA 2)

## 1. Descripción Completa del Dataset

El dataset seleccionado para el proyecto consiste en una matriz de series temporales combinadas que unifican el comportamiento energético y operativo de la planta industrial.

### Instancias Totales
El conjunto de datos cuenta con un histórico cronológico consolidado de **16 instancias** mensuales principales, que abarcan desde enero de 2025 hasta el último período disponible de 2026.

### Características (Columnas) y Tipos de Datos

La matriz de entrenamiento para el modelo predictivo está estructurada por las siguientes variables:

| Característica (Columna) | Descripción Física | Tipo de Dato (Python) | Rol en el Modelo |
| :--- | :--- | :--- | :--- |
| **Mes** | Período cronológico del registro (Enero a Diciembre). | `String` (Categórica) | Índice / Estacionalidad |
| **kWh_Medidor_Produccion** | Consumo eléctrico del Medidor n.º 4156946 (Naves productivas). | `Float64` (Numérica) | Target / Feature |
| **kWh_Medidor_Servicios** | Consumo eléctrico del Medidor de soporte fijos e infraestructura. | `Float64` (Numérica) | Target / Feature |
| **Produccion_lts_kg** | Volumen físico total de producción de la fábrica en el mes. | `Float64` (Numérica) | Feature Principal |
| **consumo_gas_procesado** | Consumo de gas natural de la planta en metros cúbicos (m³). | `Float64` (Numérica) | Feature Térmica |

### Información Relevante Adicional (Metadatos Fijos)
Complementariamente, el dataset cuenta con dos estructuras de metadatos estáticos llamadas **Fichas de Potencia** (`Produccion.xlsx` y `Servicios.xlsx`). No suman filas variables a la regresión, pero operan como la Línea de Base (*Baseline*) del modelo, detallando las capacidades nominales instaladas de la planta:
* **Ficha de Producción:** 6 instancias (Naves 300 a 1100 y Sopladoras) con columnas de potencia (*Arranque kW, Máximo kW, Carga kW, Mínimo kW*).
* **Ficha de Servicios:** 10 instancias de equipos críticos (Compresores, calderas, iluminación, efluentes) con sus potencias de diseño en kW.

---

## 2. Origen de los Datos y Fecha de Adquisición

* **Fuente:** Los datos provienen directamente de los registros internos del área de infraestructura, mantenimiento y servicios generales de la planta industrial de la empresa **Tecnomyl**, ubicada en Río Grande, Tierra del Fuego.
* **Fecha de adquisición:** Datos operativos históricos correspondientes al ciclo completo del año 2025 y los meses consolidados del año 2026.

---

## 3. Proceso de Recopilación y Preprocesamiento Realizado

Los archivos originales se encontraban en formatos de hojas de cálculo diseñados para la visualización humana, con tablas superpuestas y fórmulas dependientes. Para transformarlos en la matriz limpia descrita anteriormente, se aplicó el siguiente pipeline en Python utilizando la librería **Pandas**:

1. **Desvinculación y Planchado de Fórmulas:** Se identificaron celdas del histórico de 2025 que estaban ligadas a archivos locales externos de 2026 (lo que generaba la pérdida de referencias y errores de tipo `#REF!`). Se procedió a congelar los datos mediante un pegado especial de valores puros.
2. **Alineación de Matrices mediante Pandas:** Utilizando indexación por posiciones (`iloc[4:, :]`), se descartaron las primeras 4 filas de los archivos Excel, eliminando títulos institucionales y cuadros combinados de texto para dejar las cabeceras alineadas con los meses.
3. **Remoción de Filas de Control:** Se programaron filtros lógicos para remover las filas de "Totales" y "Promedios Ponderados" que venían incrustadas al final de cada ciclo anual, aislando únicamente los meses cronológicos reales.
4. **Normalización Categórica:** Se procesó la columna `Mes` mediante transformaciones de cadenas (`.str.lower().str.strip()`) para unificar la nomenclatura y neutralizar errores de tipeo manual.
5. **Unificación Horizontal (Merge de Medidores):** En lugar de fusionar ciegamente los consumos eléctricos en una sola variable, se realizó un *merge* horizontal vinculando las tablas por la clave `Mes`. Esto preservó la separación entre el medidor indexado a la producción pesada y el medidor de servicios basal.
6. **Coerción de Tipos:** Se forzó la transformación de todas las columnas numéricas de consumo y volumen a tipo `float64` mediante `pd.to_numeric(errors='coerce')`, garantizando la compatibilidad matemática con los algoritmos de Machine Learning.

---