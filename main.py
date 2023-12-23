import os
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import filedialog, simpledialog, messagebox, ttk
from PIL import ImageTk


def initialize():
    global chosen_point, selected_color, font, x
    chosen_point = None
    selected_color = (0, 0, 0)
    font = ImageFont.truetype("arial.ttf", 50)
    x = 0

initialize()


def select_file():
    global file_path, img_display
    file_path = filedialog.askopenfilename(filetypes=[("Image File", '.jpg .png .jpeg')], title="Select an image")
    file_label.config(text=f"Imagen seleccionada: {os.path.basename(file_path)}")
    img = Image.open(file_path)
    img_display = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
    canvas.config(width=img_display.width(), height=img_display.height())

def select_color():
    global selected_color
    selected_color = askcolor()[0]
    color_button.config(background=rgb2hex(selected_color))
    draw_label()

def rgb2hex(rgb):
    return "#%02x%02x%02x" % rgb


def change_font_size(val):
    global font
    font = ImageFont.truetype("arial.ttf", int(val))
    draw_label()

def input_number():
    global x
    x = simpledialog.askinteger("Cantidad", "Ingrese la cantidad de boletos a generar")

def on_click(event):
    global chosen_point 
    chosen_point = (event.x, event.y)
    draw_label()
    print(chosen_point)

def draw_label():
    global img_display, chosen_point
    if chosen_point and file_path:
        img = Image.open(file_path)
        draw = ImageDraw.Draw(img)
        draw.text(chosen_point, "0000", font=font, fill=selected_color)
        img_display = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)

def generate_images():
    if 'file_path' not in globals():
        messagebox.showerror("Error", "No se ha seleccionado un archivo")
        return
    
    input_number()
    output_dir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', 'Output')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(x):
        try:
            img = Image.open(file_path)
            draw = ImageDraw.Draw(img)
            draw.text(chosen_point, str(i+1), font=font, fill=selected_color)
            # if image is png, convert to jpg
            if img.mode == 'RGBA':
                img.save(os.path.join(output_dir, f"{i+1}.png"))
                progress['value'] = (i+1)/x*100
                progress.update()
            else:
                img.save(os.path.join(output_dir, f"{i+1}.jpg"))
                progress['value'] = (i+1)/x*100
                progress.update()
        except Exception as e:
            messagebox.showerror("Error", e)
            return
        

    os.startfile(output_dir)

root = tk.Tk()
root.title("Image Generator")

file_button = tk.Button(root, text="Seleccionar Imagen", command=select_file)
file_button.pack()

color_button = tk.Button(root, text="Seleccionar Color", command=select_color, background=rgb2hex(selected_color), foreground="white")   
color_button.pack()


font_size_slider = tk.Scale(root, from_=1, to=200, orient=tk.HORIZONTAL, command=change_font_size)
font_size_slider.pack()

file_label = tk.Label(root, text="Selected File: None")
file_label.pack()

canvas = tk.Canvas(root)
canvas.pack()

canvas.bind("<Button-1>", on_click)

# number_button = tk.Button(root, text="Input Number", command=input_number)
# number_button.pack()
progress = ttk.Progressbar(root, orient = tk.HORIZONTAL, length = 100, mode = 'determinate')
progress.pack(side=tk.LEFT)

generate_button = tk.Button(root, text="Generate Images", command=generate_images)
generate_button.pack(side=tk.RIGHT)

root.mainloop()
