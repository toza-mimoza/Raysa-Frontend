import time
import ray

ray.init()  # Specify this system has 4 CPUs.


@ray.remote
def do_some_work(x):
    time.sleep(1)  # Replace this with work you need to do.
    return x


start = time.time()
results = ray.get([do_some_work.remote(x) for x in range(100)])
print("duration =", time.time() - start)
print("results = ", results)
