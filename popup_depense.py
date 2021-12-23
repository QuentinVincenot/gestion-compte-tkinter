from tkinter import *


class PopupDepense(Toplevel):
    def __init__(self, application, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        # Garder la référence vers l'application principale
        self.application = application
        # Configuration de la fenêtre popup et de ses composants
        self.__configurer_popup_depense__()
        # Rendre cette fenêtre popup modale par rapport à la fenêtre principale
        self.grab_set()
        self.focus_force()

    def __configurer_popup_depense__(self):
        # Configuration des propriétés de la fenêtre popup dépense
        self.title("Ajouter une dépense")
        # Configuration des dimensions et positions initiale de la popup d'ajout de dépense (centrée sur l'écran)
        largeur, hauteur = 300, 110
        position_droite = int(self.application.fenetre_principale.winfo_screenwidth()/2 - largeur/2)
        position_bas = int(self.application.fenetre_principale.winfo_screenheight()/2 - hauteur/2)
        self.geometry(f"{largeur}x{hauteur}+{position_droite}+{position_bas}")
        # Empêcher le redimensionnement de la popup
        self.resizable(False, False)
        # Changement de l'icone bitmap de la fenêtre popup
        self.iconbitmap('./icone_depense.ico')
        # Configuration de la frame globale de la popup et de ses composants
        zone_formulaire = Frame(self)
        zone_formulaire.pack()
        # Initialisation du label, du champs de texte et de l'écouteur d'événements pour le nom de l'opération
        zone_champs_operation = Frame(zone_formulaire)
        zone_champs_operation.pack(pady=10)
        label_operation = Label(zone_champs_operation, text="Opération:", width=10, anchor='e')
        label_operation.pack(side=LEFT, padx=(0, 5))
        texte_operation = StringVar(value='Courses')
        texte_operation.trace("w", lambda name, index, mode, texte=texte_operation: self.__verifier_contenu_champs__())
        self.champ_texte_operation = Entry(zone_champs_operation, textvariable=texte_operation)
        self.champ_texte_operation.pack(side=RIGHT)
        # Initialisation du label, du champs de texte et de l'écouteur d'événements pour le montant de l'opération
        zone_champs_montant = Frame(zone_formulaire)
        zone_champs_montant.pack(pady=(0, 10))
        label_montant = Label(zone_champs_montant, text="Montant:", width=10, anchor='e')
        label_montant.pack(side=LEFT, padx=(0, 5))
        texte_montant = StringVar(value='-54.48')
        texte_montant.trace("w", lambda name, index, mode, texte=texte_montant: self.__verifier_contenu_champs__())
        self.champ_texte_montant = Entry(zone_champs_montant, textvariable=texte_montant)
        self.champ_texte_montant.pack(side=RIGHT)
        # Initialisation des boutons valider et fermer, côte à côte dans une zone de confirmation
        zone_boutons = Frame(zone_formulaire)
        zone_boutons.pack()
        self.bouton_valider = Button(zone_boutons, text="Valider", width=7, command=self.__valider_depense__)
        self.bouton_valider.pack(side=LEFT, padx=(0, 5))
        self.bouton_annuler = Button(zone_boutons, text="Annuler", width=7, command=self.quitter)
        self.bouton_annuler.pack(side=RIGHT)

    def __verifier_contenu_champs__(self):
        # Vérifier que les deux champs sont remplis et que le deuxième est un nombre
        deux_champs_remplis = (len(self.champ_texte_operation.get()) > 0 and len(self.champ_texte_montant.get()) > 0)
        try:
            valeur_montant = round(float(self.champ_texte_montant.get()), 2)
            deuxieme_champs_nombre = True if valeur_montant < 0.0 else False
        except ValueError:
            deuxieme_champs_nombre = False
        # Si les deux champs sont bien remplis et que le deuxième est bien un nombre, l'opération est valide
        self.bouton_valider['state'] = NORMAL if (deux_champs_remplis and deuxieme_champs_nombre) else DISABLED

    def __valider_depense__(self):
        # Récupérer les valeurs inscrites dans les deux champs de texte pour l'opération et le montant
        nom_operation = self.champ_texte_operation.get()
        montant_operation = round(float(self.champ_texte_montant.get()), 2)
        # Insérer la nouvelle opération de dépense dans l'historique des opérations
        self.application.ajouter_depense(nom_operation, montant_operation)
        # Fermer cette popup après validation et insertion de la nouvelle dépense
        self.quitter()

    def quitter(self):
        # Destruction de cette fenêtre popup
        self.destroy()
