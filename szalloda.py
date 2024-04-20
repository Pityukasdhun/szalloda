from datetime import datetime


class Szoba:
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam
        self.foglalasok = []

    def foglalas_hozzaad(self, foglalas):
        self.foglalasok.append(foglalas)

    def foglalas_lemondas(self, foglalas):
        if foglalas in self.foglalasok:
            self.foglalasok.remove(foglalas)
            return True
        else:
            return False

    def ellenoriz_idopont(self, datum):
        for foglalas in self.foglalasok:
            if foglalas.datum == datum:
                return False
        return True


class Foglalás:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum


class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam, kilatas=False):
        super().__init__(ar=50 if not kilatas else 100, szobaszam=szobaszam)


class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam, tengeri_nepeszet=False):
        super().__init__(ar=80 if not tengeri_nepeszet else 120, szobaszam=szobaszam)


class Szalloda:
    def __init__(self, nev, szobak):
        self.nev = nev
        self.szobak = szobak

    def foglalas(self, szobaszam, datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                if szoba.ellenoriz_idopont(datum):
                    foglalas = Foglalás(szoba, datum)
                    szoba.foglalas_hozzaad(foglalas)
                    return foglalas
                else:
                    return None
        return None

    def foglalas_lemondas(self, foglalas):
        for szoba in self.szobak:
            if foglalas in szoba.foglalasok:
                szoba.foglalas_lemondas(foglalas)
                return True
        return False

    def listaz_foglalasok(self):
        for szoba in self.szobak:
            for foglalas in szoba.foglalasok:
                print(f"Szoba: {szoba.szobaszam}, Dátum: {foglalas.datum.strftime('%Y-%m-%d')}")


def main():
    szoba1 = EgyagyasSzoba(101)
    szoba2 = KetagyasSzoba(201)
    szoba3 = EgyagyasSzoba(102)
    szoba4 = KetagyasSzoba(202)
    szoba5 = EgyagyasSzoba(103)

    szobak = [szoba1, szoba2, szoba3, szoba4, szoba5]

    szalloda = Szalloda("Példa Szálloda", szobak)

    # Feltöltés 5 foglalással
    szalloda.foglalas(101, datetime(2024, 4, 20))
    szalloda.foglalas(201, datetime(2024, 4, 22))
    szalloda.foglalas(102, datetime(2024, 4, 24))
    szalloda.foglalas(202, datetime(2024, 4, 26))
    szalloda.foglalas(103, datetime(2024, 4, 28))

    while True:
        print("\nVálasszon műveletet:")
        print("1. Foglalás")
        print("2. Lemondás")
        print("3. Foglalások listázása")
        print("4. Kilépés")

        valasztas = input("Adja meg a kívánt művelet számát: ")

        if valasztas == "1":
            szobaszam = int(input("Adja meg a foglalni kívánt szoba számát: "))
            datum_str = input("Adja meg a foglalás dátumát (YYYY-MM-DD formátumban): ")
            try:
                datum = datetime.strptime(datum_str, "%Y-%m-%d")
                if datum.date() >= datetime.now().date():
                    foglalas = szalloda.foglalas(szobaszam, datum)
                    if foglalas:
                        print("Sikeres foglalás!")
                    else:
                        print("Hiba: A megadott időpontban a szoba már foglalt.")
                else:
                    print("Hiba: A megadott dátum nem lehet múltbeli.")
            except ValueError:
                print("Hiba: Helytelen dátumformátum.")
        elif valasztas == "2":
            print("Jelenleg foglalt szobák:")
            szalloda.listaz_foglalasok()
            if any(szoba.foglalasok for szoba in szalloda.szobak):
                index = int(input("Adja meg a lemondani kívánt foglalás sorszámát: "))
                if 1 <= index <= len(szalloda.szobak):
                    szoba = szalloda.szobak[index - 1]
                    if szoba.foglalasok:
                        index2 = int(input("Adja meg a lemondani kívánt foglalás sorszámát: "))
                        if 1 <= index2 <= len(szoba.foglalasok):
                            foglalas = szoba.foglalasok[index2 - 1]
                            if szalloda.foglalas_lemondas(foglalas):
                                print("A foglalás sikeresen lemondva.")
                            else:
                                print("Hiba: Nem létező foglalás sorszám.")
                        else:
                            print("Hiba: Nem létező foglalás sorszám.")
                    else:
                        print("A kiválasztott szobára nincs foglalás.")
                else:
                    print("Hiba: Nem létező szoba sorszám.")
            else:
                print("Nincsenek foglalások.")
        elif valasztas == "3":
            print("Jelenleg foglalt szobák:")
            szalloda.listaz_foglalasok()
        elif valasztas == "4":
            print("Kilépés...")
            break
        else:
            print("Hiba: Érvénytelen választás. Kérjük, válasszon újra.")


if __name__ == "__main__":
    main()
