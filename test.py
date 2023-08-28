try:
    import speech_recognition as sr
except ModuleNotFoundError:
    print("Le module n'est pas installé")
import subprocess
import os
import Voice_app
import webbrowser

# Trouver le chemin d'accès et l'ouvrir
def searchfile(fichier):
    dossier_debut = "C:\\"
    nom_fichier_recherche = fichier + ".exe"
    for dossier_actuel, sous_dossiers, fichiers in os.walk(dossier_debut):
        for fichier in fichiers:
            if fichier == nom_fichier_recherche:
                chemin_complet = os.path.join(dossier_actuel, fichier)
                print("Fichier trouvé :", chemin_complet)
    subprocess.Popen(chemin_complet)

# faire un switch on/off du la fonction bouton dans le fichier Gui.py
def recognizer(switch):
    global loop
    if switch:
        loop = True
    else:
        loop = False
    Voice()
# Definir le micro
def set_microphone(name=str):
    global indexmic
    indexmic = sr.Microphone().list_microphone_names().index(name)
    
# Reconnaissance Vocal
def Voice():
    #print(loop)
    r = sr.Recognizer()
    r.pause_threshold = 0.5
    #print(sr.Microphone().list_microphone_names())
    with sr.Microphone(device_index=indexmic) as source:
        while loop:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, phrase_time_limit=5)
            try:
                text = r.recognize_google(audio, language="fr-FR")
                text = ''.join(text)
                print(text)
                if text.startswith("ok Windows"):
                    text = text.split()
                    print("Ca marche !")
                    if ("démarre" in text or "lance" in text) :
                        for app in Voice_app.Application :
                            if app in text:
                                searchfile(fichier=Voice_app.Application[app])
                    if "recherche" in text :
                        url = []
                        if ("Internet" in text or "google" in text) : # sur 
                            for i in range(text.index("recherche")+1, text.index("Internet")-1):
                                url.append(text[i])
                            url = " ".join(url)
                            webbrowser.open("https://www.google.com/search?q="+url)
                        if "YouTube" in text :
                            for i in range(text.index("recherche"), text.index("YouTube")):
                                url.append(text[i])
                            url = " ".join(url)
                            webbrowser.open("https://www.youtube.com/results?search_query="+url)
            except sr.UnknownValueError:
                #print("erreur")
                pass


def CheckMicro():
    p = sr.Microphone().get_pyaudio().PyAudio()
    num_devices = p.get_device_count()
    print("Liste des périphériques d'entrée audio disponibles :")
    Micro_available = []
    for i in range(num_devices):
        device_info = p.get_device_info_by_index(i)
        if device_info["maxInputChannels"] > 0 and device_info["hostApi"] == 0:
                print(f"{i+1}. {device_info['name']}")
                Micro_available.append(device_info['name'])
                print(Micro_available)
    return Micro_available
