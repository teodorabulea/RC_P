import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

class Connect(QDialog):
    def __init__(self):
        super(Connect,self).__init__()
        loadUi("login.ui",self)
        self.conectarebutton.clicked.connect(self.connectfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password) #ascunde parola
    

    def connectfunction(self):
        user=self.user.text()
        password=self.password.text()
        print("Successfully logged in with user: ", user, "and password:", password)
        mqtt_ap=MQTT()
        widget.addWidget(mqtt_ap)
        widget.setCurrentIndex(widget.currentIndex()+1)

class MQTT(QDialog):
    def __init__(self):
        super(MQTT, self).__init__()
        loadUi("MQTT.ui",self)


app=QApplication(sys.argv)
mainwindow=Connect()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1000)
widget.setFixedHeight(600)
widget.show()
app.exec_()