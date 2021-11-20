# Udělal RxiPland

# 2021

import pydirectinput
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView
import sqlite3
import random


class Ui_MainWindow(object):

    def loaddata(self):

        global cur, tablerow

        connection = sqlite3.connect('databaze.db')
        cur = connection.cursor()

        try:

            sqlstr = 'SELECT * FROM tabulka'

            tablerow=0
            results = cur.execute(sqlstr)
            self.tableWidget.setRowCount(500)

            for row in results:
                self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
                self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
                self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                tablerow+=1

            self.lineEdit_2.clear()
            self.lineEdit.clear()

        except:

            VytvoritTabulku = "CREATE TABLE 'tabulka' ('Jméno' TEXT, '#' TEXT, 'Aktivní' TEXT)"

            cur.execute(VytvoritTabulku)

            connection.commit()
            cur.close()
            self.loaddata()


    #push button 2 enter - spustí se, když uživatel dá enter pro odeslání jména a počtu subů, namísto ručního stisknutí tlačítka přidat

    def button2ENTER(self):

        self.label_3.setHidden(True)

        global ZmacknutejEnter

        ZmacknutejEnter = int(1)

        self.button2()

    
    #push button 2 - přidat
    
    def button2(self):

        self.label_3.setHidden(True)

        global ZmacknutejEnter

        if self.lineEdit_2.text() == "":
            self.lineEdit_2.clear()
            self.lineEdit.clear()
            return
        else:
            text = self.lineEdit_2.text()
            

        if (self.lineEdit.text()) == "":
            sub = 1
            return
        else:
            try:
                sub = int(self.lineEdit.text())
            
            except:
                return
        
        stav ='Ano'
        
        if sub <=0:
            self.lineEdit_2.clear()
            self.lineEdit.clear()
            return
      
        self.lineEdit_2.clear()
        self.lineEdit.clear()

        sqliteConnection = sqlite3.connect('databaze.db')
        cursor = sqliteConnection.cursor()

        sqlite_insert_query = "insert into tabulka(Jméno, '#', Aktivní) values(?, ?, ?)"

        val = (text, sub, stav)

        cursor.execute(sqlite_insert_query, val)
        sqliteConnection.commit()
        cursor.close()

        try:

            if ZmacknutejEnter == 1:
                try:
                    pydirectinput.keyDown('shift')
                    pydirectinput.press('tab')
                    pydirectinput.keyUp('shift')

                    ZmacknutejEnter = int(0)

                except:

                    pass
        
        except:

            pass

        self.loaddata()


    #push button - změnit aktivitu

    def button(self):

        try:

            self.label_3.setHidden(True)

            global Jmeno1, Aktivita1

            connection = sqlite3.connect('databaze.db')
            cur = connection.cursor()

            if Aktivita1 == "Ne":
            
                sql_update_query = ("UPDATE tabulka set Aktivní='Ano' where Jméno='{Jmeno1}'".format(Jmeno1=Jmeno1))

            elif Aktivita1 == "Ano":

                sql_update_query = ("UPDATE tabulka set Aktivní='Ne' where Jméno='{Jmeno1}'".format(Jmeno1=Jmeno1))

            cur.execute(sql_update_query)
            connection.commit()
            cur.close()
            self.loaddata()

        except:

            pass

    #push button 3 - vylosovat

    def button3(self):

        try:
            global tablerow

            vsechnySubove = []

            tablerow = int(tablerow)

            for radky in range(tablerow):

                Jmeno2 = str(self.tableWidget.item(radky, 0).text())

                PocetSubu = int(self.tableWidget.item(radky, 1).text())

                AnoNe = str(self.tableWidget.item(radky, 2).text())


                if AnoNe == "Ano":

                    for i in range(PocetSubu):

                        vsechnySubove.append(Jmeno2)

            vylosovany = str(random.choice(vsechnySubove))

            self.label_3.setText(vylosovany)

            self.label_3.setHidden(False)

        except:

            pass

    #push button 4 - aktivovat všechny

    def button4(self):

        try:

            self.label_3.setHidden(True)

            connection = sqlite3.connect('databaze.db')
            cur = connection.cursor()

            sql_update_query = "UPDATE tabulka set Aktivní='Ano' where Aktivní='Ne'"


            cur.execute(sql_update_query)
            connection.commit()
            cur.close()
            self.loaddata()

        except:

            return

    #push button 5 - deaktivovat všechny

    def button5(self):

        try:

            self.label_3.setHidden(True)

            sqliteConnection = sqlite3.connect('databaze.db')
            cursor = sqliteConnection.cursor()
        
            sql_update_query = "UPDATE tabulka set Aktivní='Ne' where Aktivní='Ano'"


            cursor.execute(sql_update_query)
            sqliteConnection.commit()
            cursor.close()
            self.loaddata()

        except:

            return

    def zmenitAktivitu(self):

        try:

            self.label_3.setHidden(True)

            global Jmeno1, Aktivita1

            vybraneJmeno = self.tableWidget.currentRow()

            Jmeno1 = str(self.tableWidget.item(vybraneJmeno, 0).text())

            # Aktivita1 je pro zjištění jestli je aktivní nebo ne

            Aktivita1 = str(self.tableWidget.item(vybraneJmeno, 2).text())

        except:

            return


    def pressTab(self):

        text = self.lineEdit_2.text()

        if text != "":
            pydirectinput.press('tab')
        else:
            return


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Duplikant sterakova softwaru na suby")
        MainWindow.resize(888, 621)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #line edit 2 vstup pro jméno

        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(430, 80, 261, 31))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.lineEdit_2.returnPressed.connect(self.pressTab)

        #line edit - vstup pro počet subů

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(730, 80, 101, 31))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit.returnPressed.connect(self.button2ENTER)

        #label - "jméno"

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(432, 50, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")

        #label 2 - "počet subů"

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(732, 50, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        #label 3 - zobrazení vylosovaného člověka

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(430, 280, 381, 81))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.label_3.setHidden(True)



        #push button 2 - přidat

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(640, 130, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_2.clicked.connect(self.button2)

        #push button - změnit aktivitu
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(430, 130, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.pushButton.clicked.connect(self.button)

        #push button 3 - vylosovat

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 520, 351, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_3.clicked.connect(self.button3)


        #push button 4 - aktivovat všechny

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(430, 520, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_4.clicked.connect(self.button4)

        #push button 5 - deaktivovat všechny

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(650, 520, 181, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_5.clicked.connect(self.button5)

        #tableWidget - tabulka

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 20, 351, 461))
        self.tableWidget.setAutoFillBackground(False)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnWidth(0,180)
        self.tableWidget.setColumnWidth(1,27)
        self.tableWidget.setColumnWidth(2,101)
        self.loaddata()

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.tableWidget.cellClicked.connect(self.zmenitAktivitu)


        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 888, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sterakdary - Rimworld"))
        self.label.setText(_translate("MainWindow", "Jméno"))
        self.label_2.setText(_translate("MainWindow", "Počet subů"))
        self.label_3.setText(_translate("MainWindow", ""))
        self.pushButton.setText(_translate("MainWindow", "Změnit aktivitu"))
        self.pushButton_2.setText(_translate("MainWindow", "Přidat"))
        self.pushButton_3.setText(_translate("MainWindow", "Vylosovat"))
        self.pushButton_4.setText(_translate("MainWindow", "Aktivovat všechny"))
        self.pushButton_5.setText(_translate("MainWindow", "Deaktivovat všechny"))
        self.tableWidget.setSortingEnabled(True)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Jméno"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "#"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Aktivní"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
