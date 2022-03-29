import subprocess, logging, time, os

logging.basicConfig(
    filename='logger.log',
    filemode='w',
    format='%(asctime)s - %(message)s',
    level=logging.INFO
)

def get_task_status(task_name):
    tasks = subprocess.check_output(f'tasklist /v /fi "IMAGENAME eq {task_name}"').decode('cp866', 'ignore').split("\r\n")

    for task in tasks:
        if task_name in task:
            return False if 'Not Responding' in task else True
    
    return 0

def exo_handle(start=False):
    # start_uri = 'C:\Program Files\EXO\EXOop4\Eo4Run.Exe'
    # stop_uri = 'C:\Program Files\EXO\EXOstop.exe'

    name = 'Eo4Run' if start else 'EXOstop'
    uri = 'C:\Windows\\notepad.exe' if start else 'C:\Windows\\notepad.exe'

    try:
        logging.info(f'Running {name}.')
        status = subprocess.run(uri, check=True)
        return status
    except:
        logging.info(f'{name} failed to run.')
        return 0


if __name__ == '__main__':
    logging.info('Checking for hung processes..')
    task_name = 'Notepad.exe' #'Eo4Run.Exe' #
    task = get_task_status(task_name)

    if task == 0:
        logging.info(f'Failed to find {task_name}.')
    elif task:
        logging.info(f'Task {task_name} is Running or Unknown.')
    else:
        logging.info(f'{task_name} is Not Responding, restarting services.')
        exo_handle()
        time.sleep(45)
        logging.info(f'{task_name} has been stoped, starting service.')
        exo_handle(True)        