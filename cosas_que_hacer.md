# Corregir la base del código antes que el contenido

**Objetivo: Dejar el proyecto lo mas estable.**

- arreglar errores de estructura en entities.py
- revisar clases con métodos mal escritos o mal indentados
- asegurar que todas las entidades se inicializan correctamente

## Objetivos Especificos

**Enfocarse en estos puntos:**

- movimiento del personaje
- colisiones
- daño y muerte
- animaciones básicas
- respawn de enemigos


## Limpiar la lógica de los estados

- estado de animación
- estado de combate
- estado de vida
- estado de movimiento

## Ordenar el archivo entities.py

- dejar una clase base bien hecha
- que las clases hijas solo definan datos y comportamientos específicos
- evitar mezclar lógica de animación, combate y enemigos en un solo bloque

## Probar una sola mecánica a la vez

1. movimiento
2. salto
3. ataque
4. daño
5. enemigos
6. rondas


## ¿Qué corregir primero?

## Prioridad alta

- errores de inicialización en entities.py
- métodos mal definidos
- clases que no se construyen bien
- lógica de colisiones que no sea consistente

## Prioridad media

- animaciones duplicadas o conflictivas
- manejo de cámara
- reinicio de rondas y enemigos

## Prioridad baja

- mejoras visuales
- sonidos
- balance de combate
- contenido extra

> En resumen: primero estabilidad, luego gameplay, luego pulido.
