import time

def measure_time(func, *args):
    start = time.time()
    try:
        result = func(*args)
    except Exception as e:
        result = None
        print(f"Error in {func.__name__}: {e}")
    end = time.time()
    return result, end - start
