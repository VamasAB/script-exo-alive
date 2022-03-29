import subprocess

if __name__ == '__main__':
    tasks = subprocess.check_output('tasklist /v').decode('cp866', 'ignore').split("\r\n")

    for task in tasks:
        print(task)