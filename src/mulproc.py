import multiprocessing as mp
from tqdm import tqdm


class MulprocWithQueue():
    def __init__(self, job_func, job_items):
        self.num_units = mp.cpu_count()
        self.job_func = self._wrap(job_func)
        self.job_items = job_items
        self.queue = mp.Queue(maxsize=self.num_units)
        self.queue_lock = mp.Lock()

    def run(self):
        pool = mp.Pool(self.num_units, self.job_func)
        for queue_item in tqdm(self.job_items, total=len(self.job_items)):
            self.queue.put(queue_item)
        for _ in range(self.num_units):
            self.queue.put(None)
        pool.close()
        pool.join()

    def _wrap(self, job_func):
        def wrapped():
            while True:
                with self.queue_lock:
                    item = self.queue.get()
                if item is None:
                    break
                job_func(item)
        return wrapped