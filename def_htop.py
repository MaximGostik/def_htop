import psutil, json, datetime
from time import time

def write_cpu_info(func):
    file_name = "CPU-Info.json"

    def worker():
        res = func()
        with open(file_name, "w") as file:
            file.write(json.dumps(res, indent=4))
        return res

    return worker


@write_cpu_info
def get_cpu_percent(): #возвращает сведения о загруженности ядер

    data = psutil.cpu_percent(interval=1, percpu=True)
    diction = {}
    for i in range(len(data)):
        diction[i] = data[i]

    return diction


def show_cpu_percent(): #выводит сведения о загруженности ядер

    info = get_cpu_percent()

    for i in range(len(info)):
        counter = info[i] // 5
        print(i, '[' + '|' * round(counter) + '.' * (20 - round(counter)), info[i], '%]', end = '\n')

def write_mem_info(func):

    file_name = "Mem-Info.json"
    def worker():
        res = func()
        with open(file_name, "w") as file:
            file.write(json.dumps(res, indent=4))
        return res
    return worker

@write_mem_info
def get_mem_info():#возвращает сведения об используемой оперативной памяти

    data = psutil.virtual_memory()
    name = data._fields
    diction = {}

    for i in range(len(name)):
        diction[name[i]] = data[i]

    return diction


def show_mem_info():#выводит сведения об используемой оперативной памяти

    data = get_mem_info()

    counters = int(data['percent']) // 5
    mem_used = round(data['used'] / 1024**3, 2)
    mem_total = round(data['total'] / 1024**3, 2)
    print('\nMem[' + '|' * counters + '.' * (20 - counters), mem_used, '/', mem_total, 'Gb]')

def write_load_average(func):

    file_name = "Load-Average-Info.json"
    def worker():
        res = func()
        with open(file_name, "w") as file:
            file.write(json.dumps(res, indent=4))
        return res

    return worker
@write_load_average
def get_load_average():#выводит сведения о средней загруженности

    return [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]


def show_load_average():#выводит сведения о средней загруженности

    print('Load average:', *get_load_average())

def write_swap_memory(func):
    file_name = "Swap.memory_Info.json"

    def worker():
        res = func()
        with open(file_name, "w") as file:
            file.write(json.dumps(res, indent=4))
        return res

    return worker
@write_swap_memory
def get_swap_memory():

    return psutil.swap_memory()
def show_swap_memory():

    info = psutil.swap_memory()

    total = info[0] // 1024 ** 2
    used = info[1] // 1024 ** 2
    print('Swp[' + '|' * round(used / total / 20) + '.' * (20 - round(used / total / 20)), used, 'Мб /', total, 'Мб]')

def write_up_time(func):

    file_name = "Up_Time_Info.json"

    def worker():

        res = func()
        with open(file_name, "w") as file:
            file.write(json.dumps(res))
        return res

    return worker

@write_up_time
def get_up_time():

    dt = datetime.timedelta(seconds=time() - psutil.boot_time())
    dt = str(dt)
    return dt

def show_up_time():

    print('Uptime:', get_up_time())


def write_pids(func):

    file_name = "Pids.json"

    def worker():
        res = func()
        with open(file_name, "w") as file:
            file.write(json.dumps(res, indent=4))
        return res

    return worker

@write_pids
def get_pids():
    info = []

    for i in psutil.process_iter(['pid', 'name', 'status']):
        info.append(i.info)

    return info

def show_pids(info):

    print('Tasks:', len(psutil.pids()), '\n')
    format_pid = "{pid:<7} {name:<28} {status:<20}"
    print("{:<7} {:<28} {:<20}".format("PID", "Name", "Status"))
    for p in info:
        print(format_pid.format(**p))


def htop():
    return show_cpu_percent(), show_mem_info(), show_swap_memory(), show_load_average(), show_up_time(), show_pids(get_pids())

htop()
