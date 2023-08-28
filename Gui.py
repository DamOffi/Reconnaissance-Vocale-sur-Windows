from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import test
import threading

def button():
    if StartButton["text"] == "Démarrer":
        switch = True
        StartButton["text"] = "Arrêter"
        StartButton.update()     
    else:
        switch = False
        StartButton["text"] = "Démarrer"
        StartButton.update()
    threading.Thread(target=test.recognizer, args=(switch,)).start()

#ouverture du programme On vérifie le fichier settings.txt si il fonctionne correctement
try:
    with open("settings.txt", "r") as fichier:
        try:
            t = fichier.readlines()
            micro = []
            if t[0].split()[1] == ":":
                for i in range(2, len(t[0].split())):
                    micro.append(t[0].split()[i])
                micro = " ".join(micro)
                test.set_microphone(micro)
            else:
                raise IndexError
        except IndexError:
             with open("settings.txt", "w") as fichierw:
                  filesettings_init = ["Microphones : None", "Languages : French"]
                  for settings in filesettings_init:
                       fichierw.write("%s\n" % settings)
    root = Tk()
    root.resizable(False, False)
    root.title("Reconnaissance Vocal")

    Reco_voc_txt = Label(root, text="Reconnaissance Vocal", font={"Arial",32, "bold"}, foreground="Black", width=32, height=4)
    Reco_voc_txt.pack(side=TOP)

    StartButton = Button(root, font={"Arial",32, "bold"}, text="Démarrer", command=button)
    StartButton.pack(side=BOTTOM, fill=X)

    # Menus/Onglets
    List_Menu = Menu(root)

    Micro_Index = IntVar()

    # settings : Changer Micro, changer la langue, Mettre un toggle au démmarage du pc
    def Settings():
        root1 = Toplevel()
        root1.title("Paramètre")
        root1.geometry("500x155")
        root1.resizable(False,False)
        #print(Micro_Index.get())
        
        def update(event):
            global Micro_selected
            Micro_selected = list_micro.get()
            #print(Micro_selected)

        # la fonction Apply pour le Bouton Appliquer
        def Apply():
            global t
            global micro
            #print(micro)
            Micro_Index.set(list_micro.current())
            with open("settings.txt", "w") as fichier:
                t = [i.replace(micro, Micro_selected) if i == t[0] else i for i in t]
                #print(t)
                micro = Micro_selected
                test.set_microphone(micro)
                fichier.writelines(t)
        # Partie : Changer Micro
        Micro_frame = Frame(root1, background="Red")
        Micro_frame.pack(side=LEFT, anchor=NW)
        test1 = Label(Micro_frame, text="Périphérique d'entrée",font={"Arial",32}, background="Green")
        test1.pack()

        list_micro = ttk.Combobox(Micro_frame, values=test.CheckMicro())
        list_micro.bind("<<ComboboxSelected>>", update)
        list_micro.pack()

        if Micro_Index.get() is not None:
            list_micro.current(Micro_Index.get())
        else:
            list_micro.current(0)

        # le bouton Appliquer
        ApplyButton = Button(root1, font={"Arial",32, "bold"}, text="Appliquer", command=Apply)
        ApplyButton.pack(side=BOTTOM)
        root1.mainloop()

    List_Menu.add_command(label="Paramètre", command=Settings)

    root.config(menu=List_Menu)
    root.protocol("WM_DELETE_WINDOW", print("salut"))
    root.mainloop()

except FileNotFoundError:
    messagebox.showerror(title="Error #001", message="Le fichier settings.txt n'existe pas")