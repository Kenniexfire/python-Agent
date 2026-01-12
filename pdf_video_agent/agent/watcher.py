from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from agent.processor import process_pdf

class PDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".pdf"):
            process_pdf(event.src_path)

def watch_folder(path="./content_dropbox"):
    event_handler = PDFHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()