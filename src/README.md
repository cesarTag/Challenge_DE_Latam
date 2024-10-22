# **Documentación del Proyecto**

Este proyecto contiene un conjunto de **seis funciones** distribuidas en varios archivos Python. Cada función aborda uno de los tres problemas definidos en el desafío, ofreciendo dos versiones para cada uno: una optimizada para **uso de memoria** y otra optimizada para **tiempo de ejecución**. A continuación, se explica cada archivo en detalle, definiendo los **pasos que sigue cada solución** y el **propósito de cada implementación**.

---

## **1. Archivo: `q1_memory.py`**  

Esta implementación resuelve el problema de **Q1**: encontrar las **10 fechas con más tweets** y el **usuario más activo en cada una**, utilizando un enfoque **modular basado en MapReduce**. La solución prioriza la **optimización en memoria**, usando **generadores** y manejando errores de forma robusta mediante **logger**.

---

## **Estructura del Código**

### **1. `leer_tweets()`**
Lee el archivo NDJSON línea por línea y genera un **objeto JSON** para cada tweet. Esta función utiliza un **generador** para evitar cargar todo el archivo en memoria.

```python
def leer_tweets(file_path: str) -> Generator[Dict, None, None]
```

#### **Argumentos**
- `file_path (str)`: Ruta del archivo NDJSON.

#### **Retorno**
- `Generator[Dict]`: Generador de objetos JSON.

#### **Responsabilidades**
- Lee el archivo en modo streaming.
- Registra advertencias para JSONs malformados sin detener la ejecución.

---

### **2. `map_tweets()`**
Procesa los tweets para crear dos contadores:
1. **`date_counts`**: Contador de tweets por fecha.
2. **`date_user_counts`**: Contador de usuarios por fecha.

```python
def map_tweets(tweets: Generator[Dict, None, None]) -> Tuple[Counter, defaultdict]
```

#### **Argumentos**
- `tweets (Generator)`: Generador de tweets en formato JSON.

#### **Retorno**
- `Tuple[Counter, defaultdict]`: Contador de tweets por fecha y usuarios por fecha.

#### **Responsabilidades**
- Extraer la fecha y el usuario de cada tweet.
- Actualizar los contadores de forma incremental.
- Manejar errores de **KeyError** si falta información en algún tweet.

---

### **3. `reduce_tweets()`**
Obtiene las **10 fechas con más tweets** y el **usuario más activo en cada una**.

```python
def reduce_tweets(date_counts: Counter, date_user_counts: defaultdict) -> List[Tuple[datetime.date, str]]
```

#### **Argumentos**
- `date_counts (Counter)`: Contador de tweets por fecha.
- `date_user_counts (defaultdict)`: Contador de usuarios por fecha.

#### **Retorno**
- `List[Tuple[datetime.date, str]]`: Lista con las 10 fechas más activas y sus usuarios más frecuentes.

#### **Responsabilidades**
- Usa `most_common()` para seleccionar las fechas con más tweets.
- Encuentra el usuario más activo en cada fecha.

---

### **4. `q1_memory()`**
Función principal que coordina las fases de **Map** y **Reduce** para resolver el problema Q1.
``` python
def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]
```

#### **Argumentos**
- `file_path (str)`: Ruta del archivo NDJSON.

#### **Retorno**
- `List[Tuple[datetime.date, str]]`: Lista con las 10 fechas más activas y los usuarios más frecuentes.

#### **Responsabilidades**
- Verifica que la ruta del archivo no sea nula.
- Llama a las funciones `leer_tweets()`, `map_tweets()`, y `reduce_tweets()`.
- Registra errores y resultados importantes con el **logger**.

---

### **Fortalezas de la Implementación**
- **Modularidad:**
Cada función tiene una única responsabilidad, facilitando el mantenimiento y las pruebas.

- **Optimización de Memoria:**
Usa generadores para evitar cargar el archivo completo en memoria.

- **Escalabilidad:**
La estructura modular permite extender la solución a entornos paralelos o distribuidos.

- **Manejo Robusto de Errores:**
Usa logger para registrar advertencias y errores, manteniendo el flujo del programa sin interrupciones.


### **Debilidades de la Implementación**
- **Velocidad:**
El procesamiento secuencial puede ser más lento comparado con enfoques vectorizados.

- **Limitaciones en Paralelismo:**
No aprovecha múltiples núcleos de CPU, aunque puede ser adaptada para ello.
---

## **2. Archivo: `q1_time.py`**
Esta implementación resuelve el problema Q1 utilizando un enfoque modular basado en **MapReduce**, priorizando la **optimización en tiempo de ejecución**.

---

## **Estructura Modular del Código**

### **1. `leer_tweets()`**
Lee el archivo NDJSON línea por línea utilizando un **generador**, evitando cargar todo en memoria.

```python
def leer_tweets(file_path: str) -> Generator[Dict, None, None]
```

#### **Argumentos**
- `file_path (str)`: Ruta del archivo NDJSON.

#### **Retorno**
- `Generator[Dict]`: Generador que produce tweets en formato JSON.

#### **Responsabilidades**
- Leer archivos grandes mediante streaming.
- Ignorar tweets malformados sin detener la ejecución.
- Manejar excepciones de archivo y decodificación JSON.

---

### **2. `map_tweets()`**
Crea dos contadores:
1. **`date_counts`**: Contador del total de tweets por fecha.
2. **`date_user_counts`**: Contador de tweets por usuario agrupados por fecha.

```python
def map_tweets(tweets: Generator[Dict, None, None]) -> Tuple[Counter, defaultdict]
```

#### **Argumentos**
- `tweets (Generator)`: Generador de tweets en JSON.

#### **Retorno**
- `Tuple[Counter, defaultdict]`: Contadores de tweets por fecha y usuarios por fecha.

#### **Responsabilidades**
- Extraer fechas y usuarios de los tweets.
- Usar **`defaultdict`** para evitar verificaciones adicionales.
- Registrar advertencias si falta información crítica.

---

### **3. `reduce_tweets()`**
Reduce los resultados para encontrar las **10 fechas más activas** y los **usuarios más frecuentes** en cada fecha.

```python
def reduce_tweets(
        date_counts: Counter, date_user_counts: defaultdict
) -> List[Tuple[datetime.date, str]]
```

#### **Argumentos**
- `date_counts (Counter)`: Contador de tweets por fecha.
- `date_user_counts (defaultdict)`: Contador de usuarios por fecha.

#### **Retorno**
- `List[Tuple[datetime.date, str]]`: Lista de las 10 fechas más activas y los usuarios más frecuentes.

#### **Responsabilidades**
- Usar **`most_common()`** para encontrar las fechas más activas.
- Usar **`max()`** para encontrar los usuarios más activos en cada fecha.

---

### **4. `q1_time()`**
Función principal que coordina las fases de **Map** y **Reduce**.

```python
def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]
```

#### **Argumentos**
- `file_path (str)`: Ruta del archivo NDJSON.

#### **Retorno**
- `List[Tuple[datetime.date, str]]`: Lista con las fechas más activas y los usuarios más frecuentes.

#### **Responsabilidades**
- Verificar que el path del archivo no sea nulo.
- Registrar errores si el archivo no se puede abrir.
- Integrar todas las fases del proceso para generar el resultado final.

---


### **Fortalezas de la Implementación**
- **Optimización en Tiempo:**
Uso de max() para encontrar usuarios más activos rápidamente.
defaultdict evita verificaciones adicionales, mejorando la velocidad.

- **Manejo Robusto de Errores:**
El logger registra errores y advertencias, permitiendo que el proceso continúe.

- **Modularidad:**
Cada función tiene una única responsabilidad, facilitando el mantenimiento y la extensión.

### **Debilidades de la Implementación**

- **Paralelismo:**
Actualmente, no aprovecha múltiples núcleos de CPU, aunque se puede extender fácilmente.

- **Consumo de Memoria:**
Usa contadores en memoria, lo que puede ser problemático para archivos extremadamente grandes.

---
## **Comparación General de las Implementaciones Q1**

| **Aspecto**                 | **Optimización en Memoria** (`q1_memory`)                | **Optimización en Tiempo** (`q1_time`)                   |
|-----------------------------|----------------------------------------------------------|---------------------------------------------------------|
| **Objetivo Principal**       | Minimizar el consumo de memoria durante la ejecución.    | Acelerar el procesamiento para obtener resultados más rápidamente. |
| **Estructuras de Datos**     | Utiliza **múltiples contadores** (`Counter` y `defaultdict`) para dividir las tareas. | Utiliza un **único contador global** para evitar múltiples operaciones. |
| **Uso de Generadores**       | Sí, para evitar cargar todo el archivo en memoria.       | Sí, para mantener un flujo rápido de lectura.            |
| **Actualización de Contadores** | Distribuye la carga entre contadores más pequeños por fecha y usuario. | Mantiene un contador global para minimizar las operaciones. |
| **Manejo de Errores**        | Registra advertencias en el logger para tweets malformados sin detener la ejecución. | Maneja errores de forma similar, priorizando la velocidad. |
| **Velocidad**                | Más lento debido a la gestión distribuida de contadores. | Más rápido al utilizar un flujo continuo con menos operaciones. |
| **Consumo de Memoria**       | Menor, debido al uso de múltiples contadores más pequeños. | Mayor, ya que el contador global ocupa más espacio en memoria. |
| **Escalabilidad**            | Ideal para sistemas con recursos de memoria limitados.  | Ideal para sistemas donde la velocidad es más importante que la memoria. |

---

## **3. Archivo: `q2_memory.py`**  

Esta versión del problema **Q2** utiliza la metodología **MapReduce** para contar las ocurrencias de emojis en tweets, priorizando la **optimización del uso de memoria**. El enfoque se basa en procesar los tweets en **streaming** y usar estructuras de datos eficientes que minimizan la carga en memoria.

---

## **Estructura del Código**

### **1. `leer_tweets()`**
Esta función lee el archivo NDJSON en **streaming**, generando los tweets uno por uno para evitar cargar el archivo completo en memoria.

```python
def leer_tweets(file_path: str) -> Generator[Dict, None, None]
```

#### **Argumentos**
- `file_path (str)`: Ruta del archivo NDJSON.

#### **Retorno**
- `Generator[Dict]`: Generador que produce cada tweet como un objeto JSON.

#### **Responsabilidades**
- Procesar el archivo en modo streaming.
- Ignorar líneas malformadas y registrar advertencias sin detener la ejecución.

---

### **2. `map_emojis()`**
Procesa cada tweet para extraer los emojis del contenido y acumular sus ocurrencias.

```python
def map_emojis(tweets: Generator[Dict, None, None]) -> Counter
```

#### **Argumentos**
- `tweets (Generator)`: Generador de tweets en JSON.

#### **Retorno**
- `Counter`: Contador con las ocurrencias de cada emoji.

#### **Responsabilidades**
- Extraer emojis del contenido del tweet.
- Actualizar el `Counter` solo si hay emojis.

---

### **3. `reduce_emojis()`**
Combina múltiples contadores para obtener el total de ocurrencias por emoji.

```python
reduce_emojis(emoji_counters: List[Counter]) -> Counter
```

#### **Argumentos**
- `emoji_counters (List[Counter])`: Lista de contadores de emojis.

#### **Retorno**
- `Counter`: Contador combinado con las ocurrencias totales de cada emoji.

#### **Responsabilidades**
- Usar la operación de suma de `Counter` para combinar los resultados.

---

### **4. `q2_memory()`**
Función principal que coordina las fases de **Map** y **Reduce** para resolver Q2 con optimización en memoria.

```python
def q2_memory(file_path: str) -> List[Tuple[str, int]]
```

#### **Argumentos**
- `file_path (str)`: Ruta del archivo NDJSON.

#### **Retorno**
- `List[Tuple[str, int]]`: Lista de los 10 emojis más comunes y sus frecuencias.

#### **Responsabilidades**
- Verificar que la ruta del archivo no sea nula.
- Coordinar las fases de **Map** y **Reduce**.
- Registrar errores y advertencias mediante **logger**.

---

### **Fortalezas de la Implementación**
- **Optimización de Memoria:**
Procesa los tweets en streaming, minimizando el uso de memoria.
Usa generadores para evitar la carga completa del archivo en memoria.

- **Manejo Robusto de Errores:**
El logger registra advertencias sin interrumpir el flujo de ejecución.
Captura errores de archivo y decodificación JSON.

- **Extensibilidad:**
La estructura modular permite añadir paralelismo en futuras versiones si es necesario.

### **Debilidades de la Implementación**
- **Velocidad:**
Aunque optimiza el uso de memoria, el procesamiento secuencial puede ser más lento comparado con técnicas paralelas.

- **Limitaciones en Escalabilidad:**
No aprovecha múltiples núcleos de CPU, aunque es posible extender la implementación en el futuro.

---

## **4. Archivo: `q2_time.py`**  

Esta implementación resuelve el problema **Q2** usando la metodología **MapReduce**, enfocándose en optimizar el **tiempo de ejecución**. El uso de **generadores**, el procesamiento eficiente con contadores y la estructura modular garantizan que la solución sea rápida y escalable.

---

## **Estructura del Código**

### **1. `leer_tweets()`**
Esta función lee el archivo NDJSON línea por línea utilizando un generador, lo que permite un procesamiento eficiente y rápido.

```python
def leer_tweets(file_path: str) -> Generator[Dict, None, None]
```
#### **Argumentos**
- `file_path (str)`: Ruta del archivo NDJSON.

#### **Retorno**
- `Generator[Dict]`: Generador que produce cada tweet en formato JSON.

#### **Responsabilidades**
- Leer archivos grandes mediante streaming.
- Registrar advertencias para JSONs malformados sin detener la ejecución.

---

### **2. `map_emojis()`**
Extrae los emojis de cada tweet y acumula sus ocurrencias en un solo paso para optimizar la velocidad.

```python
def map_emojis(tweets: Generator[Dict, None, None]) -> Counter
```

#### **Argumentos**
- `tweets (Generator)`: Generador de tweets en JSON.

#### **Retorno**
- `Counter`: Contador con las ocurrencias de cada emoji.

#### **Responsabilidades**
- Procesar el contenido del tweet y extraer los emojis.
- Actualizar el contador eficientemente.

---

### **3. `reduce_emojis()`**
Combina varios contadores de emojis en uno solo, optimizando el proceso de reducción.

```python
def reduce_emojis(emoji_counters: List[Counter]) -> Counter:
```

#### **Argumentos**
- `emoji_counters (List[Counter])`: Lista de contadores de emojis.

#### **Retorno**
- `Counter`: Contador combinado con las ocurrencias totales de cada emoji.

#### **Responsabilidades**
- Usar la operación de suma de `Counter` para combinar eficientemente los resultados.

---

### **4. `q2_time()`**
Función principal que coordina las fases de **Map** y **Reduce** para resolver el problema Q2.

```python
def q2_time(file_path: str) -> List[Tuple[str, int]]
```
#### **Argumentos**
- `file_path (str)`: Ruta del archivo NDJSON.

#### **Retorno**
- `List[Tuple[str, int]]`: Lista de los 10 emojis más comunes y sus frecuencias.

#### **Responsabilidades**
- Verificar que la ruta del archivo no sea nula.
- Integrar las fases de **Map** y **Reduce** para obtener los resultados finales.

---

### **Fortalezas de la Implementación**

- **Optimización en Tiempo:**
Uso de generadores para minimizar operaciones innecesarias.
Contador de emojis actualizado en un solo paso.

- **Manejo Robusto de Errores:**
El logger registra errores sin interrumpir el flujo del programa.
Captura excepciones en la apertura del archivo y en la decodificación de JSON.

- **Modularidad y Escalabilidad:**
La estructura modular facilita la extensión del código a entornos paralelos o distribuidos.


### **Debilidades de la Implementación**
- **Uso Moderado de Memoria:**
Aunque es rápido, mantiene un contador en memoria que puede ser problemático con archivos muy grandes.
- **Paralelismo no Implementado:**
No aprovecha múltiples núcleos de CPU, aunque se puede extender fácilmente.
---
## **Principales Diferencias en ambas Implementaciones**

| **Aspecto**                 | **Optimización en Memoria**                                | **Optimización en Tiempo**                                |
|-----------------------------|------------------------------------------------------------|----------------------------------------------------------|
| **Objetivo Principal**       | Reducir el consumo de memoria durante la ejecución.        | Acelerar el procesamiento para obtener resultados más rápido. |
| **Procesamiento**            | Procesa el archivo en **streaming** línea por línea para minimizar el uso de memoria. | Usa operaciones en **un solo paso** para reducir la sobrecarga computacional. |
| **Contador de Emojis**       | Mantiene múltiples contadores pequeños que se combinan en la fase de **Reduce**. | Utiliza un único **contador global** para minimizar las operaciones y acelerar el proceso. |
| **Uso de Generadores**       | Sí, para evitar cargar todo el archivo en memoria.         | Sí, para mantener un flujo rápido y eficiente.            |
| **Manejo de Errores**        | Registra advertencias para tweets malformados sin interrumpir la ejecución. | Registra errores sin interrumpir el flujo para maximizar la velocidad. |
| **Escalabilidad**            | Mejor para archivos muy grandes donde la memoria es limitada. | Ideal para escenarios donde la velocidad es crítica y la memoria no es un problema. |
| **Consumo de Memoria**       | Bajo, ya que utiliza múltiples contadores en pequeñas fases de procesamiento. | Moderado, ya que mantiene un contador global en memoria durante todo el proceso. |
| **Velocidad**                | Más lento debido a múltiples fases de mapeo y reducción.   | Más rápido al procesar todo en un único contador y reducir operaciones innecesarias. |

---

## **5. Archivo: `q3_memory.py`**  

Esta versión del problema **Q3** utiliza la metodología **MapReduce** para contar las menciones de usuarios en tweets, priorizando la **optimización en tiempo de ejecución**. El enfoque se basa en procesar los tweets rápidamente usando **expresiones regulares precompiladas** y **contadores eficientes**.

---

## **Estructura del Código**

### **1. `leer_tweets()`**
Lee el archivo NDJSON línea por línea mediante un generador para mantener la eficiencia durante la ejecución.

#### **Argumentos**
- `file_path (str)`: Ruta del archivo NDJSON.

#### **Retorno**
- `Generator[Dict]`: Generador que produce cada tweet como un objeto JSON.

#### **Responsabilidades**
- Leer los tweets sin cargarlos todos en memoria.
- Manejar excepciones y registrar advertencias para JSONs malformados.

---

### **2. `map_mentions()`**
Busca menciones de usuarios dentro del contenido de los tweets y acumula sus ocurrencias en un `Counter`.

#### **Argumentos**
- `tweets (Generator)`: Generador de tweets en JSON.

#### **Retorno**
- `Counter`: Contador con las menciones acumuladas de cada usuario.

#### **Responsabilidades**
- Usar una expresión regular para identificar menciones de usuarios.
- Actualizar el contador eficientemente para evitar operaciones repetitivas.

---

### **3. `reduce_mentions()`**
Combina varios contadores de menciones en un único `Counter`.

#### **Argumentos**
- `mention_counters (List[Counter])`: Lista de contadores de menciones.

#### **Retorno**
- `Counter`: Contador con las menciones totales combinadas.

#### **Responsabilidades**
- Usar la suma de `Counter` para combinar resultados rápidamente.

---

### **4. `q3_memory()`**
Función principal que coordina las fases de **Map** y **Reduce** para resolver Q3 de manera eficiente.

#### **Argumentos**
- `file_path (str)`: Ruta del archivo NDJSON.

#### **Retorno**
- `List[Tuple[str, int]]`: Lista de los 10 usuarios más mencionados con sus frecuencias.

#### **Responsabilidades**
- Verificar que la ruta no sea nula.
- Coordinar las fases de **Map** y **Reduce** para obtener resultados precisos y rápidos.

---

### **Fortalezas de la Implementación**

- **Optimización en Tiempo:**
Uso de expresión regular compilada para mejorar la velocidad en la búsqueda de menciones.
El contador se actualiza en un solo paso para maximizar la eficiencia.

- **Manejo Robusto de Errores:**
El logger registra advertencias sin detener la ejecución.
Captura excepciones relacionadas con la apertura y decodificación del archivo.

- **Modularidad y Extensibilidad:**
El diseño modular permite añadir fácilmente paralelismo o integración con sistemas distribuidos.

### **Debilidades de la Implementación**
- **Uso Moderado de Memoria:**
Aunque es rápido, mantiene un contador en memoria que puede ser problemático con archivos muy grandes.

- **Paralelismo no Implementado:**
No aprovecha múltiples núcleos de CPU, aunque se puede extender fácilmente.
  
---

## **6. Archivo: `q3_time.py`**  

Esta implementación de **Q3** usa la metodología **MapReduce** para contar las menciones de usuarios (@usuario) en tweets, priorizando la **optimización del tiempo de ejecución**. Se utilizan generadores y técnicas eficientes de conteo para garantizar un procesamiento rápido y escalable.

---

## **Estructura del Código**

### **1. `leer_tweets()`**
Esta función lee el archivo NDJSON utilizando un generador para reducir los accesos a estructuras en memoria.

#### **Argumentos**
- `file_path (str)`: Ruta del archivo NDJSON.

#### **Retorno**
- `Generator[Dict]`: Generador que produce cada tweet como un objeto JSON.

#### **Responsabilidades**
- Leer el archivo de forma secuencial para optimizar la velocidad.
- Registrar advertencias para tweets malformados sin detener la ejecución.

---

### **2. `map_mentions()`**
Esta función procesa cada tweet y extrae las menciones de usuarios utilizando expresiones regulares para mejorar el rendimiento.

#### **Argumentos**
- `tweets (Generator)`: Generador de tweets en JSON.

#### **Retorno**
- `Counter`: Contador con las menciones de cada usuario.

#### **Responsabilidades**
- Utilizar expresiones regulares precompiladas para mejorar el tiempo de ejecución.
- Actualizar el contador en un solo paso para maximizar la velocidad.

---

### **3. `reduce_mentions()`**
Combina varios contadores en un solo `Counter`, consolidando las ocurrencias de usuarios mencionados.

#### **Argumentos**
- `mention_counters (List[Counter])`: Lista de contadores de menciones.

#### **Retorno**
- `Counter`: Contador con las menciones combinadas de usuarios.

#### **Responsabilidades**
- Utilizar operaciones eficientes de suma entre contadores.

---

### **4. `q3_time_map()`**
Función principal que coordina las fases de **Map** y **Reduce** para obtener los 10 usuarios más mencionados.

#### **Argumentos**
- `file_path (str)`: Ruta del archivo NDJSON.

#### **Retorno**
- `List[Tuple[str, int]]`: Lista de los 10 usuarios más mencionados y sus frecuencias.

#### **Responsabilidades**
- Verificar que la ruta del archivo no sea nula.
- Registrar errores y advertencias utilizando **logger**.

---
### **Fortalezas de la Implementación**
**Optimización en Tiempo:**
Uso de expresiones regulares precompiladas para minimizar el tiempo de búsqueda.
Procesamiento en un solo paso para maximizar la eficiencia.

**Manejo Robusto de Errores:**
Registro de errores y advertencias mediante logger sin detener la ejecución.

**Modularidad:**
La estructura modular permite futuras extensiones para paralelismo o distribución.

### **Debilidades de la Implementación**
**Uso de Memoria Moderado:**
Mantener un Counter global en memoria puede ser un desafío para archivos muy grandes.

**Falta de Paralelismo:**
No aprovecha múltiples núcleos, aunque la implementación es fácilmente extensible.

---

## **Comparación Ambos Enfoques**

| **Aspecto**                 | **Optimización en Memoria** (`q3_memory`)                 | **Optimización en Tiempo** (`q3_time`)                   |
|-----------------------------|----------------------------------------------------------|---------------------------------------------------------|
| **Objetivo Principal**       | Reducir el consumo de memoria.                           | Maximizar la velocidad de procesamiento.                |
| **Procesamiento**            | Usa múltiples contadores que se combinan en la fase de **Reduce**. | Mantiene un **contador global** para minimizar operaciones. |
| **Expresiones Regulares**    | Usa una expresión regular sin precompilar (menos eficiente). | Usa **expresiones regulares precompiladas** para acelerar la búsqueda. |
| **Generadores**              | Utiliza **generadores** para procesar los tweets en streaming. | Utiliza **generadores** para reducir operaciones de E/S. |
| **Uso de Memoria**           | Menor consumo de memoria, debido a múltiples contadores pequeños. | Mayor consumo de memoria al mantener un contador global en ejecución. |
| **Velocidad de Ejecución**   | Más lento, debido al uso de múltiples contadores.        | Más rápido al mantener un flujo continuo con un solo contador. |
| **Manejo de Errores**        | Usa **logger** para advertencias y errores sin detener el proceso. | Usa **logger** de forma similar para un seguimiento robusto. |
| **Escalabilidad**            | Adecuado para sistemas con **memoria limitada**.         | Ideal para sistemas donde la **velocidad es crítica** y hay memoria disponible. |

---

## **Casos de Uso Recomendados**

### **Optimización en Memoria**
- **Archivos extremadamente grandes** que no pueden cargarse completamente en memoria.
- Sistemas con **recursos de memoria limitados**.
- Situaciones donde el tiempo de ejecución no es crítico.

### **Optimización en Tiempo de Ejecución**
- **Sistemas con suficiente memoria** disponible.
- Escenarios donde **la velocidad es crítica**, como procesamiento en tiempo real.
- Casos donde se necesita **procesar grandes volúmenes de datos rápidamente**.

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
| **[q1_memory_json.py](./q1_memory_json.py)**      | Rápido                    | Muy bajo               | Baja                        | Baja                       | Sí (si la simplicidad es clave)     |
| **[q1_memory_polars.py](./q1_memory_polars.py)**    | Moderado                   | Alta               | Alta                        | Media                      | Sí (si se necesita velocidad)       |
| **[q1_memory_pyspark.py](./q1_memory_pyspark.py)**   | Muy rápido (distribuido) | Moderada               | Muy alta                    | Alta                       | No (excesivo para 400 MB)           |
| **[q1_memory_tqdm.py](./q1_memory_tqdm.py)**      | Rápido (paralelo)        | Alta                   | Alta                        | Media                      | Sí (en sistemas multicore)          |

---

## **Conclusión**

Para un archivo **NDJSON de 400 MB**, las opciones más recomendadas son:

- **[q1_memory_json.py](./q1_memory_json.py)** : Si se prioriza la simplicidad y el uso eficiente de memoria.
- **[q1_memory_tqdm.py](./q1_memory_tqdm.py)**: Ideal si se tiene acceso a una máquina con múltiples núcleos para aprovechar el procesamiento paralelo.
- **[q1_memory_polars.py](./q1_memory_polars.py)**: Si se necesita mayor velocidad sin comprometer demasiada memoria.

El enfoque con **PySpark** en el archivo **[q1_memory_pyspark.py](./q1_memory_pyspark.py)** es adecuado para datasets más grandes o si el procesamiento forma parte de un flujo distribuido.

**Es por esto que para el resto de los desafios se realizaron basados en la libreria json de python.**
