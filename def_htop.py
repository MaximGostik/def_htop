import psutil
import pandas as pd
pd.set_option('display.max_rows', None)
from datetime import timedelta
from time import time

def get_cpu_percent():

    data = psutil.cpu_percent(interval=1, percpu=True)
    diction = {}
    for i in range(len(data)):
        diction[i] = data[i]

    return diction

def show_cpu_percent():

    info = get_cpu_percent()

    for i in range(len(info)):
        counter = info[i] // 5
        print(i, '[' + '|' * round(counter) + '.' * (20 - round(counter)), info[i], '%]', end = '\n')


def get_mem_info():

    data = psutil.virtual_memory()
    name = ['Total', 'Available', 'Percent', 'Used', 'Free']
    diction = {}

    for i in range(len(name)):
        diction[name[i]] = data[i]

    return diction

def show_mem_info():

    data = get_mem_info()

    counter = int(data['Percent']) // 5
    data_used = round(data['Used'] / 1024**3, 2)
    data_total = round(data['Total'] / 1024**3, 2)
    print('\nMem[' + '|' * counter + '.' * (20 - counter), data_used, '/', data_total, 'Gb]')

def show_load_average():

    print('Load average:', *[x / psutil.cpu_count() * 100 for x in psutil.getloadavg()])

def show_swap_memory():

    info = psutil.swap_memory()

    total = info[0] // 1024 ** 2
    used = info[1] // 1024 ** 2
    print('Swp[' + '|' * round(used / total / 20) + '.' * (20 - round(used / total / 20)), used, 'Мб /', total, 'Мб]')


def show_up_time():

    print('Uptime:', timedelta(seconds=time()-psutil.boot_time()))


def show_pids():

    info, PID, name, status = [], [], [], []

    for i in psutil.process_iter(['pid', 'name', 'username']):
        i = str(i)
        info.append(i[15:-1].split(','))

    for j in info:
        PID.append(j[0][4:])
        name.append(j[1][7:-1])
        status.append(j[2][9:-1])

    new_data = pd.DataFrame({
        'PID':PID,
        'NAME':name,
        'STATUS':status
    })

    print('Tasks:', len(psutil.pids()), '\n')
    print(new_data)

def htop():
    return show_cpu_percent(), show_mem_info(), show_swap_memory(), show_load_average(), show_up_time(), show_pids()

htop()