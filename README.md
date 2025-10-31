# Sistema de Decisión de Propinas usando Lógica Difusa

## 1. Modelo y Descripción del Problema

### Contexto

En un restaurante, decidir cuánta propina dejar es una decisión subjetiva que depende de múltiples factores. Este proyecto implementa un **sistema de inferencia difusa** que determina automáticamente el porcentaje de propina basándose en dos criterios principales:

-   **Calidad del servicio**: Evaluación subjetiva del servicio recibido (atención, rapidez, amabilidad)
-   **Calidad de la comida**: Evaluación de la comida (sabor, presentación, temperatura)

### Variables del Sistema

#### Variables de Entrada (Antecedentes)

1. **Calidad del Servicio**

    - Universo de discurso: [0, 10]
    - Conjuntos difusos:
        - `mala`: [0, 0, 5] - función triangular
        - `aceptable`: [0, 5, 10] - función triangular
        - `excelente`: [5, 10, 10] - función triangular

2. **Calidad de la Comida**
    - Universo de discurso: [0, 10]
    - Conjuntos difusos:
        - `mala`: [0, 0, 5] - función triangular
        - `aceptable`: [0, 5, 10] - función triangular
        - `excelente`: [5, 10, 10] - función triangular

#### Variable de Salida (Consecuente)

3. **Propina**
    - Universo de discurso: [0, 25]% del total de la cuenta
    - Conjuntos difusos:
        - `baja`: [0, 0, 13] - función triangular
        - `media`: [0, 13, 25] - función triangular
        - `alta`: [13, 25, 25] - función triangular

### Funciones de Pertenencia

Se utilizan **funciones triangulares** (`trimf`) para modelar los conjuntos difusos. Estas funciones permiten representar la transición gradual entre categorías, capturando la naturaleza imprecisa del razonamiento humano.

### Reglas Difusas

El sistema opera bajo tres reglas principales:

1. **Regla 1**: SI el servicio es malo O la comida es mala → ENTONCES la propina es baja
2. **Regla 2**: SI el servicio es aceptable → ENTONCES la propina es media
3. **Regla 3**: SI el servicio es excelente O la comida es excelente → ENTONCES la propina es alta

## 2. Implementación con scikit-fuzzy

### Instalación de Dependencias

```bash
pip install -r requirements.txt
```

### Ejecución del Sistema

```bash
python sistema_propinas_fuzzy.py
```

### Estructura del Código

El código implementa:

1. **Definición de variables difusas** usando `ctrl.Antecedent` y `ctrl.Consequent`
2. **Creación de funciones de pertenencia** usando `fuzz.trimf`
3. **Establecimiento de reglas** con `ctrl.Rule`
4. **Sistema de control** mediante `ctrl.ControlSystem`
5. **Simulación y cálculo** con `ctrl.ControlSystemSimulation`
6. **Visualización** de resultados con `matplotlib`

### Resultados Generados

El programa crea automáticamente una carpeta `output/` y genera 4 gráficos en ella:

1. **output/funciones_pertenencia.png**: Visualización de todas las funciones de pertenencia
2. **output/resultado_ejemplo.png**: Ejemplo de inferencia difusa para un caso específico
3. **output/superficie_control_3d.png**: Superficie tridimensional que muestra la relación entre entradas y salida
4. **output/analisis_sensibilidad.png**: Análisis de cómo varía la propina al cambiar cada variable

### Ejemplos de Salida

El sistema evalúa automáticamente varios casos:

**Caso 1**: Servicio malo (3/10), Comida excelente (8/10)

-   Propina sugerida: ~13.5%

**Caso 2**: Servicio aceptable (6.5/10), Comida aceptable (6/10)

-   Propina sugerida: ~13%

**Caso 3**: Servicio excelente (9/10), Comida excelente (9.5/10)

-   Propina sugerida: ~20%

**Caso 4**: Servicio malo (2/10), Comida mala (3/10)

-   Propina sugerida: ~6.5%

## 3. Recomendaciones y Conclusiones

### Interpretación de Resultados

El sistema muestra un comportamiento intuitivo:

-   Cuando **ambos factores son malos**, la propina es baja (~5-8%)
-   Cuando **al menos uno es excelente**, la propina aumenta significativamente
-   La **calidad del servicio tiene mayor peso** en la decisión (observable en el análisis de sensibilidad)
-   El sistema maneja bien la **incertidumbre** inherente a las evaluaciones subjetivas

### Ventajas de la Lógica Difusa

1. **Captura la subjetividad**: Modela el razonamiento humano que no es binario
2. **Transiciones suaves**: No hay cambios bruscos en la salida
3. **Interpretable**: Las reglas son fáciles de entender y modificar
4. **Robusto**: Funciona bien con datos imprecisos o ruidosos

### Posibles Mejoras

1. **Añadir más variables**: Considerar ambiente, limpieza, precio
2. **Refinamiento de reglas**: Incorporar más reglas para casos específicos
3. **Funciones de pertenencia ajustadas**: Usar funciones gaussianas o trapezoidales
4. **Ponderación de variables**: Dar diferentes pesos a servicio vs. comida
5. **Personalización**: Permitir al usuario ajustar sus preferencias

### Aplicaciones Prácticas

-   **Apps de restaurantes**: Integración en sistemas de pago digital
-   **Sistemas de recomendación**: Evaluar establecimientos
-   **Capacitación**: Herramienta educativa para personal de servicio
-   **Control de calidad**: Monitoreo de satisfacción del cliente

## 4. Tecnologías Utilizadas

-   **Python 3.x**: Lenguaje de programación
-   **scikit-fuzzy**: Librería de lógica difusa
-   **NumPy**: Cálculos numéricos
-   **Matplotlib**: Visualización de datos

## 5. Referencias

-   Documentación oficial de scikit-fuzzy: https://pythonhosted.org/scikit-fuzzy/
-   Zadeh, L. A. (1965). "Fuzzy sets". Information and Control.
-   Mamdani, E. H. (1974). "Application of fuzzy algorithms for control of simple dynamic plant"

---
