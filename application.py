import tkinter.filedialog
from tkinter import *
from tkinter import ttk
from popup_revenu import PopupRevenu
from popup_depense import PopupDepense
from fenetre_a_propos import FenetreAPropos


class Application:
    NOMBRE_OPERATIONS = 0
    def __init__(self):
        # Création de la fenêtre principale
        self.fenetre_principale = Tk()
        # Variable pour les fenêtres popup "ajouter un revenu" et "ajouter une dépense"
        self.popup_revenu = None
        self.popup_depense = None
        # Variable pour la fenêtre "à propos"
        self.fenetre_a_propos = None
        # Remplissage des opérations initiales
        self.__remplir_operations_initiales__()
        # Configuration de la fenêtre principale
        self.__configurer_fenetre_principale__()
        # Initialisation de la barre de menus
        self.__initialiser_menus__()
        # Configuration des boutons liés aux opérations d'ajout de revenu et de dépense
        self.__configurer_boutons_operations__()
        # Configuration de la table des opérations et la barre de défilement associée
        self.__configurer_table_operations__()
        # Configuration de l'espace de synthèse en bas de la fenêtre principale
        self.__configurer_synthese_operations__()
        # Lancement de la boucle d'événements pour la fenêtre principale
        self.fenetre_principale.mainloop()

    def __remplir_operations_initiales__(self):
        # Initialisation des opérations (à prendre en compte dès le lancement de l'application)
        self.liste_operations = [
            {'operation': 'Salaire', 'montant': 1450.76},
            {'operation': 'Courses lundi', 'montant': -33.45}
        ]
        Application.NOMBRE_OPERATIONS = len(self.liste_operations)

    def __configurer_fenetre_principale__(self):
        # Configuration des propriétés de la fenêtre principale
        self.fenetre_principale.title("Gestion de compte")
        # Configuration des dimensions et positions initiale de la fenêtre principale (centrée sur l'écran)
        largeur, hauteur = 300, 335
        position_droite = int(self.fenetre_principale.winfo_screenwidth()/2 - largeur/2)
        position_bas = int(self.fenetre_principale.winfo_screenheight()/2 - hauteur/2)
        self.fenetre_principale.geometry(f"{largeur}x{hauteur}+{position_droite}+{position_bas}")
        # Empêcher le redimensionnement de la fenêtre principale
        self.fenetre_principale.resizable(False, False)
        # Changement de l'icone bitmap de la fenêtre principale
        self.fenetre_principale.iconbitmap("./icone_compte.ico")

    def __initialiser_menus__(self):
        # Initialisation du menu 'Fichier' de la fenêtre principale
        menu_bar = Menu(self.fenetre_principale)
        self.menu_fichier = Menu(menu_bar, tearoff=0)
        self.menu_fichier.add_command(label="Réinitialiser", command=self.__reinitialiser_liste_operations__)
        self.menu_fichier.add_separator()
        self.menu_fichier.add_command(label="Charger...", command=self.charger_liste_operations)
        self.menu_fichier.add_command(label="Enregistrer sous...", command=self.sauvegarder_liste_operations)
        self.menu_fichier.add_separator()
        self.menu_fichier.add_command(label="Quitter", command=self.quitter)
        menu_bar.add_cascade(label="Fichier", menu=self.menu_fichier)
        # Initialisation du menu 'A propos' de la fenêtre principale
        menu_a_propos = Menu(menu_bar, tearoff=0)
        menu_a_propos.add_command(label="A propos", command=self.ouvrir_fenetre_a_propos)
        menu_bar.add_cascade(label="Aide", menu=menu_a_propos)
        # Ajout du menu global à la fenêtre principale de l'application
        self.fenetre_principale.config(menu=menu_bar)

    def __configurer_boutons_operations__(self):
        # Initialisation d'un espace pour regrouper les boutons d'ajout d'opérations
        zone_boutons = Frame(self.fenetre_principale)
        zone_boutons.pack(pady=(10, 10))
        # Création du bouton d'ajout d'une opération de revenu
        bouton_revenu = Button(zone_boutons, text="Revenu (+)", foreground="green", width=10,
                               command=self.__ouvrir_popup_revenu__)
        bouton_revenu.pack(side=LEFT)
        # Création du bouton d'ajout d'une opération de dépense
        bouton_depense = Button(zone_boutons, text="Dépense (-)", foreground="red", width=10,
                               command=self.__ouvrir_popup_depense__)
        bouton_depense.pack(side=RIGHT)

    def __configurer_table_operations__(self):
        # Initialisation d'un espace pour regrouper la table des opérations et la barre de défilement
        zone_operations = Frame(self.fenetre_principale)
        zone_operations.pack(pady=(0, 10))
        # Création d'un style graphique particulier pour modifier les entêtes de la table des opérations
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", show="headings", background="#C8C8C8", font=(None, 10, 'bold'))
        # Création et configuration de la table des opérations
        self.table_operations = ttk.Treeview(zone_operations, style="Treeview")
        self.table_operations['columns'] = ('Opération', 'Montant')
        self.table_operations.column("#0", width=0, stretch=NO)
        self.table_operations.column("Opération", anchor=CENTER, width=150)
        self.table_operations.column("Montant", anchor=CENTER, width=80)
        self.table_operations.heading("#0", text="", anchor=CENTER)
        self.table_operations.heading("Opération", text="Opération", anchor=CENTER)
        self.table_operations.heading("Montant", text="Montant", anchor=CENTER)
        # Configuration du menu contextuel sur la table des opérations
        m = Menu(self.fenetre_principale, tearoff=0)
        def ouvrir_menu_contextuel(event):
            try:
                self.id_ligne_selectionnee = self.table_operations.identify_row(event.y)
                self.table_operations.selection_set(f"{self.id_ligne_selectionnee}")
                m.tk_popup(event.x_root, event.y_root)
            finally:
                m.grab_release()
        m.add_command(label="Supprimer", command=self.__supprimer_operation__)
        self.table_operations.bind("<Button-3>", ouvrir_menu_contextuel)
        # Insertion des opérations initiales dans la table des opérations
        for index, operation in enumerate(self.liste_operations):
            montant_a_afficher = '+' + str(operation['montant']) if operation['montant'] >= 0.0 else str(operation['montant'])
            self.table_operations.insert(parent='', index='end', iid=index, text='',
                                         values=(operation['operation'], montant_a_afficher))
        self.table_operations.pack(side=LEFT)
        # Création de la barre de défilement associée à la table des opérations
        barre_defilement_verticale = ttk.Scrollbar(zone_operations, orient="vertical")
        barre_defilement_verticale.pack(side=RIGHT, fill='y')
        barre_defilement_verticale.config(command=self.table_operations.yview)
        self.table_operations.configure(yscrollcommand=barre_defilement_verticale.set)
        # Figeage de la taille des colonnes dans la table des opérations
        def empecher_redimensionnement_colonnes(event):
            if self.table_operations.identify_region(event.x, event.y) == "separator":
                return "break"
        self.table_operations.bind('<Button-1>', empecher_redimensionnement_colonnes)

    def __configurer_synthese_operations__(self):
        # Calcul du total des opérations (revenus - dépenses)
        montant_resultat = 0.0
        # Initialisation d'un espace pour le texte de synthèse des opérations
        zone_synthese = Frame(self.fenetre_principale)
        zone_synthese.pack(pady=(0, 10))
        # Création du label
        self.label_total = Label(zone_synthese, text=f"Total: {montant_resultat} €", font=(None, 10, 'bold'))
        self.label_total.pack()
        # Mise à jour du total des opérations au lancement de l'application
        self.__mettre_a_jour_synthese__()

    def __ouvrir_popup_revenu__(self):
        # Ouvrir et initialiser une popup pour ajouter une opération de type "revenu"
        self.popup_revenu = PopupRevenu(self)

    def __ouvrir_popup_depense__(self):
        # Ouvrir et initialiser une popup pour ajouter une opération de type "dépense"
        self.popup_depense = PopupDepense(self)

    def ajouter_revenu(self, nom_operation, montant_operation):
        # Ajoute l'opération dans la liste des opérations déjà effectuées
        self.liste_operations += [{'operation': nom_operation, 'montant': montant_operation}]
        # Ajoute l'opération de revenu dans la table des opérations
        montant_a_afficher = f"+{montant_operation:.2f}"
        self.table_operations.insert(parent='', index='end', iid=Application.NOMBRE_OPERATIONS, text='',
                                     values=(nom_operation, montant_a_afficher))
        # Mise à jour du nombre total d'opérations dans l'historique, et du résultat dans la synthèse
        Application.NOMBRE_OPERATIONS += 1
        self.__mettre_a_jour_synthese__()
        # Mise à jour du menu "Enregistrer sous..." si jamais c'est la première opération ajoutée
        self.__mettre_a_jour_menu_sauvegarder__()
        # Destruction de la fenêtre popup de revenu
        self.popup_revenu = None

    def ajouter_depense(self, nom_operation, montant_operation):
        # Ajoute l'opération dans la liste des opérations déjà effectuées
        self.liste_operations += [{'operation': nom_operation, 'montant': montant_operation}]
        # Ajoute l'opération de dépense dans la table des opérations
        montant_a_afficher = f"{montant_operation:.2f}"
        self.table_operations.insert(parent='', index='end', iid=Application.NOMBRE_OPERATIONS, text='',
                                     values=(nom_operation, montant_a_afficher))
        # Mise à jour du nombre total d'opérations dans l'historique, et du résultat dans la synthèse
        Application.NOMBRE_OPERATIONS += 1
        self.__mettre_a_jour_synthese__()
        # Mise à jour du menu "Enregistrer sous..." si jamais c'est la première opération ajoutée
        self.__mettre_a_jour_menu_sauvegarder__()
        # Destruction de la fenêtre popup de dépense
        self.popup_depense = None

    def __supprimer_operation__(self):
        try:
            # Récupération de l'opération sélectionnée pour la suppression
            operation_a_supprimer = self.table_operations.item(self.id_ligne_selectionnee)
            operation, montant = operation_a_supprimer['values']
            objet_operation = {'operation': operation, 'montant': round(float(montant), 2)}
            if objet_operation in self.liste_operations:
                # Suppression de l'opération de la table des opérations
                self.table_operations.delete(self.id_ligne_selectionnee)
                # Suppression de l'opération de la liste des opérations
                self.liste_operations.remove(objet_operation)
        except ValueError as error:
            print(error)
            pass
        finally:
            # Mise à jour de la synthèse et du total des opérations
            self.__mettre_a_jour_synthese__()
            # Mise à jour du statut du menu "Enregistrer sous..." si besoin
            self.__mettre_a_jour_menu_sauvegarder__()

    def __mettre_a_jour_synthese__(self):
        # Calcul du résultat de toutes les opérations effectuées, listées dans l'historique
        montant_resultat_operations = round(sum([operation['montant'] for _, operation in enumerate(self.liste_operations)]), 2)
        # Mise à jour du label synthétisant le résultat dans la fenêtre principale
        self.label_total['text'] = f"Total: {montant_resultat_operations:.2f} €"

    def __mettre_a_jour_menu_sauvegarder__(self):
        # Calcul du statu du menu "Enregistrer sous..." en fonction du nombre d'opérations dans l'historique
        statut_menu_enregistrer = "normal" if len(self.liste_operations) > 0 else "disabled"
        # Mise à jour du statut du menu "Enregistrer sous..."
        self.menu_fichier.entryconfig("Enregistrer sous...", state=statut_menu_enregistrer)

    def __reinitialiser_liste_operations__(self):
        # Vidage de la liste des opérations
        self.liste_operations = []
        Application.NOMBRE_OPERATIONS = 0
        # Vidage de la table des opérations
        for ligne_operation in self.table_operations.get_children():
            self.table_operations.delete(ligne_operation)
        # Mise à jour de la synthèse des opérations (vierge)
        self.__mettre_a_jour_synthese__()
        # Désactriver le menu "Enregistrer sous...", puisque la liste des opérations a été vidée
        self.__mettre_a_jour_menu_sauvegarder__()

    def charger_liste_operations(self):
        # Ouverture du dialogue et sélection du fichier d'opérations sauvegardées
        types_fichiers_filtres = [("Fichiers texte", ".txt")]
        fichier_a_charger = tkinter.filedialog.askopenfile(title="Sélectionnez un fichier...",
            initialdir="/", filetypes=types_fichiers_filtres)
        # Vérification de la validité du fichier de sauvegarde sélectionné
        if fichier_a_charger is not None:
            # Réinitialisation de la liste complète des opérations, on repart d'un état vierge
            self.__reinitialiser_liste_operations__()
            # Ouverture du fichier et lecture des opérations ligne à ligne
            with open(fichier_a_charger.name, 'r') as fichier_ouvert:
                lignes_operations = fichier_ouvert.readlines()
                for ligne_operation in lignes_operations:
                    informations_operation = ligne_operation.replace('\n', '').split('@')
                    nom_operation = informations_operation[0]
                    montant_operation = round(float(informations_operation[1]), 2)

                    # Ajoute l'opération dans la liste des opérations déjà effectuées
                    self.liste_operations += [{'operation': nom_operation, 'montant': montant_operation}]
                    # Ajoute l'opération de dépense dans la table des opérations
                    montant_a_afficher = f"{montant_operation:.2f}" if montant_operation < 0.0 else f"+{montant_operation:.2f}"
                    self.table_operations.insert(parent='', index='end', iid=Application.NOMBRE_OPERATIONS, text='',
                                                 values=(nom_operation, montant_a_afficher))
                    # Mise à jour du nombre total d'opérations dans l'historique, et du résultat dans la synthèse
                    Application.NOMBRE_OPERATIONS += 1
                # Mise à jour de la synthèse des opérations (avec le nombre d'opérations chargées depuis le fichier)
                self.__mettre_a_jour_synthese__()
                # Mise à jour du menu "Enregistrer sous..."
                self.__mettre_a_jour_menu_sauvegarder__()
                # Affichage d'une popup d'information comme quoi les opérations ont bien été chargées
                tkinter.messagebox.showinfo("Opérations chargées !",
                                            f"Les opérations courantes ont bien été chargées depuis le fichier suivant : \"{fichier_a_charger.name}\" !")

    def sauvegarder_liste_operations(self):
        # Ouverture du dialogue pour enregistrer les opérations en cours dans un fichier
        types_fichiers_filtres = [("Fichiers texte", ".txt")]
        fichier_de_sauvegarde = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".txt",
            filetypes=types_fichiers_filtres)
        if fichier_de_sauvegarde is not None:
            # Si le fichier dans lequel enregistrer est valide, on écrit les opérations ligne par ligne
            lignes_a_sauvegarder = []
            for operation in self.liste_operations:
                texte_ligne_a_sauvegarder = f"{operation['operation']}@{operation['montant']}\n"
                lignes_a_sauvegarder += [texte_ligne_a_sauvegarder]
            # On écrit toutes les lignes correspondant aux opérations et on ferme le fichier
            fichier_de_sauvegarde.writelines(lignes_a_sauvegarder)
            fichier_de_sauvegarde.close()
            # Affichage d'une popup d'information comme quoi les opérations ont bien été enregistrées
            tkinter.messagebox.showinfo("Opérations enregistrées !",
                f"Les opérations courantes ont bien été enregistrées dans le fichier suivant : \"{fichier_de_sauvegarde.name}\" !")

    def ouvrir_fenetre_a_propos(self):
        # Ouvrir et initialiser la fenêtre "à propos" de l'application
        self.fenetre_a_propos = FenetreAPropos(self)

    def quitter(self):
        # Fermeture et destruction de la fenêtre principale de l'application
        self.fenetre_principale.destroy()
