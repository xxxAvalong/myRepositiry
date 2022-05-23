import cv2
import numpy as np


def nothing(*args):
    pass


images_name = []
for i in range(0, 4):
    images_name.append(f'{i}.jpeg')

'''for img in images_name:
    img_ = cv2.imread(img)
    img_ = cv2.resize(img_, (700, 700))
    img_ = cv2.GaussianBlur(img_, (7, 7), cv2.BORDER_DEFAULT)
    grey_img = cv2.cvtColor(img_, cv2.COLOR_BGR2HSV)

    outlines = cv2.Canny(grey_img, 60, 60)

    cv2.imshow(f'{img}', outlines)

cv2.waitKey(0)'''

img_n = images_name[0]
img = cv2.imread(img_n)
img = cv2.resize(img, (700, 700))
'''grey_img = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
grey_img = cv2.GaussianBlur(grey_img, (5, 5), cv2.BORDER_DEFAULT)'''

cv2.namedWindow('set')
cv2.createTrackbar('low', 'set', 0, 999, nothing)
cv2.createTrackbar('high', 'set', 127, 999, nothing)
############################################################
cv2.namedWindow('Set1', cv2.WINDOW_KEEPRATIO)
# Trackbar regulacie dtieni
cv2.createTrackbar('H1', 'Set1', 0, 255, nothing)
cv2.createTrackbar('H2', 'Set1', 255, 255, nothing)
# Trackbar regulacie sytosti
cv2.createTrackbar('S1', 'Set1', 0, 255, nothing)
cv2.createTrackbar('S2', 'Set1', 255, 255, nothing)
# Trackbar regulacie jasu
cv2.createTrackbar('V1', 'Set1', 0, 255, nothing)
cv2.createTrackbar('V2', 'Set1', 255, 255, nothing)
#############################################################
matrix = np.zeros(img.shape[:-1], dtype='uint8')
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

new_values = False
new_values_1 = False
while True:
    values = {}
    value_container1 = {}  # Kontainer z hodnotami masky
    #######################################################
    h1 = cv2.getTrackbarPos('H1', 'Set1')  # Dolna hranica odtieny v ramci HSV masky
    value_container1['H1'] = h1  # Zapisujeme H1 do kontaineru
    h2 = cv2.getTrackbarPos('H2', 'Set1')  # Horna hranica odtieny v ramci HSV masky
    value_container1['H2'] = h2  # Zapisujeme H2 do kontaineru

    s1 = cv2.getTrackbarPos('S1', 'Set1')  # Horna hranica sytosti v ramci HSV masky
    value_container1['S1'] = s1  # Zapisujeme S1 do kontaineru
    s2 = cv2.getTrackbarPos('S2', 'Set1')  # Horna hranica sytosti v ramci HSV masky
    value_container1['S2'] = s2  # Zapisujeme S2 do kontaineru

    v1 = cv2.getTrackbarPos('V1', 'Set1')  # Horna hranica jasu v ramci HSV masky
    value_container1['V1'] = v1  # Zapisujeme V1 do kontaineru
    v2 = cv2.getTrackbarPos('V2', 'Set1')  # Horna hranica jasu v ramci HSV masky
    value_container1['V2'] = v2  # Zapisujeme V2 do kontaineru
    #######################################################
    if value_container1 != new_values:  # Ak hodnoty v tomto kontainere odlisuju sa od
        # hodnot kontainera z predosloho cyklu, - tak vypiseme do kozoly
        print(f"\nActual MASK:\n"
              f"low_clr = ({value_container1['H1']}, "
              f"{value_container1['S1']}, "
              f"{value_container1['V1']})\n"
              f"high_clr = ({value_container1['H2']}, "
              f"{value_container1['S2']}, "
              f"{value_container1['V2']})")
    new_values_1 = value_container1  # Skopirujem aktualne hodnoty do vonkajsej premennej
    #######################################################
    h_min = (h1, s1, v1)  # Dolne hodnoty farebnej masky
    h_max = (h2, s2, v2)  # Horne hodnoty farebnej masky
    masked_image = cv2.inRange(hsv_img, h_min, h_max)  # Maskovany obrazk

    result_scr_h = img.shape[1]
    result_scr_w = img.shape[0]
    result_scr = cv2.resize(masked_image, (result_scr_h, result_scr_w))

    # cv2.imshow('result', result_scr)
    #######################################################################
    low_can = cv2.getTrackbarPos('low', 'set')
    high_can = cv2.getTrackbarPos('high', 'set')

    values['low'] = low_can
    values['high'] = high_can

    if values != new_values:
        print(values['low'], values['high'])
    new_values = values

    '''outlines = cv2.Canny(result_scr.copy(), low_can, high_can)
    cv2.imshow('outlines', outlines)'''

    contours, hierarchy = cv2.findContours(
        result_scr, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    matrix = np.zeros(result_scr.shape, dtype='uint8')

    '''for c in contours:
        rect = cv2.minAreaRect(c)

        box = cv2.boxPoints(rect)
        box = np.int0(box)'''

    cv2.drawContours(matrix, contours, -1, 255, 1)

    cv2.imshow('found', matrix)

    cv2.waitKey(30)



