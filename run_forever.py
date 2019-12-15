import time
from multiprocessing import Process, Value
from gui_main import gui_main
from handler.monitor import is_alive
from configs.config import check_detection_process_interval


def subprocess_run(detection_flag: Value) -> Process:
    p = Process(target=gui_main, args=(detection_flag,))
    p.start()
    return p


def main():
    detection_flag = Value('i', 0)  # variable(integer) with shared memory between multi processes
    p = subprocess_run(detection_flag)

    while True:
        time.sleep(check_detection_process_interval)
        if is_alive(detection_flag):
            print('The detection process is <alive>')
        else:
            print('The detection process is <dead>!')
            p.terminate()  # kill the subprocess
            time.sleep(1)
            print('reboot')
            detection_flag = Value('i', 0)
            p = subprocess_run(detection_flag)


if __name__ == '__main__':
    main()
