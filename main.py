import os
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import filedialog, simpledialog, messagebox, ttk
from PIL import ImageTk


class ImageGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Image Generator")
        self.root.config(background=self.rgb2hex((229, 232, 232)))

        self.chosen_point = None
        self.color_button = tk.Button()
        self.selected_color = (0, 0, 0)
        self.font = ImageFont.truetype("arial.ttf", 50)
        self.x = 0
        self.file_path = None
        self.img_display = None

        self.create_widgets()

    def create_widgets(self):
        left_frame = tk.Frame(self.root)
        left_frame.grid(row=0, column=0, padx=10, pady=5)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, pady=10)

        file_button = tk.Button(left_frame, text="Seleccionar Imagen", command=self.select_file)
        file_button.pack(pady=25)

        self.color_button = tk.Button(left_frame, text="Seleccionar Color", command=self.select_color,
                                 background=self.rgb2hex(self.selected_color), foreground="white")
        self.color_button.pack(pady=25)

        font_size_slider = tk.Scale(left_frame, from_=12, to=250,
                                    orient=tk.HORIZONTAL, command=self.change_font_size)
        font_size_slider.pack(pady=25)

        canvas = tk.Canvas(self.root)
        canvas.pack()

        canvas.bind("<Button-1>", self.on_click)

        progress = ttk.Progressbar(left_frame, orient=tk.HORIZONTAL,
                                   length=100, mode='determinate')
        progress.pack(pady=25)

        generate_button = tk.Button(
            left_frame, text="Generar Imagenes", command=self.generate_images)
        generate_button.pack(pady=25)
        
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.select_file)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.canvas = canvas
        self.progress = progress
    
    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_label = tk.Label(about_window, text="Image Generator App v1.0")
        about_label.pack()

        url = 'https://github.com/arielfernando1/pastenumber'
        about_link = tk.Label(about_window, text=url, fg="blue", cursor="hand2")
        about_link.bind("<Button-1>", lambda e: os.system(f"open {url}"))
        about_link.pack()
        


    def select_file(self):
        self.file_path = filedialog.askopenfilename(
            filetypes=[("Image File", '.jpg .png .jpeg')], title="Select an image")
        self.root.title(f"Image Generator - {self.file_path}")
        img = Image.open(self.file_path)
        self.img_display = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_display)
        self.canvas.config(width=self.img_display.width(), height=self.img_display.height())

    def select_color(self):
        self.selected_color = askcolor()[0]
        self.color_button.config(background=self.rgb2hex(self.selected_color))
        self.draw_label()

    def change_font_size(self, val):
        self.font = ImageFont.truetype("arial.ttf", int(val))
        self.draw_label()

    def on_click(self, event):
        self.chosen_point = (event.x, event.y)
        self.draw_label()

    def draw_label(self):
        if self.chosen_point and self.file_path:
            img = Image.open(self.file_path)
            draw = ImageDraw.Draw(img)
            draw.text(self.chosen_point, "0000", font=self.font, fill=self.selected_color)
            self.img_display = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_display)

    def generate_images(self):
        if not self.file_path:
            messagebox.showerror("Error", "No se ha seleccionado un archivo")
            return

        self.input_number()

        output_dir = os.path.join(os.environ['HOME'], 'Desktop', 'Output') if os.name == 'posix' else os.path.join(os.environ['USERPROFILE'], 'Desktop', 'Output')

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for i in range(self.x):
            try:
                img = Image.open(self.file_path)
                draw = ImageDraw.Draw(img)
                draw.text(self.chosen_point, str(i+1), font=self.font, fill=self.selected_color)
                if img.mode == 'RGBA':
                    img.save(os.path.join(output_dir, f"{i+1}.png"))
                else:
                    img.save(os.path.join(output_dir, f"{i+1}.jpg"))
                self.progress['value'] = (i+1)/self.x*100
                self.progress.update()
            except Exception as e:
                messagebox.showerror("Error", e)
                return

        if os.name == 'nt':
            os.startfile(output_dir)
        elif os.name == 'posix':
            os.system(f"open {output_dir}")

    def input_number(self):
        self.x = simpledialog.askinteger(
            "Cantidad", "Ingrese la cantidad de boletos a generar")

    def rgb2hex(self, rgb):
        return "#%02x%02x%02x" % rgb

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ImageGenerator()
    app.run()
