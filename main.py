from pathlib import Path
from tkinter import filedialog, messagebox
from PIL import Image

import customtkinter as ctk

log_window = None
info_window = None
log_textbox = None
selected_gcode_file = None

def modify_gcode(fichier, nb_layer, sp):
    """Modifie le fichier Gcode en ajoutant une commande de modification de vitesse à une couche spécifiée.
    
    Args:
        fichier (str): Le chemin vers le fichier Gcode.
        nb_layer (int): Le numéro de la couche à modifier.
        sp (int): La nouvelle vitesse à définir.

    Returns:
        bool: True si la modification a réussi, False sinon.
    """
    with open(fichier, 'r') as f_entree:
        contenu = f_entree.read()    
        index_debut_couche = contenu.find(f"LAYER:{nb_layer}") 

    if index_debut_couche != -1:
        index_fin_ligne = contenu.find("\n", index_debut_couche)
        if index_fin_ligne != -1:
            contenu_modifie = contenu[:index_fin_ligne + 1] + f"M220 S{sp}\n" + contenu[index_fin_ligne + 1:]
            
            with open(fichier, 'w') as f_sortie:
                f_sortie.write(contenu_modifie)
            return True
    return False

def select_file():
    """Ouvre une boîte de dialogue pour sélectionner un fichier Gcode."""
    global selected_gcode_file
    selected_gcode_file = filedialog.askopenfilename(filetypes=[("Fichiers Gcode", "*.gcode")])
    if selected_gcode_file:
        pass

log_entries_list = []

def add_log_entry(fichier, couche, vitesse, textbox):
    """Ajoute une entrée au journal des modifications.

    Args:
        fichier (str): Le fichier Gcode modifié.
        couche (int): Le numéro de la couche modifiée.
        vitesse (int): La nouvelle vitesse définie.
        textbox: Le widget de texte où afficher le journal.
    """
    nom_fichier = Path(fichier).name
    log_entries_list.append((nom_fichier, couche, vitesse))
    update_log_textbox_content(textbox)

def update_log_textbox_content(textbox):
    """Met à jour le widget de texte avec les entrées du journal."""
    textbox.configure(state="normal")
    textbox.delete(1.0, "end")  
    for entry in log_entries_list:
        textbox.insert("end", f"{entry}\n")
    textbox.configure(state="disabled")

def create_info_window():
    """Crée une fenêtre d'informations avec des liens et des coordonnées de contact."""
    global info_window
    if not info_window:
        info_window = ctk.CTkToplevel(app)
        info_window.geometry("400x200")
        info_window.title("Info")
        info_window.resizable(True, True)

        label = ctk.CTkLabel(info_window, text="Informations:")
        label.pack(padx=10, pady=10)

        email_frame = ctk.CTkFrame(info_window)
        email_frame.pack(padx=10, pady=5)

        email_text = "Email: formationpython2024@gmail.com"
        email = ctk.CTkTextbox(email_frame, wrap="word", height=3, width=250)
        email.pack(side="left")
        email.insert("end", email_text)
        
        chemin_img_copie = Path(__file__).parent.absolute() / "ressources" / "copie.png"
        pil_img = Image.open(chemin_img_copie)
        img_copie = ctk.CTkImage(pil_img)
        
        copy_button_email = ctk.CTkButton(email_frame, text="", command=lambda: app.clipboard_clear() or app.clipboard_append("formationpython2024@gmail.com") or app.update(), width=1, height=1, image=img_copie, fg_color="green", hover_color="#00FF00")
        copy_button_email.pack(side="right")

        github_frame = ctk.CTkFrame(info_window)
        github_frame.pack(padx=10, pady=5)

        github_text = "Github: https://github.com/XDarkSnake"
        github = ctk.CTkTextbox(github_frame, wrap="word", height=3, width=250)
        github.pack(side="left")
        github.insert("end", github_text)

        copy_button_github = ctk.CTkButton(github_frame, text="", command=lambda: app.clipboard_clear() or app.clipboard_append("https://github.com/XDarkSnake") or app.update(), width=1, height=1, image=img_copie, fg_color="green", hover_color="#00FF00")
        copy_button_github.pack(side="right")

        nom_prenom_label = ctk.CTkLabel(info_window, text="Matisse Briand", anchor="se")
        nom_prenom_label.pack(side="bottom", padx=10, pady=10, anchor="se")

        info_window.protocol("WM_DELETE_WINDOW", on_info_window_close)
        info_window.geometry("+{}+{}".format(app.winfo_rootx() + app.winfo_width(), app.winfo_rooty()))
        
        info_window.lift()

def create_log_window():
    """Crée une fenêtre de logs pour afficher le journal des modifications du Gcode."""
    global log_window, log_textbox
    if not log_window:
        log_window = ctk.CTkToplevel(app)
        log_window.geometry("500x150")
        log_window.title("Logs")
        log_window.resizable(True, True)

        label = ctk.CTkLabel(log_window, text="Logs:")
        label.pack(padx=10, pady=10)

        log_textbox = ctk.CTkTextbox(log_window, height=10, state="normal")
        log_textbox.pack(expand=True, fill="both", padx=10, pady=2)

        update_log_textbox_content(log_textbox)

        log_window.protocol("WM_DELETE_WINDOW", on_log_window_close)

        x_pos = app.winfo_rootx()
        y_pos = app.winfo_rooty() + app.winfo_height() + 20
        log_window.geometry("+{}+{}".format(x_pos, y_pos))

        log_window.lift()

def on_info_window_close():
    """Gère la fermeture de la fenêtre d'informations."""
    global info_window
    if info_window:
        info_window.destroy()
        info_window = None
        app.lift()

def on_log_window_close():
    """Gère la fermeture de la fenêtre de logs."""
    global log_window
    if log_window:
        log_window.destroy()
        log_window = None
        app.lift()

def main():
    """Modifie le Gcode et affiche le journal des modifications."""
    global log_textbox
    couche = input_1.get()
    vitesse = input_2.get()
    if not couche.isdigit() or not vitesse.isdigit():
        messagebox.showwarning("Attention", "Les valeurs doivent être des nombres entiers.")
        return

    if not selected_gcode_file:
        messagebox.showwarning("Attention", "Sélectionnez un fichier")
        return

    if modify_gcode(selected_gcode_file, couche, vitesse):
        add_log_entry(selected_gcode_file, couche, vitesse, log_textbox)
        messagebox.showinfo("Info", f"La vitesse {vitesse} a bien été modifiée à la couche {couche}")
    else:
        messagebox.showwarning("Attention", "La couche n'est pas trouvée ! ")

    app.lower()

app = ctk.CTk()
ctk.set_appearance_mode("dark")
app.geometry("600x200")
app.title("Printer 3D")
app.resizable(False, False)

title_label = ctk.CTkLabel(app, text="Printer 3D", font=("Helvetica", 16), text_color="red")
title_label.pack(side="top", padx=10, pady=10)

input_frame = ctk.CTkFrame(app)
input_frame.pack(side="top", padx=10, pady=10)

input_1_label = ctk.CTkLabel(input_frame, text="Couche :")
input_1_label.pack(side="left", padx=5)

input_1 = ctk.CTkEntry(input_frame, placeholder_text="Entrez la couche")
input_1.pack(side="left", padx=5)

input_2_label = ctk.CTkLabel(input_frame, text="Vitesse :")
input_2_label.pack(side="left", padx=5)

input_2 = ctk.CTkEntry(input_frame, placeholder_text="Entrez la vitesse")
input_2.pack(side="left", padx=5)

button_frame = ctk.CTkFrame(app)
button_frame.pack(side="top", pady=10)

button_file = ctk.CTkButton(button_frame, text="Choisir un fichier", command=lambda: (select_file(), app.lift()), fg_color="blue", hover_color="#0211BC")
button_file.pack(side="left", padx=10)

button_ok = ctk.CTkButton(button_frame, text="Ok", command=lambda: (main(), app.lift()), fg_color="orange", hover_color="#FF8000")
button_ok.pack(side="left", padx=10)

button_logs = ctk.CTkButton(app, text="Logs", width=10, command=lambda: (create_log_window(), app.lift()), fg_color="red", hover_color="#C52404")
button_logs.place(relx=0, rely=0, anchor='nw')

chemin_img_info = Path(__file__).parent.absolute() / "ressources" / "info.png"
pil_img = Image.open(chemin_img_info)
pil_img = Image.open(chemin_img_info)
img_info = ctk.CTkImage(pil_img)
button_info = ctk.CTkButton(app, image=img_info, text="", width=1, command=lambda: (create_info_window(), app.lift()))
button_info.place(relx=1, rely=0, anchor='ne')

app.mainloop()
