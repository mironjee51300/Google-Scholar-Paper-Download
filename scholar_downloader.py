import os
import re
import time
import requests
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread
from scholarly import scholarly

class ScholarDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Scholar Downloader Pro")
        self.root.geometry("550x580")
        
        self.is_paused = False
        self.is_running = False
        self.history_file = "download_record.txt"

        # Topic Entry
        tk.Label(root, text="Search Topic:", font=('Segoe UI', 10, 'bold')).pack(pady=5)
        self.topic_entry = tk.Entry(root, width=60)
        self.topic_entry.pack(pady=5)

        # Year Range
        year_frame = tk.Frame(root)
        year_frame.pack(pady=10)
        tk.Label(year_frame, text="From Year:").pack(side="left")
        self.start_year = tk.Entry(year_frame, width=8)
        self.start_year.insert(0, "2020")
        self.start_year.pack(side="left", padx=5)
        
        tk.Label(year_frame, text="To Year:").pack(side="left")
        self.end_year = tk.Entry(year_frame, width=8)
        self.end_year.insert(0, "2026")
        self.end_year.pack(side="left", padx=5)

        # Download Count
        tk.Label(root, text="Number of New Papers to Get:").pack(pady=5)
        self.count_entry = tk.Entry(root, width=10)
        self.count_entry.insert(0, "5")
        self.count_entry.pack(pady=5)

        # Buttons
        self.start_btn = tk.Button(root, text="START DOWNLOAD", command=self.start_thread, bg="#1a73e8", fg="white", font=('Segoe UI', 10, 'bold'), height=2)
        self.start_btn.pack(pady=15, fill="x", padx=100)

        self.pause_btn = tk.Button(root, text="Pause", command=self.pause_process, state="disabled", width=12)
        self.pause_btn.pack(side="left", padx=60)

        self.resume_btn = tk.Button(root, text="Resume", command=self.resume_process, state="disabled", width=12)
        self.resume_btn.pack(side="right", padx=60)

        # Status & Counters
        self.counter_label = tk.Label(root, text="Total Papers in History: 0", fg="green", font=('Arial', 9, 'italic'))
        self.counter_label.pack(side="bottom", pady=5)

        self.status_label = tk.Label(root, text="Status: Ready", fg="#555", wraplength=400)
        self.status_label.pack(side="bottom", pady=20)

    def clean_filename(self, text):
        """Sanitizes titles so Windows can open them without errors."""
        text = re.sub(r'[\\/*?:"<>|]', "", text)
        return text[:140].strip()

    def load_history(self, save_path):
        """Reads the history file to track what is already on your laptop."""
        path = os.path.join(save_path, self.history_file)
        if not os.path.exists(path):
            return set()
        with open(path, "r", encoding="utf-8") as f:
            history = set(line.strip() for line in f if line.strip())
            self.counter_label.config(text=f"Total Papers in History: {len(history)}")
            return history

    def save_to_history(self, save_path, title):
        path = os.path.join(save_path, self.history_file)
        with open(path, "a", encoding="utf-8") as f:
            f.write(title + "\n")

    def pause_process(self):
        self.is_paused = True
        self.status_label.config(text="Status: Paused")

    def resume_process(self):
        self.is_paused = False
        self.status_label.config(text="Status: Resuming...")

    def start_thread(self):
        if not self.topic_entry.get():
            messagebox.showerror("Error", "Please enter a topic")
            return
        
        save_path = filedialog.askdirectory(title="Select Folder (Google Drive or Local)")
        if not save_path:
            return

        self.is_running = True
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal")
        self.resume_btn.config(state="normal")
        
        Thread(target=self.run_downloader, args=(save_path,), daemon=True).start()

    def run_downloader(self, save_path):
        topic = self.topic_entry.get()
        try:
            limit = int(self.count_entry.get())
            s_year = int(self.start_year.get())
            e_year = int(self.end_year.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for years and count")
            self.is_running = False
            self.start_btn.config(state="normal")
            return

        downloaded_history = self.load_history(save_path)
        self.status_label.config(text=f"Status: Searching {s_year}-{e_year}...")
        
        # Searching with Year Constraints
        search_query = scholarly.search_pubs(topic, year_low=s_year, year_high=e_year)

        new_downloads = 0
        while new_downloads < limit:
            if not self.is_running: break
            while self.is_paused: time.sleep(0.5) 

            try:
                pub = next(search_query)
                raw_title = pub['bib'].get('title', 'Unknown Title')
                safe_title = self.clean_filename(raw_title)

                # Avoid duplicates
                if safe_title in downloaded_history:
                    continue

                if 'eprint_url' in pub:
                    url = pub['eprint_url']
                    self.status_label.config(text=f"Downloading: {safe_title}...")
                    
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                    response = requests.get(url, headers=headers, timeout=30, stream=True)
                    
                    if response.status_code == 200:
                        file_path = os.path.join(save_path, f"{safe_title}.pdf")
                        
                        with open(file_path, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=1024 * 512):
                                if chunk: f.write(chunk)
                        
                        self.save_to_history(save_path, safe_title)
                        downloaded_history.add(safe_title)
                        new_downloads += 1
                        
                        self.counter_label.config(text=f"Total Papers in History: {len(downloaded_history)}")
                        self.status_label.config(text=f"Success: {new_downloads}/{limit} new papers saved.")
                        time.sleep(2)
            except StopIteration:
                break
            except Exception as e:
                print(f"Skipping: {e}")

        messagebox.showinfo("Done", f"Downloaded {new_downloads} new papers successfully.")
        self.is_running = False
        self.start_btn.config(state="normal")
        self.status_label.config(text="Status: Ready")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScholarDownloader(root)
    root.mainloop()
