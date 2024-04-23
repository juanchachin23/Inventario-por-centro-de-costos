import sys
import pyodbc
from PyQt5 import uic, QtCore
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QMessageBox
import mysql.connector
import numpy
from PyQt5.QtCore import QDate, QDateTime, pyqtSlot
import datetime
from datetime import  timedelta
import sqlite3 



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("screen1.ui", self)
        
        ##
        
        self.botonhazclickenesteboton.clicked.connect(self.gotoScreen2)
        self.botonentradadatosnuevos.clicked.connect(self.gotoScreen3)
        self.botonentradadatosexistentes.clicked.connect(self.gotoScreen4)
        self.boton3_2.clicked.connect(self.registroutilizacion)
        self.introducirsuministro()
        self.SumCaducado()
        self.registroreciente()
        self.horasistema()
        
        

        a=0
        ## botones que permiten cambiar entre las pantallas
        while (a<=5):
           self.Caduco_6.setColumnWidth(a, 100)
           a+=1
        
        self.Caduco_6.setHorizontalHeaderLabels(
        ["Suministro", "Marca", "Ubicacion", "Caduco", "Medida", "El Dia"])
        self.boton3_3.clicked.connect(self.caducado)

        self.tableWidget.setColumnWidth(0, 50)
        while (a<=8):
           self.tableWidget.setColumnWidth(a, 100)
           a+=1
        
        self.tableWidget.setHorizontalHeaderLabels(
        ["ID", "Suministro", "Categoria", "Stock", "Medida", "Valor unitario", "Valor total", "Ubicacion", "Marca"])
        self.registroreciente()
        ##

    def SumCaducado(self):
        connection = sqlite3.connect("suministroinv.db")
        cursor = connection.cursor()
        selec='Select DISTINCT nombre from suministro join condicion on condicion.suministro_IdSum=suministro.IdSum where perecedero=1'
        cursor.execute(selec)
        pls=numpy.asarray(cursor.fetchall()).flatten()
        
        self.SumCaduc_6.clear(); self.UbiCaduc_6.clear(); self.MarCaduc_6.clear()
        self.SumCaduc_6.addItems(pls)
        self.SumCaduc_6.activated.connect(self.MarCaducado)
        self.SumCaduc_6.activated.connect(self.Ubicaducado)
    
    def MarCaducado(self):
        suministro=str(self.SumCaduc_6.currentText())
        connection = sqlite3.connect("suministroinv.db")
        cursor = connection.cursor()
        selec='Select DISTINCT marca from suministro where nombre="'+suministro+'"'
        cursor.execute(selec)
        pls=numpy.asarray(cursor.fetchall()).flatten()
        
        self.MarCaduc_6.clear()
        self.MarCaduc_6.addItem("")
        self.MarCaduc_6.addItems(pls)


    def Ubicaducado(self):
        suministro=str(self.SumCaduc_6.currentText())
        connection = sqlite3.connect("suministroinv.db")
        cursor = connection.cursor()
        selec='select ubicacion.Ubicacion from ubicacion join suministro on suministro.IdUbicación=ubicacion.IdUbicación where suministro.nombre="'+suministro+'"'        
        cursor.execute(selec)
        pls=numpy.asarray(cursor.fetchall()).flatten()        
        self.UbiCaduc_6.clear()
        self.UbiCaduc_6.addItem("")
        self.UbiCaduc_6.addItems(pls)

    def caducado(self):
        connection = sqlite3.connect("suministroinv.db")
        cursor = connection.cursor()
        select = "select suministro.nombre, suministro.marca, ubicacion.ubicacion, entrada.Cantidad as Caduco, stock.medida, fecha_Caducidad from suministro join ubicacion on ubicacion.IdUbicación=suministro.IdUbicación left join entrada on entrada.suministro_IdSum=suministro.IdSum left join stock on stock.idSuministro=suministro.IdSum left join condicion on condicion.suministro_IdSum=suministro.IdSum where perecedero=1 "
        
        if len(str(self.SumCaduc_6.currentText()))>0:
            select+="and suministro.nombre='"+str(self.SumCaduc_6.currentText())+"' "

        if len(str(self.MarCaduc_6.currentText()))>0:
            select+="and suministro.marca='"+str(self.MarCaduc_6.currentText())+"' "
        
        if len(str(self.UbiCaduc_6.currentText()))>0:
            select+="and ubicacion.ubicacion='"+str(self.UbiCaduc_6.currentText())+"' "   
        
        dia = self.Desde_6.date().day()
        if(int(dia)<10):
            dia = '0'+str(dia)
        else:
            dia=str(dia)
        mes = self.Desde_6.date().month()
        if(int(mes)<10):
            mes = '0'+str(mes)
        else:
            mes=str(mes)
        ano = self.Desde_6.date().year()
        ano = str(ano)        
        fechaDesde_6 = ano + "-" + mes + "-" + dia
        if len(fechaDesde_6)>3:
            select+=" and Fecha_Caducidad>'"+fechaDesde_6+"' "

        dia = self.Cuando.date().day()
        if(int(dia)<10):
            dia = '0'+str(dia)
        else:
            dia=str(dia)
        mes = self.Cuando.date().month()
        if(int(mes)<10):
            mes = '0'+str(mes)
        else:
            mes=str(mes)
        ano = self.Cuando.date().year()
        ano = str(ano)        
        fechaCuando = ano + "-" + mes + "-" + dia
        if len(fechaCuando)>3:
            select+="and Fecha_Caducidad<'"+fechaCuando+"' "
      
        self.Caduco_6.clear()
        self.Caduco_6.setRowCount(100)
        tablerow = 0
        self.Caduco_6.setHorizontalHeaderLabels(
        ["Suministro", "Marca", "Ubicacion", "Caduco", "Medida", "El Dia"])
        for row in cursor.execute(select):
            self.Caduco_6.setItem(
                tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.Caduco_6.setItem(
                tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.Caduco_6.setItem(
                tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.Caduco_6.setItem(
                tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.Caduco_6.setItem(
                tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))   
            self.Caduco_6.setItem(
                tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
            tablerow += 1
    
    def introducirsuministro(self):
        connection = sqlite3.connect("suministroinv.db")
        cursor = connection.cursor()
        selec='Select DISTINCT nombre from suministro '
        cursor.execute(selec)
        pls=numpy.asarray(cursor.fetchall()).flatten()
        
        self.comboBox_11.clear(); self.comboBox_13.clear(); self.comboBox_12.clear()
        self.comboBox_11.addItems(pls)
        self.comboBox_11.activated.connect(self.introducirmarca)
    
    def introducirmarca(self):
        suministro=str(self.comboBox_11.currentText())
        connection = sqlite3.connect("suministroinv.db")
        cursor = connection.cursor()
        selec='Select DISTINCT marca from suministro where nombre="'+suministro+'"'
        cursor.execute(selec)
        pls=numpy.asarray(cursor.fetchall()).flatten()
        
        self.comboBox_12.clear()
        self.comboBox_12.addItems(pls)
        self.comboBox_12.activated.connect(self.introduciubica)


    def introduciubica(self):
        suministro=str(self.comboBox_11.currentText())
        marca=str(self.comboBox_12.currentText())
        connection = sqlite3.connect("suministroinv.db")
        cursor = connection.cursor()
        selec='select ubicacion.Ubicacion from ubicacion join suministro on suministro.IdUbicación=ubicacion.IdUbicación where suministro.nombre="'+suministro+'" and suministro.marca="'+marca+'"'        
        cursor.execute(selec)
        pls=numpy.asarray(cursor.fetchall()).flatten()        
        self.comboBox_13.clear()
        self.comboBox_13.addItems(pls)

        
        
        ##Activacion de botones del formulario de utilizacion del suministro
        
    ##Darle tamano a las columnas de registros recientes y definir cabecera

    ##
    def gotoScreen2(self):
        screen2 = Screen2()
        widget.addWidget(screen2)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoScreen3(self):
        screen3 = Screen3()
        widget.addWidget(screen3)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotoScreen4(self):
        screen4 = Screen4()
        widget.addWidget(screen4)
        widget.setCurrentIndex(widget.currentIndex()+1)
        ## funciones de botones que permiten cambiar entre las pantallas
    
        ##hola = self.spinBox_3.value()
        ##consul="insert(nombre,apellido)values(?,?);"
        ##param = (hola, ape)

    def validar_datos(self):
        band = True
        alert = ""

        if len(self.comboBox_11.currentText()) == 0:
            alert = alert + "Por favor seleccione un suministro\n"
            band = False
        
        if len(self.lineEdit_4.text()) == 0:
            alert = alert + "Por favor describa para que se utilizo\n"
            band = False
        
        if len(self.comboBox_12.currentText()) == 0:
            alert = alert + "Por favor seleccione una marca\n"
            band = False
        
        if len(self.comboBox_13.currentText()) == 0:
            alert = alert + "Por favor seleccione una ubicacion\n"
            band = False

        if (self.doubleSpinBox_5.value()) == 0.00:
            alert = alert + "El campo de ingresar cantidad debe ser distinto a 0.\n"
            band = False
            
        if (self.spinBox_2.value()) == 0:
            alert = alert + "El campo de ingresar el numero de dias de la duracion de uso debe ser distinto a 0.\n"
            band = False
        
        if self.doubleSpinBox_5.value() > 0 and len(self.comboBox_12.currentText()) != 0 and len(self.comboBox_13.currentText()) != 0 and len(self.comboBox_11.currentText()) != 0:
            connection=sqlite3.connect('suministroinv.db')
            cursor=connection.cursor()
            select="select stock.cantidad from stock join suministro \
                on suministro.IdSum=stock.idSuministro \
                join ubicacion on  ubicacion.IdUbicación=suministro.IdUbicación \
                where ubicacion='"+ str(self.comboBox_13.currentText())+"' and suministro.nombre='"+ str(self.comboBox_11.currentText())+"' \
                and suministro.Marca='"+ str(self.comboBox_12.currentText())+"'"
            cursor.execute(select)
            comp=str(cursor.fetchone()[0])
            if self.doubleSpinBox_5.value() > float(comp):
                alert = alert + "Esta intentando usar mas suministros de los que hay\n"
                band = False

        if len(self.comboBox_9.currentText()) == 0:
            alert = alert + "Por favor seleccione la duracion de uso\n"
            band = False
        
        if (self.dateEdit.date().year()) < 2000:
            alert = alert + "El año debe ser mayor a 1999.\n"
            band = False

        if not band:

            dialog = QMessageBox()
            dialog.setText(alert)
            dialog.setWindowTitle('Aviso')
            dialog.setIcon(QMessageBox.Warning)
            dialog.setDetailedText(
                'Para poder completar un registro es necesario rellenar todos los campos')
            dialog.setStandardButtons(QMessageBox.Retry)
            dialog.exec_()

        else:
            self.registroutilizacion

        return band

    def registroutilizacion(self):
        if self.validar_datos():
            Nombre=str(self.comboBox_11.currentText())
            Marca=str(self.comboBox_12.currentText())
            Cantidad=float(self.doubleSpinBox_5.value())
            cantidadReusable=float(self.doubleSpinBox_4.value())
            ubicacion=str(self.comboBox_13.currentText())
            dia = self.dateEdit.date().day()
            if(int(dia)<10):
                dia = '0'+str(dia)
            else:
                dia=str(dia)
            mes = self.dateEdit.date().month()
            if(int(mes)<10):
                mes = '0'+str(mes)
            else:
                mes=str(mes)
            ano = self.dateEdit.date().year()
            ano = str(ano)        
            fechaUtil = ano + "-" + mes + "-" + dia
            Duracion=self.spinBox_2.value()
            descripcion=str(self.lineEdit_4.text())

            dialog = QMessageBox()
            dialog.setText('Registro completado')
            dialog.setWindowTitle('Aviso')
            dialog.setIcon(QMessageBox.NoIcon)
            dialog.setDetailedText(
                'El registro se ha completado exitosamente debido a que se llenaron todos los campos de manera adecuada.                                                                            Para poder ver el registro, dirigete a la pantalla de registros recientes o a la pantalla de reportes!')
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.exec_()

            connection=sqlite3.connect("suministroinv.db")
            cursor=connection.cursor()
            
            select='select ubicacion from ubicacion'
            cursor.execute(select)
            revision=cursor.fetchall()
            lista=numpy.asarray(revision)
            pls=lista.flatten()


            for word in pls:
                if ubicacion in word:
                    print(ubicacion, word)
                    a=1
                    
                    
            if a==1:
                select='Select IdUbicación from ubicacion where ubicacion="'+ubicacion+'";'
                cursor.execute(select)
                idubic=str(numpy.asarray(cursor.fetchone())[0])

            else:
                print('No existe tal ubicacion en la base de datos')
                quit()

            a=0

            connection.commit()



            select='select nombre from suministro where (marca="'+Marca+'" and idubicación='+idubic+')'
            cursor.execute(select)
            revision=cursor.fetchall()
            lista=numpy.asarray(revision)
            pls=lista.flatten()

            for word in pls:
                if Nombre in word:
                    select='select marca from suministro'
                    cursor.execute(select)
                    revision=cursor.fetchall()
                    lista=numpy.asarray(revision)
                    pls=lista.flatten()
                    for word in pls:
                        if Marca in word:
                            a=1

            if a==1:
                select='Select Idsum from suministro where (nombre="'+Nombre+'" AND Marca="'+Marca+'" AND IdUbicación='+idubic+')'
                cursor.execute(select)
                idsum=str(numpy.asarray((cursor.fetchone()))[0])


                update='update stock set cantidad=cantidad-'+str(Cantidad-cantidadReusable)+" where IdSuministro="+idsum
                cursor.execute(update)


            else:
                print("No se encontró el suministro especificado")
                quit()


            insert= "Insert into utilizacion (Descripcion, Cantidad, Cantidad_Reusable, Fecha_Utilización, Duracion_de_uso, suministro_IdSum) values \
                                ('"+descripcion+"',"+ str(Cantidad)+","+ str(cantidadReusable)+ ",'"+ fechaUtil+"' ,"+str(Duracion)+","+idsum+")"
            cursor.execute(insert)  

            connection.commit()

    def duraciondeuso_cantidad(self):
        print(self.spinBox_2.value())

    def duraciondeuso_escala(self):
        print(self.comboBox_9.currentText())

    def horasistema(self):

        DateTime = datetime.datetime.now()
        self.fecha.setText('Fecha: %s/%s/%s %s:%s' % (DateTime.day, DateTime.month, DateTime.year, DateTime.hour, DateTime.minute))

    
    '''
    def camposFaltantes(self):
        dialog = QMessageBox()
        dialog.setText('complete el registro')
        dialog.setWindowTitle('Aviso')
        dialog.setIcon(QMessageBox.Warning)
        dialog.setDetailedText(
            'Para poder completar un registro es necesario rellenar todos los campos')
        dialog.setStandardButtons(QMessageBox.Retry)
        dialog.exec_()'''     

    
    ## funciones de botones del formulario de utilizacion del suministro

    def registroreciente(self):
        connection = sqlite3.connect("suministroinv.db")
        cursor = connection.cursor()
        select = "select suministro.IdSum, suministro.Nombre, categoria.Nombre, stock.Cantidad, stock.Medida, suministro.Valor_unitario, stock.Cantidad * suministro.Valor_unitario as 'valortotal', ubicacion.Ubicacion, suministro.Marca from suministro join ubicacion on suministro.IdUbicación=ubicacion.IdUbicación join categoria on suministro.idCategoría=categoria.idCategoría join stock on stock.idSuministro=suministro.IdSum"
       
        self.tableWidget.setRowCount(100)
        tablerow = 0
        for row in cursor.execute(select):
            self.tableWidget.setItem(
                tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(
                tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.tableWidget.setItem(
                tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.tableWidget.setItem(
                tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.tableWidget.setItem(
                tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            self.tableWidget.setItem(
                tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
            self.tableWidget.setItem(
                tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
            self.tableWidget.setItem(
                tablerow, 7, QtWidgets.QTableWidgetItem(str(row[7])))
            self.tableWidget.setItem(
                tablerow, 8, QtWidgets.QTableWidgetItem(str(row[8])))
            tablerow += 1
            ##Explicar documentacion ahora

class Screen2(QMainWindow):


    def __init__(self):
        super(Screen2, self).__init__()
        loadUi("screen2.ui", self)
        self.botonreporteentradasum.clicked.connect(self.gotoScreen1)
        self.boton1_4.clicked.connect(self.gotoScreen1)
        self.boton1_7.clicked.connect(self.gotoScreen1)
        self.horasistema()
        #Cambiar pantallas

        a=1
        self.tableWidget.setColumnWidth(0, 50)
        while (a<=7):
           self.tableWidget.setColumnWidth(a, 100)
           a+=1        
        self.tableWidget.setHorizontalHeaderLabels(
            ["Id", "Fecha", "Suministro", "Marca", "Categoria", "Cantidad", "$/Unitario", "$ de Compra"])
        self.entrada()
        ##Darle tamano a las columnas del reporte de entrada y definir cabecera
        
        a=1
        self.tableWidget_2.setColumnWidth(0, 50)
        while (a<=7):
           self.tableWidget_2.setColumnWidth(a, 100)
           a+=1
        self.tableWidget_2.setHorizontalHeaderLabels(["ID", "Fecha", "Suministro", "Marca", "Cantidad", "Unidad", "Descripcion", "Cantidad reusable", "Coste total"])
        self.salida()
        # Darle tamano a las columnas del reporte de salida y definir cabecera
        
        a=1
        self.tableWidget_3.setColumnWidth(0, 50)
        while (a<=13):
           self.tableWidget_3.setColumnWidth(a, 70)
           a+=1
        self.tableWidget_3.setHorizontalHeaderLabels(["ID", "Categoria", "Suministro", "Marca", "ID-Entrada","Entrada", "ID-Salidad","Salida", "Stock", "$ Unitario", "$ total", "Ubicacion"])
        self.stock()
        # Darle tamano a las columnas del reporte de stock y definir cabecera

    def horasistema(self):
        DateTime = datetime.datetime.now()
        self.fecha_2.setText('Fecha: %s/%s/%s %s:%s' % (DateTime.day, DateTime.month, DateTime.year, DateTime.hour, DateTime.minute))
        self.fecha.setText('Fecha: %s/%s/%s %s:%s' % (DateTime.day, DateTime.month, DateTime.year, DateTime.hour, DateTime.minute))
        self.fecha_3.setText('Fecha: %s/%s/%s %s:%s' % (DateTime.day, DateTime.month, DateTime.year, DateTime.hour, DateTime.minute))

    def gotoScreen1(self):
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)
        #funcion para volver a la primera pantalla

    def entrada(self):
        connection = sqlite3.connect("suministroinv.db")
        cursor = connection.cursor()
        select = "Select entrada.IdEntrada as 'Id', entrada.Fecha_entrada, suministro.nombre, suministro.marca, categoria.Nombre, entrada.cantidad, suministro.valor_unitario as 'Valor unitario', entrada.Valor_de_Compra as 'Valor de compra'  from suministro join categoria on categoria.idCategoría=suministro.IdCategoría inner join entrada on entrada.suministro_IdSum=suministro.idsum order by IdEntrada"

        self.tableWidget.setRowCount(100)
        tablerow = 0
        print(cursor.execute(select))

        for row in cursor.execute(select):
            self.tableWidget.setItem(
                tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(
                tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.tableWidget.setItem(
                tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.tableWidget.setItem(
                tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.tableWidget.setItem(
                tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            self.tableWidget.setItem(
                tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
            self.tableWidget.setItem(
                tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
            self.tableWidget.setItem(
                tablerow, 7, QtWidgets.QTableWidgetItem(str(row[7])))
            
            tablerow += 1
        ##Funcion que realiza el reporte de entrada

    def salida(self):
        connection = sqlite3.connect("suministroinv.db")
        cursor = connection.cursor()
        select = "select utilizacion.IdUtil, utilizacion.Fecha_Utilización, suministro.Nombre, suministro.Marca, utilizacion.Cantidad, stock.Medida, utilizacion.Descripcion, utilizacion.Cantidad_Reusable, (utilizacion.Cantidad-utilizacion.Cantidad_Reusable)* suministro.Valor_unitario as 'Valor total'  from utilizacion  join suministro on suministro.IdSum=utilizacion.suministro_IdSum  join stock on suministro.IdSum=stock.idSuministro"

        self.tableWidget_2.setRowCount(100)
        tablerow = 0
        for row in cursor.execute(select):
            self.tableWidget_2.setItem(
                tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.tableWidget_2.setItem(
                tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.tableWidget_2.setItem(
                tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.tableWidget_2.setItem(
                tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.tableWidget_2.setItem(
                tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            self.tableWidget_2.setItem(
                tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
            self.tableWidget_2.setItem(
                tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
            self.tableWidget_2.setItem(
                tablerow, 7, QtWidgets.QTableWidgetItem(str(row[7])))
            self.tableWidget_2.setItem(
                tablerow, 8, QtWidgets.QTableWidgetItem(str(row[8])))
            tablerow += 1
        # Funcion que realiza el reporte de salida

    def stock(self):
        connection=sqlite3.connect("suministroinv.db")
        cursor=connection.cursor()
        select="select suministro.IdSum, categoria.Nombre, suministro.Nombre, suministro.marca, entrada.identrada, entrada.cantidad as 'Entrada', utilizacion.IdUtil as 'IdSalidad' ,utilizacion.cantidad-utilizacion.cantidad_reusable as 'salida', stock.Cantidad, suministro.valor_unitario, (stock.Cantidad*suministro.valor_unitario) as '$total', ubicacion.Ubicacion from suministro join ubicacion on suministro.IdUbicación=ubicacion.IdUbicación join categoria on suministro.idCategoría=categoria.idCategoría join stock on stock.idSuministro=suministro.IdSum left join entrada on suministro.IdSum=entrada.suministro_IdSum left join utilizacion on utilizacion.suministro_IdSum=suministro.IdSum"

        self.tableWidget_3.setRowCount(100)
        tablerow=0
        for row in cursor.execute(select):
               self.tableWidget_3.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
               self.tableWidget_3.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
               self.tableWidget_3.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
               self.tableWidget_3.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
               self.tableWidget_3.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
               self.tableWidget_3.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
               self.tableWidget_3.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
               self.tableWidget_3.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(str(row[7])))
               self.tableWidget_3.setItem(tablerow, 8, QtWidgets.QTableWidgetItem(str(row[8])))
               self.tableWidget_3.setItem(tablerow, 9, QtWidgets.QTableWidgetItem(str(row[9])))
               self.tableWidget_3.setItem(tablerow, 10, QtWidgets.QTableWidgetItem(str(row[10])))
               self.tableWidget_3.setItem(tablerow, 11, QtWidgets.QTableWidgetItem(str(row[11])))
               tablerow+=1

    

class Screen3(QMainWindow):

    def __init__(self):
        super(Screen3, self).__init__()
        loadUi("screen3.ui", self)
        ##
        self.botonforsumnue.clicked.connect(self.gotoScreen1)
        ##funcion del boton para volver a la primera pantalla
        self.introducircategoria()
        self.introducirmarca()
        self.introducirsuministro()
        self.introduciubica()
        ##Si se definen todas las variables dentro de este, no hay que hacerlo varias veces
        self.boton3.clicked.connect(self.registrarentradanueva)
        #self.boton3.clicked.connect(self.camposFaltantes)
        #comento campos faltantes por que aunque llene todos los campos no me deja por algun motivo
       


        # activacion de botones del formulario de entrada de datos (suministro nuevo)
    ##
    def nuevosuministro(self):
        flag=str(self.comboBox_5.currentText())
        if(flag=="Nuevo Suministro"):   
            name, done1=QtWidgets.QInputDialog.getText(
                self, 'Digite un dato nuevo', 'Coloque el texto del suministro aqui'
             )
            if(done1==True):
                self.comboBox_5.addItem(str(name))
                index=self.comboBox_5.findText(name, QtCore.Qt.MatchFixedString)
                self.comboBox_5.setCurrentIndex(index)  

    def gotoScreen1(self):
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)
    ## funcion del boton para volver a la primera pantalla
   
    def nuevacategoria(self):
        flag=str(self.comboBox_2.currentText())
        if(flag=="Nueva Categoria"):   
            name, done1=QtWidgets.QInputDialog.getText(
                self, 'Digite un dato nuevo', 'Coloque el texto del suministro aqui'
             )
            if(done1==True):
                self.comboBox_2.addItem(str(name)) 
                index=self.comboBox_2.findText(name, QtCore.Qt.MatchFixedString)
                self.comboBox_2.setCurrentIndex(index)  
    
    def introducircategoria(self):
        connection = sqlite3.connect("suministroinv.db")
        cursor = connection.cursor()
        selec='Select nombre from categoria'
        cursor.execute(selec)
        pls=numpy.asarray(cursor.fetchall()).flatten()
        self.comboBox_2.clear(); 
        self.comboBox_2.addItems(pls)
        self.comboBox_2.addItem("Nueva Categoria")
        self.comboBox_2.activated.connect(self.nuevacategoria)

    def introducirsuministro(self):
        connection = sqlite3.connect("suministroinv.db")
        cursor = connection.cursor()
        selec='Select DISTINCT nombre from suministro'
        cursor.execute(selec)
        pls=numpy.asarray(cursor.fetchall()).flatten()    
        self.comboBox_5.clear(); 
        self.comboBox_5.addItems(pls)
        self.comboBox_5.addItem("Nuevo Suministro")
        self.comboBox_5.activated.connect(self.nuevosuministro)
        
    def nuevamarca(self):
        flag=str(self.comboBox_3.currentText())
        if(flag=="Nueva Marca"):   
            name, done1=QtWidgets.QInputDialog.getText(
                self, 'Digite un dato nuevo', 'Coloque el texto del suministro aqui'
             )
            if(done1==True):
                self.comboBox_3.addItem(str(name))     
                index=self.comboBox_3.findText(name, QtCore.Qt.MatchFixedString)
                self.comboBox_3.setCurrentIndex(index)  
           
    
    def introducirmarca(self):
        connection = sqlite3.connect("suministroinv.db")
        cursor = connection.cursor()
        selec='Select DISTINCT marca from suministro'
        cursor.execute(selec)
        pls=numpy.asarray(cursor.fetchall()).flatten()
        self.comboBox_3.clear()
        self.comboBox_3.addItems(pls)
        self.comboBox_3.addItem("Nueva Marca")
        self.comboBox_3.activated.connect(self.nuevamarca)

    def nuevaubicacion(self):
        flag=str(self.comboBox.currentText())
        if(flag=="Nueva Ubicación"):   
            name, done1=QtWidgets.QInputDialog.getText(
                self, 'Digite un dato nuevo', 'Coloque el texto del suministro aqui'
             )
            if(done1==True):
                self.comboBox.addItem(str(name)) 
                index=self.comboBox.findText(name, QtCore.Qt.MatchFixedString)
                self.comboBox.setCurrentIndex(index)  

    def introduciubica(self):
        connection = sqlite3.connect("suministroinv.db")
        cursor = connection.cursor()
        selec='select ubicacion.Ubicacion from ubicacion'        
        cursor.execute(selec)
        pls=numpy.asarray(cursor.fetchall()).flatten()
        self.comboBox.clear()
        self.comboBox.addItems(pls)
        self.comboBox.addItem("Nueva Ubicación")
        self.comboBox.activated.connect(self.nuevaubicacion)

    def sifuepres(self):
        perecedero=1
        print(perecedero)

    def nofuepres(self):
        perecedero=0
        print(perecedero)

    def validar_datos(self):
        band = True
        alert = ""

        if (self.comboBox_5.currentText()) == 'Nuevo Suministro':
            alert = alert + "Por favor seleccione o cree un suministro\n"
            band = False

        if (self.comboBox_3.currentText()) == 'Nueva Marca':
            alert = alert + "Por favor seleccione o cree una marca.\n"
            band = False

        if (self.comboBox_2.currentText()) == 'Nueva Categoria':
            alert = alert + "Por favor seleccione o cree una categoria.\n"
            band = False

        if (self.comboBox.currentText()) == 'Nueva Ubicación':
            alert = alert + "Por favor seleccione o cree una ubicacion.\n"
            band = False

        if (self.doubleSpinBox.value()) == 0.00:
            alert = alert + "El campo de ingresar cantidad debe ser distinto a 0.\n"
            band = False

        if len(self.lineEdit_5.currentText()) == 0:
            alert = alert + "El campo de Ingresar medida no debe estar vacio.\n"
            band = False

        if (self.doubleSpinBox_3.value()) == 0.00:
            alert = alert + "El campo de Ingresar valor unitario debe ser distinto a 0.\n"
            band = False

        if (self.dateEdit.date().year()) < 2000:
            alert = alert + "El año debe ser mayor a 1999.\n"
            band = False

        if (self.radioButton_3.isChecked()) == 0 and (self.radioButton_4.isChecked()) == 0:
            alert = alert + "Por favor indicar si el producto es perecedero o no\n"
            band = False
            
            

        if not band:
            
            dialog = QMessageBox()
            dialog.setText(alert)
            dialog.setWindowTitle('Aviso')
            dialog.setIcon(QMessageBox.Warning)
            dialog.setDetailedText(
                'Para poder completar un registro es necesario rellenar todos los campos')
            dialog.setStandardButtons(QMessageBox.Retry)
            dialog.exec_()

        else:
            self.registrarentradanueva

        return band

    def registrarentradanueva(self):
        if self.validar_datos():
            Nombre = str(self.comboBox_5.currentText())
            Marca = str(self.comboBox_3.currentText())
            Categoria =str(self.comboBox_2.currentText())
            ubicacion = str(self.comboBox.currentText())
            Cantidad = float(self.doubleSpinBox.value())
            medida = str(self.lineEdit_5.currentText())
            ValorUnitario = float(self.doubleSpinBox_3.value())
            ValorCompra = Cantidad*ValorUnitario
            dia = self.dateEdit.date().day()
            if(int(dia)<10):
                dia = '0'+str(dia)
            else:
                dia=str(dia)
            print(dia)
            mes = self.dateEdit.date().month()
            if(int(mes)<10):
                mes = '0'+str(mes)
            else:
                mes=str(mes)
            print(mes)
            ano = self.dateEdit.date().year()
            ano = str(ano)
            print(ano)
            fechaEntrada = ano + "-" + mes + "-" + dia
            print(fechaEntrada)
            vidautil=self.spinBox.value()
            a=0
            perecedero=2
            if self.radioButton_3.isChecked():
                perecedero=1
            if self.radioButton_4.isChecked():
                perecedero=0
            print(int(fechaEntrada[0:4]),int(fechaEntrada[5:7]), int(fechaEntrada[8:10]))
        
            dialog = QMessageBox()
            dialog.setText('Registro completado')
            dialog.setWindowTitle('Aviso')
            dialog.setIcon(QMessageBox.NoIcon)
            dialog.setDetailedText(
                'El registro se ha completado exitosamente debido a que se llenaron todos los campos de manera adecuada.                                                                            Para poder ver el registro, dirigete a la pantalla de registros recientes o a la pantalla de reportes!')
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.exec_()
        
            connection=sqlite3.connect("suministroinv.db")
            cursor=connection.cursor()

            select='select ubicacion from ubicacion'
            cursor.execute(select)
            revision=cursor.fetchall()
            lista=numpy.asarray(revision)
            pls=lista.flatten()


            for word in pls:
                if ubicacion in word:
                    a=1
                    
            if a==1:
                select='Select IdUbicación from ubicacion where ubicacion="'+ubicacion+'";'
                cursor.execute(select)
                idubic=str(numpy.asarray(cursor.fetchone())[0])

            else:
                insert= "Insert into ubicacion (Ubicacion) values ('"+ ubicacion+"')"
                cursor.execute(insert)
                connection.commit()
                select='Select IdUbicación from ubicacion where ubicacion="'+ubicacion+'";'
                cursor.execute(select)
                idubic=str(numpy.asarray(cursor.fetchone())[0])


            a=0

            select='select nombre from categoria'
            cursor.execute(select)
            revision=cursor.fetchall()
            lista=numpy.asarray(revision)
            pls=lista.flatten()

            for word in pls:
                if Categoria in word:
                    a=1
                
                    
            if a==1:
                select='Select IdCategoría from categoria where Nombre="'+Categoria+'";'
                cursor.execute(select)
                IdCategoría=str(numpy.asarray(cursor.fetchone())[0])

            else:
                insert= "Insert into categoria (Nombre) values ('"+ Categoria+"')"
                cursor.execute(insert)
                connection.commit()
                select='Select IdCategoría from categoria where Nombre="'+Categoria+'";'
                cursor.execute(select)
                IdCategoría=str(numpy.asarray(cursor.fetchone())[0])
                
            a=0


            connection.commit()



            select='select nombre from suministro where (IdCategoría='+IdCategoría+' AND idubicación='+idubic+')'
            cursor.execute(select)
            revision=cursor.fetchall()
            lista=numpy.asarray(revision)
            pls=lista.flatten()

            for word in pls:
                if Nombre in word:
                    select='select marca from suministro'
                    cursor.execute(select)
                    revision=cursor.fetchall()
                    lista=numpy.asarray(revision)
                    pls=lista.flatten()
                    for word in pls:
                        if Marca in word:
                            a=1

            if a==1:
                select='Select Idsum from suministro where (nombre="'+Nombre+'" AND Marca="'+Marca+'" AND IdUbicación='+idubic+')'
                cursor.execute(select)
                idsum=str(numpy.asarray((cursor.fetchone()))[0])

                
                update='update stock set cantidad=cantidad+'+str(Cantidad)+" where IdSuministro="+idsum
                cursor.execute(update)
            

            else:
                if perecedero==1:
                    insert= "Insert into suministro(Nombre, Marca, Valor_unitario, VidaÚtil, IdCategoría, IdUbicación) values ('"+ Nombre+"', '"+ Marca+"',"+ str(ValorUnitario)+","+str(vidautil)+ "," +IdCategoría+ "," +idubic+ ')'
                    cursor.execute(insert)
                    select='Select Idsum from suministro where (nombre="'+Nombre+'" AND Marca="'+Marca+'" AND IdUbicación='+idubic+')'
                    cursor.execute(select)
                    idsum=str(numpy.asarray((cursor.fetchone()))[0])
                    fechaCaduc=datetime.date(int(fechaEntrada[0:4]),int(fechaEntrada[5:7]), int(fechaEntrada[8  :10]))                    
                    insert= 'Insert into condicion(suministro_IdSum, Perecedero, Fecha_Caducidad) values (' +str(idsum)+','+str(perecedero)+',"'+str(fechaCaduc+timedelta(days=vidautil))+'")'
                    cursor.execute(insert)

                if perecedero==0:
                    insert="Insert into suministro(Nombre, Marca, Valor_unitario, IdCategoría, IdUbicación) values ('"+ Nombre+"', '"+ Marca+"',"+ str(ValorUnitario)+"," +IdCategoría+ "," +idubic+ ')'
                    cursor.execute(insert)
                    select='Select Idsum from suministro where (nombre="'+Nombre+'" AND Marca="'+Marca+'" AND IdUbicación='+idubic+')'
                    cursor.execute(select)
                    idsum=str(numpy.asarray((cursor.fetchone()))[0])
                    insert= 'Insert into condicion(suministro_IdSum, Perecedero) values ('+str(idsum)+','+str(perecedero)+')'
                    cursor.execute(insert)
                
                insert= "Insert into stock (idSuministro, cantidad, medida) values ("+idsum+","+str(Cantidad) +",'"+ medida+"')"
                cursor.execute(insert)

            insert= "Insert into entrada (Cantidad, Fecha_entrada, Valor_de_Compra, suministro_IdSum) values ('"+ str(Cantidad)+"', '"+ fechaEntrada+"',"+str(ValorCompra)+","+idsum+")"
            cursor.execute(insert)  

            connection.commit()
        
    ##Con esto ya se pueden introducir valores en la bdd. Si puedes, repite esta en la de suministro nuevo
    # pero cambiandole lo que recibe la fecha
    #   

    # funciones que recogen los datos de los campos de texto,  los convierten en variables cuando se presiona el boton del formulario de entrada de datos (suministro nuevo)
    
    '''
    def camposFaltantes(self):
        dialog = QMessageBox()
        dialog.setText('complete el registro')
        dialog.setWindowTitle('Aviso')
        dialog.setIcon(QMessageBox.Warning)
        dialog.setDetailedText('Para poder completar un registro es necesario rellenar todos los campos')
        dialog.setStandardButtons(QMessageBox.Retry)
        dialog.exec_()  '''        
        ##Pantalla para cuando hay un error aun no se usara

class Screen4(QMainWindow):

    def __init__(self):
        super(Screen4, self).__init__()
        loadUi("screen4.ui", self)

        self.botonformusumexis.clicked.connect(self.gotoScreen1)
        #conexion del boton a la funcion
        
        self.boton3.clicked.connect(self.registrarentradanueva)
        #self.boton3.clicked.connect(self.camposFaltantes)
        self.introducircategoria()


    def gotoScreen1(self):
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)
        # funcion del boton para volver a la primera pantalla

    def fechadeentrad(self):
        dia = self.dateEdit_2.date().day()
        dia = str(dia)
        mes = self.dateEdit_2.date().month()
        mes = str(mes)
        ano = self.dateEdit_2.date().year()
        ano = str(ano)
        fecha = ano + "-" + mes + "-" + dia

    def introducircategoria(self):
        connection = sqlite3.connect("suministroinv.db")
        cursor = connection.cursor()
        selec='Select nombre from categoria'
        cursor.execute(selec)
        pls=numpy.asarray(cursor.fetchall()).flatten()
        
        self.comboBox_4.clear(); self.comboBox_3.clear(); self.comboBox_2.clear(); self.comboBox.clear()
        self.comboBox_4.addItems(pls)
        self.comboBox_4.activated.connect(self.introducirsuministro)

    def introducirsuministro(self):
        categoria=str(self.comboBox_4.currentText())
        connection = sqlite3.connect("suministroinv.db")
        cursor = connection.cursor()
        selec='select DISTINCT suministro.nombre from suministro join categoria on suministro.IdCategoría=categoria.idCategoría where categoria.Nombre="'+categoria+'"'
        cursor.execute(selec)
        pls=numpy.asarray(cursor.fetchall()).flatten()
        
        self.comboBox_2.clear()
        self.comboBox_2.addItems(pls)
        self.comboBox_2.activated.connect(self.introducirmarca)
    
    def introducirmarca(self):
        suministro=str(self.comboBox_2.currentText())
        connection = sqlite3.connect("suministroinv.db")
        cursor = connection.cursor()
        selec='Select DISTINCT marca from suministro where nombre="'+suministro+'"'
        cursor.execute(selec)
        pls=numpy.asarray(cursor.fetchall()).flatten()
        
        self.comboBox.clear()
        self.comboBox.addItems(pls)
        self.comboBox.activated.connect(self.introduciubica)


    def introduciubica(self):
        suministro=str(self.comboBox_2.currentText())
        marca=str(self.comboBox.currentText())
        connection = sqlite3.connect("suministroinv.db")
        cursor = connection.cursor()
        selec='select ubicacion.Ubicacion from ubicacion join suministro on suministro.IdUbicación=ubicacion.IdUbicación where suministro.nombre="'+suministro+'" and suministro.marca="'+marca+'"'        
        cursor.execute(selec)
        pls=numpy.asarray(cursor.fetchall()).flatten()        
        self.comboBox_3.clear()
        self.comboBox_3.addItems(pls)

    def validar_datos(self):
        band = True
        alert = ""

        '''
        if (self.comboBox_4.currentText()) == 'Nuevo Suministro':
            alert = alert + "Por favor seleccione o cree un suministro\n"

            band = False'''

        if len(self.comboBox_2.currentText()) == 0:
            alert = alert + "Por favor seleccione un nombre del suministro\n"
            band = False

        if len(self.comboBox.currentText()) == 0:
            alert = alert + "Por favor seleccione una marca\n"
            band = False

        if len(self.comboBox_3.currentText()) == 0:
            alert = alert + "Por favor seleccione una ubicacion\n"
            band = False

        if (self.doubleSpinBox.value()) == 0.00:
            alert = alert + "El campo de ingresar cantidad debe ser distinto a 0.\n"
            band = False

        if len(self.lineEdit_5.currentText()) == 0:
            alert = alert + "El campo de medida no debe estar vacio\n"
            band = False

        if (self.doubleSpinBox_3.value()) == 0.00:
            alert = alert + "El campo de ingresar valor unitario debe ser distinto a 0.\n"
            band = False

        if (self.dateEdit_2.date().year()) < 2000:
            alert = alert + "El año debe ser mayor a 1999.\n"
            band = False


        if not band:

            dialog = QMessageBox()
            dialog.setText(alert)
            dialog.setWindowTitle('Aviso')
            dialog.setIcon(QMessageBox.Warning)
            dialog.setDetailedText(
                'Para poder completar un registro es necesario rellenar todos los campos')
            dialog.setStandardButtons(QMessageBox.Retry)
            dialog.exec_()

        else:
            self.registrarentradanueva

        return band

    def registrarentradanueva(self):
        if self.validar_datos():
            Nombre = str(self.comboBox_2.currentText())
            Marca = str(self.comboBox.currentText())
            Categoria =str(self.comboBox_4.currentText())
            ubicacion = str(self.comboBox_3.currentText())
            Cantidad = float(self.doubleSpinBox.value())
            medida = str(self.lineEdit_5.currentText())
            ValorUnitario = float(self.doubleSpinBox_3.value())
            ValorCompra = Cantidad*ValorUnitario
            dia = self.dateEdit_2.date().day()

            if(int(dia)<10):
                dia = '0'+str(dia)
            else:
                dia=str(dia)
            mes = self.dateEdit_2.date().month()
            if(int(mes)<10):
                mes = '0'+str(mes)
            else:
                mes=str(mes)
            ano = self.dateEdit_2.date().year()
            ano = str(ano)
            fechaEntrada = ano + "-" + mes + "-" + dia
            a=0

            dialog = QMessageBox()
            dialog.setText('Registro completado')
            dialog.setWindowTitle('Aviso')
            dialog.setIcon(QMessageBox.NoIcon)
            dialog.setDetailedText(
                'El registro se ha completado exitosamente debido a que se llenaron todos los campos de manera adecuada.                                                                            Para poder ver el registro, dirigete a la pantalla de registros recientes o a la pantalla de reportes!')
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.exec_()

            connection=sqlite3.connect("suministroinv.db")
            cursor=connection.cursor()

            select='select ubicacion from ubicacion'
            cursor.execute(select)
            revision=cursor.fetchall()
            lista=numpy.asarray(revision)
            pls=lista.flatten()


            for word in pls:
                if ubicacion in word:
                    a=1
                    
            if a==1:
                select='Select IdUbicación from ubicacion where ubicacion="'+ubicacion+'";'
                cursor.execute(select)
                idubic=str(numpy.asarray(cursor.fetchone())[0])

            else:
                insert= "Insert into ubicacion (Ubicacion) values ('"+ ubicacion+"')"
                cursor.execute(insert)
                connection.commit()
                select='Select IdUbicación from ubicacion where ubicacion="'+ubicacion+'";'
                cursor.execute(select)
                idubic=str(numpy.asarray(cursor.fetchone())[0])


            a=0

            select='select nombre from categoria'
            cursor.execute(select)
            revision=cursor.fetchall()
            lista=numpy.asarray(revision)
            pls=lista.flatten()

            for word in pls:
                if Categoria in word:
                    a=1
                
                    
            if a==1:
                select='Select IdCategoría from categoria where Nombre="'+Categoria+'";'
                cursor.execute(select)
                IdCategoría=str(numpy.asarray(cursor.fetchone())[0])

            else:
                insert= "Insert into categoria (Nombre) values ('"+ Categoria+"')"
                cursor.execute(insert)
                connection.commit()
                select='Select IdCategoría from categoria where Nombre="'+Categoria+'";'
                cursor.execute(select)
                IdCategoría=str(numpy.asarray(cursor.fetchone())[0])
                
            a=0


            connection.commit()



            select='select nombre from suministro where (IdCategoría='+IdCategoría+' AND idubicación='+idubic+')'
            cursor.execute(select)
            revision=cursor.fetchall()
            lista=numpy.asarray(revision)
            pls=lista.flatten()

            for word in pls:
                if Nombre in word:
                    select='select marca from suministro'
                    cursor.execute(select)
                    revision=cursor.fetchall()
                    lista=numpy.asarray(revision)
                    pls=lista.flatten()
                    for word in pls:
                        if Marca in word:
                            a=1

            if a==1:
                select='Select Idsum from suministro where (nombre="'+Nombre+'" AND Marca="'+Marca+'" AND IdUbicación='+idubic+')'
                cursor.execute(select)
                idsum=str(numpy.asarray((cursor.fetchone()))[0])

                
                update='update stock set cantidad=cantidad+'+str(Cantidad)+" where IdSuministro="+idsum
                cursor.execute(update)
            insert= "Insert into entrada (Cantidad, Fecha_entrada, Valor_de_Compra, suministro_IdSum) values ('"+ str(Cantidad)+"', '"+ fechaEntrada+"',"+str(ValorCompra)+","+idsum+")"
            cursor.execute(insert)
            

            connection.commit()
    



app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
mainwindow = MainWindow()
QDate.currentDate().toPyDate()

widget.addWidget(mainwindow)

widget.setFixedHeight(539)
widget.setFixedWidth(779)


widget.show()


try:
    sys.exit(app.exec_())
except:
    print("Exiting")
