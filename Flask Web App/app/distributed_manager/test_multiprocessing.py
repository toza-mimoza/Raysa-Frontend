import multiprocessing
import time
import random
import queue


def worker(input_queue, stop_event):
    while not stop_event.is_set():
        try:
            # Check if any URL has arrived in the input queue. If not,
            # loop back and try again.
            url = input_queue.get(True, 1)
            input_queue.task_done()
        except queue.Empty:
            continue

        print("Started working on:", url)

        # Random delay to simulate fake processing.
        time.sleep(random.randint(1, 3))

        print("Stopped working on:", url)


def master():
    urls = [
        "https://jsonplaceholder.typicode.com/todos/1",
        "https://jsonplaceholder.typicode.com/todos/1",
        "https://jsonplaceholder.typicode.com/todos/1",
    ]

    input_queue = multiprocessing.JoinableQueue()
    stop_event = multiprocessing.Event()

    workers = []

    # Create workers.
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(input_queue, stop_event))
        workers.append(p)
        p.start()

    # Distribute work.
    for url in urls:
        input_queue.put(url)

    # Wait for the queue to be consumed.
    input_queue.join()

    # Ask the workers to quit.
    stop_event.set()

    # Wait for workers to quit.
    for w in workers:
        w.join()

    print("Done")


if __name__ == "__main__":
    master()
