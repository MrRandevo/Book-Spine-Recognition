import numpy as np 
import cv2  
import math 
#Funkcja zwraca trzeci element z listy

def takethird(elem):
    return elem[2]
 
# Wczytywanie zdjecia #
filename = "WMA3.jpg"
image = cv2.imread(filename)
image2 = image.copy()
 
#Rozmiary zdjecia
img_x = image.shape[1]
img_y = image.shape[0] 
#Konwersja do przestrzeni barw GRAY
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
#Zastosowanie filtru medianowego, w celu usuniecia szumu
gray = cv2.medianBlur(gray, 3 )
  
#Zwraca element strukturalny o rozmiarach 3x3
k1 = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3) ) 
#Operator Cannyego, sluzy do wykrywania krawędzi
edges = cv2.Canny(gray, 45,120, apertureSize = 3 )   

#Operacja morfologiczna zamknięcia (dylatacja->erozja)
closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, k1, iterations = 2) 
 
cv2.namedWindow("closed",cv2.WINDOW_NORMAL)
cv2.imshow("closed", closed)

cv2.namedWindow("edges",cv2.WINDOW_NORMAL)
cv2.imshow("edges", edges)

#Znajdowanie lini na obrazie
lines = cv2.HoughLinesP(edges, 1, np.pi/480, 275, minLineLength=120, maxLineGap=450)

sorted_lines = []
for line in lines:
    x1, y1, x2, y2 = line[0]

    # Zmienne pomoga okreslic nachylenie lini
    temp1 = int(x2-x1)
    temp2 = int(y2-y1)
    # Jezeli linia jest idealnie pionowa, wtedy
    # przyjmujemy ze kat nachylenia to 0 stopni, a wiec tg = 0
    if(temp1 == 0):
        tang = 0

    # Jezeli jest inaczej to liczony jest tangens
    else:
        tang = math.tan(temp2/temp1)

    # Jezeli kat nachylenia jest mniejszy niz 40 stopni w ktoras ze stron
    # to tworzone sa przedluzenia lini, ktore dodawane sa odpowiedniej listy
    if(  tang > -0.9 and tang < 0.9  and (temp1 < 100) )  :
        x3 = int(y1*temp1/temp2)
        x3 = x1 - x3
        x4 = int((img_y - y2) * temp1 /temp2)
        x4 = x2 + x4
        # obliczanie srodka lini (pozwoli posortowac oraz sfiltrowac zbyt duza
        # ilosc bliskich siebie lini)
        x_sr = int((x3+x4)/2)

        sorted_lines.append((x3,x4,x_sr))

        # Rysuje linie na kopii obrazy (przed filtrowaniem lini)
        cv2.line(image2,(x3, 0),(x4, img_y), (0, 255, 0),2)

#Posortowanie lini, zaleznie od wspolrzednych srodka
sorted_lines.sort(key = lambda x : x[2])

#Algorytm oczyszczajacy linie obok siebie
tab = []
y = []
i = 0
for x in range (len(sorted_lines)):
    if((x == len(sorted_lines) -1) or (x in y) ):
        continue
    else:
        i += 1
        tmp = sorted_lines[i][2] - sorted_lines[x][2]
        if(tmp>63):
            pass
        else:
            while(tmp<63):
                tab.append(sorted_lines[i])
                y.append(i)
                if(i == (len(sorted_lines) -1)):
                    break;
                i += 1
                tmp = sorted_lines[i][2] - sorted_lines[x][2]
 
# Lista zawiera linie po sortowaniu
z = list(set(sorted_lines) - set(tab))

# Rysuje linie na glownym obrazie (po filtrowaniu lini)
for x in range (len(z)):
    cv2.line(image,(z[x][0], 0),(z[x][1], img_y), (0, 255, 0),2)
    
print ("Liczba ksiazek to:", len(z)-1 )
#Wyswietlanie zdjec
cv2.namedWindow("Przed sortowaniem",cv2.WINDOW_NORMAL)
cv2.imshow("Przed sortowaniem", image2)
cv2.namedWindow("Po sortowaniu",cv2.WINDOW_NORMAL)
cv2.imshow("Po sortowaniu", image)
cv2.imwrite("Zdjecie_po_wykryciu.jpg", image)
cv2.waitKey(0)