import threading
import time

start = time.perf_counter()


def do_something():
    while True:
        print("Hej")
        time.sleep(1)
        print("då")


t1 = threading.Thread(target=do_something, daemon=True)
t2 = threading.Thread(target=do_something, daemon=True)

t1.start()
t2.start()

input()

finish = time.perf_counter()

print(f'Finished in {round(finish - start, 2)} second(s)')
