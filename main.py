import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog
import requests
from const import api_key
city = ''


class PomForm(QDialog):
        def __init__(self):
            super().__init__()
            uic.loadUi('pom.ui', self)
            with open('text_file.txt', 'r', encoding='utf8') as file:
                    data = file.readlines()
            self.label.setText(f"Хотите узнать погоду в городе {data[0]}?")
            self.pushButton.clicked.connect(self.run)

        def run(self):
            if self.radioButton.isChecked() == True:
                self.close()
                with open('text_file.txt', 'r', encoding='utf8') as file:
                    data = file.readlines()
                global city
                city = data[0]
                print(city)
                file.close()
                self.second_form = TreeForm()
                self.second_form.show()
            elif self.radioButton_2.isChecked() == True:
                self.close()
                self.second_form = OneForm()
                self.second_form.show()
            else:
                self.second_form = Erorr2()
                self.second_form.show()


class OneForm(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui.1.ui', self)
        self.pushButton.clicked.connect(self.run)

    def run(self):
        global city
        city = self.lineEdit.text()
        if len(city):
            self.close()
            self.second_form = TreeForm()
            self.second_form.show()
            if self.checkBox.isChecked() == True:
                with open ('text_file.txt', 'r') as f:
                    old_data = f.read()
                new_data = old_data.replace(old_data, city)
                with open ('text_file.txt', 'w') as f:
                    f.write(new_data)
        else:
            self.second_form = Erorr()
            self.second_form.show()


class Erorr(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui.erorr.ui', self)
    

class Erorr2(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui.erorr2.ui', self)

                
class TreeForm(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui.3.ui', self)
        self.pushButton.clicked.connect(self.run3)
        try:
            a = f"https://api.weatherstack.com/current?access_key={api_key}&query=" + city
            response = requests.get(url=a)
            answer = response.json()
            self.label_2.setText(answer["request"]["query"])
            self.label_4.setText(str(answer["current"]["temperature"]))
            self.label_7.setText(str(answer["current"]["feelslike"]))
            self.label_10.setText(str(int(answer["current"]["wind_speed"] * 1000 / 3600)))
            self.label_12.setText(str(int(int(answer["current"]["pressure"]) * 0.75)))
            self.label_14.setText(str(answer["current"]["precip"]))
            self.label_16.setText(str(answer["current"]["humidity"]))
            self.label_18.setText(str(answer["current"]["cloudcover"]))
            self.label_20.setText(str(answer["current"]["visibility"]))
        except KeyError:
            self.second_form = Erorr()
            self.second_form.show()

    def run3(self):
        self.close()
        self.second_form = OneForm()
        self.second_form.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open('text_file.txt', 'r', encoding='utf8') as file:
        data = file.readlines()
    if data:
        ex = PomForm()
        ex.show()
        sys.exit(app.exec())
    else:
        ex = OneForm()
        ex.show()
        sys.exit(app.exec())