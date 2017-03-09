# -*- coding: utf-8 -*-
from .blocking import launch as _launch
from concurrent.futures import ThreadPoolExecutor

def launch(cmd, stdin, entry_sep=b''):
    # Do not pass a thread_name_prefix to ThreadPoolExecutor
    # as that is only for py36 and beyond.
    executor = ThreadPoolExecutor(max_workers=1)
    future = executor.submit(_launch, cmd, stdin, entry_sep)
    future.add_done_callback(lambda x: executor.shutdown(wait=False))
    return future
