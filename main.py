import subprocess

def get_all_tasks():
    tasks = subprocess.check_output('tasklist /v').decode('cp866', 'ignore').split("\r\n")

    for task in tasks:
        print(task)


def get_task(name):
    tasks = subprocess.check_output('tasklist /v').decode('cp866', 'ignore').split("\r\n")

    _ = []

    for task in tasks:
        if name in task:
            _.append(task)
    return _


def check_if_alive(task_name):
    task_list = get_task(task_name)

    count = len(task_list)

    if count > 0:
        print('Found {} tasks named {}'.format(count, task_name))
        for task in task_list:
            if 'Not Responding' in task:
                print('Task: {} is Not responding'.format(task_name))
            else:
                print('Task: {} is Running or Unknown'.format(task_name))
    else:
        print('No task(s) found.')


check_if_alive('Eo4Run.Exe')
#get_all_tasks()
