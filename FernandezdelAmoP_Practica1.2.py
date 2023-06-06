
# -*- coding: utf-8 -*-

#Práctica 1, Parte Opcional: PABLO FERNÁNDEZ DEL AMO  04231435X

from multiprocessing import Process, current_process
from multiprocessing import Semaphore, Array, BoundedSemaphore
from multiprocessing import Manager, Value
from time import sleep 
from random import randint, random


N = 10 # number of integers produced by each producer
NProducers = 5 # Number of producers

Buffer_size = 2 # size of the buffer of each producer, difference with part 1


def delay(factor = 3):
    sleep(random()/factor)


def producer(personal_buffer, empty, non_empty):
    data = -1
    for iter in range(N): 
        non_empty.acquire()
        data = randint(data + 2, data + 40) 
        print(f"Producer {current_process().name} has produced the number: {data}")
        personal_buffer[iter % Buffer_size] = data

        print('Writing...')
        empty.release() 
       
    

    print(f"The producer {current_process().name} has finished producing") # print message to indicate that the producer has finished producing
    non_empty.acquire()
    for i in range(Buffer_size):
        personal_buffer[i] = -1
    empty.release()

       

def minimum(storages, positions):
    min_val, min_prod = -1, -1
    finished = True
    i = 0
    while i < NProducers and finished:
        idx = positions[i].value
        val = storages[i][idx]
        if val != -1:
            finished = False
            min_prod = i
            min_val = val
        i += 1
    for j in range(i, NProducers):
        idx = positions[j].value
        val = storages[j][idx]
        if val > 0 and val < min_val:
            min_val = val
            min_prod = j
    return finished, min_prod, min_val


def merge(storages, empty, non_empty, merged_products, positions):
    # Wait for all producers to produce something
    for sem in empty:
        sem.acquire()
    
    # Iterate while there are still producers producing numbers
    finished = False
    finished_producers = 0  # Add a counter for finished producers
    while not finished and finished_producers < NProducers:  # Stop if all producers are finished
        finished, index, val = minimum(storages, positions)
        # Print a message indicating that the collector is choosing a number to append
        print('Collector choosing a number from storage to append...')
        if not finished:
            try: 
                pos = (positions[index].value + 1) % Buffer_size
                positions[index].value = pos
                print(f"Collector has picked up and appended the number: {val}.")
                print('Ordering...')
                merged_products.append(val)

                delay()
                
            finally:
                non_empty[index].release()
                empty[index].acquire()
        else:
            print('Finished')
            finished_producers += 1  # Increment the counter if a producer is finished

                


def main():
    # Use a Manager() to share information between processes
    manager = Manager()
    # Create a shared list to store merged products
    merged_products = manager.list()
    positions = [Value('i', 0) for _ in range(NProducers)]

    storages = [Array('i', Buffer_size) for _ in range(NProducers)]

    # Two lists of semaphores foe each task
    non_empty = [BoundedSemaphore(Buffer_size) for _ in range(NProducers)]
    empty = [Semaphore(0) for _ in range(NProducers)] # In this section, we change the Lock() and use the Semaphore with size NBuffer,
    processes = []         

    for arr in storages:
        for pos in range(Buffer_size):
            arr[pos] = -2 #They start with -2 in its positions

    # Create NProd producer processes and append them to processes list
    for prod_number in range(NProducers):
        processes.append(Process(target=producer, name=f"Producer_{prod_number}",
                                  args=[storages[prod_number], empty[prod_number], non_empty[prod_number]]))
        
    # Create a consumer process and append it to processes list
    processes.append(Process(target=merge, name="Collector",
                             args=[storages, empty, non_empty, merged_products, positions]))
    
    print(f"Merged products before execution: {list(merged_products)}")
    print("Storage before execution: \n[", end = ' ')
    for i in storages:
        print(i[:], end =' ')
    print(']')

    # Start all processes
    for p in processes:
        p.start()
    # Wait for all processes to finish
    for p in processes:
        p.join()

    # Print the storage and merged products lists before and after execution
    print("Storage after execution: \n[", end = ' ')
    for i in storages:
        print(i[:], end =' ')
    print(']')
    

    # Print the merged products list after execution
    print(f"Merged products after execution: {list(merged_products)}")



if __name__ == '__main__':
    main()
