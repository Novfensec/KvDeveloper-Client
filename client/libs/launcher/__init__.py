from __future__ import annotations

__all__ = ("ApplicationLauncher",)

import os, sys, shutil, threading, subprocess # nosec
import requests

from kivy.app import App
from kivy.clock import mainthread
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.properties import StringProperty
from kivy.utils import platform

from carbonkivy.behaviors import DeclarativeBehavior
from View.base_screen import LoadingLayout

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
        self.app = App.get_running_app()
        self.loading_layout = LoadingLayout()
        if platform == "android":
            self.target_dir = os.path.join(AppStorageDir, self.app_name)
        else:    
            self.target_dir = os.path.expanduser(f"~/Applications/{self.app_name}")

    def launch_app(self, *args) -> None:
        self.app.status = "Starting launch operations.."
        self.display_indicator()
        threading.Thread(target=self.download_and_run).start()

    def download_and_run(self, *args) -> None:
        try:
            if os.path.exists(self.target_dir):
                shutil.rmtree(self.target_dir)
            os.makedirs(self.target_dir, exist_ok=True)

            self.app.status = f"Downloading files from server at {self.server_url}"
            
            files_to_fetch = [self.entrypoint] + self.fetch_kv_files()
            for filename in files_to_fetch:
                self.download_file_from_server(filename)

            self.app.status = "Running app..."
            self.run_entrypoint()

        except Exception as e:
            self.app.status = f"Error: {e}"

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
            print(f"[SYNC] Downloaded {filename} at {local_path}")
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
            if (self.process and (self.process.poll() != None)) or (self.app.running == False):
                break

    def run_entrypoint(self) -> None:
        entrypoint_path = os.path.abspath(os.path.join(self.target_dir, self.entrypoint))
        self.display_indicator(False)
        if platform == "android":
            launch_client_activity(entrypoint_path)
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

    @mainthread
    def display_indicator(self, val: bool = True, *args) -> None:
        try:
            if val:
                Window.add_widget(self.loading_layout)
            elif val==False:
                Window.remove_widget(self.loading_layout)
        except Exception:
            return
