# PRPA-Practica1 Curso 22/23 Pablo Fernández del Amo
The scripts are commented step by step. // El código está comentado paso a paso.

English:

Module Multiprocessing to execute Consumer - Producer Programme

Implement a concurrent merge:

We have NPROD processes that produce non-negative numbers in increasing order. When a process finishes producing, it produces a -1. Each process stores the value produced in a shared variable with the consumer, a -2 indicates that the storage is empty.

There is a merge process that should take the numbers and store them in increasing order in a single list (or array). The process should wait for the producers to have an element ready and insert the smallest one.

Lists of semaphores must be created. Each producer only handles its own semaphores for its data. The merge process must handle all the semaphores.

This is implemented in FernandezdelAmoP_Practica1.1.py

OPTIONAL: a fixed-size buffer can be implemented so that producers put values in the buffer. This is done in FernandezdelAmoP_Practica1.2.py

Español: 

Módulo Multiprocessing para ejecutar Programa Consumidor - Productor

Implementar un merge concurrente:

Tenemos NPROD procesos que producen números no negativos en orden creciente. Cuando un proceso termina de producir, produce un -1. Cada proceso almacena el valor producido en una variable compartida con el consumidor, un -2 indica que el almacenamiento está vacío.

Hay un proceso de combinación que debe tomar los números y almacenarlos en orden creciente en una sola lista (o matriz). El proceso debe esperar a que los productores tengan un elemento listo e inserten el más pequeño.

Se deben crear listas de semáforos. Cada productor solo maneja sus propios semáforos para sus datos. El proceso de fusión debe manejar todos los semáforos.

Esto está implementado en FernandezdelAmoP_Practica1.1.py

OPCIONAL: se puede implementar un búfer de tamaño fijo para que los productores pongan valores en el búfer. Esto se hace en FernandezdelAmoP_Practica1.2.py
