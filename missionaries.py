import string
from Astar import Nodo, Gioco, Azione

MAX_CAPACITA_BARCA = 2
NUM_MISSIONARI = 3
NUM_CANNIBALI = 3

# Classe NodoMissionari (estensione della classe Nodo di Astar)
class NodoM(Nodo):
    # Costruttore
    def __init__(self, ma, ca, mb, cb, b, precedente=None) -> None:
        super().__init__(precedente)
        self.ma:int = ma
        self.ca:int = ca
        self.mb:int = mb
        self.cb:int = cb
        self.b:string = b

    # Funzione per riportare se un nodo è finale
    def obiettivo(self) -> bool:
        return self.ca == 0 and self.cb == NUM_CANNIBALI\
            and self.ma == 0 and self.mb == NUM_MISSIONARI

    # Funzione per riportare se un nodo è valido
    def valido(self) -> bool:
        # Uno stato è valido se il totale dei cannibali e dei missionari è sempre 3
        if self.ca + self.cb == NUM_CANNIBALI and self.ma + self.mb == NUM_MISSIONARI:
            # Inoltre devono esserci in ogni momento tra 0 e 3 cannibali su ogni sponda del fiume
            if 0 <= self.ca <= NUM_CANNIBALI and 0 <= self.cb <= NUM_CANNIBALI:
                # Lo stesso deve valere per i missionari
                if 0 <= self.ma <= NUM_MISSIONARI and 0 <= self.mb <= NUM_MISSIONARI:
                    # E su ogni sponda devono esserci più missionari che cannibali
                    if self.ma >= self.ca or self.ma == 0:
                        if self.mb >= self.cb or self.mb == 0:
                            return True
        # Altrimenti è uno stato invalido
        return False

    # Funzione euristica
    def H(self) -> int:
        return self.ma + self.ca

    # Ridefinizione del concetto di uguaglianza tra nodi
    def __eq__(self, altro) -> bool:
        return self.ca == altro.ca and self.cb == altro.cb and self.ma == altro.ma\
            and self.mb == altro.mb and self.b == altro.b

    # Funzione per stampare le informazioni del nodo
    # Nodo nel formato (Ma, Ca, Mb, Cb, Barca)
    def formato_stampa(self) -> string:
        return "(" + str(self.ma) + "," + str(self.ca) + "," + str(self.mb) + "," + str(self.cb) + "," + str(self.b) + ")"

# Classe AzioneMissionari (estensione della classe Azione di Astar)
class AzioneM(Azione):
    # Costruttore
    def __init__(self, costo=1, id=None, c=0, m=0) -> None:
        self.c = c      # Numero di cannibali da trasportare
        self.m = m      # Numero di missionari da trasportare
        super().__init__(costo, id)
    
    # Funzione per compiere un'azione
    # Riporta il nuovo nodo se l'azione è compiuta, None se l'azione è invalida
    def applica(self, nodoPrecedente: NodoM) -> NodoM:
        # Distingui le azioni tra carry e carryback
        if self.id == 'carry':
            # Controlla che i valori di c ed m siano corretti
            if self.c + self.m > MAX_CAPACITA_BARCA:
                return None     # Azione impossibile

            # Controlla che la barca sia sul lato giusto per applicare l'azione
            if nodoPrecedente.b != 'A':
                return None     # Azione impossibile

            # Genera un nuovo nodo
            ca = nodoPrecedente.ca - self.c
            ma = nodoPrecedente.ma - self.m
            cb = nodoPrecedente.cb + self.c
            mb = nodoPrecedente.mb + self.m
            b = 'B'

            nodoSuccessivo = NodoM(ca, ma, cb, mb, b, nodoPrecedente)
            nodoSuccessivo.g = nodoPrecedente.g + self.costo
            nodoSuccessivo.h = nodoSuccessivo.H()
            nodoSuccessivo.f = nodoSuccessivo.g + nodoSuccessivo.h
            
            # Controlla che il nodo sia valido
            if nodoSuccessivo.valido():
                # Riporta il nuovo nodo
                return nodoSuccessivo
            
            # Altrimenti riporta None
            return None

        elif self.id == 'carryback':
            # Controlla che i valori di c ed m siano corretti
            if self.c + self.m > MAX_CAPACITA_BARCA:
                return None     # Azione impossibile

            # Controlla che la barca sia sul lato giusto per applicare l'azione
            if nodoPrecedente.b != 'B':
                return None     # Azione impossibile

            # Genera un nuovo nodo
            ca = nodoPrecedente.ca + self.c
            ma = nodoPrecedente.ma + self.m
            cb = nodoPrecedente.cb - self.c
            mb = nodoPrecedente.mb - self.m
            b = 'A'

            nodoSuccessivo = NodoM(ca, ma, cb, mb, b, nodoPrecedente)
            nodoSuccessivo.g = nodoPrecedente.g + self.costo
            nodoSuccessivo.h = nodoSuccessivo.H()
            nodoSuccessivo.f = nodoSuccessivo.g + nodoSuccessivo.h
            
            # Controlla che il nodo sia valido
            if nodoSuccessivo.valido():
                # Riporta il nuovo nodo
                return nodoSuccessivo

            # Altrimenti riporta None
            return None

# Classe GiocoMissionari (estensione della classe Gioco di Astar)
class GiocoM(Gioco):
    # Costruttore
    def __init__(self) -> None:
        # Definizione del nodo iniziale
        self.nodoIniziale = NodoM(NUM_MISSIONARI, NUM_CANNIBALI, 0, 0, 'A')
        
        # Definizione di tutte le azioni possibili
        self.azioniPossibili:list[AzioneM] = []
        self.azioniPossibili.append(AzioneM(1, 'carry', 2, 0))
        self.azioniPossibili.append(AzioneM(1, 'carry', 0, 2))
        self.azioniPossibili.append(AzioneM(1, 'carry', 1, 1))
        self.azioniPossibili.append(AzioneM(1, 'carry', 1, 0))
        self.azioniPossibili.append(AzioneM(1, 'carry', 0, 1))
        self.azioniPossibili.append(AzioneM(1, 'carryback', 2, 0))
        self.azioniPossibili.append(AzioneM(1, 'carryback', 0, 2))
        self.azioniPossibili.append(AzioneM(1, 'carryback', 1, 1))
        self.azioniPossibili.append(AzioneM(1, 'carryback', 1, 0))
        self.azioniPossibili.append(AzioneM(1, 'carryback', 0, 1))
        
        return

# Funzione main
def main():
    # Crea un'istanza del gioco
    gioco = GiocoM()

    # Richiama l'algoritmo A*
    percorso = gioco.astar_algo()

    # Se è stato restituito un percorso allora stampalo
    if percorso is not None:
        print("Soluzione:", percorso)


main()  # Invocazione del programma principale