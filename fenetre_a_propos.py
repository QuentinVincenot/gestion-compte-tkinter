from tkinter import *


class FenetreAPropos(Toplevel):
    def __init__(self, application, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        # Garder la référence vers l'application principale
        self.application = application
        # Configuration de la fenêtre popup et de ses composants
        self.__configurer_popup_a_propos__()
        # Rendre cette fenêtre popup modale par rapport à la fenêtre principale
        self.grab_set()
        self.focus_force()

    def __configurer_popup_a_propos__(self):
        # Configuration des propriétés de la fenêtre popup dépense
        self.title("A propos")
        # Configuration des dimensions et positions initiale de la popup d'ajout de dépense (centrée sur l'écran)
        largeur, hauteur = 300, 150
        position_droite = int(self.application.fenetre_principale.winfo_screenwidth()/2 - largeur/2)
        position_bas = int(self.application.fenetre_principale.winfo_screenheight()/2 - hauteur/2)
        self.geometry(f"{largeur}x{hauteur}+{position_droite}+{position_bas}")
        # Empêcher le redimensionnement de la popup
        self.resizable(False, False)
        # Changement de l'icone bitmap de la fenêtre popup
        self.iconbitmap('./icone_a_propos.ico')
        # Configuration de la frame globale de la popup et de ses composants
        zone_texte = Frame(self)
        zone_texte.pack()
        # Initialisation du label, du champs de texte et de l'écouteur d'événements pour le nom de l'opération
        texte_a_propos = "Ce programme de gestion de compte a été créé\n" \
                         "de mon entière imagination. Merci de respecter\n" \
                         "mon travail et de ne pas le recopier sans m'en\n" \
                         "informer en amont !\n\n" \
                         "Quentin VINCENOT\n\n\u00A9 Quentin VINCENOT (2021-présent)"
        label_texte = Label(zone_texte, text=texte_a_propos)
        label_texte.pack(pady=0)
        texte_version = "Version 1.0"
        label_version = Label(zone_texte, text=texte_version, fg='#FF9632', font=(None, 10, 'bold'))
        label_version.pack()
