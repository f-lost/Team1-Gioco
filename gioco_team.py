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





#Esempio di utilizzo
gioco1 = IndovinaIlNumero()
utente = Utente("stefano")
classifica = Classifica()
gioco1.start(utente)




        
