import subprocess
from re import search
from typing import Tuple

SPIN = {
    0: '|',
    1: '/',
    2: '-',
    3: '\\',
}

def get_lol_client_port_pw() -> Tuple[str, str]:
    """gets lol client port and pw for using the client api"""
    p = str(subprocess.Popen(
        "wmic PROCESS WHERE name='LeagueClientUx.exe' GET commandline",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ).communicate()[0])
    # print(p)
    port = search('--app-port=([0-9]*)', p).group().split('=')[1]
    pw = search('--remoting-auth-token=([\w-]*)', p).group().split('=')[1]
    return port, pw

def wait_for_task(task: str):
    """patience is a virtue"""
    tasklist = ''
    tasklist = str(subprocess.check_output('tasklist', shell=True))
    i=0
    while not task in tasklist:
        print(f'waiting for {task} {SPIN[i%4]}', end='\r')
        tasklist = str(subprocess.check_output('tasklist', shell=True))
        i += 1
    print(''*(14+len(str(task))), end='\r')