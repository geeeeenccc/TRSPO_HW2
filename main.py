import random
import threading
import datetime


class Point:
    def __init__(self, x, y):
        self.X = x
        self.Y = y


class Container:
    def __init__(self):
        self.Pi = 0
        # self.Event = threading.Event()

    # def print_pi(self):
    #     print(f"Pi = {self.Pi}")


def montecarlo_calc_pi(points_th):
    inside = 0
    for p in points_th:
        if p.X ** 2 + p.Y ** 2 <= 1:
            inside += 1
    return inside / len(points_th) * 4.0


def generate_point():
    x = random.random()
    y = random.random()
    return Point(x, y)


# Function for multithreading, calculates Pi for a portion of points
def multithreading_helper(container_th):
    points_th = [generate_point() for _ in range(Size // ThreadNumber)]
    result_pi = montecarlo_calc_pi(points_th)
    container_th.Pi = result_pi
    # container_th.Event.set()


if __name__ == "__main__":
    Size = 10_000_000
    ThreadNumber = 48

    # Calculate Pi using a single thread
    print("One thread:")
    start = datetime.datetime.now()
    points = [generate_point() for _ in range(Size)]
    pi = montecarlo_calc_pi(points)
    end = datetime.datetime.now()
    print(f"{pi} for {(end - start).total_seconds()} sec")

    # Calculate Pi using multiple threads
    print("Multi-threading:")
    start = datetime.datetime.now()
    containers = []
    threads = []

    # Create and start multiple threads for parallel Pi calculation
    for _ in range(ThreadNumber):
        container = Container()

        containers.append(container)
        thread = threading.Thread(target=multithreading_helper, args=(container,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    pi = 0

    for container in containers:
        pi = pi + container.Pi

    pi = pi / ThreadNumber
    end = datetime.datetime.now()
    print(f"{pi} for {(end - start).total_seconds()} sec")
