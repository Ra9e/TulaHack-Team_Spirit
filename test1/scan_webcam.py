import cv2
import pyzbar.pyzbar as pyzbar
import pyautogui

from simple_facerec import SimpleFacerec
from test1.parser import Parsing

sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

prs = Parsing()

abbrList = {"sergo the best": "Ш.С.С", "karen": "С.К.С", "danil": "Х.Д.А", "lex": "Б.А.С"}
man_name = ""

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN


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

            try:
                prs.parse(s)
                cv2.putText(frame, str(prs.expire_time_getter()), (50, 60), font, 4,
                            (0, 255, 0), 2)

                print(prs.FIO_getter())
                if validate(man_name, prs.FIO_getter()):
                    message = prs.status_getter()+" до "+prs.expire_time_getter()+" на имя "+prs.FIO_getter()
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

