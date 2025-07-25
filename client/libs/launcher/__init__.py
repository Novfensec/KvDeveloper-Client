from __future__ import annotations

__all__ = ("ApplicationLauncher",)

import os, sys, shutil, threading, subprocess  # nosec
import requests
from html.parser import HTMLParser
from urllib.parse import urljoin

from kivy.app import App
from kivy.clock import mainthread
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.properties import StringProperty, ListProperty
from kivy.utils import platform

from carbonkivy.behaviors import DeclarativeBehavior
from View.base_screen import LoadingLayout

if platform == "android":
    from libs.launcher.android import (
        AppStorageDir,
        launch_client_activity,
    )


class LinkExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs) -> None:
        if tag == "a":
            for attr, value in attrs:
                if attr == "href":
                    self.links.append(value)


class ApplicationLauncher(EventDispatcher, DeclarativeBehavior):

    entrypoint = StringProperty()

    app_name = StringProperty()

    target_dir = StringProperty()

    server_url = StringProperty()

    status = StringProperty()

    allowed_extensions = ListProperty()

    def __init__(self, **kwargs) -> None:
        super(ApplicationLauncher, self).__init__(**kwargs)
        self.process = None
        self.app = App.get_running_app()
        self.loading_layout = LoadingLayout()
        if platform == "android":
            self.target_dir = os.path.join(AppStorageDir, self.app_name)
        else:
            self.target_dir = os.path.expanduser(
                f"~/Client/Applications/{self.app_name}"
            )

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

            files_to_fetch = [self.entrypoint] + self.fetch_files()
            for filename in files_to_fetch:
                self.download_file_from_server(filename)

            self.app.status = "Running app..."
            self.run_entrypoint()

        except Exception as e:
            self.app.status = f"Error: {e}"

    def fetch_files(self, url: str = None, seen: set = None) -> list:
        """
        Recursively fetches all allowed files from the server using only built-in modules,
        skipping disallowed patterns like __pycache__/, *.pyc, *.pyo, etc.
        """
        if seen is None:
            seen = set()
        if url is None:
            url = self.server_url.rstrip("/") + "/"

        files = []

        try:
            response = requests.get(url, timeout=3)
            response.raise_for_status()
            parser = LinkExtractor()
            parser.feed(response.text)

            for href in parser.links:
                if not href or href == "../":
                    continue  # Skip parent links

                # Skip unwanted patterns
                if href.startswith("__pycache__/") or href.endswith(
                    (".pyc", ".pyo", ".pyd")
                ):
                    continue

                full_url = urljoin(url, href)
                if full_url in seen:
                    continue
                seen.add(full_url)

                if any(
                    href.lower().endswith(ext.lower())
                    for ext in self.allowed_extensions
                ):
                    # Get relative path for correct download location
                    relative_path = full_url.replace(
                        self.server_url.rstrip("/") + "/", ""
                    )
                    files.append(relative_path)
                elif href.endswith("/"):  # A subdirectory
                    files.extend(self.fetch_files(full_url, seen))
        except Exception as e:
            print(f"[FETCH ERROR] {e}")

        return files

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
            if (self.process and (self.process.poll() != None)) or (
                App.get_running_app().running == False
            ):
                break

    def run_entrypoint(self) -> None:
        entrypoint_path = os.path.abspath(
            os.path.join(self.target_dir, self.entrypoint)
        )
        self.display_indicator(False)
        self.start_auto_sync()
        try:
            if platform == "android":
                launch_client_activity(entrypoint_path)
            else:
                self.process = subprocess.Popen(
                    [sys.executable, entrypoint_path], cwd=self.target_dir
                )  # nosec
                print(f"[RUN] {self.entrypoint} launched...")
        except Exception as e:
            print(e)
            self.app.running = False
            self.app.notify(
                status="Error",
                title="Error",
                subtitle=f"{e}",
            )

    def restart_entrypoint(self) -> None:
        if platform == "windows":
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
            elif val == False:
                Window.remove_widget(self.loading_layout)
        except Exception:
            return
