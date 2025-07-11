import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from subprocess import run

class OpenAPIHandler(FileSystemEventHandler):
    def __init__(self, filepath):
        self.filepath = filepath

    def on_modified(self, event):
        if event.src_path.endswith(self.filepath):
            print(f"{self.filepath} changed, regenerating backend...")
            run(["python", "generate_pipeline.py", "--input", self.filepath])

if __name__ == "__main__":
    path_to_watch = "openapi3.yaml"
    event_handler = OpenAPIHandler(path_to_watch)
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=False)
    observer.start()
    print(f"Watching {path_to_watch} for changes...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
