"""
Wrapper Tkinter pour le Jeu de la Vie des Citrouilles
Ce fichier contient tout le code technique pour l'affichage.
Les lycéens n'ont pas besoin de modifier ce fichier.
"""

import tkinter as tk
from tkinter import ttk
import time

class PumpkinGameOfLife:
    """Classe wrapper pour gérer l'affichage du jeu de la vie"""
    
    def __init__(self, largeur=40, hauteur=30, taille_cellule=20):
        """
        Initialise le jeu avec une grille de citrouilles
        
        Args:
            largeur: nombre de colonnes
            hauteur: nombre de lignes
            taille_cellule: taille en pixels de chaque cellule
        """
        self.largeur = largeur
        self.hauteur = hauteur
        self.taille_cellule = taille_cellule
        self.en_cours = False
        self.vitesse = 200  # milliseconds entre chaque génération
        
        # Création de la grille (0 = vide, 1 = citrouille vivante)
        self.grille = [[0 for _ in range(largeur)] for _ in range(hauteur)]
        
        # Interface graphique
        self.root = tk.Tk()
        self.root.title("🎃 Le Jeu de la Vie des Citrouilles 🎃")
        self.root.configure(bg='#1a1a2e')
        
        self._creer_interface()
        
    def _creer_interface(self):
        """Crée l'interface graphique complète"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(padx=10, pady=10)
        
        # Titre
        titre = tk.Label(
            main_frame, 
            text="🎃 JEU DE LA VIE DES CITROUILLES 🎃",
            font=('Arial', 18, 'bold'),
            bg='#1a1a2e',
            fg='#ff8c00'
        )
        titre.pack(pady=10)
        
        # Canvas pour la grille
        self.canvas = tk.Canvas(
            main_frame,
            width=self.largeur * self.taille_cellule,
            height=self.hauteur * self.taille_cellule,
            bg='#16213e',
            highlightthickness=2,
            highlightbackground='#ff8c00'
        )
        self.canvas.pack(pady=10)
        self.canvas.bind('<Button-1>', self._clic_souris)
        
        # Frame pour les contrôles
        controls_frame = tk.Frame(main_frame, bg='#1a1a2e')
        controls_frame.pack(pady=10)
        
        # Boutons
        style_btn = {
            'font': ('Arial', 11, 'bold'),
            'bg': '#ff8c00',
            'fg': 'white',
            'activebackground': '#ff6b00',
            'relief': 'raised',
            'bd': 3,
            'padx': 15,
            'pady': 8
        }
        
        self.btn_start = tk.Button(
            controls_frame,
            text="▶ Démarrer",
            command=self.demarrer,
            **style_btn
        )
        self.btn_start.grid(row=0, column=0, padx=5)
        
        self.btn_pause = tk.Button(
            controls_frame,
            text="⏸ Pause",
            command=self.pause,
            state='disabled',
            **style_btn
        )
        self.btn_pause.grid(row=0, column=1, padx=5)
        
        self.btn_reset = tk.Button(
            controls_frame,
            text="🔄 Réinitialiser",
            command=self.reinitialiser,
            **style_btn
        )
        self.btn_reset.grid(row=0, column=2, padx=5)
        
        # Label pour la génération
        self.generation = 0
        self.label_gen = tk.Label(
            main_frame,
            text=f"Génération: {self.generation}",
            font=('Arial', 12),
            bg='#1a1a2e',
            fg='#ff8c00'
        )
        self.label_gen.pack(pady=5)
        
        # Instructions
        instructions = tk.Label(
            main_frame,
            text="Cliquez sur la grille pour placer/retirer des citrouilles",
            font=('Arial', 10),
            bg='#1a1a2e',
            fg='#cccccc'
        )
        instructions.pack(pady=5)
        
        self._dessiner_grille()
    
    def _dessiner_grille(self):
        """Dessine la grille avec les citrouilles"""
        self.canvas.delete('all')
        
        # Dessiner les lignes de la grille
        for i in range(self.hauteur + 1):
            self.canvas.create_line(
                0, i * self.taille_cellule,
                self.largeur * self.taille_cellule, i * self.taille_cellule,
                fill='#0f3460', width=1
            )
        
        for j in range(self.largeur + 1):
            self.canvas.create_line(
                j * self.taille_cellule, 0,
                j * self.taille_cellule, self.hauteur * self.taille_cellule,
                fill='#0f3460', width=1
            )
        
        # Dessiner les citrouilles
        for i in range(self.hauteur):
            for j in range(self.largeur):
                if self.grille[i][j] == 1:
                    self._dessiner_citrouille(i, j)
    
    def _dessiner_citrouille(self, ligne, colonne):
        """Dessine une citrouille à la position donnée"""
        x1 = colonne * self.taille_cellule + 2
        y1 = ligne * self.taille_cellule + 2
        x2 = x1 + self.taille_cellule - 4
        y2 = y1 + self.taille_cellule - 4
        
        # Corps de la citrouille (orange)
        self.canvas.create_oval(
            x1, y1, x2, y2,
            fill='#ff8c00',
            outline='#cc6600',
            width=2
        )
        
        # Tige (vert)
        cx = (x1 + x2) / 2
        self.canvas.create_line(
            cx, y1, cx, y1 - 3,
            fill='#228b22',
            width=2
        )
    
    def _clic_souris(self, event):
        """Gère les clics de souris pour ajouter/retirer des citrouilles"""
        if self.en_cours:
            return
        
        colonne = event.x // self.taille_cellule
        ligne = event.y // self.taille_cellule
        
        if 0 <= ligne < self.hauteur and 0 <= colonne < self.largeur:
            self.grille[ligne][colonne] = 1 - self.grille[ligne][colonne]
            self._dessiner_grille()
    
    def demarrer(self):
        """Démarre la simulation"""
        self.en_cours = True
        self.btn_start.config(state='disabled')
        self.btn_pause.config(state='normal')
        self._boucle_jeu()
    
    def pause(self):
        """Met en pause la simulation"""
        self.en_cours = False
        self.btn_start.config(state='normal')
        self.btn_pause.config(state='disabled')
    
    def reinitialiser(self):
        """Réinitialise la grille"""
        self.pause()
        self.grille = [[0 for _ in range(self.largeur)] for _ in range(self.hauteur)]
        self.generation = 0
        self.label_gen.config(text=f"Génération: {self.generation}")
        self._dessiner_grille()
    
    def _boucle_jeu(self):
        """Boucle principale du jeu"""
        if not self.en_cours:
            return
        
        # Appel de la fonction calculer_prochaine_generation du main.py
        from main import calculer_prochaine_generation
        self.grille = calculer_prochaine_generation(self.grille)
        
        self.generation += 1
        self.label_gen.config(text=f"Génération: {self.generation}")
        self._dessiner_grille()
        
        self.root.after(self.vitesse, self._boucle_jeu)
    
    def lancer(self):
        """Lance la fenêtre principale"""
        self.root.mainloop()



def compter_voisins(grille, ligne, colonne):
    hauteur = len(grille)
    largeur = len(grille[0])
    compteur = 0
    
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni = ligne + di
            nj = colonne + dj
            if 0 <= ni < hauteur and 0 <= nj < largeur:
                compteur += grille[ni][nj]
    
    return compteur
