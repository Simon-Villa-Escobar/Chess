# Chess Game in Python

Este es un proyecto de un juego de ajedrez escrito en Python, inspirado por los [tutoriales de Eddie Sharick](https://www.youtube.com/playlist?list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_) en YouTube. El objetivo de este proyecto es crear un motor de ajedrez funcional utilizando algoritmos de búsqueda y evaluación básicos, como el algoritmo NegaMax con poda alfa-beta, incorporando técnicas de inteligencia artificial (AI) para la toma de decisiones.

## Tecnologías Utilizadas

- **Python**: Lenguaje de programación principal.
- **Pygame**: Utilizado para la interfaz gráfica del usuario (GUI) y para manejar la interacción del usuario.
- **Numpy** (opcional): Puede ser utilizado para mejorar la eficiencia de ciertas operaciones matemáticas y de manipulación de matrices.

## Funcionalidades

- **Movimiento de Piezas**: Implementación completa de las reglas de movimiento de cada pieza de ajedrez.
- **Detección de Jaque y Jaque Mate**: El juego detecta situaciones de jaque y jaque mate.
- **Algoritmo de Búsqueda y Evaluación**: Uso del algoritmo NegaMax con poda alfa-beta para evaluar el mejor movimiento posible, implementando técnicas de AI.
- **Interfaz Gráfica**: Utiliza Pygame para renderizar el tablero de ajedrez y las piezas.
- **Movimientos Aleatorios**: Función para seleccionar movimientos válidos de forma aleatoria (útil para pruebas).

## Requisitos

- Python 3.6 o superior
- Pygame

## Instalación

1. Clona el repositorio:
    ```sh
    git clone https://github.com/tuusuario/tu-repositorio.git
    cd tu-repositorio
    ```

2. Instala las dependencias:
    ```sh
    pip install pygame
    ```

3. (Opcional) Instala Numpy para mejorar la eficiencia:
    ```sh
    pip install numpy
    ```

## Uso

Ejecuta el script principal para iniciar el juego de ajedrez:

```sh
python ChessMain.py
```

## Mejoras Potenciales

- Optimización con Numpy: Para mejorar la eficiencia de ciertas operaciones matemáticas, se puede utilizar la biblioteca Numpy.
- Profundidad de Búsqueda: Incrementar la profundidad de búsqueda para considerar más movimientos futuros.
- Ordenación de Movimientos: Implementar una estrategia de ordenación de movimientos para evaluar primero los movimientos más prometedores.
- Transposition Tables: Utilizar tablas de transposición para almacenar y reutilizar resultados de evaluaciones de tableros previamente calculados, reduciendo la redundancia en los cálculos.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar este proyecto, por favor sigue estos pasos:

1. Haz un fork del proyecto.
2. Crea una nueva rama (`git checkout -b feature-nueva-caracteristica`).
3. Realiza los cambios necesarios y haz commit (`git commit -am 'Añadir nueva característica'`).
4. Haz push a la rama (`git push origin feature-nueva-caracteristica`).
5. Abre un Pull Request.

