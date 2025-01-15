from tkinter import *
from tkinter import colorchooser
from datetime import datetime
from PIL import Image
import pyautogui
import os

last_x, last_y = None, None
brush_color = 'black'

def last_coords(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y

def draw(event):
    global last_x, last_y, brush_color
    canvas.create_line(last_x, last_y, event.x, event.y, fill=brush_color, width=brush_scale.get(), capstyle=ROUND, smooth=True)
    last_x, last_y = event.x, event.y

def erase(event):
    global last_x, last_y
    current_x, current_y = event.x, event.y
    canvas.create_line(last_x, last_y, current_x, current_y, fill='white', width=eraser_scale.get(), capstyle=ROUND, smooth=True)
    last_x, last_y = current_x, current_y

def brush_tool():
    canvas.bind("<Button-1>", last_coords)
    canvas.bind("<B1-Motion>", draw)

def choose_color():
    global brush_color
    brush_color = colorchooser.askcolor()[1]
    return brush_color

def eraser():
    canvas.bind("<Button-1>", last_coords)
    canvas.bind("<B1-Motion>", erase)

def save_png():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    canvas_x = canvas.winfo_rootx()
    canvas_y = canvas.winfo_rooty()
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    pyautogui.screenshot(imageFilename=f"Photo_{timestamp}.png", region=(canvas_x, canvas_y, canvas_width, canvas_height))
    print(f"Image saved as 'Photo_{timestamp}.png'")
    return timestamp

def save_pdf():
    timestamp = save_png()
    tempfile_name = f"Photo_{timestamp}.png"
    pdffile_name = f"PDF_{timestamp}.pdf"
    temp_img = Image.open(tempfile_name)
    temp_img.save(pdffile_name)
    os.remove(tempfile_name)
    print(f"Temporary Image 'Photo_{timestamp}.png' removed")
    print(f"PDF saved as 'PDF_{timestamp}.pdf'")

root = Tk()
root.title("White Board")
root.geometry("1200x800")
root.configure(bg="#f0f0f0")
root.resizable(False, False)

canvas = Canvas(root, bg="white", width=1150, height=550)
canvas.pack()

brush_frame = Frame(root)
brush_frame.pack(side=LEFT, padx=25, pady=15)

brush_button = Button(brush_frame, text="BRUSH", command=brush_tool, width=60, height=2, bg="grey", fg="black", relief=FLAT, borderwidth=0)
brush_button.pack()

brush_scale = Scale(brush_frame, from_=0, to=100, orient=HORIZONTAL, length=300)
brush_scale.pack(pady=10)

brush_color_button = Button(brush_frame, text="CHOOSE COLOR", command=choose_color, width=30, height=2, bg="grey", fg="black", relief=FLAT, borderwidth=0)
brush_color_button.pack(pady=20)


eraser_frame = Frame(root)
eraser_frame.pack(side=LEFT, padx=25, pady=15)

eraser_button = Button(eraser_frame, text="ERASER", command=eraser, width=60, height=2, bg="grey", fg="black", relief=FLAT, borderwidth=0)
eraser_button.pack()

eraser_scale = Scale(eraser_frame, from_=0, to=100, orient=HORIZONTAL, length=300)
eraser_scale.pack()


save_frame = Frame(root)
save_frame.pack(side=LEFT, padx=25, pady=15)

savepng_button = Button(save_frame, text="SAVE(PNG)", command=save_png, width=20, height=2, bg="white", fg="black", relief=FLAT, borderwidth=0)
savepng_button.pack(pady=20)

savepdf_button = Button(save_frame, text="SAVE(PDF)", command=save_pdf, width=20, height=2, bg="white", fg="black", relief=FLAT, borderwidth=0)
savepdf_button.pack(pady=20)


root.mainloop()
