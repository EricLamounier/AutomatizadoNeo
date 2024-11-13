import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class RestartHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print("Alteração detectada. Reiniciando...")
            subprocess.run(self.command, shell=True)


if __name__ == "__main__":
    path = "."  # Diretório a ser monitorado
    command = "python main.py"  # Comando para reiniciar seu script

    event_handler = RestartHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
