from queue import PriorityQueue

#---Elementi utili---#
# Coda di priorità contenente i nodi scoperti non visitati
esplorare = PriorityQueue()
# Coda di priorità contenente i nodi scoperti già visitati
visitati = PriorityQueue()

# Classe Nodo
class Nodo():
    # Costruttore
    def __init__(self, pos=None, precedente=None, tempo=0) -> None:
        self.g:int = 0                          # Costo del percorso finora sostenuto
        self.h:int = 0                          # Costo stimato per raggiungere il goal
        self.f:int = 0                          # Costo totale del percorso
        self.posizione:list[int] = pos          # Posizione nel formato (x, y)
        self.precedente:Nodo = precedente       # Nodo padre per risalire al percorso
        self.tempo:int = tempo                  # Tempo di generazione del nodo (0..15)

    # Ridefinizione del concetto di uguaglianza tra nodi: 
    # devono essere nella stessa posizione allo stesso tempo
    def __eq__(self, altro) -> bool:
        assert(isinstance(altro, Nodo))
        return self.posizione == altro.posizione and self.tempo == altro.tempo

    # Ridefinizione del concetto di minore tra nodi: 
    # il più piccolo deve avere una f minore
    def __lt__(self, altro) -> bool:
        assert(isinstance(altro, Nodo))
        return self.f < altro.f

    # Funzione per definire uno stato obiettivo
    def obiettivo(self) -> bool:
        # Inserire qui
        return None  

    # Funzione per definire la validità di un nodo
    def valido(self) -> bool:
        # Inserire qui
        return None

    # Funzione euristica: restituisce una stima dei passi 
    # da compiere per arrivare all'obiettivo
    def H(self) -> int:
        # Inserire qui
        return None

# Classe Azione
class Azione():
    # Costruttore
    def __init__(self, c=0, id=None) -> None:
        self.costo = c  # Costo dell'azione 
        self.id = id    # Azione identificata da un numero, stringa, ...

    # Funzione per compiere un'azione
    # Riporta il nuovo nodo se l'azione è compiuta, None se l'azione è invalida
    def applica(self, nodoPrecedente:Nodo) -> Nodo:
        # Inserire qui
        # Usare con Nodo.valido() per verificare la validità del nuovo nodo generato
        # Impostare i campi f, g, h del nodo generato (valido)
        return None

# Classe gioco
class Gioco():
    # Costruttore
    def __init__(self, m:list[list], ni:Nodo, ap:list[Azione]) -> None:
        self.matrice:list[list] = m
        self.nodoIniziale:Nodo = ni
        self.azioniPossibili:list[Azione] = ap

    # Funzione per trovare i nodi adiacenti al nodo passato come parametro
    # Restituisce una lista di nodi
    def cerca_adiacenti(self, nodoCorrente:Nodo) -> list[Nodo]:
        adiacenti:list[Nodo] = []

        # Per ogni azione disponibile
        for azione in self.azioniPossibili:
            # Prova ad applicare l'azione
            nuovoNodo = azione.applica(nodoCorrente)
            
            # Se l'azione non porta alla perdita, aggiungi il nuovo nodo alla lista dei nodi adiacenti
            if nuovoNodo is not None:
                adiacenti.append(nuovoNodo)

        return adiacenti

    # Implementazione di A*
    # Restituisce una lista di posizioni nella mappa dalla partenza all'obiettivo
    # oppure None se non c'è soluzione al problema
    def astar_algo(self) -> list[list[int]]:
        # Aggiungi il nodo iniziale alla coda esplorare, con costo 0
        esplorare.put((0, self.nodoIniziale))

        #---Inizia l'esplorazione---#
        # Finché la lista di nodi da esplorare non è vuota 
        while len(esplorare.queue) != 0:
            # Estrai il primo elemento (a costo f minimo)
            nodoCorrente = esplorare.get()[1]
            # E inseriscilo nella lista di nodi visitati
            visitati.put(nodoCorrente) 

            # Se il nodo corrente corrisponde all'obiettivo allora riporta il percorso fatto
            if NodoCorrente.obiettivo():
                print("Soluzione trovata")
                # Ricostruisci il percorso dalla fine verso l'inizio
                percorso:list[list[int]] = []
                while NodoCorrente is not None:
                    percorso.append(NodoCorrente.posizione)
                    NodoCorrente = NodoCorrente.precedente

                # Restituisci il percorso inverso (inizio -> fine)
                print(percorso[::-1])
                return percorso[::-1]

            # Altrimenti cerca i nodi adiacenti al nodo corrente
            adiacenti = self.cerca_adiacenti(NodoCorrente)

            # Per ogni nodo adiacente trovato
            for n in adiacenti:
                # Se il nodo è già stato visitato non fare nulla
                if cerca_nodo(visitati, n) is not None:
                    continue

                # Controlla che il nodo da aggiungere (n) non sia già in esplorare
                presente = cerca_nodo(esplorare, n)
                if presente is not None:
                    # Se c'è controlla che non abbia valore di G maggiore o uguale di quello già presente
                    if n.g >= presente.g:
                        # Scarta il nodo
                        continue

                # Altrimenti aggiungi il nodo alla lista da esplorare
                esplorare.put((n.f, n))

                #---Torna ad esplorare i nodi adiacenti al corrente---#
            #---Esplora nuovi nodi, se ci sono---#

        # Se sei in questo punto, non hai trovato la soluzione
        print("Soluzione non trovata.")
        return None

# Funzione ausiliaria per cercare un nodo all'interno di una lista
# Restituisce il nodo trovato oppure None
def cerca_nodo(lista:PriorityQueue, nodo:Nodo) -> Nodo:
    # Se la lista è vuota ritorna subito
    if len(lista.queue) == 0:
        return False

    # Scorri tutti gli elementi
    for n in lista.queue:
        # Se non è un nodo allora è una tupla contenente il nodo
        if not isinstance(n, Nodo): 
            n = n[1]
        # Se trovi il nodo riportalo
        if nodo == n: 
            return n
    
    # Il nodo non è stato trovato
    return None