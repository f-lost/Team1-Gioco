'''obbiettivo: gestionale ad oggetti ripetibile che fa:

1) registrazione/login/salvataggio_dei_dati/esci

2)funzionalità, a chi ha fatto login associa un punteggio

questo punteggio ci dice a quante funzionalità può accedere
0 punti -> 1 funzionalità, 1 punto -> 2 funzionalità (base/facile) ecc ecc

MASSIMO 10 funzionalità (livelli di difficoltà)

classifica salvata
'''

from abc import ABC, abstractmethod
import pprint, random, time

class Menù:
    def init(self):
        self.registrato = False
        self.utenti_registrati = {}
        self.opzioni = {
            "1 -": "Registrati come nuovo utente",
            "2 -": "Inizia il gioco",
            "3 -": "Visualizza classifica",
            "4 -": "Guida ai giochi",
            "5 -": "Impostazioni profilo",
            "6 -": "Visualizza record personali",
            "7 -": "Esci"
            }

    def mostra_menù(self):
        print("\ Menù Principale /")
        for key, value in self.opzioni.items():
            if key == "2" and not self.registrato:
                continue
        print(f"{key} {value}")

    def scegli_opzione(self):
        scelta = input("Scegli un'opzione dal Menù")
        if scelta == "1":
            self.registra_utente()
        elif scelta == "2" and not self.registrato:
            print("Devi registrarti prima di iniziare il gioco")
            return None
        return scelta

    def registrazione_utente(self):
        print("Registrazione in corso...")
        time.sleep(2)

        while True:
            username = input("Scegli il tuo username: ").lower()
            if not username:
                print("Devi necessariamente inserire un username. Riprova.")
            elif username in self.utenti_registrati:
                print("Questo username è già presente, scegline un altro.")
            else:
                break

        punchline = input("Scegli un tuo motto personale: ").lower()
        if not punchline:
            punchline = "Non hai inserito nessun motto, peccato."

        print("Salvataggio delle informazioni")
        time.sleep(2)

        self.utenti_registrati[username] = punchline
        self.registrato = True

        print("Registrazione completata")
        time.sleep(1)
        print(f"Benvenuto giocatore {username}, il tuo motto è: {punchline}, ti auguro buona fortuna!")


class Utente:

    def __init__(self, nome):

        self.__nome = nome
        self.__punteggio = 0
        self.__alias = ""

    def get_nome(self):

        return self.__nome
    
    def get_alias(self):

        return self.__alias
    
    def __set_alias(self, alias):

        self.__alias = alias

    def nome_utente(self):

        alias = input("Inserisci uno username: ")

        self.__set_alias(alias)


    def get_punteggio(self):

        return self.__punteggio
    
    def __set_punteggio(self, punti):

        self.__punteggio += punti

    
    def aggiungi_punti(self, punti):

        self.__set_punteggio(punti)
    
    def stampa_punteggio(self):

        print(self.__get_punteggio())


class Classifica:


    def __init__(self):

        self.__classifica = {}

    def __get_classifica(self):

        return self.__classifica
    
    def __set_classifica(self, utente, valore):

        if utente in self.__classifica:

            self.__classifica[utente.get_nome()].append(valore)

        else:

            print("Ora sei in classifica!")
            self.__classifica[utente.get_nome()] = [valore]
        
    def aggiungi_a_classifica(self, utente, valore):

        self.__set_classifica(utente, valore)

    def stampa_classifica(self):

        pprint.pprint(self.__get_classifica())

    def salva_classifica(self):

        pass



class Gioco(ABC):

    def init(self, nome):
        self.nome = nome

    @abstractmethod
    def calcola_punteggio(self):
        pass
 

class IndovinaIlNumero(Gioco):

    def init(self):
        super().init("Indovina il Numero")

    def start(self, utente):
        numero_segreto = random.randint(1, 100)
        tentativi = 0
        print("Benvenuto a 'Indovina il Numero'!")
        while True:
            tentativo = int(input("Indovina il numero (1-100): "))
            tentativi += 1
            if tentativo < numero_segreto:
                print("Troppo basso!")
            elif tentativo > numero_segreto:
                print("Troppo alto!")
            else:
                print(f"Complimenti! Hai indovinato il numero in {tentativi} tentativi.")

                self.calcola_punteggio(tentativi, utente)

                break

    def calcola_punteggio(self, tentativi, utente):

        if tentativi <= 5:

            utente.aggiungi_punti(100)
            print("ECCEZIONALE! 100 punti per te!")

        elif 5 < tentativi <= 10:

            utente.aggiungi_punti(50)
            print("BRAVISSIMO! 50 punti per te!")

        elif 10 < tentativi <=20:

            utente.aggiungi_punti(25)
            print("Bravo! 25 punti per te!")

        else:

            utente.aggiungi_punti(5)
            print("Potevi fare di meglio... 5 punti per te!")


class IndovinaEquazioni(Gioco):


    def init(self):
        super().init("Indovina equazioni")

    def start(self, nome_utente):
        print(f"Ciao {nome_utente}! In questo gioco dovrai risolvere un'equazione di primo grado. Se il risultato è con la virgola approssima alle prime due cifre significative! FAI VELOCE!")

        a = 0
        while a == 0:
            a = random.randint(-10,10)

        b = random.randint(-100, 100)

        print(f"Risolvi l'equazione {a}x + {b} = 0 \n")

        sol = round(-b/a, 2)

        while True:
            t1 = time.time()
            #print(sol)
            x = float(input("Qual è la tua soluzione? "))
            x=round(x, 2)

            punteggio = time.time() - t1
            punteggio = round(punteggio, 3)
            if x  == sol:
                print(nome_utente, "ci hai messo ", punteggio, " secondi per completarlo!")
                break
            else:
                print("Ritenta!")

        return punteggio


class Saltacavallo(Gioco):
    def __init__(self):
        super().__init__("Saltacavallo")
        self.giocatori = []
        self.vite = []
    # distribuisci_carte: Questo metodo crea un mazzo di carte 
    # (numeri da 2 a 13, dove 11 è il Fante, 12 è il Cavallo e 13 è il Re) e lo mescola. 
    # Distribuisce una carta a ciascun giocatore.
    def distribuisci_carte(self):
        mazzo = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] * 4  # 
        random.shuffle(mazzo)
        return [mazzo.pop() for _ in range(len(self.giocatori))]
#     start: Questo metodo gestisce il flusso del gioco. Chiede il numero di giocatori, 
# inizializza le vite e distribuisce le carte. 
# Ogni giocatore esegue azioni basate sul valore della carta ricevuta:

# Carte da 2 a 7: Nessuna azione.

# Cavallo (11): Dona una vita al secondo giocatore alla destra.

# Fante (12): Dona una vita al giocatore alla sinistra.

# Re (13): Aggiunge una vita al giocatore.

# Asso (1): Perde una vita.


    def start(self):

        num_giocatori = int(input("Quanti giocatori partecipano? "))
        self.giocatori = list(range(1, num_giocatori + 1))
        self.vite = [2] * num_giocatori  # Ogni giocatore inizia con 2 vite

        while len(self.giocatori) > 1:
            carte = self.distribuisci_carte()
            print("\nCarte distribuite:")
            for i, carta in enumerate(carte):
                print(f"Giocatore {self.giocatori[i]} ha ricevuto una carta di valore {carta}")
             # Carte da 2 a 7: Nessuna azione.
            for i, carta in enumerate(carte):
                if 2 <= carta <= 7:
                    continue
               
                # Cavallo (11): Dona una vita al secondo giocatore alla destra.
                elif carta == 11:  # Cavallo
                    destinatario = (i - 2) % len(self.giocatori)
                    self.vite[destinatario] += 1
                    self.vite[i] -= 1
                    # Fante (12): Dona una vita al giocatore alla sinistra.
                elif carta == 12:  # Fante
                    # (i - 2) % len(self.giocatori): Questo calcolo determina
                    # l'indice del secondo giocatore alla destra del giocatore corrente. 
                    # L'operatore % (modulo) assicura che l'indice rimanga 
                    # all'interno dei limiti della lista, gestendo correttamente i casi in cui i - 2 risulti negativo.
                    destinatario = (i + 1) % len(self.giocatori)
                    self.vite[destinatario] += 1
                    self.vite[i] -= 1
                    # Re (13): Aggiunge una vita al giocatore.
                elif carta == 13:  # Re
                    self.vite[i] += 1
                    # Asso (1): Perde una vita.
                elif carta == 1:  # Asso
                    self.vite[i] -= 1
            #zip(self.giocatori, self.vite): Combina le liste self.giocatori e self.vite in coppie (giocatore, vite).

             # [g for g, v in zip(self.giocatori, self.vite) if v > 0]: Crea una nuova lista di giocatori (g) che hanno ancora vite (v > 0). 
             # In altre parole, rimuove i giocatori che non hanno più vite.
            self.giocatori = [g for g, v in zip(self.giocatori, self.vite) if v > 0]
            self.vite = [v for v in self.vite if v > 0]

            print("\nStato delle vite:")
            for i, vite in enumerate(self.vite):
                print(f"Giocatore {self.giocatori[i]} ha {vite} vite")

        print(f"\nIl vincitore è il Giocatore {self.giocatori[0]}!")


class SassoCartaForbici(Gioco):

    def __init__(self):
        
        super().__init__("Sasso, Carta o Forbici")
    
    def start(self, utente):

        possibili_scelte_pc = {"Sasso", "Carta", "Forbici"}
        print("Benvenuto a 'Sasso, Carta o Forbici'!")

        while True:

            scelta_casuale_pc = random.choice(possibili_scelte_pc)
            scelta_utente = input("Cosa vuoi fare? Sasso, Carta o Forbice?:  ").lower()

            pass







#Esempio di utilizzo
gioco1 = IndovinaIlNumero()
utente = Utente("stefano")
classifica = Classifica()
gioco1.start(utente)




        
