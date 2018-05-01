import math
from VectorImage import VectorMap

lmRadius = 0.5  #Radius der Landmarks

def lmWinkel(pointB, pointLM):
    '''Berechnet Landmark-Winkel
    pointB - Punkt aus dessen Perspektive das LM gesehen werden
    pointLM - Punkt des Landmark
    Rueckgabe - (Winkelhalbierende, Linker Winkel, Rechter Winkel,
                Winkelspanne, Farbe)
    '''

    # Winkel zwischen pointB und LM-Mittelpunkt
    xDif = pointLM[0] - pointB[0]
    yDif = pointLM[1] - pointB[1]
    winkelA = math.atan2(yDif, xDif)
    # Winkel zwischen pointB und LM-Kante
    entfernung = math.sqrt(xDif**2 + yDif**2)
    winkelB = math.atan(lmRadius / entfernung)
    winkelL = winkelA + winkelB
    if winkelL > math.pi:
        winkelL = winkelL - math.pi * 2

    winkelR = winkelA - winkelB
    if winkelR < -1 * math.pi:
        winkelR = winkelR + math.pi * 2

    #Rueckgabe: Winkelhalbierende, Linker Winkel, Rechter Winkel, Winkelspanne,
    #                                                       's' fuer Schwarz
    retTup = (winkelA, winkelL, winkelR, math.fabs(winkelB * 2), 'S')

    return retTup

def printWtupInDgr(winkel):
    '''Debugfunktion'''
    s = ""
    for i in range(len(winkel)-1):
        s = s + str(math.degrees(winkel[i])) + " : "
    print (s, winkel[len(winkel)-1])

def ueberschneidungLoeschen(winkel):
    '''Loescht Landmarks die sich ueberschneiden
    Das LM das weiter entfernt ist, wird behalten
    winkel - Tupel mit LM-Daten (Aufbau s. lmWinkel)
    '''
    winkel = sorted(winkel)
    i = 0
    wSize = len(winkel)
    r = lambda x: (x+1)%wSize
    while i < wSize and wSize > 1:
        wDif = winkel[r(i)][2] - winkel[i][1]
        grenze = winkel[r(i)][3] + winkel[i][3]
        if wDif < 0 and math.fabs(wDif) < grenze:
            if winkel[i][3] > winkel[r(i)][3]:
                del winkel[i]
            else:
                del winkel[r(i)]
            wSize = wSize - 1
        else:
            i = i + 1
    return tuple(winkel)

def wWinkelEinfg(winkel):
    '''Fuegt "weisse" Winkel zwischen "schwarze" Winkel ein
    winkel - Tupel mit LM-Daten (Aufbau s. lmWinkel)
    '''
    arr = []
    last = len(winkel)-1
    for i in range(last):
        arr.append(winkel[i])
        mitte = (winkel[i][1] + winkel[i+1][2])/2
        breite = winkel[i+1][2] - winkel[i][1]
        arr.append((mitte, winkel[i+1][2], winkel[i][1], breite, 'W'))

    arr.append(winkel[last])
    breite = winkel[0][2] - winkel[last][1]
    if breite < 0:
        breite = 2 * math.pi + breite
    mitte = winkel[last][1] + breite / 2
    if mitte > math.pi:
        mitte = mitte - math.pi * 2
        arr.insert(0, (mitte, winkel[0][2], winkel[last][1], breite, 'W') )
    else:
        arr.append((mitte, winkel[0][2], winkel[last][1], breite, 'W'))

    return tuple(arr)

class cmpKlasse:
    '''Hilfsklasse zur Umsetzung einer Vergleichsfunktion fuer Listensortierung
    von - der Winkel dessen Nachbar gesucht wird
    '''
    def __init__(self, von):
        self.von = von

    def nachbarCmp(self, a, b):
        if a[4] != self.von[4]:
            difA = 2 * math.pi
        else:
            difA = self.von[0] - a[0]
            difA = math.fabs(difA)
            if difA > math.pi:
                difA = 2 * math.pi - difA

        if b[4] != self.von[4]:
            difB = 2 * math.pi
        else:
            difB = self.von[0] - b[0]
            difB = math.fabs(difB)
            if difB > math.pi:
                difB = 2 * math.pi - difB

        dif = difA - difB
        return int(dif * 100)

def findeNachbar(winkel, von):
    '''Ermitteln des Nachbarn eines Winkels
    winkel - Winkeldaten(Aufbau s. lmWinkel)
    von - Der Winkel dessen Nachbar in "winkel" gesucht wird
    '''
    arr = list(winkel)
    k = cmpKlasse(von)
    arr = sorted(arr, key = k) #arr wird nach Entfernung zu "von" sortiert

    return arr[0]

def bildeVectKomp(winkelS, winkelR):
    '''Berechnung einer Vektorkomponente des Homing-Vektors
    Die Vektorkomponente beinhaltet einen Richtungs- und einem Drehungsvektor
    winkelS - Der Winkel aus dem Snapshot
    winkelR - Der Nachbarwinkel aus der Retina
    '''
    if winkelR[3] > winkelS[3]:
        vR = Vect(winkelR[0] + math.pi)
    else:
        vR = Vect(winkelR[0])

    wDif = winkelR[0] - winkelS[0]
    if wDif > math.pi:
        wDif = -2 * math.pi + wDif
    elif wDif < -1 * math.pi:
        wDif = 2 * math.pi + wDif

    if wDif < 0:
        vD = Vect(winkelR[0] - math.pi / 2)
    else:
        vD = Vect(winkelR[0] + math.pi / 2)

    return (3 * vR[0] + vD[0], 3 * vR[1] + vD[1])

def Vect(a):
    '''Erzeugen eines Einheitsvektors aus einem Winkel'''
    return (math.cos(a), math.sin(a))

def berechneHomingVector(standort, landmarks, snapshot):
    '''Berechnung des Homing-Vektors am angegebenen Standort
    standort - Die Koordinaten des aktuelle Standorts der Biene
    landmarks - Die Koordinaten der Landmarks
    snapshot - Die Snapshot-Winkel(Aufbau s. lmWinkel)
    '''
    standortWinkel = []
    for lm in landmarks:
        standortWinkel.append(lmWinkel(standort, lm))
    standortWinkel = tuple(standortWinkel)
    standortWinkel = ueberschneidungLoeschen(standortWinkel)

    standortWinkel = wWinkelEinfg(standortWinkel)

    v = (0, 0)
    for sw in snapshot:
        nachbar = findeNachbar(standortWinkel, sw)
        r = bildeVectKomp(sw, nachbar)
        v = (v[0] + r[0], v[1] + r[1])
    betrag = math.sqrt(v[0]**2 + v[1]**2)
    v = (v[0]/betrag, v[1]/betrag)
    return v

def berechneAbweichung(homingV, standort):
    '''Berechnung der Abweichung zwischen Homing- und Idealvektor
    homingV - Homing-Vektor
    standort - Koordinaten des aktuellen Standorts der Biene
    '''
    wS = math.atan2(-1 * standort[1], -1 * standort[0])
    wH = math.atan2(homingV[1], homingV[0])
    dif = math.fabs(wS - wH)
    if dif > math.pi:
        dif = math.pi * 2 - dif
    return dif / math.pi

if __name__ == "__main__":

    landmarks = ((3.5, 2), (3.5, -2), (0, -4))
    w1 = lmWinkel((0, 0), landmarks[0])
    w2 = lmWinkel((0, 0), landmarks[1])
    w3 = lmWinkel((0, 0), landmarks[2])
    snapshot = w1, w2, w3

    snapshot = ueberschneidungLoeschen(snapshot)
    snapshot = wWinkelEinfg(snapshot)

    vectormap = VectorMap((15, 15), 60)

    for standort in landmarks:
        vectormap.drawLandmark((standort[0]+7, (-1 * standort[1])+7))

    for x in range(-7, 8, 1):
        for y in range(-7, 8, 1):
            standort = (x, y)
            if standort in landmarks or standort == (0, 0):
                continue
            v = berechneHomingVector(standort, landmarks, snapshot)
            abw = berechneAbweichung(v, standort)
            vectormap.drawVector((x + 7, (-1*y) + 7), (v[0], v[1]*-1), abw)
    vectormap.saveMap("result.png")
    print("")
    print("Das Bild mit den Vektoren wurde im gleichen Verzeichnis unter dem Namen result.png erstellt!")
