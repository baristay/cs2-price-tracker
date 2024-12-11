import os
import logging

#Log Settings
currentdir = os.path.dirname(os.path.abspath(__file__))
logdir = os.path.join(currentdir, "Logs")
loglist = os.listdir(logdir)
loglist.sort()
logdir = os.path.join(logdir, loglist[-1])

logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler(logdir, mode="a",encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.info("Starting Sorting_Logs_Prices.py Script...")


def deleting_excess(list: list,directory: str,directoryname: str,excessCount: int=5):
    logger.info(f"Checking directory count for: {directoryname}.")
    if len(list) > excessCount:
        logger.info(f"File count from {directoryname} directory is greater than provided exessCount. Exess count: {excessCount}, File count: {len(list)}")
        excess = len(list) - excessCount
        for i in range(excess):
            filedir = os.path.join(directory, list[i])
            os.remove(filedir)
            logger.info(f"{list[i]} file is deleted.")
    else:
        logger.info(f"File count from directory is less than provided exessCount. Exess count: {excessCount}, File count: {len(list)}")

def main():
    Logname = "Logs"
    Dataname = "Data"

    current_dir = os.getcwd()
    current_dir = current_dir.replace("scripts", "")
    csvout_dir = os.path.join(current_dir, Dataname)
    log_dir = os.path.join(current_dir, Logname)

    cvslist = os.listdir(csvout_dir)
    loglist = os.listdir(log_dir)

    cvslist.sort(key=lambda x: os.path.getctime(os.path.join(csvout_dir, x)))
    loglist.sort(key=lambda x: os.path.getctime(os.path.join(log_dir, x)))

    deleting_excess(loglist, log_dir, Logname)
    deleting_excess(cvslist,csvout_dir, Dataname)

if __name__ == "__main__":
    main()
