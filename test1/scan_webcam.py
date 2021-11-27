import cv2
import pyzbar.pyzbar as pyzbar
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from simple_facerec import SimpleFacerec

sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

abbrList = {"sergo the best": "Ш.С.С", "karen": "С.К.С", "danil": "Х.Д.А", "lex": "Б.А.С"}

man_name = ""

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
driver = webdriver.Chrome()

def validate(ph_name, r):
    print(ph_name)
    if "sergo the best" == ph_name and r == abbrList["sergo the best"]:
        return r
    elif "karen" == ph_name and r == abbrList["karen"]:
        return r
    elif "danil" == ph_name and r == abbrList["danil"]:
        return r
    elif "lex" == ph_name and r == abbrList["lex"]:
        return r
    else:
        return 'These are different people'

#url = "https://www.gosuslugi.ru/covid-cert/status/c7e8f7a4-e237-4754-976d-ab6b21817e50?lang=ru" # леша работает
#url = "https://www.gosuslugi.ru/covid-cert/status/177be104-7ab1-46b3-9734-5cf9455643af?lang=ru" # карина работает
#url = "https://www.gosuslugi.ru/covid-cert/verify/9610000030478107?lang=ru&ck=8f7566eb9c3c3faa1d1cc5a417331198" # сергей не работает
#url = "https://www.gosuslugi.ru/covid-cert/status/db87cb9e-28ae-4fbd-a52a-bfd388444fac?lang=ru" # сергей работает
#url = "https://www.gosuslugi.ru/covid-cert/verify/9610000037817045?lang=ru&ck=4681c73ee10e18e0ec4873e8836aefef" # данил не работает
#url = "https://www.gosuslugi.ru/covid-cert/status/903d035d-af83-4e10-a1d9-46a2937680dc?lang=ru" #данил работает
while True:
    _, frame = cap.read()
    decodedObjects = pyzbar.decode(frame)

    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        man_name = name

        cv2.putText(frame, name, (x1, y1 - 10), font, 1, (0, 255, 0), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    for obj in decodedObjects:
        #print("Data", obj.data)

        s = obj.data.decode('UTF-8')
        if "https://www.gosuslugi.ru/covid-cert/" in s:
            print("Data: ", obj.data, "\n")

            driver.get(s)
            try:
                el = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/div[4]/div/span[2]")
                # print(el.text)

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                d = soup.find('span', class_='status-value cert-name').text
                f = soup.find('div', class_='small-text gray').text
                r = soup.find('div', class_='attrValue title-h6 bold text-center').text
                cv2.putText(frame, str(f), (50, 60), font, 4,
                            (0, 255, 0), 2)

                r = r.replace('*', '').replace(' ', '.')
                #print(d)
                #print(f)
                print(r)
                print(man_name)
                print(validate(man_name, r))

            except:
                pass

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()

