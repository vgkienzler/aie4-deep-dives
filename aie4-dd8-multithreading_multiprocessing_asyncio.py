"""
Here is the result of a run:

=======================================================
=== I/O-Bound Task ===

Sequential Execution (I/O-bound):
I/O Task Complete
I/O Task Complete
I/O Task Complete
Sequential Execution Time: 3.00 seconds

Multithreading Execution (I/O-bound):
I/O Task Complete
I/O Task CompleteI/O Task Complete

Multithreading Execution Time: 1.00 seconds

Multiprocessing Execution (I/O-bound):
I/O Task Complete
I/O Task CompleteI/O Task Complete

Multiprocessing Execution Time: 1.21 seconds

Asyncio Execution (I/O-bound):
I/O Task Complete
I/O Task Complete
I/O Task Complete
Asyncio Execution Time: 1.01 seconds
========================================================

Explanation: You can see here that for IO-bound tasks, multithreading and multiprocessing
are faster than sequential execution.
Sequential execution requires a total of 3 seconds to complete all three tasks, while
multithreading and multiprocessing take only 1 second. This is because the I/O-bound tasks
are waiting for the sleep function to complete, and the threads and processes can run concurrently.

========================================================
=== CPU-Bound Task ===

Sequential Execution (CPU-bound):
CPU Task Complete with 41538 primes
CPU Task Complete with 41538 primes
CPU Task Complete with 41538 primes
Sequential Execution Time: 6.57 seconds

Multithreading Execution (CPU-bound):
CPU Task Complete with 41538 primesCPU Task Complete with 41538 primes

CPU Task Complete with 41538 primes
Multithreading Execution Time: 6.46 seconds

Multiprocessing Execution (CPU-bound):
CPU Task Complete with 41538 primes
CPU Task Complete with 41538 primes
CPU Task Complete with 41538 primes
Multiprocessing Execution Time: 4.37 seconds

Asyncio Execution (CPU-bound):
CPU Task Complete with 41538 primes
CPU Task Complete with 41538 primes
CPU Task Complete with 41538 primes
Asyncio Execution Time: 10.65 seconds

Process finished with exit code 0
========================================================

Explanation: For CPU-bound tasks, multiprocessing is faster than sequential execution.
In this case, the CPU-bound task is finding prime numbers up to a limit.
The sequential execution requires a total of 6.57 seconds to complete all three tasks,
while multiprocessing takes only 4.37 seconds.
Multithreading is not faster than sequential execution because of the Global Interpreter Lock (GIL)
in Python, which prevents multiple threads from executing Python code simultaneously. Asyncio is
not suitable for CPU-bound tasks because it is designed for I/O-bound tasks and does not provide
true parallelism.
"""

## Dependencies
import time
import threading
import multiprocessing
import asyncio

# Define the limit for the CPU-bound task
LIMIT = 500000


# Define an I/O-bound task using sleep
def io_bound_task():
    time.sleep(1)
    print("I/O Task Complete")


# Define a CPU-bound task (finding primes up to a limit)
def cpu_bound_task():
    count = 0
    for num in range(2, LIMIT):
        if all(num % i != 0 for i in range(2, int(num ** 0.5) + 1)):
            count += 1
    print(f"CPU Task Complete with {count} primes")
    return count


# Sequential Execution
def sequential_execution(n_tasks, task_func):
    """Runs n_tasks one after the other, sequentially calling task_func().
    Measures the total time for all tasks, which shows the time without concurrency."""
    start = time.time()
    for _ in range(n_tasks):
        task_func()
    end = time.time()
    print(f"Sequential Execution Time: {end - start:.2f} seconds")


# Multithreading Execution
def multithreading_execution(n_tasks, task_func):
    """Creates a new Thread for each task.
    Starts and joins all threads, measuring total execution time.
    Shows improvement in I/O-bound tasks due to concurrent threads."""
    start = time.time()
    threads = []
    for _ in range(n_tasks):
        thread = threading.Thread(target=task_func)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    end = time.time()
    print(f"Multithreading Execution Time: {end - start:.2f} seconds")


# Multiprocessing Execution
def multiprocessing_execution(n_tasks, task_func):
    """Uses the Process class to create separate processes for each task.
    Each task runs in its process, fully independent (great for CPU-bound tasks)."""
    start = time.time()
    processes = []
    for _ in range(n_tasks):
        process = multiprocessing.Process(target=task_func)
        process.start()
        processes.append(process)

    for process in processes:
        process.join()
    end = time.time()
    print(f"Multiprocessing Execution Time: {end - start:.2f} seconds")


# Asyncio Execution
async def async_io_task():
    """Run the I/O-bound task asynchronously."""
    await asyncio.sleep(1)
    print("I/O Task Complete")


async def asyncio_cpu_task():
    """Is required because the function needs to be defined as 'async'."""
    return cpu_bound_task()


async def asyncio_execution(n_tasks, task_func):
    """Uses async functions (task_func), await and .gather() to simulate asynchronous tasks.
    Runs all tasks concurrently within a single event loop, avoiding the overhead of threads or processes."""
    start = time.time()
    if task_func == async_io_task:
        tasks = [task_func() for _ in range(n_tasks)]
        await asyncio.gather(*tasks)
    else:
        tasks = [task_func() for _ in range(n_tasks)]
        await asyncio.gather(*tasks)
    end = time.time()
    print(f"Asyncio Execution Time: {end - start:.2f} seconds")


if __name__ == "__main__":
    """In Python, multiprocessing on platforms like Windows and macOS requires that all code that
    creates new processes be enclosed in an if __name__ == "__main__": block. 
    This ensures that child processes don’t re-import the entire module (which can lead to infinite loops)."""

    # Set number of tasks for IO-bound task
    n_tasks_io_bound = 3

    # Run tests for I/O-bound task
    print("=== I/O-Bound Task ===")
    print("\nSequential Execution (I/O-bound):")
    sequential_execution(n_tasks_io_bound, io_bound_task)

    print("\nMultithreading Execution (I/O-bound):")
    multithreading_execution(n_tasks_io_bound, io_bound_task)

    print("\nMultiprocessing Execution (I/O-bound):")
    multiprocessing_execution(n_tasks_io_bound, io_bound_task)

    print("\nAsyncio Execution (I/O-bound):")
    asyncio.run(asyncio_execution(n_tasks_io_bound, async_io_task))

    # Set number of tasks and limit for CPU-bound task
    n_tasks_cpu_bound = 3

    # Run tests for CPU-bound task
    print("\n=== CPU-Bound Task ===")
    print("\nSequential Execution (CPU-bound):")
    sequential_execution(n_tasks_cpu_bound, cpu_bound_task)

    print("\nMultithreading Execution (CPU-bound):")
    multithreading_execution(n_tasks_cpu_bound, cpu_bound_task)

    print("\nMultiprocessing Execution (CPU-bound):")
    multiprocessing_execution(n_tasks_cpu_bound, cpu_bound_task)

    print("\nAsyncio Execution (CPU-bound):")
    asyncio.run(asyncio_execution(n_tasks_cpu_bound, asyncio_cpu_task))
