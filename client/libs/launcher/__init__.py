from __future__ import annotations

__all__ = ("ApplicationLauncher",)

import os, sys, shutil, threading, subprocess # nosec
import requests

from kivy.event import EventDispatcher
from kivy.properties import StringProperty
from kivy.utils import platform

from carbonkivy.behaviors import DeclarativeBehavior

if platform == "android":
    from libs.launcher.android import AppStorageDir, launch_client_activity, finish_client_activity

class ApplicationLauncher(EventDispatcher, DeclarativeBehavior):

    entrypoint = StringProperty()

    app_name = StringProperty()

    target_dir = StringProperty()

    server_url = StringProperty()

    status = StringProperty()

    def __init__(self, **kwargs) -> None:
        super(ApplicationLauncher, self).__init__(**kwargs)
        self.process = None
        self.running = None
        if platform == "android":
            self.target_dir = os.path.join(AppStorageDir, self.app_name)
        else:    
            self.target_dir = os.path.expanduser(f"~/Applications/{self.app_name}")

    def launch_app(self, *args) -> None:
        self.status = "Starting launch operations.."
        threading.Thread(target=self.download_and_run).start()

    def download_and_run(self, *args) -> None:
        try:
            if os.path.exists(self.target_dir):
                shutil.rmtree(self.target_dir)
            os.makedirs(self.target_dir, exist_ok=True)

            self.status = f"Downloading files from server at {self.server_url}"
            
            files_to_fetch = [self.entrypoint] + self.fetch_kv_files()
            for filename in files_to_fetch:
                self.download_file_from_server(filename)

            self.status = "Running app..."
            self.run_entrypoint()

        except Exception as e:
            self.status.text = f"Error: {e}"

    def fetch_kv_files(self) -> list | None:
        kv_files = []
        try:
            response = requests.get(f"{self.server_url}/", timeout=3)
            for line in response.text.splitlines():
                if '.kv' in line:
                    parts = line.split('"')
                    for part in parts:
                        if part.endswith('.kv') and part not in kv_files:
                            kv_files.append(part)
        except Exception: # nosec
            pass
        return kv_files

    def download_file_from_server(self, filename: str) -> None:
        url = f"{self.server_url}/{filename}"
        local_path = os.path.join(self.target_dir, filename)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        try:
            r = requests.get(url, timeout=3)
            r.raise_for_status()
            with open(local_path, "wb") as f:
                f.write(r.content)
            print(f"[SYNC] Downloaded: {filename}")
        except Exception as e:
            print(f"[ERROR] Failed to download {filename}: {e}")
        self.start_auto_sync()

    def start_auto_sync(self) -> None:
        threading.Thread(target=self.sync_loop, daemon=True).start()

    def sync_loop(self) -> None:
        import time
        while True:
            try:
                r = requests.get(f"{self.server_url}/changes.json", timeout=3)
                if r.status_code == 200:
                    changed_files = r.json()
                    for file in changed_files:
                        self.download_file_from_server(file)
                        if file == self.entrypoint:
                            self.restart_entrypoint()
            except Exception as e:
                print(f"[SYNC ERROR] {e}")
            time.sleep(3.0)  # Poll interval
            if (self.process and (self.process.poll() != None)) or (self.running == False):
                break

    def run_entrypoint(self) -> None:
        entrypoint_path = os.path.abspath(os.path.join(self.target_dir, self.entrypoint))
        if platform == "android":
            launch_client_activity(entrypoint_path)
            self.running = False
        else:
            self.process = subprocess.Popen([sys.executable, entrypoint_path], cwd=self.target_dir) # nosec
            print(f"[RUN] {self.entrypoint} launched...")

    def restart_entrypoint(self) -> None:
        if platform == "android":
            finish_client_activity()
        else:
            if self.process and self.process.poll() is None:
                print("[RESTART] Killing previous process...")
                self.process.terminate()
                self.process.wait()
        print(f"[RESTART] Restarting {self.entrypoint}")
        self.run_entrypoint()



