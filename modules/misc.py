import logging, datetime, os, glob

def init_log(name, max_logs):
    if max_logs != -1:
        logs = glob.glob("logs/*.log")
        if len(logs) >= max_logs:
            try:
                for x in logs:
                    os.remove(x)
            except Exception as e:
                print("Removal of logs has failed!")
                print(e)
    log_name = os.path.join("log", datetime.datetime.today().strftime(f"%d-%m-%Y_%H-%M-%S_{name}.log"))
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(filename=log_name,
                filemode='w',
                format='%(asctime)s:%(msecs)d %(name)s %(levelname)s %(message)s',
                datefmt='%H:%M',
                level=logging.DEBUG)
    logging.info("Logger started!")
    return logging.getLoggerClass().root.handlers[0].baseFilename