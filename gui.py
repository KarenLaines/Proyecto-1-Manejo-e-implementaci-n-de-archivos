import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from gif_reader import read_gif_info
from data_handler import load_data, save_data
import os


class GIFInfoApp:
    def _init_(self, master):
        self.master = master
        self.master.title("Extractor de Información de GIF")
        self.master.geometry("900x620")
        self.master.configure(bg="#191970")  # Fondo midnight blue

        # Crear estilo personalizado
        style = ttk.Style()
        style.theme_use("clam")  # Usa un tema moderno
        style.configure("TFrame", background="#191970", borderwidth=0)
        style.configure(
            "TLabel", background="#191970", foreground="white", font=("Helvetica", 10)
        )
        style.configure(
            "TButton",
            background="white",
            foreground="indian red",
            font=("Helvetica", 10, "bold"),
            padding=8,
        )
        style.map(
            "TButton",
            background=[("active", "slategray2")],
            foreground=[("active", "white")],
        )

        # Encabezado
        header_frame = tk.Frame(master, bg="#191970")
        header_frame.pack(fill="x", pady=(20, 10))
        header = tk.Label(
            header_frame,
            text="Extractor de Información de GIF",
            font=("Georgia", 24, "bold"),
            fg="gold",
            bg="#191970",
        )
        header.pack()

        # Contenedor de botones con fondo geométrico
        button_frame = tk.Frame(master, bg="#191970")
        button_frame.pack(pady=20, padx=20, fill="x")

        self.open_button = ttk.Button(
            button_frame,
            text="Abrir Carpeta",
            command=self.load_gifs_from_folder,
            style="TButton",
        )
        self.open_button.grid(row=0, column=0, padx=10, pady=5, ipadx=10, ipady=5)

        self.load_button = ttk.Button(
            button_frame,
            text="Cargar Datos desde JSON",
            command=self.load_data_from_json,
            style="TButton",
        )
        self.load_button.grid(row=0, column=1, padx=10, pady=5, ipadx=10, ipady=5)

        self.save_button = ttk.Button(
            button_frame,
            text="Guardar Cambios",
            command=self.save_changes,
            style="TButton",
        )
        self.save_button.grid(row=0, column=2, padx=10, pady=5, ipadx=10, ipady=5)

        self.close_button = ttk.Button(
            button_frame, text="Salir", command=master.quit, style="TButton"
        )
        self.close_button.grid(row=0, column=3, padx=10, pady=5, ipadx=10, ipady=5)

        # Configuración de botones para bordes redondeados
        for child in button_frame.winfo_children():
            child.configure(style="TButton")

        # Área de información con barra de desplazamiento
        self.canvas = tk.Canvas(master, bg="#191970", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(
            master, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = ttk.Frame(self.canvas, style="TFrame")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=20)
        self.scrollbar.pack(side="right", fill="y", pady=20)

    # Funciones

    def load_gifs_from_folder(self):
        folder_path = filedialog.askdirectory(title="Seleccionar Carpeta")
        if folder_path:
            self.display_gif_info_from_folder(folder_path)

    def display_gif_info_from_folder(self, folder_path):
        try:
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()

            gif_files = [
                f for f in os.listdir(folder_path) if f.lower().endswith(".gif")
            ]
            if not gif_files:
                messagebox.showinfo(
                    "Información",
                    "No se encontraron archivos GIF en la carpeta seleccionada.",
                )
                return

            for gif_file in gif_files:
                file_path = os.path.join(folder_path, gif_file)
                gif_info = read_gif_info(file_path)
                self.display_gif_info(file_path, gif_info)

        except Exception as e:
            messagebox.showerror("Error", f"Error al leer los archivos: {e}")

    def display_gif_info(self, file_path, gif_info):
        frame = ttk.Frame(self.scrollable_frame, style="TFrame")
        frame.pack(pady=10, padx=20, fill="x")

        # Canvas para mostrar el GIF
        canvas = tk.Canvas(
            frame, width=180, height=180, bg="#333333", bd=1, relief="solid"
        )
        canvas.pack(side=tk.LEFT, padx=10)
        gif_image = tk.PhotoImage(file=file_path)
        canvas.create_image(90, 90, image=gif_image)
        canvas.image = gif_image

        # Listbox para mostrar la información
        listbox = tk.Listbox(
            frame,
            width=60,
            height=8,
            font=("Helvetica", 10),
            bg="#191970",
            fg="slategray2",
            selectbackground="gold",
        )
        listbox.pack(side=tk.LEFT, padx=10)
        for key, value in gif_info.items():
            listbox.insert(tk.END, f"{key}: {value if value else 'N/A'}")

        edit_button = ttk.Button(
            frame,
            text="Editar Información",
            command=lambda: self.edit_gif_info(listbox, gif_info, file_path),
            style="TButton",
        )
        edit_button.pack(side=tk.LEFT, padx=10)

    def load_data_from_json(self):
        try:
            data = load_data()
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            for gif_info in data:
                self.display_gif_info(gif_info["File Path"], gif_info)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los datos: {e}")

    def edit_gif_info(self, listbox, gif_info, file_path):
        selected_index = listbox.curselection()
        if not selected_index:
            messagebox.showinfo(
                "Información",
                "Por favor, selecciona un elemento de la lista para editar.",
            )
            return

        selected_index = selected_index[0]
        selected_line = listbox.get(selected_index)

        if ": " in selected_line:
            key, value = selected_line.split(": ", 1)
            new_value = simpledialog.askstring(
                "Editar Información", f"Editar {key}", initialvalue=value
            )

            if new_value is not None:
                listbox.delete(selected_index)
                listbox.insert(selected_index, f"{key}: {new_value}")
                gif_info[key] = new_value
                self.update_json_data(file_path, gif_info)

    def update_json_data(self, file_path, updated_info):
        data = load_data()
        for gif_info in data:
            if gif_info["File Path"] == file_path:
                gif_info.update(updated_info)
                break
        save_data(data)

    def save_changes(self):
        data = []
        for frame in self.scrollable_frame.winfo_children():
            listbox = frame.winfo_children()[1]
            gif_info = {}
            for item in listbox.get(0, tk.END):
                if ": " in item:
                    key, value = item.split(": ", 1)
                    gif_info[key] = value
            data.append(gif_info)
        save_data(data)
        messagebox.showinfo("Información", "Los cambios han sido guardados.")
