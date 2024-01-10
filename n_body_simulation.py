# An N-body simulation of gravitational forces.
# This code is ugly and slow and wastes memory. Also it's in Finnish.
# I wrote it many years ago.



# Simuloidaan pistemäisten massakappaleiden liikettä.

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from math import sqrt
from math import sin
from random import uniform

def r(k1, k2): # kappaleiden välinen etäisyys
    return sqrt((k1[0]-k2[0])**2 + (k1[1]-k2[1])**2)

T = 10 # simulaation kesto
deltaT = 0.005
G = 0.1 # gravitaatiovakio

# Tallennetaan sijainnit kahdessa eri muodossa animointia varten.
sijainnit = []
offsetSijainnit = []

# Alustetaan kappaleet. Eri vaihtoehtoja alkukokoonpanoiksi.
kokoonpano = 0
if kokoonpano == 0:
    kappaleet = []
    for i in range(20):
        kappaleet.append([
            uniform(1, 5),
            [uniform(-2, 2), uniform(-2, 2)],
            [uniform(-0.5, 0.5), uniform(-0.5, 0.5)]
        ])
if kokoonpano == 1:
    kappaleet = [
        #[massa, [x, y], [v_x, v_y]]
        [10, [0.5, 0.5], [0.2, -0.2]],
        [1, [-0.5, -0.5], [-0.2, 0.2]],
        [1, [-0.1, -0.2], [-0.2, 0.2]],
        [1, [-0.04, -0.9], [-0.2, 0.2]],
        [1, [-0.1, -0.4], [-0.2, 0.2]],
        [1, [-0, -0], [-0.2, 0.2]]
    ]



# Lasketaan ensin fysiikka.

for timestep in range(int((T/deltaT))):
    # G = sin(0.01*timestep)
    # Tallennetaan uudet sijainnit.
    uudetOffsetSijainnit = []
    for kappale in kappaleet:
        uudetOffsetSijainnit.append([kappale[1][0], kappale[1][1]])
    offsetSijainnit.append(uudetOffsetSijainnit)

    xArvot = []
    yArvot = []
    for i in range(len(kappaleet)):
        xArvot.append(kappaleet[i][1][0])
        yArvot.append(kappaleet[i][1][1])
    sijainnit.append([xArvot, yArvot])
    
    # Kappaleeseen A kohdistuu kunkin muun kappaleen B aiheuttama voima,
    # joiden resultantti lasketaan.
    resultantit = []
    for kappaleA in kappaleet:
        sijaintiA = kappaleA[1] # Haetaan kappaleen A nykyiset koordinaatit.
        resultantti = [0, 0]
        for kappaleB in kappaleet:
            sijaintiB = kappaleB[1]
            if r(sijaintiA, sijaintiB) > 0.05:
                # Allaolevat laskut lasketaan kaikille kappaleille B,
                # jotka eivät ole samassa pisteessä kuin kappale A.
                suuntavektori = [sijaintiB[0]-sijaintiA[0],
                                 sijaintiB[1]-sijaintiA[1]]
                # Newtonin painovoimalaista saadaan:
                voimanSuuruus = G*((kappaleA[0]*kappaleB[0])/
                                   ((r(sijaintiA, sijaintiB))**2))
                yksikkovektori = [element * (1/r(sijaintiA, sijaintiB))
                                  for element in suuntavektori]
                voimavektori = [element * voimanSuuruus 
                                for element in yksikkovektori]
                resultantti = [resultantti[i]+voimavektori[i]
                               for i in range(len(resultantti))]
        resultantit.append(resultantti)

    # Lasketaan kullekin kappaleelle resultanttivoiman aiheuttama kiihtyvyys.
    # a=F/m
    kiihtyvyydet = []
    for i in range(len(resultantit)):
        kiihtyvyydet.append([element * (1/kappaleet[i][0])
                            for element in resultantit[i]])
    
    # Lasketaan kullekin kappaleelle uusi nopeus, kun sitä kiihdytetään
    # äsken lasketulla kiihtyvyydellä deltaT pituinen aika.
    nopeuksienMuutokset = []
    for i in range(len(kiihtyvyydet)):
        nopeuksienMuutokset.append([element * deltaT 
                            for element in kiihtyvyydet[i]])
    for i in range(len(kappaleet)):
        kappaleet[i][2][0] = kappaleet[i][2][0] + nopeuksienMuutokset[i][0]
        kappaleet[i][2][1] = kappaleet[i][2][1] + nopeuksienMuutokset[i][1]

    # Liikutetaan kutakin kappaletta uudella nopeudella deltaT verran.
    for i in range(len(kappaleet)):
        kappaleet[i][1][0] = kappaleet[i][1][0] + deltaT*kappaleet[i][2][0]
        kappaleet[i][1][1] = kappaleet[i][1][1] + deltaT*kappaleet[i][2][1]



# Animoidaan tilanne äsken laskettujen sijaintitietojen pohjalta.

fig = plt.figure(figsize=(8,8))
ax = plt.axes(xlim=(-2, 2),ylim=(-2, 2))
scatter=ax.scatter(sijainnit[0][0], sijainnit[0][1]) # sijainnit alussa

# Tehdään lista kunkin kappaleen massasta. Listan avulla muutetaan 
# pisteiden koko animaatiossa.
koot = len(kappaleet)*[0]
for i in range(len(koot)):
    koot[i] = kappaleet[i][0] * 15
scatter.set_sizes(koot)

# Piirretään lisäksi jälki kappaleen liikeradasta.
trailScatter=ax.scatter(None, None)
trailScatter.set_sizes([element*0.005 for element in koot])

def update(frame):
    trail = [[0, 0]]
    for i in range(max(0, frame-100), frame):
        for j in offsetSijainnit[i]:
            trail.append(j)

    if frame < len(sijainnit):
        scatter.set_offsets(offsetSijainnit[frame])
        trailScatter.set_offsets(trail)

anim = FuncAnimation(fig, update, interval=5000*deltaT)

plt.show()