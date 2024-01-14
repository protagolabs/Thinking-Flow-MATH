import os
import logging 
import datetime 

# Set up the log for each time.
now = datetime.datetime.now()
name = os.getlogin()
USER = name.upper()
file_path = f"log/{USER}/{datetime.date.today()}"
os.makedirs(file_path,exist_ok=True)
def creat_logger(folder_path=f"log/{USER}/{datetime.date.today()}/", logging_name=f"Exp-{now.hour}:{now.minute}", suf_name=".log", name=""):
    if name:
        log_full_path = folder_path + name + suf_name
    else:
        log_full_path = folder_path + logging_name + suf_name
    logger = logging.getLogger(logging_name)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler(log_full_path, encoding='UTF-8',mode = 'w')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
logger = creat_logger()