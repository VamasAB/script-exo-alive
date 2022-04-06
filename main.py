import subprocess, logging, time, smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import environ

env = environ.Env()
environ.Env.read_env()

logging.basicConfig(
    filename='logger.log',
    # filemode='w',
    format='%(asctime)s - %(message)s',
    level=logging.INFO
)

debug = env.int('DEBUG')

#https://realpython.com/python-send-email/

def mail_to():
    recipiants = env.list('RECIPIANTS')
    smtp_server = env('SMTP_SERVER')
    sender_email = env('SENDER_EMAIL')
    port = env('PORT') # For SSL
    password = env('PASSWORD')
    exo_server = env('EXO_SERVER')

    message = MIMEMultipart("alternative")
    message["Subject"] = f'Automatisk omstart av {exo_server}'
    message["From"] = sender_email
    message["To"] = ", ".join(recipiants)

    # Create the plain-text and HTML version of your message
    text = """\
    Omstart har skett av {exo_server}."""
    html = """\
    <html>
        <body>
            <p>Omstart har skett av {exo_server}.</p>
        </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, recipiants, message.as_string().format(exo_server=exo_server))
        logging.info('Sent e-mails responsible staff.')
    except Exception as e:
        # Print any error messages to stdout
        logging.info('Failed to send e-mails.')
        print(e)
    finally:
        server.quit() 


def get_task_status(task_name):
    tasks = subprocess.check_output(f'tasklist /v /fi "IMAGENAME eq {task_name}"').decode('cp866', 'ignore').split("\r\n")

    for task in tasks:
        if task_name in task:
            return False if 'Not Responding' in task else True
    
    return 0


def exo_handle(start=False):
    start_uri = ['C:\Program Files\EXO\EXOop4\Eo4Run.Exe', 'C:\Windows\\notepad.exe']
    stop_uri = ['C:\Program Files\EXO\EXOstop.exe', 'C:\Windows\\winhlp32.exe']

    name = 'Eo4Run' if start else 'EXOstop'
    uri = start_uri[debug] if start else stop_uri[debug]

    try:
        status = subprocess.Popen(uri)
        logging.info(f'Succesfully ran {name}.')
        return status
    except:
        logging.info(f'{name} failed to run.')
        return 0


if __name__ == '__main__':
    logging.info('-----------------------------------------------------')
    logging.info('Checking for hung processes..')
    task_name = ['Eo4Run.Exe', 'Notepad.exe']
    task = get_task_status(task_name[debug])

    if task == 0:
        logging.info(f'Failed to find any running {task_name[debug]}.')
    elif task and debug == 0:
        logging.info(f'Task {task_name[debug]} is Running or Unknown, no action required.')
    else:
        logging.info(f'{task_name[debug]} is Not Responding, restarting services.')
        
        retry = 1
        # Trying to run Exostop 5 times before exiting script        
        while retry <= 5:
            logging.info(f'Running EXOstop, try {retry} of 5.')
            stop_status = exo_handle()
            if stop_status == 0:
                retry += 1
            else:
                break
        
        # Trying to run Eo4Run if EXOstop was successful and Exo is not still running.
        if stop_status != 0:
            retry = 1
            while retry <= 5:
                time.sleep(10)
                logging.info(f'Starting service {task_name[debug]}, try {retry} of 5.')
                start_status = get_task_status(task_name[debug])
                if start_status == 0:
                    task = exo_handle(True)
                    if task != 0:
                        mail_to()
                        break
                    else:
                        retry += 1
                else:
                    retry += 1
        else:
            logging.info(f'Failed to stop EXO service, closing down.')