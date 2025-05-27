"""
timing.py — Інструменти для вимірювання часу та частоти виконання.
"""

import time


class Timer:
    """
    Контекстний таймер для вимірювання часу виконання.
    """

    def __init__(self, label="Блок", verbose=True):
        self.label = label
        self.verbose = verbose
        self.start_time = None
        self.elapsed = None

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.elapsed = time.perf_counter() - self.start_time
        if self.verbose:
            print(f"[⏱] {self.label} виконано за {self.elapsed:.4f} сек")


class RateTracker:
    """
    Відстежує частоту виконання циклу (оновлень в секунду).
    """

    def __init__(self, window_size=100):
        self.window_size = window_size
        self.timestamps = []

    def tick(self):
        """
        Викликається на кожному циклі. Повертає поточну частоту (Hz).
        """
        now = time.perf_counter()
        self.timestamps.append(now)

        if len(self.timestamps) > self.window_size:
            self.timestamps.pop(0)

        if len(self.timestamps) < 2:
            return 0.0

        duration = self.timestamps[-1] - self.timestamps[0]
        if duration == 0:
            return 0.0

        return (len(self.timestamps) - 1) / duration

    def get_rate(self) -> float:
        """
        Повертає останню обчислену частоту.
        """
        return self.tick()
