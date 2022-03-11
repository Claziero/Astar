from queue import PriorityQueue
from random import random
from time import sleep
import pygame
import numpy as np
import collections
import time

pygame.font.init()
pygame.mixer.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
win_surface = myfont.render('YOU WON', False, (255, 255, 255))
lose_surface = myfont.render('YOU LOST', False, (255, 255, 255))

RATE_TH = 5
WIDTH, HEIGHT = 640, 320
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")
FPS = 30

#---Elementi utili---
#Coda di priorità contenente i nodi scoperti non visitati
esplorare = PriorityQueue()
#Coda di priorità contenente i nodi scoperti già visitati
visitati = PriorityQueue()
#Costante costo
COSTO = 1

#Classe Nodo
class Nodo():
    #Costruttore
    def __init__(self, pos = None, precedente = None, tempo = 0) -> None:
        self.g = 0
        self.h = 0
        self.f = 0
        self.posizione = pos
        self.precedente = precedente
        self.tempo = tempo

    #Ridefinizione del concetto di uguaglianza tra nodi: devono essere nella stessa posizione allo stesso tempo
    def __eq__(self, altro) -> bool:
        assert(isinstance(altro, Nodo))
        return self.posizione == altro.posizione and self.tempo == altro.tempo #TBC

    #Ridefinizione del concetto di minore tra nodi: deve avere una f minore
    def __lt__(self, altro):
        assert(isinstance(altro, Nodo))
        return self.f < altro.f

    #Funzione per definire uno stato obiettivo
    def obiettivo(self) -> bool:
        return self.posizione[0] == 0

class frogger_game:
    def __init__(self):
        self.state_matrix = np.asarray([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1], #[1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])
        self.frog_pos = (7, 7)
        self.statemap = {}
        self.path = None

    # 0-Nothing, 1-left, 2-up, 3-right, 4-down
    def step(self, action):
        lose = False
        win = False
        self.aggiorna_campo(1)

        if (action == 1):
            self.frog_pos = (self.frog_pos[0], max(0, self.frog_pos[1] - 2))
        elif (action == 2):
            self.frog_pos = (max(0, self.frog_pos[0] - 1), self.frog_pos[1])
        elif (action == 3):
            self.frog_pos = (self.frog_pos[0], min(15, self.frog_pos[1] + 2))
        elif (action == 4):
            self.frog_pos = (min(7, self.frog_pos[0] + 1), self.frog_pos[1])

        if (self.state_matrix[self.frog_pos[0]][self.frog_pos[1]] != 0):
            lose = True

        if (self.frog_pos[0] == 0):
            win = True

        return lose, win

    def simple_reactive(self):
        action = 0
        if (self.frog_pos[0] >= 4 and self.frog_pos[0] <= 5):
            if (self.state_matrix[self.frog_pos[0] - 1][self.frog_pos[1] + 1] == 0):
                action = 2
        else:
            if (self.state_matrix[self.frog_pos[0] - 1][self.frog_pos[1] - 1] == 0):
                action = 2

        return action

    #Funzione per aggiornare il campo scorrendo nelle due direzioni
    def aggiorna_campo(self, incremento) -> None:
        r1 = collections.deque(self.state_matrix[1])
        r2 = collections.deque(self.state_matrix[2])
        r3 = collections.deque(self.state_matrix[3])
        r4 = collections.deque(self.state_matrix[4])
        r5 = collections.deque(self.state_matrix[5])
        r6 = collections.deque(self.state_matrix[6])
        r1.rotate(incremento)
        r2.rotate(incremento)
        r3.rotate(-incremento)
        r4.rotate(-incremento)
        r5.rotate(incremento)
        r6.rotate(incremento)
        r1 = list(r1)
        r2 = list(r2)
        r3 = list(r3)
        r4 = list(r4)
        r5 = list(r5)
        r6 = list(r6)
        self.state_matrix = np.asarray([self.state_matrix[0], r1, r2, r3, r4, r5, r6, self.state_matrix[7]])
        
    #Funzione per controllare una mossa: restituisce True se valida, False se porta alla perdita
    def controlla_pos(self, posizione) -> bool:
        if (self.state_matrix[posizione[0]][posizione[1]] != 0):
            return False    #Perso
        return True    #Non perso

    #Funzione per provare le mosse possibili in ogni punto
    def get_neighbors(self, nodo_corrente:Nodo):
        adjac_lis = []

        #Incrementa il tempo e fai scorrere il campo (tempo modulo larghezza della mappa)
        tempo = (nodo_corrente.tempo + 1) % 16
        self.aggiorna_campo(tempo)

        #Per ogni azione disponibile
        for action in range(5):
            if(action == 0):    #NONE
                pos = nodo_corrente.posizione
            elif(action == 1):  #LEFT
                pos = (nodo_corrente.posizione[0], max(0, nodo_corrente.posizione[1] - 2))
            elif(action == 2):  #UP
                pos = (max(0, nodo_corrente.posizione[0] - 1), nodo_corrente.posizione[1])
            elif(action == 3):  #RIGHT
                pos = (nodo_corrente.posizione[0], min(15, nodo_corrente.posizione[1] + 2))
            elif(action == 4):  #DOWN
                pos = (min(7, nodo_corrente.posizione[0] + 1), nodo_corrente.posizione[1])

            #Prova la mossa scelta
            mossa_buona = self.controlla_pos(pos)
            
            #Se l'azione non porta alla perdita, aggiungi un nuovo nodo alla lista dei vicini
            if(mossa_buona):
                #Imposta un nuovo nodo con la sua posizione e aggiungilo alla lista adiacenti
                n = Nodo(pos, nodo_corrente, tempo)
                adjac_lis.append(n)

        #Ripristina lo stato precedente del gioco
        self.aggiorna_campo(-tempo)
        return adjac_lis

    def h(self, n:Nodo): #H
        distanceFromEndLane = n.posizione[0] - 1
        return distanceFromEndLane

    def mapAState(self, position, matrix):
        self.statemap[position] = matrix

    def a_star_path_to_actions(self):
        if not self.path:
            self.path = self.A_star_agent()
            self.path.pop(0)

        if len(self.path) > 0:
            next_pose = self.path.pop(0)
            difference = np.array(next_pose) - np.array(self.frog_pos)

            if difference[0] < 0:
                return 2                # 2-up
            elif difference[0] > 0:
                return 4                # 4-down
            elif difference[1] > 0:
                return 3                # 3-right
            elif difference[1] < 0:
                return 1                # 1-left
        return 0               # 0-Nothing

    def A_star_agent(self):
        #Aggiungi il nodo iniziale alla coda esplorare, con costo 0
        nodo_iniziale = Nodo((7, 7))
        esplorare.put((0, nodo_iniziale))

        #---Inizia l'esplorazione---#
        #Finché la lista di nodi da esplorare non è vuota 
        while(len(esplorare.queue) != 0):
            #Estrai il primo elemento (a costo minimo)
            nodo_corrente = esplorare.get()[1]
            #E inseriscilo nella lista di nodi visitati
            visitati.put(nodo_corrente) 

            #Se il nodo corrente corrisponde all'obiettivo allora riporta il percorso fatto
            if(nodo_corrente.obiettivo()):
                print("Soluzione trovata")
                #Ricostruisci il percorso dalla fine verso l'inizio
                percorso = []
                while(nodo_corrente is not None):
                    percorso.append(nodo_corrente.posizione)
                    nodo_corrente = nodo_corrente.precedente

                #Restituisci il percorso inverso (inizio -> fine)
                print(percorso[::-1])
                return percorso[::-1]

            #Altrimenti cerca i nodi adiacenti al nodo corrente
            adiacenti = self.get_neighbors(nodo_corrente)

            #Per ogni nodo adiacente trovato
            for n in adiacenti:
                #Se il nodo è già stato visitato non fare nulla
                if(cerca_nodo(visitati, n)):
                    continue

                #Imposta i campi del nodo (F, G, H)
                n.g = nodo_corrente.g + COSTO
                n.h = self.h(n)
                n.f = n.g + n.h

                #Controlla che il nodo da aggiungere (n) non sia già in esplorare
                presente = cerca_nodo(esplorare, n)
                if(presente is not False):
                    #Se c'è controlla che non abbia valore di G maggiore di quello già presente
                    if(n.g >= presente.g):
                        #Scarta il nodo
                        continue

                #Aggiungi il nodo alla lista da esplorare
                esplorare.put((n.f, n))

                #---Torna ad esplorare i nodi adiacenti al corrente---#
            #---Esplora nuovi nodi, se ci sono---#

        #Se sei in questo punto, non hai trovato la soluzione
        print("Soluzione non trovata. Terminazione del programma")
        exit(1)
        return None

#Funzione per cercare un nodo all'interno di una lista
def cerca_nodo(lista:PriorityQueue, nodo:Nodo):
    #Se la lista è vuota ritorna subito
    if(len(lista.queue) == 0):
        return False

    #Scorri tutti gli elementi
    for n in lista.queue:
        #Se non è un nodo allora è una tupla contenente il nodo
        if(not isinstance(n, Nodo)):
            n = n[1]
        #Se trovi il nodo riportalo
        if(nodo == n):
            return n
    
    #Il nodo non è stato trovato
    return False

def draw_window(game):
    WIN.fill((0, 0, 0))

    for r in range(len(game.state_matrix)):
        for c in range(len(game.state_matrix[r])):
            if (game.state_matrix[r][c] == 1):
                pygame.draw.rect(surface=WIN, color=(155, 155, 155), rect=(c * 40, r * 40, 40, 40), border_radius=3)
    pygame.draw.circle(surface=WIN, color=(0, 255, 0),
                       center=((game.frog_pos[1] * 40) + 16, (game.frog_pos[0] * 40) + 16), radius=16)
    pygame.display.update()

def draw_win():
    # WIN.fill((0, 0, 0))
    WIN.blit(win_surface, (220, 140))
    pygame.display.update()
    sleep(1)
    pygame.quit()

def draw_lost():
    # WIN.fill((0, 0, 0))
    WIN.blit(lose_surface, (220, 140))
    pygame.display.update()
    sleep(1)
    pygame.quit()

def main():
    clock = pygame.time.Clock()
    run = True
    game = frogger_game()
    lost = False
    win = False

    t = int(random() * 14 + 1)
    print("Random:", t)
    game.aggiorna_campo(t)

    while run:
        clock.tick(FPS)
        if ((not lost) and (not win)):
            draw_window(game)
        elif (lost):
            draw_window(game)
            draw_lost()

        else:
            draw_window(game)
            draw_win()

        if ((not lost) and (not win)):
            #action = game.simple_reactive()
            action = game.a_star_path_to_actions()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
            
            time.sleep(0.5)
            lost, win = game.step(action)

main()