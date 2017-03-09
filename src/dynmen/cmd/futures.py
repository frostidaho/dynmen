from .blocking import launch as _launch
from concurrent.futures import ThreadPoolExecutor

def launch(cmd, stdin, entry_sep=b''):
    tname = 'dynmen_cmd_futures'
    executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix=tname)
    future = executor.submit(_launch, cmd, stdin, entry_sep)
    future.add_done_callback(lambda x: executor.shutdown(wait=False))
    return future
