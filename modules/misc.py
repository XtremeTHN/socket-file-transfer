import logging, datetime, os, glob

def init_log(name, max_logs):
    if max_logs != -1:
        logs = glob.glob("logs/*.log")
        if len(logs) >= max_logs:
            try:
                for x in logs:
                    os.remove(x)
            except:
                print("Removal of logs has failed!")
                return
    name = datetime.datetime.today().strftime("%d-%m-%Y_%H-%M_auto-adb.log")
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(filename="logs/log.log" if not name else "logs/" + name,
                filemode='w',
                format='%(asctime)s:%(msecs)d %(name)s %(levelname)s %(message)s',
                datefmt='%H:%M',
                level=logging.DEBUG)
    logging.info("Logger started!")
    return logging.getLogger(name)