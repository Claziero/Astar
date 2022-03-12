from queue import PriorityQueue
import string

#---Elementi utili---#
# Coda di priorità contenente i nodi scoperti non visitati
esplorare = PriorityQueue()
# Coda di priorità contenente i nodi scoperti già visitati
visitati = PriorityQueue()

# Classe Nodo
class Nodo():
    # Costruttore
    def __init__(self, precedente=None) -> None:
        self.g:int = 0                          # Costo del percorso finora sostenuto
        self.h:int = 0                          # Costo stimato per raggiungere il goal
        self.f:int = 0                          # Costo totale del percorso
        self.precedente:Nodo = precedente       # Nodo padre per risalire al percorso

    # Ridefinizione del concetto di uguaglianza tra nodi
    def __eq__(self, altro) -> bool:
        assert(isinstance(altro, Nodo))
        # Inserisci qui
        return None

    # Ridefinizione del concetto di minore tra nodi
    def __lt__(self, altro) -> bool:
        assert(isinstance(altro, Nodo))
        # Inserisci qui
        return None

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

    # Funzione per stampare gli elementi di un nodo
    def formato_stampa(self) -> string:
        # Inserire qui
        return

# Classe Azione
class Azione():
    # Costruttore
    def __init__(self, costo=1, id=None) -> None:
        self.costo = costo  # Costo dell'azione 
        self.id = id        # Azione identificata da un numero, stringa, ...

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
    def __init__(self, ni:Nodo, ap:list[Azione]) -> None:
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
    def astar_algo(self, stampa=False) -> list[list]:
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
            if nodoCorrente.obiettivo():
                print(">>Soluzione trovata")
                # Ricostruisci il percorso dalla fine verso l'inizio
                percorso:list[list[int]] = []
                while nodoCorrente is not None:
                    percorso.append(nodoCorrente.formato_stampa())
                    nodoCorrente = nodoCorrente.precedente

                # Stampa il percorso (se richiesto)
                if stampa: print(">>Sol:", percorso[::-1])
                # Restituisci il percorso inverso (inizio -> fine)
                return percorso[::-1]

            # Altrimenti cerca i nodi adiacenti al nodo corrente
            adiacenti = self.cerca_adiacenti(nodoCorrente)

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

            # Stampa riepilogo delle liste (se richiesto)
            if stampa:
                print(">Lista Esplorare: ", end="||")
                for e in esplorare.queue:
                    e = e[1]
                    print(e.formato_stampa(), end="||")
                print()

                print(">Lista Visitati: ", end="||")
                for e in visitati.queue:
                    print(e.formato_stampa(), end="||")
                print()
                print()

        # Se sei in questo punto, non hai trovato la soluzione
        print(">>Soluzione non trovata.")
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