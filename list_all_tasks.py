import subprocess

def get_all_tasks():
    tasks = subprocess.check_output('tasklist /v').decode('cp866', 'ignore').split("\r\n")

    for task in tasks:
        print(task)

get_all_tasks()