# PRPA-Practica1
Module Multiprocessing to execute Consumer - Producer Programme

Implement a concurrent merge:

We have NPROD processes that produce non-negative numbers in increasing order. When a process finishes producing, it produces a -1. Each process stores the value produced in a shared variable with the consumer, a -2 indicates that the storage is empty.

There is a merge process that should take the numbers and store them in increasing order in a single list (or array). The process should wait for the producers to have an element ready and insert the smallest one.

Lists of semaphores must be created. Each producer only handles its own semaphores for its data. The merge process must handle all the semaphores.

OPTIONAL: a fixed-size buffer can be implemented so that producers put values in the buffer.
