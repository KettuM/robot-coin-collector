import pygame
import random
    
class Kolikkojahti:
    def __init__(self):
        pygame.init()
        
        self.lataa_kuvat()
        self.uusi_peli()
        
        self.leveys = 640
        self.korkeus = 480
        
        robo = pygame.image.load("robo.png")
        self.robon_leveys = robo.get_width()
        self.robon_korkeus = robo.get_height()
    
        self.naytto = pygame.display.set_mode((self.leveys, self.korkeus))
        self.fontti = pygame.font.SysFont("Calibri", 24)
        self.color = (0, 5, 50)
    
        self.loppu = False
    
        pygame.display.set_caption("Kolikkojahti")
        
        self.silmukka()
    
    
    def lataa_kuvat(self): #lataa kuvat peliin
        self.kuvat = []
        for nimi in ["hirvio", "kolikko", "robo"]:
            self.kuvat.append(pygame.image.load(nimi + ".png"))
    
    
    def hirviot(self): #arpoo koordinaatit x- ja y-akseleilta tuleville hirviöille
        self.vaaka_koordinaatit = []
        self.pysty_koordinaatit = []
        for i in range(3):
            self.vaaka_hirvio_x = random.randint(10, 600)
            self.vaaka_hirvio_y = -30 - random.randint(0, 150)
            self.pysty_hirvio_x = -30 - random.randint(0, 150)
            self.pysty_hirvio_y = random.randint(10, 460)
            self.vaaka_koordinaatit.append([self.vaaka_hirvio_x, self.vaaka_hirvio_y])
            self.pysty_koordinaatit.append([self.pysty_hirvio_x, self.pysty_hirvio_y])
    
    
    def kolikot(self): #arpoo koordinaatit napattavalle kolikolle
        self.rahan_leveys = self.kuvat[1].get_width()
        self.rahan_korkeus = self.kuvat[1].get_height()
        
        self.raha_x = random.randint(0, self.leveys - self.rahan_leveys)
        self.raha_y = random.randint(0, self.korkeus - self.rahan_korkeus)
        self.rahat.append([self.raha_x, self.raha_y])
        
    
    def uusi_peli(self): #aloitustilanne
        self.tulos = 0
        self.robo_x = 315 
        self.robo_y = 200 
        self.rahat = []
        self.oikealle = False
        self.vasemmalle = False
        self.ylos = False
        self.alas = False
        self.hirviot()
        self.loppu = False
    
    
    def silmukka(self): #pelilooppi
        kello = pygame.time.Clock()
        while True:
            self.tutki_tapahtumat()
            if self.loppu == False:
                self.piirra_naytto()
    
            kello.tick(60)
    
    
    def tutki_tapahtumat(self): #määrittää näppäimet robotin liikkumiselle sekä F2- ja ESC-näppäinten tapahtumat
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_r:
                    self.uusi_peli()
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = True
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = True  
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = True   
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = True
    
            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = False
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = False
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = False
                    
            if tapahtuma.type == pygame.QUIT:
                exit()
    
        if self.vasemmalle:
            if self.robo_x > 0:
                self.liiku(0, -2)
        
        if self.oikealle:
            if self.robo_x + self.robon_leveys < self.leveys:
                self.liiku(0, 2)
        
        if self.ylos:
            if self.robo_y > 0:
                self.liiku(-2, 0)
    
        if self.alas:
            if self.robo_y + self.robon_korkeus < self.korkeus:
                self.liiku(2, 0)
        
    
    def piirra_naytto(self):
        pisteet = self.fontti.render(f"Pisteet: {self.tulos}", True, (255, 0, 0)) 
        
        self.naytto.fill(self.color)
    
        if len(self.rahat) == 0:            #kolikkolistan läpikäynti
            self.kolikot()
        for i in range(len(self.rahat)):
            self.naytto.blit(self.kuvat[1], (self.rahat[i][0], self.rahat[i][1])) #piirtää kolikon listalla oleviin koordinaatteihin
            luku = i
            self.rahan_nappaus(luku) #tarkistaa onko robotti rahan kohdalla
        
        robo = self.kuvat[2]
        self.naytto.blit(robo, (self.robo_x, self.robo_y)) #piirtää robotin näytölle
    
        self.naytto.blit(pisteet, (20, 10)) #piirtää pisteet näytölle
    
        for i in range(len(self.vaaka_koordinaatit)): 
            if self.loppu != True:
                x = self.vaaka_koordinaatit[i][0]
                y = self.vaaka_koordinaatit[i][1]
                self.naytto.blit(self.kuvat[0], (x, y))# piirtää x-akselin hirviöt listalla oleviin koordinaatteihin
    
                x2 = self.pysty_koordinaatit[i][0]
                y2 = self.pysty_koordinaatit[i][1]
                self.pysty_hirvio = self.naytto.blit(self.kuvat[0], (x2, y2)) #piirtää y-akselien hirviöt listalla oleviin koordinaatteihin
    
                
                self.loppu = self.pelin_loppu(i) #tarkistaa osuuko robotti hirviöön
                self.hirvio_liikkuu(i)
                
            if self.loppu: #jos robotti osuu hirviöön, piirtää lopputekstit ja pisteet näytölle
                self.loppunaytto()
                self.naytto.blit(pisteet, (20, 10))
    
        pygame.display.flip()
        
    
    def liiku(self, liike_y, liike_x): #liikuttaa robottia
        if self.loppu:
            return
        self.robo_x += liike_x
        self.robo_y += liike_y
    
    
    def hirvio_liikkuu(self, i: int): #liikuttaa hirviöitä. Jos peli loppuu, pysäyttää hirviöiden liikkeet
        if self.loppu:
            for i in range(len(self.vaaka_koordinaatit)):
                self.vaaka_koordinaatit[i][0] += 0
                self.vaaka_koordinaatit[i][1] += 0
        
            for i in range(len(self.pysty_koordinaatit)):
                self.pysty_koordinaatit[i][0] += 0
                self.pysty_koordinaatit[i][1] += 0
        else:
            self.vaaka_koordinaatit[i][1] += random.randint(1, 3)
            self.pysty_koordinaatit[i][0] += random.randint(1, 3) 
    
            if self.vaaka_koordinaatit[i][1] > self.korkeus:
                self.vaaka_koordinaatit[i][0] = random.randint(0, 600)
                self.vaaka_koordinaatit[i][1] = 0
                self.vaaka_koordinaatit[i][1] -= random.randint(20, 600)
            
            if self.pysty_koordinaatit[i][0] > self.leveys:
                self.pysty_koordinaatit[i][0] = 0
                self.pysty_koordinaatit[i][0] -= random.randint(20, 600)
                self.pysty_koordinaatit[i][1] = random.randint(0, 460)
    
    
    def rahan_nappaus(self, luku: int): #tarkistaa onko robotti rahan kohdalla. Jos on, poistaa rahan ruudulta
        kohta_x = self.rahat[luku][0] + self.rahan_leveys >= self.robo_x and self.raha_x <= self.robo_x + self.robon_leveys
        kohta_y = self.rahat[luku][1] + self.rahan_korkeus >= self.robo_y and self.raha_y <= self.robo_y + self.robon_korkeus
    
        if kohta_x == True and kohta_y == True:
            self.tulos += 1
            self.raha_x = random.randint(660, 1200)
            self.raha_y = random.randint(500, 1000)
            self.rahat.remove(self.rahat[luku])
    
    
    def pelin_loppu(self, i:int): #tarkistaa osuuko robotti hirviöihin. Jos osuu, palauttaa True.
        #return True
        kohta_x_vaaka_hirvio = self.vaaka_koordinaatit[i][0] + self.kuvat[0].get_width() >= self.robo_x and self.vaaka_koordinaatit[i][0] <= self.robo_x + self.robon_leveys
        kohta_y_vaaka_hirvio = self.vaaka_koordinaatit[i][1] + self.kuvat[0].get_height() >= self.robo_y and self.vaaka_koordinaatit[i][1] <= self.robo_y + self.robon_korkeus
    
        kohta_x_pysty_hirvio = self.pysty_koordinaatit[i][0] + self.kuvat[0].get_width() >= self.robo_x and self.pysty_koordinaatit[i][0] <= self.robo_x + self.robon_leveys
        kohta_y_pysty_hirvio= self.pysty_koordinaatit[i][1] + self.kuvat[0].get_height() >= self.robo_y and self.pysty_koordinaatit[i][1] <= self.robo_y + self.robon_korkeus
    
        if kohta_x_vaaka_hirvio == True and kohta_y_vaaka_hirvio == True or kohta_x_pysty_hirvio == True and kohta_y_pysty_hirvio == True:
            return True
        else:
            return False
    
    
    def loppunaytto(self): #pelin loputtua näytön tausta menee mustaksi ja näytölle piirtyy kyseiset tekstit
        self.naytto.fill((0, 0, 0))
        go_teksti = self.fontti.render("Game over", True, (255, 0, 0))
        go_teksti_x = self.leveys / 2 - go_teksti.get_width() / 2
        go_teksti_y = self.korkeus / 2 - go_teksti.get_height() / 2
        pygame.draw.rect(self.naytto, (0, 0, 0), (go_teksti_x, go_teksti_y, go_teksti.get_width(), go_teksti.get_height()))
    
        r_teksti = self.fontti.render("r = uusi peli", True, (255, 0, 0))
        r_teksti_x = self.leveys / 2 - r_teksti.get_width() / 2
        r_teksti_y = self.korkeus / 2 - r_teksti.get_height() / 2
        pygame.draw.rect(self.naytto, (0, 0, 0), (r_teksti_x, r_teksti_y, r_teksti.get_width(), r_teksti.get_height()))
    
        esc_teksti = self.fontti.render("ESC = sulje", True, (255, 0, 0))
        esc_teksti_x = self.leveys / 2 - esc_teksti.get_width() / 2
        esc_teksti_y = self.korkeus / 2 - esc_teksti.get_height() / 2
        pygame.draw.rect(self.naytto, (0, 0, 0), (esc_teksti_x, esc_teksti_y, esc_teksti.get_width(), esc_teksti.get_height()))
    
    
        self.naytto.blit(go_teksti, (go_teksti_x, go_teksti_y))
        self.naytto.blit(r_teksti, (r_teksti_x, r_teksti_y+50))
        self.naytto.blit(esc_teksti, (esc_teksti_x, esc_teksti_y+80))
    
        #peli startataan uudelleen r --> jolloin kutsutaan uusi_peli(), joka käynnistää peliloopin uudelleen
        
    
    
    
if __name__ == "__main__":
    Kolikkojahti()    