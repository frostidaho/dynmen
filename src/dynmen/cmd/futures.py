# -*- coding: utf-8 -*-
from .blocking import launch as _launch
from concurrent.futures import ThreadPoolExecutor

def launch(cmd, fn_input):
    # Do not pass a thread_name_prefix to ThreadPoolExecutor
    # as that is only for py36 and beyond.
    executor = ThreadPoolExecutor(max_workers=1)
    future = executor.submit(_launch, cmd, fn_input)
    future.add_done_callback(lambda x: executor.shutdown(wait=False))
    return future
