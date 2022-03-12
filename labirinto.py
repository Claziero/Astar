from Astar import Gioco, Nodo, Azione
import string

# Definizione costanti globali
RIGHE = 4
COLONNE = 4
OBIETTIVO = (3, 4)
PARTENZA = (3, 1)

# Classe NodoLabirinto (estensione della classe Nodo di Astar)
class NodoL(Nodo):
    # Costruttore
    def __init__(self, i, j, precedente=None) -> None:
        super().__init__(precedente)
        self.i = i
        self.j = j

    # Funzione per riportare se un nodo è finale
    def obiettivo(self) -> bool:
        # Il nodo finale è in posizione (3, 4)
        return (self.i, self.j) == OBIETTIVO

    # Funzione per riportare se un nodo è valido
    def valido(self) -> bool:
        # Uno stato è valido se la posizione è libera e non c'è un muro
        # e se la posizione rientra nei confini della mappa
        return 1 <= self.i <= RIGHE and 1 <= self.j <= COLONNE\
            and matrice[self.i-1][self.j-1] != 1

    # Funzione euristica
    def H(self) -> int:
        # Riporta la distanza euclidea tra il nodo e l'obiettivo
        return (OBIETTIVO[0] - self.i)**2 + (OBIETTIVO[1] - self.j)**2

    # Ridefinizione del concetto di uguaglianza tra nodi
    def __eq__(self, altro) -> bool:
        # Due nodi sono uguali se hanno la stessa posizione
        return self.i == altro.i and self.j == altro.j

    # Funzione per stampare le informazioni del nodo
    # Nodo nel formato (i, j), cioè la posizione del nodo nel labirinto
    def formato_stampa(self) -> string:
        return "(" + str(self.i) + "," + str(self.j) + ")"

# Classe AzioneLabirinto (estensione della classe Azione di Astar)
class AzioneL(Azione):
    # Costruttore
    def __init__(self, id=None) -> None:
        # Azioni possibili:
        # 1 = UP        (i-1, j)    costo = 1
        # 2 = DIAG.NE   (i-1, j+1)  costo = 2
        # 3 = FORWARD   (i, j+1)    costo = 1
        # 4 = DIAG.SE   (i+1, j+1)  costo = 2
        # 5 = DOWN      (i+1, j)    costo = 2
        
        if id == 1:
            self.costo = 1
            self.maschera = (-1, 0)
        elif id == 2:
            self.costo = 2
            self.maschera = (-1, +1)
        elif id == 3:
            self.costo = 1
            self.maschera = (0, +1)
        elif id == 4:
            self.costo = 2
            self.maschera = (+1, +1)
        elif id == 5:
            self.costo = 2
            self.maschera = (+1, 0)
        
        return
    
    # Funzione per compiere un'azione
    # Riporta il nuovo nodo se l'azione è compiuta, None se l'azione è invalida
    def applica(self, nodoPrecedente: NodoL) -> NodoL:
        # Crea un nuovo nodo con le nuove coordinate in base all'azione
        nodoSuccessivo = NodoL(nodoPrecedente.i + self.maschera[0],
                                nodoPrecedente.j + self.maschera[1], nodoPrecedente)

        # Controlla che il nuovo nodo sia valido
        if nodoSuccessivo.valido():
            # Se valido imposta i parametri dei costi e restituisci il nodo
            nodoSuccessivo.g = nodoPrecedente.g + self.costo
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
        self.nodoIniziale = NodoL(PARTENZA[0], PARTENZA[1])
        
        # Definizione di tutte le azioni possibili
        self.azioniPossibili:list[AzioneL] = []
        self.azioniPossibili.append(AzioneL(1))
        self.azioniPossibili.append(AzioneL(2))
        self.azioniPossibili.append(AzioneL(3))
        self.azioniPossibili.append(AzioneL(4))
        self.azioniPossibili.append(AzioneL(5))

        # Definizione della matrice di gioco
        global matrice
        matrice = [ [0, 0, 1, 0],
                    [0, 1, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 0] ]
        
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


main()  # Invocazione del programma principale