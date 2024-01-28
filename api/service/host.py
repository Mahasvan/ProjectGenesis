import os
import platform
import signal
import socket
import subprocess
import time
import re
import psutil

start_time = time.time()  # we use this for uptime


def get_processor_name():
    # https://stackoverflow.com/questions/4842448/getting-processor-information-in-python
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Darwin":
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
        command = "sysctl -n machdep.cpu.brand_string"
        return subprocess.check_output(command, shell=True).decode().strip()
    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        all_info = subprocess.check_output(command, shell=True).decode().strip()
        for line in all_info.split("\n"):
            if "model name" in line:
                return re.sub(".*model name.*:", "", line, 1)
    return platform.processor()


def pretty_time_from_seconds(time_remaining: int):
    if time_remaining < 0:
        return "0 seconds"
    minutes, seconds = divmod(time_remaining, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)

    final_string_to_join = []
    if weeks > 0:
        final_string_to_join.append(f"{weeks} {'weeks' if weeks != 1 else 'week'}")
    if days > 0:
        final_string_to_join.append(f"{days} {'days' if days != 1 else 'day'}")
    if hours > 0:
        final_string_to_join.append(f"{hours} {'hours' if hours != 1 else 'hour'}")
    if minutes > 0:
        final_string_to_join.append(f"{minutes} {'minutes' if minutes != 1 else 'minute'}")
    if seconds > 0:
        final_string_to_join.append(f"{seconds} {'seconds' if seconds != 1 else 'second'}")

    if len(final_string_to_join) > 1:
        final_string = ", ".join(final_string_to_join[:-1]) + f", and {final_string_to_join[-1]}"
    else:
        final_string = ", ".join(final_string_to_join)
    return final_string


async def hostinfo():
    response = {
        "os": platform.system(),
        "hostname": socket.gethostname(),
        "cpu": get_processor_name(),
        "cpu_threads": os.cpu_count(),
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
    }
    return response


async def uptime():
    now_time = time.time()
    seconds = now_time - start_time
    pretty_uptime = pretty_time_from_seconds(int(seconds))
    response = {
            "seconds": seconds,
            "text": pretty_uptime
        }
    return response
