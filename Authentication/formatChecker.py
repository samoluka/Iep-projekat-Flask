# Sva polja su obavezna i njihov sadržaj je sledeći:
#  jmbg: string dužine 13 karaktera koji predstavlja jedinstveni matični broj
# građanina formata DDMMYYYRRBBBK, delovi stringa su sledeći:
# o DD – dan rođenja, vrednost iz opsega [1, 31];
# o MM – mesec rođenja, vrednost iz opsega [1, 12];
# o YYY – poslednje tri cifre godine rođenja, vrednost iz opsega [000, 999];
# o RR – region u kom je rođen korisnik, za Srbiju vrednost iz opsega [70,
# 99];
# o BBB – jedinstveni broj koji predstavlja osobu iz navedenog regiona, za
# muškarce je vrednost iz opsega [0, 499], za žene je vrednost iz opsega
# [500, 999]; o K – kontrolna cifra koja se računa prema sledećoj formuli;
#  forename: string od najviše 256 karaktera koji predstavlja ime korisnika;
#  surname: string od najviše 256 karaktera koji predstavlja prezime korisnika;
#  email: string od najviše 256 karaktera koji predstavlja email adresu korisnika;
#  password: string od najviše 256 karaktera koji predstavlja lozinku korisnika,
# dužina lozinke mora biti 8 ili više znakova, lozinka mora sadržati bar jednu
# cifru, jednom malo slovo i jedno veliko slovo;
# Odgovor Ukoliko su svi traženi podaci prisutni u telu zahteva i ispunjavaju navedena
# ograničenja, rezultat zahteva je kreiranje novog korisnika sa ulogom zvaničnika i
# odgovor sa statusnim kodom 200 bez dodatno sadržaja.

# U slučaju greške, rezultat zahteva je odgovor sa statusnim kodom 400 čiji je sadržaj
# JSON objekat sledećeg formata:
# {
# "message": "....."
# }
# Sadržaj polja message je:
#  “Field <fieldname> is missing.” ukoliko neko od polja nije prisutno
# ili je vrednost polja string dužine 0, <fieldname> je ime polja koje je
# očekivano u telo zahteva;
#  “Invalid jmbg.” ukoliko polje jmbg nije odgovarajućeg formata;
#  “Invalid email.” ukoliko polje email nije odgovarajuće formata;
#  “Invalid password.” ukoliko polje password nije odgovarajućeg
# formata;
#  “Email already exists.” ukoliko u bazi postoji korisnik sa istom email
# adresom;
# Odgovarajuće provere se vrše u navedenom redosledu.
import re
from email.utils import parseaddr


class FormatChecker:
    def __init__(self, jmbg, email, forename, surname, password):
        self.jmbg = jmbg
        self.email = email
        self.forename = forename
        self.surname = surname
        self.password = password

    def checkEmpty(self):
        ret = ""
        if (len(self.jmbg) == 0):
            ret += "Field jmbg is missing. "
        if (len(self.email) == 0):
            ret += "Field email is missing. "
        if (len(self.password) == 0):
            ret += "Field password is missing. "
        if (len(self.forename) == 0):
            ret += "Field forename is missing. "
        if (len(self.surname) == 0):
            ret += "Field surname is missing. "
        ret = ret if ret == "" else ret[:-1]
        return ret;

    def checkJmbg(self):
        error = "Invalid jmbg."
        if (len(self.jmbg) != 13):
            return error
        if (self.jmbg.isdecimal() == False):
            return error
        if (int(self.jmbg[0:2]) < 1 or int(self.jmbg[0:2]) > 31):
            return error
        if (int(self.jmbg[2:4]) < 1 or int(self.jmbg[2:4]) > 12):
            return error
        if (int(self.jmbg[4:7]) < 0 or int(self.jmbg[4:7]) > 999):
            return error
        if (int(self.jmbg[7:9]) < 70 or int(self.jmbg[7:9]) > 99):
            return error
        if (int(self.jmbg[9:12]) < 0 or int(self.jmbg[9:12]) > 999):
            return error
        return ""
    def checkEmail(self):
        result = parseaddr(self.email);
        if (len(result[1]) == 0):
            return "Invalid email"
        return ""
    def checkPassword(self):
        if (len(self.password)<8):
            return "Invalid password"
        if (bool(re.search('[0-9]+', self.password)) == False):
            return "Invalid password"
        if (bool(re.search('[a-z]+', self.password)) == False):
            return "Invalid password"
        if (bool(re.search('[A-Z]+', self.password)) == False):
            return "Invalid password"
        return ""