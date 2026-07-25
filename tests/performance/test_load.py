import threading
import time
import requests

URL = "http://127.0.0.1:8000/screener?min_roe=15"

results = []

def call_api():
    start = time.time()
    response = requests.get(URL)
    end = time.time()
    results.append((response.status_code, end - start))

threads = []
start = time.time()

for _ in range(10):
    t = threading.Thread(target=call_api)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end = time.time()

print("Total Time:", end - start)

for status, duration in results:
    print(status, round(duration, 3))