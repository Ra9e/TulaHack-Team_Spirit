import cv2
import pyzbar.pyzbar as pyzbar
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pyautogui

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
        return True
    elif "karen" == ph_name and r == abbrList["karen"]:
        return True
    elif "danil" == ph_name and r == abbrList["danil"]:
        return True
    elif "lex" == ph_name and r == abbrList["lex"]:
        return True
    else:
        return False


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

        s = obj.data.decode('UTF-8')
        if "https://www.gosuslugi.ru/covid-cert/" in s:
            print("Data: ", obj.data, "\n")

            driver.get(s)
            try:
                el = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/div[4]/div/span[2]")
                # print(el.text)

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                status = soup.find('span', class_='status-value cert-name').text
                expire_time = soup.find('div', class_='small-text gray').text
                FIO = soup.find('div', class_='attrValue title-h6 bold text-center').text
                cv2.putText(frame, str(expire_time), (50, 60), font, 4,
                            (0, 255, 0), 2)

                FIO = FIO.replace('*', '').replace(' ', '.')
                if validate(man_name, FIO):
                    message = status+" до "+expire_time+" на имя "+FIO
                    pyautogui.alert(text=message, title='Отчет о считывании', button='OK')
                else:
                    pyautogui.alert(text='Это QR code другого человека', title='Отчет о считывании', button='OK')

            except:
                pass
        else:
            pyautogui.alert(text='Это недействительный QR code, попробуйте снова', title='Отчет о считывании', button='OK')

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()

