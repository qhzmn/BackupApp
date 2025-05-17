# Importation of packages
import tkinter as tk  # Graph interface
from tkinter import filedialog, messagebox  # Messages
from tkinter import ttk  # Widgets, progress stick
import shutil  # Copy files
import os  # Browse the file system
import json  # Save paths of filesr
from datetime import datetime
import logging

# Main classe
class BackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Backup Program")  # Title of the window

        self.source_paths = []  # List the source folder
        self.destination_path = tk.StringVar()  # Path of destination folder
        self.historic_path = tk.StringVar()  # Path of historic file
        self.source_name = tk.StringVar()   #Name of source folder
        self.destination_name = tk.StringVar()  #Name of destination folder

        logging.basicConfig(
            filename='app.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)  # Logger
        self.logger.info("START SESSION")

        self.create_widgets()  # Create interface
        self.load_paths()  # Load of last pathst
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)


    # User interface
    def create_widgets(self):

        tk.Label(self.root, text="Source:").grid(row=0, column=0, padx=10, pady=10)
        # Sources folder
        self.source_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE, height=10, width=50)
        self.source_listbox.grid(row=0, column=1, rowspan=2, padx=10, pady=10)
        # Add/remove source folder
        tk.Button(self.root, text="Add Folder", command=self.browse_source).grid(row=0, column=2, padx=10, pady=10)
        tk.Button(self.root, text="Remove Folder", command=self.remove_selected_sources).grid(row=1, column=2, padx=10, pady=10)

        # Choose destination folder
        tk.Label(self.root, text="Destination:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.destination_path).grid(row=2, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Browse", command=self.browse_destination).grid(row=2, column=2, padx=10, pady=10)

        # Choose historic file
        tk.Label(self.root, text="File .md :").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.historic_path).grid(row=3, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Browse", command=self.browse_historic).grid(row=3, column=2, padx=10, pady=10)
        tk.Label(self.root, text="Source name :").grid(row=4, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.source_name).grid(row=4, column=1, padx=10, pady=10)
        tk.Label(self.root, text="Destination name :").grid(row=4, column=2, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.destination_name).grid(row=4, column=3, pady=10)

        # Button clean
        tk.Button(self.root, text="Erase all", command=self.reset_json).grid(row=1, column=3, padx=10, pady=10)

        # Start backup
        tk.Label(self.root, text="Folder save :").grid(row=5, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Start Backup", command=self.start_backup).grid(row=5, column=3, padx=10, pady=10)
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=5, column=1, columnspan=2, padx=10, pady=10)

    # Select source folder
    def browse_source(self):
        sources = filedialog.askdirectory(mustexist=True)
        if sources:
            self.source_paths.append(sources)
            self.source_listbox.insert(tk.END, sources)
            self.save_paths()
            self.logger.info(f"ADD SOURCE FILES: {sources}")

    # Remove source folder
    def remove_selected_sources(self):
        selected_indices = self.source_listbox.curselection()
        selected_paths = [self.source_listbox.get(i) for i in selected_indices]
        for path in selected_paths:
            self.source_paths.remove(path)
            self.logger.info(f"REMOVE SOURCE FILES: {path}")
        for i in selected_indices[::-1]:
            self.source_listbox.delete(i)
        self.save_paths()

    # Select destination folder
    def browse_destination(self):
        destination = filedialog.askdirectory(mustexist=True)
        if destination:
            self.destination_path.set(destination)
            self.save_paths()
            self.logger.info(f"ADD DESTINATION FILES: {destination}")

    # Select file .md
    def browse_historic(self):
        historique = filedialog.askopenfilename(
            title="Sélectionner un fichier Markdown",
            filetypes=[("Fichiers Markdown", "*.md"), ("Tous les fichiers", "*.*")]
        )
        if historique:
            self.logger.info(f"ADD historic FILES: {historique}")
            self.historic_path.set(historique)
            self.save_paths()

    # Backup
    def start_backup(self):
        destination = self.destination_path.get()
        destination_name = self.destination_name.get()
        source_name = self.source_name.get()
        historic = self.historic_path.get()
        if not self.source_paths or not destination:
            self.logger.info("Select the source and destination directories.")
            messagebox.showerror("Erreur", "Select the source and destination directories.")
            return
        if historic and not destination_name and not source_name:
            self.logger.info("Enter a source name & destination name.")
            messagebox.showerror("Enter a source name & destination name.")
            return
        total_files = sum([len(files) for source in self.source_paths for _, _, files in os.walk(source)])
        self.progress["maximum"] = total_files
        self.progress["value"] = 0
        try:
            self.logger.info("START BACKUP")
            for source in self.source_paths:
                self.incremental_backup(source, destination)
            if historic:
                self.writeMD(source_name, destination_name, historic)
            self.logger.info("Incremental backup completed successfully.")
            messagebox.showinfo("Succès", "Incremental backup completed successfully.")
        except Exception as e:
            self.logger.info(f"An error has occurred : {e}")
            messagebox.showerror("Error", f"An error has occurred : {e}")

    # Write in md file
    def writeMD(self, source, destination, historic):
        date_du_jour = datetime.now().date()
        self.logger.info(f"Source folder name : {source}")
        self.logger.info(f"Destination folder name: {destination}")
        if len(str(source))<24:
            source=str(source)+(24-len(str(source)))*" "
        else:
            source=str(source)[0:24]
        print(source)
        if len(str(destination))<20:
            destination=str(destination)+(20-len(str(destination)))*" "
        else:
            destination=str(destination)[0:20]

        content = "\n| "+str(date_du_jour)+" | "+source +" | Incremental  | "+ destination+ " | Succes         |"
        print(content)
        with open(historic, 'a', encoding='utf-8') as file:
            file.write(content)

    # Incremental copy function: only copies if the file does not exist or is modified
    def incremental_backup(self, source, destination):
        for root, dirs, files in os.walk(source):
            relative_path = os.path.relpath(root, source)
            dest_dir = os.path.join(destination, os.path.basename(source), relative_path)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            for file in files:
                source_file = os.path.join(root, file)
                dest_file = os.path.join(dest_dir, file)
                if not os.path.exists(dest_file) or os.path.getmtime(source_file) > os.path.getmtime(dest_file):
                    shutil.copy2(source_file, dest_file)
                self.progress["value"] += 1
                self.root.update_idletasks()

    # Save paths in JSON file
    def save_paths(self):
        data = {
            "source_paths": self.source_paths,
            "destination_path": self.destination_path.get(),
            "historic_path": self.historic_path.get()

        }
        with open("paths.json", "w") as file:
            json.dump(data, file)

    # Reload the paths save
    def load_paths(self):
        if os.path.exists("paths.json"):
            with open("paths.json", "r") as file:
                data = json.load(file)
                self.source_paths = data.get("source_paths", [])
                self.destination_path.set(data.get("destination_path", ""))
                self.historic_path.set(data.get("historic_path",""))
                for path in self.source_paths:
                    self.source_listbox.insert(tk.END, path)

    # Reset json file
    def reset_json(self):
        self.reset_fields()
        data = {
            "source_paths": [],
            "destination_path": "",
            "historic_path": ""
        }
        with open("paths.json", "w") as file:
            json.dump(data, file)
        self.logger.info("JSON paths.json initialisation")

    # Reset paths
    def reset_fields(self):
        self.logger.info("INIT VAIRABLE")
        self.source_listbox.delete(0, tk.END)
        self.source_paths = []
        self.destination_path.set("")
        self.historic_path.set("")
        self.source_name.set("")
        self.destination_name.set("")

    def on_closing(self):
        self.logger.info("DESTROY SESSION")
        self.root.destroy()


# Script
if __name__ == "__main__":
    root = tk.Tk()
    app = BackupApp(root)
    root.mainloop()
