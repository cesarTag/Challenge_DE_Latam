# **Documentación del Proyecto**

Este proyecto contiene un conjunto de **seis funciones** distribuidas en varios archivos Python. Cada función aborda uno de los tres problemas definidos en el desafío, ofreciendo dos versiones para cada uno: una optimizada para **uso de memoria** y otra optimizada para **tiempo de ejecución**. A continuación, se explica cada archivo en detalle, definiendo los **pasos que sigue cada solución** y el **propósito de cada implementación**.

---

## **1. Archivo: `q1_memory.py`**  
Este archivo contiene la función `q1_memory`, que procesa un archivo NDJSON para identificar las 10 fechas con más tweets y el usuario más activo en cada fecha, **optimizando el uso de memoria**.

### **Pasos del Código**
1. **Generador para lectura eficiente:**  
   Procesa el archivo línea por línea mediante un generador para evitar cargar todo el archivo en memoria.
2. **Estructuras de conteo:**  
   Usa `Counter` y `defaultdict` para mantener un conteo eficiente por fecha y por usuario.
3. **Construcción del resultado:**  
   Utiliza `most_common` para obtener las 10 fechas con más tweets y un `list comprehension` para construir el resultado final.

### **Implementación del Logger**
- Registra errores al abrir archivos y al decodificar JSONs malformados.

---

## **2. Archivo: `q1_time.py`**  
Este archivo contiene la función `q1_time`, que resuelve el mismo problema del archivo anterior, pero con una **optimización en tiempo de ejecución**.

### **Pasos del Código**
1. **Lectura secuencial rápida:**  
   Carga cada línea del archivo en memoria y decodifica el JSON.
2. **Uso de `defaultdict`:**  
   Estructura optimizada para evitar verificaciones adicionales en los contadores.
3. **Uso de `max`:**  
   En lugar de `most_common`, utiliza `max` para encontrar el usuario más activo, lo que mejora la eficiencia en tiempo.

### **Implementación del Logger**
- Captura advertencias para JSONs malformados y errores de lectura de archivos.

---

## **3. Archivo: `q2_memory.py`**  
La función `q2_memory` identifica los **10 emojis más frecuentes** en los tweets, **optimizando el uso de memoria**.

### **Pasos del Código**
1. **Lectura en streaming:**  
   Procesa cada línea sin cargar el archivo completo en memoria.
2. **Uso de `Counter`:**  
   El contador de emojis se actualiza en cada iteración.
3. **Manejo eficiente de errores:**  
   Ignora JSONs malformados sin detener la ejecución.

---

## **4. Archivo: `q2_time.py`**  
Este archivo contiene la función `q2_time`, que resuelve el mismo problema que `q2_memory` pero priorizando **tiempo de ejecución**.

### **Pasos del Código**
1. **Uso de generadores:**  
   Procesa los tweets rápidamente usando un generador.
2. **Actualización de `Counter`:**  
   Realiza las actualizaciones de forma incremental para mejorar el rendimiento.
3. **Expresión de errores controlada:**  
   Captura y registra excepciones sin detener la ejecución.

---

## **5. Archivo: `q3_memory.py`**  
La función `q3_memory` cuenta las **menciones de usuarios (@usuario)** en los tweets, optimizando **uso de memoria**.

### **Pasos del Código**
1. **Expresión regular compilada:**  
   La expresión regular se compila una vez para reducir la sobrecarga.
2. **Lectura línea por línea:**  
   Minimiza la memoria usada mediante procesamiento en streaming.
3. **Uso de `Counter`:**  
   Actualiza las menciones eficientemente.

---

## **6. Archivo: `q3_time.py`**  
Este archivo contiene la función `q3_time`, que resuelve el problema de menciones de usuarios, optimizando **tiempo de ejecución**.

### **Pasos del Código**
1. **Uso de generadores:**  
   Los tweets se procesan rápidamente mediante un generador.
2. **Expresión regular compilada:**  
   Aumenta la velocidad al buscar menciones de usuarios.
3. **Actualización eficiente:**  
   Actualiza el `Counter` en cada iteración solo si se encuentran menciones.

---

# **Documentación Completa de las Opciones para Resolver el Problema Q1**

Este proyecto contiene **cuatro implementaciones distintas** para resolver el problema **Q1**: identificar las 10 fechas con más tweets y el usuario más activo en cada una. El archivo a procesar es un **NDJSON de 400 MB**, lo que influye en la selección del enfoque adecuado. A continuación, se detalla la lógica utilizada en cada enfoque, sus fortalezas y debilidades, y cuándo es más conveniente utilizar cada uno.

---

## **1. Archivo: `q1_memory_json.py`**
### **Descripción**
Esta implementación utiliza estructuras simples de **`Counter`** y **`defaultdict`** para procesar los tweets línea por línea, evitando cargar todo el archivo en memoria.

### **Pasos del Código**
1. **Verificación del path:**  
   Comprueba que la ruta del archivo no sea nula o vacía.
2. **Lectura secuencial del archivo:**  
   Procesa cada línea como JSON para minimizar el uso de memoria.
3. **Uso de `Counter` y `defaultdict`:**  
   Lleva el conteo por fecha y usuario.
4. **Obtención de resultados:**  
   Usa `most_common` para encontrar las fechas con más tweets y el usuario más activo.

### **Fortalezas**
- **Eficiencia en memoria:** Procesa línea por línea sin cargar el archivo completo.
- **Simplicidad:** No requiere bibliotecas externas ni configuración adicional.

### **Debilidades**
- **Velocidad limitada:** El procesamiento secuencial es más lento para archivos grandes como el de 400 MB.

---

## **2. Archivo: `q1_memory_polars.py`**
### **Descripción**
Esta versión utiliza **Polars**, una biblioteca especializada en el manejo de datos en columnas, lo que permite operaciones más rápidas y eficientes en memoria.

### **Pasos del Código**
1. **Lectura con ejecución lazy:**  
   Lee el archivo con `pl.read_ndjson` para evitar cargar todo en memoria al inicio.
2. **Transformación de columnas:**  
   Convierte las fechas y normaliza los nombres de usuario.
3. **Agrupación y conteo:**  
   Agrupa por fecha y usuario usando operaciones vectorizadas.
4. **Obtención del resultado:**  
   Encuentra los usuarios más activos y las fechas con más tweets mediante operaciones de agrupación y ordenación.

### **Fortalezas**
- **Velocidad:** Polars es extremadamente rápido para operaciones en columnas.
- **Escalabilidad:** Puede manejar grandes datasets eficientemente en memoria.

### **Debilidades**
- **Curva de aprendizaje:** Requiere conocimiento de Polars.
- **Consumo de memoria:** Necesita suficiente RAM si se intenta cargar grandes volúmenes en una sola operación.

---

## **3. Archivo: `q1_memory_pyspark.py`**
### **Descripción**
Esta implementación usa **PySpark**, un framework de procesamiento distribuido ideal para manejar grandes volúmenes de datos.

### **Pasos del Código**
1. **Inicialización de Spark:**  
   Configura una sesión de Spark.
2. **Lectura y transformación de datos:**  
   Selecciona las columnas necesarias y transforma la fecha.
3. **Agrupación y conteo:**  
   Usa ventanas para encontrar los usuarios más activos por fecha.
4. **Ordenación y resultados:**  
   Obtiene las 10 fechas con más tweets y los usuarios más activos.

### **Fortalezas**
- **Escalabilidad extrema:** Ideal para manejar datasets mayores a varios GB.
- **Distribución de carga:** Puede ejecutarse en clústeres para mejorar la velocidad.

### **Debilidades**
- **Sobrecarga operativa:** Requiere configuración de Spark y recursos adicionales.
- **Complejidad:** No es necesario para un archivo de 400 MB a menos que se integre en un sistema distribuido.

---

## **4. Archivo: `q1_memory_tqdm.py`**
### **Descripción**
Esta versión utiliza **`tqdm`** para procesar el archivo en paralelo, acelerando el procesamiento mediante el uso de múltiples núcleos de CPU.

### **Pasos del Código**
1. **Lectura del archivo:**  
   Ofrece la opción de cargar todo el archivo o procesarlo línea por línea.
2. **Procesamiento paralelo:**  
   Usa `process_map` de `tqdm` para distribuir el trabajo.
3. **Contadores de tweets y usuarios:**  
   Usa `Counter` para mantener el conteo.
4. **Resultados:**  
   Selecciona las fechas con más tweets y los usuarios más activos.

### **Fortalezas**
- **Velocidad:** El paralelismo mejora el rendimiento en sistemas multicore.
- **Uso eficiente del CPU:** Maximiza el uso de los recursos disponibles.

### **Debilidades**
- **Uso elevado de memoria:** La paralelización puede incrementar el consumo de memoria.
- **Sobrecarga en sistemas pequeños:** No siempre es eficiente si la máquina tiene pocos núcleos.

---

## **Comparación de las Opciones para un Archivo de 400 MB**

| **Enfoque**               | **Velocidad**            | **Memoria**            | **Escalabilidad**           | **Complejidad**            | **Recomendado para NDJSON de 400 MB** |
|---------------------------|--------------------------|------------------------|-----------------------------|----------------------------|--------------------------------------|
| **q1_memory_json.py**      | Rápido                    | Muy bajo               | Baja                        | Baja                       | Sí (si la simplicidad es clave)     |
| **q1_memory_polars.py**    | Moderado                   | Alta               | Alta                        | Media                      | Sí (si se necesita velocidad)       |
| **q1_memory_pyspark.py**   | Muy rápido (distribuido) | Moderada               | Muy alta                    | Alta                       | No (excesivo para 400 MB)           |
| **q1_memory_tqdm.py**      | Rápido (paralelo)        | Alta                   | Alta                        | Media                      | Sí (en sistemas multicore)          |

---

## **Conclusión**

Para un archivo **NDJSON de 400 MB**, las opciones más recomendadas son:

- **`q1_memory_json.py`**: Si se prioriza la simplicidad y el uso eficiente de memoria.
- **`q1_memory_tqdm.py`**: Ideal si se tiene acceso a una máquina con múltiples núcleos para aprovechar el procesamiento paralelo.
- **`q1_memory_polars.py`**: Si se necesita mayor velocidad sin comprometer demasiada memoria.

El enfoque con **PySpark** es más adecuado para datasets más grandes o si el procesamiento forma parte de un flujo distribuido.

**Es por esto que para el resto de los desafios se realizaron basados en la libreria json de python.**
