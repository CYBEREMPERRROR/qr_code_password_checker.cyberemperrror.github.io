import tkinter as tk from tkinter import messagebox, simpledialog, filedialog import json, base64, os, random, string from cryptography.fernet import Fernet from PIL import Image, ImageTk

=== File paths ===

VAULT_FILE = 'vault.json' KEY_FILE = 'secret.key' QR_IMAGE_FILE = 'unlock_key.png' PROFILE_PIC = 'ethical_hacker.jpg'

=== Colors and Theme ===

THEMES = { "dark": { "bg": "#0f0f0f", "fg": "#00ff00", "btn": "#1f1f1f", "entry": "#111", }, "light": { "bg": "#f0f0f0", "fg": "#000", "btn": "#ddd", "entry": "#fff", } }

=== Global State ===

current_theme = "dark" theme = THEMES[current_theme]

=== Helper Functions ===

def load_key(): with open(KEY_FILE, 'rb') as f: return f.read()

def save_vault(data): with open(VAULT_FILE, 'w') as f: json.dump(data, f)

def load_vault(): if not os.path.exists(VAULT_FILE): return {} with open(VAULT_FILE, 'r') as f: return json.load(f)

def encrypt(password): return Fernet(load_key()).encrypt(password.encode()).decode()

def decrypt(token): return Fernet(load_key()).decrypt(token.encode()).decode()

def generate_password(length=12): characters = string.ascii_letters + string.digits + string.punctuation return ''.join(random.choice(characters) for _ in range(length))

def switch_theme(): global current_theme, theme current_theme = "light" if current_theme == "dark" else "dark" theme = THEMES[current_theme] apply_theme()

def apply_theme(): root.config(bg=theme['bg']) for widget in root.winfo_children(): try: widget.config(bg=theme['bg'], fg=theme['fg']) except: pass

=== UI Functions ===

def save_entry(): name = name_entry.get() password = pass_entry.get() if not name or not password: return messagebox.showwarning("Input error", "Fill all fields") vault[name] = encrypt(password) save_vault(vault) update_display() name_entry.delete(0, tk.END) pass_entry.delete(0, tk.END)

def update_display(): display.delete(0, tk.END) for name in vault: display.insert(tk.END, name)

def show_password(): selected = display.get(tk.ANCHOR) if not selected: return try: password = decrypt(vault[selected]) messagebox.showinfo("Password", f"{selected}: {password}") except: messagebox.showerror("Error", "Failed to decrypt password")

def export_data(): export_path = filedialog.asksaveasfilename(defaultextension=".json") if export_path: with open(export_path, 'w') as f: json.dump(vault, f) messagebox.showinfo("Exported", f"Data saved to {export_path}")

def import_data(): file_path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")]) if file_path: with open(file_path, 'r') as f: data = json.load(f) vault.update(data) save_vault(vault) update_display()

def generate_and_copy(): pwd = generate_password() pass_entry.delete(0, tk.END) pass_entry.insert(0, pwd) root.clipboard_clear() root.clipboard_append(pwd) messagebox.showinfo("Generated", "Password copied to clipboard")

def launch_main_gui(): intro.destroy() global root root = tk.Tk() root.title("QR Password Locker") root.geometry("500x500")

# Theme toggle
toggle = tk.Button(root, text="Switch Theme", command=switch_theme, bg=theme['btn'])
toggle.pack(pady=5)

# Entry
tk.Label(root, text="Account Name:", bg=theme['bg'], fg=theme['fg']).pack()
global name_entry
name_entry = tk.Entry(root, bg=theme['entry'])
name_entry.pack()

tk.Label(root, text="Password:", bg=theme['bg'], fg=theme['fg']).pack()
global pass_entry
pass_entry = tk.Entry(root, show='*', bg=theme['entry'])
pass_entry.pack()

gen_btn = tk.Button(root, text="Generate Password", command=generate_and_copy, bg=theme['btn'])
gen_btn.pack(pady=5)

save_btn = tk.Button(root, text="Save Entry", command=save_entry, bg=theme['btn'])
save_btn.pack(pady=5)

show_btn = tk.Button(root, text="Show Password", command=show_password, bg=theme['btn'])
show_btn.pack(pady=5)

exp_btn = tk.Button(root, text="Export Vault", command=export_data, bg=theme['btn'])
exp_btn.pack(pady=5)

imp_btn = tk.Button(root, text="Import Vault", command=import_data, bg=theme['btn'])
imp_btn.pack(pady=5)

global display
display = tk.Listbox(root, bg=theme['entry'])
display.pack(pady=10, fill=tk.BOTH, expand=True)

update_display()
apply_theme()
root.mainloop()

=== Intro Window ===

intro = tk.Tk() intro.title("Welcome to QR Password Locker") intro.geometry("600x400") intro.configure(bg="black")

Matrix background

canvas = tk.Canvas(intro, bg="black", highlightthickness=0) canvas.pack(fill=tk.BOTH, expand=True)

matrix_chars = ["0", "1"] matrix_drops = [0 for _ in range(100)]

Matrix Effect Animation

def draw_matrix(): canvas.delete("all") w = canvas.winfo_width() h = canvas.winfo_height() font_size = 15 columns = w // font_size

for i in range(columns):
    char = random.choice(matrix_chars)
    x = i * font_size
    y = matrix_drops[i] * font_size
    canvas.create_text(x, y, text=char, fill="green", font=('Courier', font_size))
    matrix_drops[i] = matrix_drops[i] + 1 if y < h else 0

intro.after(50, draw_matrix)

def start_app(): launch_main_gui()

Add profile image

img = Image.open(PROFILE_PIC) img = img.resize((100, 100)) profile_img = ImageTk.PhotoImage(img) img_label = tk.Label(intro, image=profile_img, bg="black") img_label.place(x=20, y=20)

Info Text

info = """BY\nNAME: YAHUZA YUNUS MUSA\nDEPARTMENT: COMPUTER SCIENCE\nCOURSE CODE: UA-CSC102\nCOURSE TITLE: SURVEY OF PROGRAMMING LANGUAGE""" info_label = tk.Label(intro, text=info, font=("Consolas", 10), fg="lime", bg="black", justify="left") info_label.place(x=140, y=25)

Continue Button

cont = tk.Button(intro, text="CONTINUE", font=("Arial", 14), command=start_app, bg="lime", fg="black") cont.place(x=250, y=300)

Run Intro

draw_matrix() intro.mainloop()

Load vault

vault = load_vault()

