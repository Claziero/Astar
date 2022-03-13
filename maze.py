from Astar import Gioco, Nodo, Azione
import string
from pyamaze import maze, agent

# Definizione costanti globali
RIGHE:int = 10
COLONNE:int = 10
OBIETTIVO:tuple[int] = (1, 1)
PARTENZA:tuple[int] = (RIGHE, COLONNE)

# Classe NodoLabirinto (estensione della classe Nodo di Astar)
class NodoL(Nodo):
    # Costruttore
    def __init__(self, pos:tuple[int], precedente=None) -> None:
        super().__init__(precedente)
        self.pos:tuple[int] = pos

    # Funzione per riportare se un nodo è finale
    def obiettivo(self) -> bool:
        # Il nodo finale è in posizione (1, 1)
        return self.pos == OBIETTIVO

    # Funzione per riportare se un nodo è valido
    def valido(self) -> bool:
        # Uno stato è valido se la posizione rientra nei confini della mappa
        return 1 <= self.pos[0] <= RIGHE and 1 <= self.pos[1] <= COLONNE

    # Funzione euristica
    def H(self) -> int:
        # Riporta la distanza euclidea tra il nodo e l'obiettivo
        return (OBIETTIVO[0] - self.pos[0])**2 + (OBIETTIVO[1] - self.pos[1])**2

    # Ridefinizione del concetto di uguaglianza tra nodi
    def __eq__(self, altro) -> bool:
        # Due nodi sono uguali se hanno la stessa posizione
        return self.pos == altro.pos

    # Funzione per stampare le informazioni del nodo
    # Nodo nel formato (i, j), cioè la posizione del nodo nel labirinto
    def formato_stampa(self) -> string:
        return self.pos

# Classe AzioneLabirinto (estensione della classe Azione di Astar)
class AzioneL(Azione):
    # Costruttore
    def __init__(self, id=None) -> None:
        # Definizione degli assi X ed Y:
        # X scorre lungo le righe (x maggiori corrispondono ad essere più in basso alla mappa)
        # Y scorre lungo le colonne (y maggiori corrispondono ad essere più a destra nella mappa)
        
        # Azioni possibili:
        # N = UP        (x-1, y)
        # E = RIGHT     (x, y+1)
        # W = LEFT      (x, y-1)
        # S = DOWN      (x+1, y)
        
        self.id = id
        if id == 'N':
            self.maschera = (-1, 0)
        elif id == 'E':
            self.maschera = (0, +1)
        elif id == 'W':
            self.maschera = (0, -1)
        elif id == 'S':
            self.maschera = (+1, 0)
        
        return
    
    # Funzione per compiere un'azione
    # Riporta il nuovo nodo se l'azione è compiuta, None se l'azione è invalida
    def applica(self, nodoPrecedente: NodoL) -> NodoL:
        # Controlla che la posizione sia definita
        if matrice.maze_map.get(nodoPrecedente.pos) == None:
            return None
        
        # Controlla che l'azione sia possibile
        if matrice.maze_map[nodoPrecedente.pos][self.id] == True:
            # Crea un nuovo nodo con le nuove coordinate in base all'azione
            pos = (nodoPrecedente.pos[0] + self.maschera[0],
                    nodoPrecedente.pos[1] + self.maschera[1])
            nodoSuccessivo = NodoL(pos, nodoPrecedente)

            # Controlla che il nuovo nodo sia valido
            if nodoSuccessivo.valido():
                # Se valido imposta i parametri dei costi e restituisci il nodo
                nodoSuccessivo.g = nodoPrecedente.g + 1
                nodoSuccessivo.h = nodoSuccessivo.H()
                nodoSuccessivo.f = nodoSuccessivo.g + nodoSuccessivo.h
                return nodoSuccessivo

        # Altrimenti riporta None
        return None

# Classe GiocoLabirinto (estensione della classe Gioco di Astar)
class GiocoL(Gioco):
    # Costruttore
    def __init__(self) -> None:
        # Definizione del nodo iniziale
        self.nodoIniziale = NodoL(PARTENZA)
        
        # Definizione di tutte le azioni possibili
        self.azioniPossibili:list[AzioneL] = []
        self.azioniPossibili.append(AzioneL('N'))
        self.azioniPossibili.append(AzioneL('E'))
        self.azioniPossibili.append(AzioneL('W'))
        self.azioniPossibili.append(AzioneL('S'))

        # Definizione della matrice di gioco
        global matrice
        matrice = maze(RIGHE, COLONNE)
        matrice.CreateMaze()
        
        return

# Funzione main
def main():
    # Crea un'istanza del gioco
    gioco = GiocoL()

    # Richiama l'algoritmo A*
    percorso = gioco.astar_algo()

    # Se è stato restituito un percorso allora stampalo
    if percorso is not None:
        print("Soluzione:", percorso)

        # Converti il percorso nella forma giusta per passarla a tracePath()
        path = {}
        for i in range(1, len(percorso)):
            path[percorso[i-1]] = percorso[i]

        # Rappresentazione grafica del percorso
        a = agent(matrice, footprints=True, filled=False)
        matrice.tracePath({a:path})

        # Configurazione della finestra
        matrice._win.title("Labirinto-Astar PyAmaze X Claziero")
        matrice._win.state("normal")    # Commentare per lo schermo intero
        matrice._win.geometry(f"{COLONNE*98}x{RIGHE*98}+0+0")

        # Carica la finestra
        matrice.run()


main()  # Invocazione del programma principale