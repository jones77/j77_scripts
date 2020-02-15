#!/usr/bin/env python3.7

import os
import sys

import psutil

DEBUG = False

BACKGROUND = ',bg=colour17'
RED = f'#[fg=red]'
RED_REVERSE = f'#[fg=red{BACKGROUND},reverse]'
MAGENTA = f'#[fg=magenta]'
PINK = f'#[fg=colour217,nobold]'
CYAN = f'#[fg=colour75]'
EMERGENCY = f'#[fg=cyan{BACKGROUND},noreverse]'
GREEN = f'#[fg=colour36,nobold]'
GREEN = f'#[fg=colour36,nobold]'
GREEN_BOLD = f'#[fg=colour36,bold]'
GREEN_REVERSE = f'#[fg=colour36{BACKGROUND},reverse]'
YELLOW = f'#[fg=colour227]'
YELLOW_REVERSE = f'#[fg=colour227{BACKGROUND},reverse]'
GREY = f'#[fg=colour243]'
GREY_REVERSE = f'#[fg=colour243{BACKGROUND},reverse]'
# FIXME: What's intro?
INTRO = f'#[fg=colour243,noreverse]#'

CPU_LOW = GREEN
CPU_HIGH = MAGENTA
CPU_110 = RED
CPU_CRAZY = EMERGENCY


if __name__ == '__main__':
    cpu_list = sorted(psutil.cpu_percent(interval=0.1, percpu=True))
    vm = psutil.virtual_memory()
    fmts = []
    for cpu in cpu_list:
        if cpu < 50.0:
            fmts.append(CPU_LOW)
        elif cpu >= 50.0 and cpu < 100.0:
            fmts.append(CPU_HIGH)
        elif cpu >= 100.0 and cpu < 110.0:
            fmts.append('{}'.format(CPU_110))
        elif cpu >= 110.0:
            fmts.append('{}'.format(CPU_CRAZY))

    # FIXME: Do fmts with deciles

    deciles = []  # string collection of cpu percentages
    for cpu in cpu_list:
        # TODO: Add option to use just "traffic lights" and no numbers
        decile_cpu = str(int(cpu / 10))
        if len(decile_cpu) == 1:
            deciles.append('{}'.format(decile_cpu))
        elif decile_cpu == '10':
            deciles.append('♨')
        elif decile_cpu == '11':
            deciles.append('!')
        else:
            deciles.append('<{}>'.format(decile_cpu))

    display = ''
    counter = 0
    for i, decile in enumerate(deciles):
        display += fmts[i]
        display += decile

    memory_used = 1 - (vm.available / vm.total)
    mem_digit = '{0:.0}'.format(memory_used)
    if mem_digit.startswith('0.'):
        mem_digit = mem_digit[2:]
    else:
        mem_digit = '!' + mem_digit + '!'

    stat = os.statvfs('.')
    du_used = int(round((1 - stat.f_bavail / stat.f_blocks) * 100))

    cwd=sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    ram_gb=int(round(vm.total/1024/1024/1024))

    print(
        f'{YELLOW}{cwd[-30:]}'
        f'{PINK}{du_used}'
        f'{GREEN}{ram_gb}'
        f'{PINK}{mem_digit}'
        f'{display}'
    )
