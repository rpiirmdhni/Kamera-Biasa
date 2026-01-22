#                     $$\ $$\                               $$\ $$\                 $$\ 
#                     \__|\__|                              $$ |$$ |                \__|
#  $$$$$$\   $$$$$$\  $$\ $$\  $$$$$$\  $$$$$$\$$$$\   $$$$$$$ |$$$$$$$\  $$$$$$$\  $$\ 
# $$  __$$\ $$  __$$\ $$ |$$ |$$  __$$\ $$  _$$  _$$\ $$  __$$ |$$  __$$\ $$  __$$\ $$ |
# $$ |  \__|$$ /  $$ |$$ |$$ |$$ |  \__|$$ / $$ / $$ |$$ /  $$ |$$ |  $$ |$$ |  $$ |$$ |
# $$ |      $$ |  $$ |$$ |$$ |$$ |      $$ | $$ | $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |
# $$ |      $$$$$$$  |$$ |$$ |$$ |      $$ | $$ | $$ |\$$$$$$$ |$$ |  $$ |$$ |  $$ |$$ |
# \__|      $$  ____/ \__|\__|\__|      \__| \__| \__| \_______|\__|  \__|\__|  \__|\__|
#           $$ |                                                                        
#           $$ |                                                                        
#           \__|                                                                        

# Nama          : Rafie Restu Ramadhani (a.k.a rpiirmdhni)
# NPM           : 10125885
# Kelas         : 1KA25
# Jurusan       : Sistem Informasi
# Fakultas      : Ilmu Komputer dan Teknologi Informasi
# Universitas   : Universitas Gunadarma
# Github        : https://github.com/rpiirmdhni

# Kamera Biasa v1.0
# Aplikasi kamera sederhana dengan fitur flash, watermark tanggal dan waktu, serta penyimpanan foto ke folder khusus.
# Dibuat menggunakan Python, OpenCV, dan CustomTkinter.
# Dibuat dengan tujuan pembelajaran dan pemenuhan nilai mata kuliah Pemrograman Algoritma dan Pemrograman 1B.

import customtkinter as ctk
import cv2
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
from datetime import datetime
import subprocess
import platform

# Konfigurasi
OUTPUT_FOLDER = "images"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Variabel global
current_frame = None
camera = None
flash_enabled = False
label_camera = None
root = None

# Inisialisasi jendela utama
def setup_window():
    global root
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.title("Kamera Biasa v1.0")
    root.geometry("1000x700")
    root.minsize(600, 600)
    
    return root

# Tampilan layar awal
def show_start_screen():
    clear_window()
    
    frame = ctk.CTkFrame(root, fg_color="#1a1a1a")
    frame.pack(fill="both", expand=True)
    
    title = ctk.CTkLabel(
        frame,
        text="Kamera Biasa",
        font=("Helvetica", 48, "bold"),
        text_color="#ffffff"
    )
    title.place(relx=0.5, rely=0.4, anchor="center")
    
    start_btn = ctk.CTkButton(
        frame,
        text="Mulai",
        font=("Helvetica", 18),
        width=200,
        height=50,
        fg_color="#4a4a4a",
        hover_color="#6a6a6a",
        corner_radius=25,
        command=show_camera_screen
    )
    start_btn.place(relx=0.5, rely=0.55, anchor="center")

# Tampilan layar kamera
def show_camera_screen():
    global camera, label_camera, flash_enabled
    
    flash_enabled = False
    
    clear_window()
    
    main_frame = ctk.CTkFrame(root, fg_color="#0a0a0a")
    main_frame.pack(fill="both", expand=True)
    
    camera_frame = ctk.CTkFrame(main_frame, fg_color="#000000")
    camera_frame.pack(side="left", fill="both", expand=True, padx=0, pady=0)
    
    label_camera = ctk.CTkLabel(camera_frame, text="")
    label_camera.pack(fill="both", expand=True)
    
    sidebar = ctk.CTkFrame(main_frame, width=120, fg_color="#1a1a1a")
    sidebar.pack(side="right", fill="y", padx=0, pady=0)
    sidebar.pack_propagate(False)
    
    button_container = ctk.CTkFrame(sidebar, fg_color="transparent")
    button_container.place(relx=0.5, rely=0.5, anchor="center")
    
    back_btn = ctk.CTkButton(
        button_container,
        text="←",
        font=("Helvetica", 24),
        width=60,
        height=60,
        fg_color="#2a2a2a",
        hover_color="#3a3a3a",
        corner_radius=30,
        command=back_to_start
    )
    back_btn.pack(pady=15)
    
    capture_btn = ctk.CTkButton(
        button_container,
        text="",
        width=70,
        height=70,
        fg_color="#ffffff",
        hover_color="#e0e0e0",
        corner_radius=35,
        border_width=4,
        border_color="#4a4a4a",
        command=take_photo
    )
    capture_btn.pack(pady=15)
    
    flash_btn = ctk.CTkButton(
        button_container,
        text="⚡",
        font=("Helvetica", 20),
        width=60,
        height=60,
        fg_color="#2a2a2a",
        text_color="#ffffff",
        hover_color="#3a3a3a",
        corner_radius=30,
        command=toggle_flash
    )
    flash_btn.pack(pady=15)
    
    folder_btn = ctk.CTkButton(
        button_container,
        text="📁",
        font=("Helvetica", 20),
        width=60,
        height=60,
        fg_color="#2a2a2a",
        hover_color="#3a3a3a",
        corner_radius=30,
        command=open_folder
    )
    folder_btn.pack(pady=15)
    
    camera = cv2.VideoCapture(0)
    update_frame()

# Perbarui frame kamera
def update_frame():
    global current_frame, label_camera, camera
    
    if camera is None or not camera.isOpened():
        return
    
    ret, frame = camera.read()
    if ret:
        current_frame = frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        label_width = label_camera.winfo_width()
        label_height = label_camera.winfo_height()
        
        if label_width > 1 and label_height > 1:
            frame_height, frame_width = frame.shape[:2]
            
            scale_w = label_width / frame_width
            scale_h = label_height / frame_height
            scale = max(scale_w, scale_h)
            
            new_width = int(frame_width * scale)
            new_height = int(frame_height * scale)
            
            frame_resized = cv2.resize(frame, (new_width, new_height))
            
            x_offset = (new_width - label_width) // 2
            y_offset = (new_height - label_height) // 2
            
            frame_cropped = frame_resized[y_offset:y_offset+label_height, x_offset:x_offset+label_width]
            
            img = Image.fromarray(frame_cropped)
            imgtk = ImageTk.PhotoImage(image=img)
            label_camera.imgtk = imgtk
            label_camera.configure(image=imgtk)
    
    if label_camera is not None:
        label_camera.after(10, update_frame)

# Ambil foto
def take_photo():
    global current_frame, flash_enabled
    
    if current_frame is None:
        return

    if flash_enabled:
        flash_overlay = ctk.CTkFrame(root, fg_color="#ffffff")
        flash_overlay.place(x=0, y=0, relwidth=1, relheight=1)

        root.update()
        root.after(200, save_photo)
        root.after(400, flash_overlay.destroy)
        root.after(450, lambda: show_toast("Foto berhasil disimpan"))
    else:
        save_photo()
        show_toast("Foto berhasil disimpan")

def show_toast(message):
    toast = ctk.CTkFrame(root, fg_color="#2a2a2a", corner_radius=10)
    toast.place(relx=0.5, rely=0.9, anchor="center")
    
    label = ctk.CTkLabel(
        toast,
        text=message,
        font=("Helvetica", 14),
        text_color="#ffffff",
        padx=30,
        pady=15
    )
    label.pack()
    
    root.after(2000, toast.destroy)

# Simpan foto dengan watermark tanggal dan waktu
def save_photo():
    global current_frame
    
    if current_frame is None:
        return
    
    timestamp = datetime.now()
    filename = "IMG_" + timestamp.strftime("%Y%m%d_%H%M%S") + ".jpg"
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    
    img = Image.fromarray(cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB))
    
    draw = ImageDraw.Draw(img)
    
    date_text = timestamp.strftime("%Y.%m.%d  %H:%M")
    
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), date_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    margin = 20
    x = img.width - text_width - margin
    y = img.height - text_height - margin
    
    shadow_offset = 2
    draw.text((x + shadow_offset, y + shadow_offset), date_text, font=font, fill=(0, 0, 0, 128))
    draw.text((x, y), date_text, font=font, fill=(255, 255, 255, 230))
    
    img.save(filepath, quality=95)

# Toggle flash
def toggle_flash():
    global flash_enabled
    flash_enabled = not flash_enabled
    
    for widget in root.winfo_children():
        if isinstance(widget, ctk.CTkFrame):
            for child in widget.winfo_children():
                if isinstance(child, ctk.CTkFrame):
                    for btn in child.winfo_children():
                        if isinstance(btn, ctk.CTkFrame):
                            for b in btn.winfo_children():
                                if isinstance(b, ctk.CTkButton) and b.cget("text") == "⚡":
                                    b.configure(
                                        fg_color="#ffffff" if flash_enabled else "#2a2a2a",
                                        text_color="#000000" if flash_enabled else "#ffffff",
                                        hover_color="#e0e0e0" if flash_enabled else "#3a3a3a"
                                    )

# Buka folder penyimpanan foto
def open_folder():
    folder_path = os.path.abspath(OUTPUT_FOLDER)
    
    if platform.system() == "Windows":
        os.startfile(folder_path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", folder_path])
    else:
        subprocess.Popen(["xdg-open", folder_path])

# Kembali ke layar awal
def back_to_start():
    global camera
    if camera is not None:
        camera.release()
        camera = None
    show_start_screen()

# Bersihkan jendela
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# Tangani penutupan jendela
def on_closing():
    global camera
    if camera is not None:
        camera.release()
    root.destroy()

# Fungsi utama
def main():
    global root
    root = setup_window()
    show_start_screen()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

# Jalankan aplikasi
if __name__ == "__main__":
    main()
