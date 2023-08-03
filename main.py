
import sys
from formulas import * 



import psutil
from PyQt5.QtCore import QTimer

import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows


from PyQt5.QtWidgets import (QDockWidget , QMainWindow,QApplication,QAction,QMenu,QLabel,QPushButton,
                            QWidget,QHBoxLayout,QSplitter,QComboBox,QHBoxLayout,QVBoxLayout,QTabWidget,
                            QDoubleSpinBox,QFrame,QCheckBox,QMessageBox,QTableWidget,QTableWidgetItem,QMenuBar,QStatusBar)

from PyQt5.QtCore import QFile, QTextStream


#___________________________________________________________________________________________________________
### base de datos 
class Unidades():
    def __init__ (self):
        self.angulos="Grados"
        self.distancias="Metros"
        self.decimales=4

class Preferencias():
    def __init__ (self):
        self.tema="claro"
        



class Cimentacion():
    def __init__(self):
        self.unidades=Unidades()
        self.cohesion=1
        self.anguloFriccion=0
        self.pesoEspecifico=3
        self.nivelFreatico=False
        self.profundidadFreatica=4
        self.pesoEspecificoSaturado=5
        self.ancho=2
        self.longitud=2
        self.profundidad=8
        self.inclinacion=9
       #factores de carga
        self.Nq=calcularNq(self.anguloFriccion,self.unidades.angulos)
        self.Nc=calcularNc(self.anguloFriccion,self.unidades.angulos)
        self.Ny=calcularNy(self.anguloFriccion,self.unidades.angulos)

       #factores de forma
        self.Fqs=calcularFqs(self.ancho,self.longitud,self.anguloFriccion,self.unidades.angulos,self.unidades.distancias)
        self.Fcs=calcularFcs(self.ancho,self.longitud,self.Nq,self.Nc,self.unidades.distancias)
        self.Fys=calcularFys(self.ancho,self.longitud,self.unidades.distancias)
       
       #factores de profundidad
        (self.Fqd,self.Fcd,self.Fyd)=calcularFactoresprofundidad(self.anguloFriccion,self.profundidad,self.ancho,self.Nc,self.unidades.angulos,self.unidades.distancias)
       
       #factores inclinacion 
        self.Fqi=calcularFci(self.inclinacion,self.unidades.angulos)
        self.Fci=self.Fqi
        self.Fyi=calcularFyi(self.inclinacion,self.anguloFriccion,self.unidades.angulos)

### clases moldes 
class Ventana(QDockWidget):
    #descripcion: es una ventana que se puede conectar con una accion para activarla y desactivarla , en cuanto se cierra ella desactiva dicha accion 
    def __init__(self,accionagregar=None):
        super().__init__()
        
        ##Conectamos con la accionagregar 
        self.accionagregar=accionagregar
        if self.accionagregar!=None:
            self.accionagregar.triggered.connect(self.connectarAction)
        
        ### configutamos el diseño de la pestaña 
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
    def closeEvent (self,event):
        if self.accionagregar != None:
            self.accionagregar.setChecked(False)
            event.accept()
        else: 
            event.accept()
    def connectarAction(self,Checked):
        if Checked==True:
            self.show()
        else: 
            self.hide()

### ventanas secundarias 
class VentanaPreferencias(QWidget):
    def __init__(self):
        super().__init__()
     ## configuraciones  objeto Ventana Preferencia
        self.setWindowTitle("Preferencias")
        self.anchoVentana=400
        self.altoVentana=300
        self.setFixedSize(self.anchoVentana,self.altoVentana)   
        self.setObjectName("Preferencias") 
        self.setProperty("class", "Preferencias")
        if preferencias.tema=="oscuro":
            self.cargar_css("styles/dark/estilospreferencias.css")
        elif preferencias.tema=="claro":
            self.cargar_css("styles/clear/estilospreferencias.css")
     ## layout del objeto objeto Ventana Preferencia  
        self.layout=QVBoxLayout() 
        self.setLayout(self.layout)
        self.layout.setContentsMargins(1,1,1,1)

     ## widgetcentral del layout (Tabla)
        self.tabla = QTabWidget()
        self.layout.addWidget(self.tabla)     
        
      
    
        
        ##______________________________________________________________________________________________________
        ## ficha Preferencia de Unidades
        ##______________________________________________________________________________________________________
        
    

        self.seccionUnidades=QWidget()
        self.tabla.addTab(self.seccionUnidades,"Unidades")    
        self.seccionUnidades.setObjectName("Unidades") 
        self.seccionUnidades.setProperty("class", "Unidades")
        #                                     ##creamos los widgets 

        self.labelAngulos=QLabel("Angulos................",self.seccionUnidades) 
        
        self.seleccionunidadesAngulos=QComboBox(self.seccionUnidades) 
        self.seleccionunidadesAngulos.addItem("Grados")  
        self.seleccionunidadesAngulos.addItem("Radianes") 
        self.seleccionunidadesAngulos.setCurrentText(datos.unidades.angulos) ### configuracion  estado inicial del widget  
        
         

        self.labelDistancia=QLabel("Distancia..............",self.seccionUnidades) 

        self.seleccionunidadesDistancias=QComboBox(self.seccionUnidades) 
        self.seleccionunidadesDistancias.addItem("Metros")  
        self.seleccionunidadesAngulos.setCurrentText(datos.unidades.distancias) ## configuramos el estado inicial del widget 
                   
                                        ##agregamos los widgets a la ficha unidades 
        
        ##agregamos los label 
        posx=10 
        posy=10 ### posicion del primer objeto 
        dimy=25
        dimx=100
        separacionvertical=5
        for i in (self.labelAngulos,self.labelDistancia):
            i.setGeometry(posx,posy,dimx,dimy)
            posy=posy+dimy+separacionvertical

        
        ###agregamos los combobox delante de los label 
        posx=posx+dimx+2  ## no mover
        posy=10  ### posicion del primer objeto 
        dimy=25
        dimx=200
        for i in (self.seleccionunidadesAngulos,self.seleccionunidadesDistancias):
            i.setGeometry(posx,posy,dimx,dimy)
            posy=posy+dimy+separacionvertical


        ##______________________________________________________________________________________________________
        ## ficha Preferencia de Interfaz
        ##_____________________________________________________________________________________________________
        self.seccionInterfaz=QWidget()
        self.tabla.addTab(self.seccionInterfaz,"Interfaz")    
        ## creamos los widgets 
        self.labelTema=QLabel("Tema................",self.seccionInterfaz) 
        
        self.seleccionInterfazTema=QComboBox(self.seccionInterfaz) 
        self.seleccionInterfazTema.addItem("oscuro")  
        self.seleccionInterfazTema.addItem("claro") 
        self.seleccionInterfazTema.setCurrentText(preferencias.tema)
        ##                               agregamos los widgets a la ficha unidades  
                ##agregamos los label 
        posx=10 
        posy=10 ### posicion del primer objeto 
        dimy=25
        dimx=100
        separacionvertical=5
        for i in (self.labelTema,):
            i.setGeometry(posx,posy,dimx,dimy)
            posy=posy+dimy+separacionvertical

        ###agregamos los combobox delante de los label 
        posx=posx+dimx+2  ## no mover
        posy=10  ### posicion del primer objeto 
        dimy=25
        dimx=200
        for i in (self.seleccionInterfazTema,):
            i.setGeometry(posx,posy,dimx,dimy)
            posy=posy+dimy+separacionvertical
        #________________________________________________________________________________________________________-
        # Botones de control
        #_______________________________________________________________________________________________    
        
        self.botonAceptar=QPushButton("Aceptar", self)
        self.botonAceptar.clicked.connect(self.funcionAceptar)
        
        self.botonCancelar=QPushButton("Cancelar", self)
        self.botonCancelar.clicked.connect(self.funcionCancelar)

        dimy=25
        dimx=100
        self.botonAceptar.setGeometry(self.anchoVentana-dimx-10,self.altoVentana-dimy-10,dimx,dimy)
        self.botonCancelar.setGeometry(self.anchoVentana-2*dimx-15,self.altoVentana-dimy-10,dimx,dimy)
        
        
        
        

        


   
    def funcionCancelar(self):
        self.close()
    def funcionAceptar(self):
        global ventanaprincipal
        ## extraemos la informacion registrada ventana preferencias 
        unidadesangulos=self.seleccionunidadesAngulos.currentText()
        unidadesdistancia=self.seleccionunidadesDistancias.currentText()
        preferenciatema=self.seleccionInterfazTema.currentText()
        ### comparamos y hacemos cambios 
        if datos.unidades.angulos==unidadesangulos:
            pass
        elif datos.unidades.angulos!=unidadesangulos:
            if unidadesangulos=="Grados": 
                datos.unidades.angulos="Grados"#actualizo unidades 
                
                ###cambio el valor del angulo Friccion a grados 
                datos.anguloFriccion=grados(datos.anguloFriccion)
                ##actualizo la entrada del angulo de friccion 
                ventanaprincipal.ventanacentral.ventanadedatos.entradaAnguloFriccion.setMaximum(89)
                ventanaprincipal.ventanacentral.ventanadedatos.entradaAnguloFriccion.setSingleStep(1) 
                ventanaprincipal.ventanacentral.ventanadedatos.entradaAnguloFriccion.setValue(datos.anguloFriccion)

                ### cambio el valor de inclinacion a grados
                datos.inclinacion=grados(datos.inclinacion)
                ###actualizo la entrada de inclinacion 
                ventanaprincipal.ventanacentral.ventanadedatos.entradaInclinacion.setMaximum(89)
                ventanaprincipal.ventanacentral.ventanadedatos.entradaInclinacion.setSingleStep(1)
                ventanaprincipal.ventanacentral.ventanadedatos.entradaInclinacion.setValue(datos.inclinacion)
            if unidadesangulos=="Radianes":
                datos.unidades.angulos="Radianes" # actualizo unidades 
                
                ## cambio el valor del angulo Friccion  a radianes 
                datos.anguloFriccion=radianes(datos.anguloFriccion)
                ## actualizo la entrada del angulo de friccion 
                ventanaprincipal.ventanacentral.ventanadedatos.entradaAnguloFriccion.setValue(datos.anguloFriccion)
                ventanaprincipal.ventanacentral.ventanadedatos.entradaAnguloFriccion.setMaximum(1.553343034274953323)
                ventanaprincipal.ventanacentral.ventanadedatos.entradaAnguloFriccion.setSingleStep(0.01)
                
                ### cambio el valor del angulo de inclinacion 
                datos.inclinacion=radianes(datos.inclinacion)
                ###actualizo la entrada del angulo de inclinacion 
                ventanaprincipal.ventanacentral.ventanadedatos.entradaInclinacion.setValue(datos.inclinacion)
                ventanaprincipal.ventanacentral.ventanadedatos.entradaInclinacion.setMaximum(1.553343034274953323)
                ventanaprincipal.ventanacentral.ventanadedatos.entradaInclinacion.setSingleStep(0.01)
   
        if datos.unidades.distancias==unidadesdistancia:
            pass
        elif datos.unidades.distancias!=unidadesdistancia:
            if unidadesdistancia=="Metros":
                pass
        

        if preferencias.tema==preferenciatema:
            pass
        elif preferencias.tema!=preferenciatema:
            preferencias.tema=preferenciatema
            if preferencias.tema=="oscuro":
                ventanaprincipal.cargar_css("styles/dark/stylePrincipal.css")
                ventanaprincipal.barradeestado.cargar_css("styles/dark/styleStatusBar.css")
                ventanaprincipal.barramenu.cargar_css("styles/dark/styleMenuBar.css")
                ventanaprincipal.ventanacentral.VentanaDeGraficos.cargar_css("styles/dark/styleGraficsWindow.css")
                ventanaprincipal.ventanacentral.ventanadetablas.cargar_css("styles/dark/styleTableWindow.css")
                ventanaprincipal.ventanacentral.ventanadedatos.cargar_css("styles/dark/styleInputDateWindow.css")
            
        self.close()    


   ### configuracion de estilos 
    def cargar_css(self, archivo_css):
        file = QFile(archivo_css)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
            file.close() 


###barra de menu 
class Acciones():
    def __init__(self):
        self.accionSalir=QAction("Salir")

        ## ACCIONES DEL MENU VENTANA 
        self.accionAbrirVentanaGraficos=QAction("Ventana de Graficos")
        self.accionAbrirVentanaGraficos.setCheckable(True)
        self.accionAbrirVentanaGraficos.setChecked(True)

        
        self.accionAbrirVentanaEntradasTablas=QAction("Ventana de Tablas ")
        self.accionAbrirVentanaEntradasTablas.setCheckable(True)
        self.accionAbrirVentanaEntradasTablas.setChecked(True)
        
        self.accionAbrirVentanaEntradasDatos=QAction("Ventana Datos ")
        self.accionAbrirVentanaEntradasDatos.setCheckable(True)
        self.accionAbrirVentanaEntradasDatos.setChecked(True)

        ## ACCIONES MENU EDITAR
        self.accionAbrirPreferencias=QAction("Preferencias")
class BarraMenu(QMenuBar):
    def __init__(self):
        super().__init__()
        if preferencias.tema=="oscuro":
            self.cargar_css("styles/dark/styleMenuBar.css")
        elif preferencias.tema=="claro":
            self.cargar_css("styles/clear/styleMenuBar.css")
        self.archivo = QMenu("Archivo",self ) 
        self.archivo.addSeparator()
        self.archivo.addAction(acciones.accionSalir) 
        
        
        self.editar=QMenu("Editar",self)
        self.editar.addSeparator()
        self.editar.addAction(acciones.accionAbrirPreferencias)
        
        self.ventana=QMenu("Ventana",self)
       
        self.ventana.addSeparator()
        self.ventana.addAction(acciones.accionAbrirVentanaGraficos)     
        self.ventana.addSeparator()
        self.ventana.addAction(acciones.accionAbrirVentanaEntradasDatos)
        self.ventanaEntradaTablasActivada=True
        self.ventana.addAction(acciones.accionAbrirVentanaEntradasTablas)
        self.ventanaEntradaDatosActivada=True
        self.ventana.addSeparator()




        self.addMenu(self.archivo)
        self.addMenu(self.editar)
        self.addMenu(self.ventana)
    def cargar_css(self, archivo_css):
        file = QFile(archivo_css)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
            file.close() 
##barra de estado 
class BarraEstado(QStatusBar):
    def __init__ (self):
        super().__init__()
        self.label_memory=QLabel(self)
        self.addPermanentWidget(self.label_memory)
    
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_memory_usage)
        self.timer.start(1000)  # 1000 ms = 1 segundo
        if preferencias.tema=="oscuro":
            self.cargar_css("styles/dark/styleStatusBar.css")
        elif preferencias.tema=="claro":
            self.cargar_css("styles/clear/styleStatusBar.css")
    def update_memory_usage(self):
        process = psutil.Process()
        memory_usage = process.memory_info().rss  # Obtener memoria en bytes
        memory_usage_mb = memory_usage / (1024 ** 2)  # Convertir a megabytes

        self.label_memory.setText(f"Memoria utilizada: {memory_usage_mb:.2f} MB")
    
    def cargar_css(self, archivo_css):
        file = QFile(archivo_css)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
            file.close() 
### areas de trabajo ventana principal 
class VentanaDeGrafico(Ventana):
    def __init__(self,accionVentanaGraficos=None):
        super().__init__(accionVentanaGraficos)
        #configuraciones generales del objeto 
        self.setWindowTitle("Ventana de Grafico")  
        self.definirbarraTareas()
        self.definircontenido()
    def definirbarraTareas(self):
        ##limpiamos la barra de tareas actual 
        self.setTitleBarWidget(QWidget()) 
        
        ##creamos el layout de la barra de tareas 
        layoutbarratareas=QHBoxLayout()
        self.titleBarWidget().setLayout(layoutbarratareas)
        layoutbarratareas.setContentsMargins(0, 0, 0, 0)
        layoutbarratareas.setSpacing(0)
        
        ##creamos los widgets de la barra de tareas  
        self.Combodegraficos=QComboBox()
        self.Combodegraficos.setFixedHeight(22)
        self.Combodegraficos.setMaximumWidth(200)
        self.Combodegraficos.addItem("Grafico 1")
        self.Combodegraficos.addItem("Grafico 2")
        self.Combodegraficos.addItem("Grafico 3")
        self.Combodegraficos.addItem("Grafico 4")

        self.titulo=QLabel("Ventana de Grafico")
        self.titulo.setFixedHeight(25)

        self.botondevista=QPushButton("░")
        self.botondevista.setFixedHeight(25)
        self.botondevista.setFixedWidth(25)
    
        ##agregamos los widgets a la barra de tareas 
        layoutbarratareas.addWidget(self.Combodegraficos)
        layoutbarratareas.addWidget(self.titulo)
        layoutbarratareas.addWidget(self.botondevista) 
    def definircontenido(self):

        self.contenido=QWidget()
        self.setWidget(self.contenido) 
        #creamos el layout del widget contenido
        self.layoutcontenido=QHBoxLayout()
        self.contenido.setLayout(self.layoutcontenido)
        self.layoutcontenido.setContentsMargins(0, 0, 0, 0)
        
        ### creo los widgets contenidos 
        
        self.texto=QLabel("GRAFICO ")
        

        ## agrego los widgets contenidos 
        self.layoutcontenido.addWidget(self.texto)
class VentanaDeGraficos(Ventana):
    def __init__(self,accion):
        super().__init__(accion)
        
        ## configuraciones generales del objeto 
        self.setWindowTitle("Ventana de Graficos")
        if preferencias.tema=="oscuro":
            self.cargar_css("styles/dark/styleGraficsWindow.css")
        elif preferencias.tema=="claro":
            self.cargar_css("styles/clear/styleGraficsWindow.css")
        ## creo el widget contenido
        self.contenido=QWidget()
        self.setWidget(self.contenido)

        ### creo el layout del widget contenido 
        self.layout=QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.contenido.setLayout(self.layout)

        ### creo las ventanas divisorias 
        self.Spliterderecho=QSplitter(2)
        self.Spliterizquierdo=QSplitter(2)
        self.Spliterprincipal=QSplitter(1)
        self.layout.addWidget(self.Spliterprincipal)
        self.Spliterprincipal.addWidget(self.Spliterizquierdo)
        self.Spliterprincipal.addWidget(self.Spliterderecho)
        
        ### creo las cuatro ventana de graficos  
        
        self.graficouno=VentanaDeGrafico()
        self.Spliterizquierdo.addWidget(self.graficouno)
        self.graficouno.botondevista.setObjectName("BotonVistauno")
        self.graficouno.botondevista.setProperty("class", "BotonVistauno")
        self.graficouno.texto.setText("Grafico 1 ")
        self.graficouno.botondevista.clicked.connect(self.funcionMostrarVentanaGraficoUno)

        self.graficodos=VentanaDeGrafico()
        self.Spliterderecho.addWidget(self.graficodos)
        self.graficodos.botondevista.setObjectName("BotonVistados")
        self.graficodos.botondevista.setProperty("class", "BotonVistados")
        self.graficodos.texto.setText("Grafico 2")
        self.graficodos.botondevista.clicked.connect(self.funcionMostrarVentanaGraficodos)

        self.graficotres=VentanaDeGrafico()
        self.Spliterizquierdo.addWidget(self.graficotres)
        self.graficotres.botondevista.setObjectName("BotonVistatres")
        self.graficotres.botondevista.setProperty("class", "BotonVistatres")
        self.graficotres.texto.setText("Grafico 3")
        self.graficotres.botondevista.clicked.connect(self.funcionMostrarVentanaGraficotres)

        self.graficocuatro=VentanaDeGrafico()
        self.Spliterderecho.addWidget(self.graficocuatro)
        self.graficocuatro.botondevista.setObjectName("BotonVistacuatro")
        self.graficocuatro.botondevista.setProperty("class", "BotonVistacuatro")
        self.graficocuatro.texto.setText("Grafico 4")
        self.graficocuatro.botondevista.clicked.connect(self.funcionMostrarVentanaGraficocuatro)
        
        ##defino el estado inicial del widget
        self.definiEstadoInicial()
    def definiEstadoInicial(self):
        self.ventanamultiple=False 
        self.graficodos.hide()
        self.graficotres.hide()
        self.graficocuatro.hide() 
    #funcioens de los widgets 
    def funcionMostrarVentanaGraficoUno(self):
        if self.ventanamultiple==False:
            self.graficodos.show()
            self.graficotres.show()
            self.graficocuatro.show()
            self.ventanamultiple=True
        elif self.ventanamultiple==True:
            self.graficodos.hide()
            self.graficotres.hide()
            self.graficocuatro.hide()
            self.ventanamultiple=False   
    def funcionMostrarVentanaGraficodos(self):
        if self.ventanamultiple==False:
            self.graficouno.show()
            self.graficotres.show()
            self.graficocuatro.show()
            self.ventanamultiple=True
        elif self.ventanamultiple==True:
            self.graficouno.hide()
            self.graficotres.hide()
            self.graficocuatro.hide()
            self.ventanamultiple=False
    def funcionMostrarVentanaGraficotres(self):
        if self.ventanamultiple==False:
            self.graficouno.show()
            self.graficodos.show()
            self.graficocuatro.show()
            self.ventanamultiple=True
        elif self.ventanamultiple==True:
            self.graficouno.hide()
            self.graficodos.hide()
            self.graficocuatro.hide()
            self.ventanamultiple=False
    def funcionMostrarVentanaGraficocuatro(self):
        if self.ventanamultiple==False:
            self.graficouno.show()
            self.graficodos.show()
            self.graficotres.show()
            self.ventanamultiple=True
        elif self.ventanamultiple==True:
            self.graficouno.hide()
            self.graficodos.hide()
            self.graficotres.hide()
            self.ventanamultiple=False
    def cargar_css(self, archivo_css):
        file = QFile(archivo_css)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
            file.close()
class VentanaDeDatos(Ventana):
    def __init__(self,accionagregar=None):
        super().__init__(accionagregar)
        
        ## configuraciones generales del objeto 
        self.setWindowTitle("Ventana de Entradas")
        self.setMinimumWidth(270)
        self.setMinimumHeight(300)
        if preferencias.tema=="oscuro":
            self.cargar_css("styles/dark/styleInputDateWindow.css")
        elif preferencias.tema=="claro":
            self.cargar_css("styles/clear/styleInputDateWindow.css")
        ### definimos el contenido 
        self.crearContenedores()
        self.crearWidgetsfichaSuelos()
        self.crearWidgetsfichaCimentaciones()
        self.agregarWidgetsfichasSuelos() ### aqui se dan condiciones generales 
        self.agregarWidgetsfichaCimentaciones()   
    def crearContenedores(self):
        ### creamos el contenedor principal 
        self.contenido=QTabWidget()
        self.setWidget(self.contenido) 

        ### creamos las fichas del contenedor principal 
        
        self.suelo=QWidget()
        self.contenido.addTab(self.suelo,"Suelo")

        self.cimentacion=QWidget()
        self.contenido.addTab(self.cimentacion,"Cimentacion") 
    def crearWidgetsfichaSuelos(self):
        
        self.labelCohesion=QLabel("Cohesion.............................",parent=self.suelo)
        
        self.entradaCohesion=QDoubleSpinBox(parent=self.suelo)
        self.entradaCohesion.setValue(datos.cohesion) 


        self.labelAnguloFriccion=QLabel("Angulo de Friccion.....................",parent=self.suelo)
        
        self.entradaAnguloFriccion=QDoubleSpinBox(parent=self.suelo)
        self.entradaAnguloFriccion.setValue(datos.anguloFriccion)
        if datos.unidades.angulos=="Grados":
            self.entradaAnguloFriccion.setMaximum(89)
        if datos.unidades.angulos=="Radianes":
            self.entradaAnguloFriccion.setMaximum(1.57)

        self.labelPesoEspecifico =QLabel("Peso Especifico..................... ",parent=self.suelo)
        
        self.entradaPesoEspecifico=QDoubleSpinBox(parent=self.suelo)
        self.entradaPesoEspecifico.setValue(datos.pesoEspecifico)

        self.activarNivelFreatico=QCheckBox("Nivel Freatico",parent=self.suelo)
        self.activarNivelFreatico.setChecked(False) #### a esto se le debe guardar una variable de estado 
        self.activarNivelFreatico.stateChanged.connect(self.funcionactivarNivelFreatico)
        

        self.labelProfundidadFreatica=QLabel("Profundidad Freatica .....................",parent=self.suelo)
        self.labelProfundidadFreatica.setEnabled(False) ### a esto se le debe guardar una variable de estado 

        self.entradaProfundidadFreatica=QDoubleSpinBox(parent=self.suelo)
        self.entradaProfundidadFreatica.setEnabled(False) ### a esto se le debe guardar una variable de esstado
        self.entradaProfundidadFreatica.setValue(datos.profundidadFreatica)
        

        self.labelPesoEspecificoSaturado=QLabel("Peso Especifico Saturado.....................",parent=self.suelo)
        self.labelPesoEspecificoSaturado.setEnabled(False) ### a esto se le debe guardar una variable de esstado

        self.entradaPesoEspecificoSaturado=QDoubleSpinBox(parent=self.suelo)
        self.entradaPesoEspecificoSaturado.setValue(datos.pesoEspecificoSaturado)
        self.entradaPesoEspecificoSaturado.setEnabled(False) ### a esto se le debe guardar una variable de esstado
    def agregarWidgetsfichasSuelos(self):
        WidgetsFichaSuelo=[
        (self.labelCohesion,self.entradaCohesion),
        (self.labelAnguloFriccion,self.entradaAnguloFriccion),
        (self.labelPesoEspecifico,self.entradaPesoEspecifico),
        "separador",
        (self.activarNivelFreatico,),
        (self.labelProfundidadFreatica,self.entradaProfundidadFreatica),
        (self.labelPesoEspecificoSaturado,self.entradaPesoEspecificoSaturado),
        "separador"
        ]
        
        #caracteristicas generales 
        posx=10
        posy=10 ## posicion inicial 
        posentradax=190
        tamx=160
        tamy=25
        tamentradax=100
        self.decimales=4
        
        for widget in WidgetsFichaSuelo:
            if type(widget)==tuple and len(widget)==2 :
                widget[0].setGeometry(posx,posy,tamx,tamy)
                widget[1].setGeometry(posentradax,posy,tamentradax,tamy)
                widget[1].setDecimals(datos.unidades.decimales)
                posy+=30
            if type(widget)==tuple and len(widget)==1 :
                widget[0].setGeometry(posx,posy,tamx,tamy)
                posy+=30
            if widget=="separador": 
                separator = QFrame(parent=self.suelo)
                separator.setFrameShape(QFrame.HLine)  # Establecer la forma del marco a una línea horizontal
                separator.setFrameShadow(QFrame.Sunken)  # Establecer el estilo del marco a "Sunken" (hundido)
                separator.setLineWidth(2)  # Establecer el ancho de la línea
                separator.setGeometry(posx,posy,250,tamy)
                posy+=20
    def crearWidgetsfichaCimentaciones(self):
    
        self.labelAncho=QLabel("Ancho................................... ",self.cimentacion)
        
        self.entradaAncho=QDoubleSpinBox(self.cimentacion)
        self.entradaAncho.setValue(datos.ancho)
        self.entradaAncho.setMinimum(0.001)
        self.entradaAncho.setMaximum(10000)
        self.entradaAncho.setSingleStep(0.01)
        

        self.labelLongitud=QLabel("Longitud.......................................",self.cimentacion)
        
        self.entradaLongitud=QDoubleSpinBox(self.cimentacion)
        self.entradaLongitud.setValue(datos.longitud)
        self.entradaLongitud.setMinimum(0.001)
        self.entradaLongitud.setMaximum(10000)
        self.entradaLongitud.setSingleStep(0.01)


        self.labelProfundidad=QLabel("Profundidad...........................................",self.cimentacion)

        self.entradaProfundidad=QDoubleSpinBox(self.cimentacion) 
        self.entradaProfundidad.setValue(datos.profundidad)

        self.labelInclinacion=QLabel("Inclinación...........................................",self.cimentacion)

        self.entradaInclinacion=QDoubleSpinBox(self.cimentacion)
        self.entradaInclinacion.setValue(datos.inclinacion) 
    def agregarWidgetsfichaCimentaciones(self): 
        
        WidgetsFichaCiementacion=[
        (self.labelAncho,self.entradaAncho),
        (self.labelLongitud,self.entradaLongitud),
        (self.labelProfundidad,self.entradaProfundidad),
        (self.labelInclinacion,self.entradaInclinacion),
        "separador"
        ] 
        #caracteristicas generales 
        posx=10
        posy=10 ## posicion inicial 
        posentradax=160
        tamx=145
        tamy=25
        tamentradax=100
        self.decimales=4
        
        for widget in WidgetsFichaCiementacion:
            if type(widget)==tuple and len(widget)==2 :
                widget[0].setGeometry(posx,posy,tamx,tamy)
                widget[1].setGeometry(posentradax,posy,tamentradax,tamy)
                widget[1].setDecimals(datos.unidades.decimales)
                posy+=30
            if type(widget)==tuple and len(widget)==1 :
                widget[0].setGeometry(posx,posy,tamx,tamy)
                posy+=30
            if widget=="separador": 
                separator = QFrame(parent=self.cimentacion)
                separator.setFrameShape(QFrame.HLine)  # Establecer la forma del marco a una línea horizontal
                separator.setFrameShadow(QFrame.Sunken)  # Establecer el estilo del marco a "Sunken" (hundido)
                separator.setLineWidth(2)  # Establecer el ancho de la línea
                separator.setGeometry(posx,posy,250,tamy)
                posy+=20
    ### funciones de los widgets 
    def funcionactivarNivelFreatico(self):
        if self.activarNivelFreatico.isChecked()==True:
            self.NivelFreatico=True
        if self.activarNivelFreatico.isChecked()==False:
            self.NivelFreatico=False
        for i in (self.labelProfundidadFreatica,self.entradaProfundidadFreatica,self.labelPesoEspecificoSaturado,self.entradaPesoEspecificoSaturado):
                i.setEnabled(self.NivelFreatico)

        datos.inclinacion=self.entradaInclinacion.value()
    def cargar_css(self, archivo_css):
        file = QFile(archivo_css)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
            file.close() 
class VentanaDeTabla(QDockWidget):
    def __init__(self,item=None):
        super().__init__()
        self.modificarbarradecontrol() 
        self.agregaTabla(item)  
       
    def modificarbarradecontrol(self):
        self.setTitleBarWidget(QWidget())## limpiamos la barra de control actual

        layoutbarratareas=QHBoxLayout() 
        self.titleBarWidget().setLayout(layoutbarratareas)
        layoutbarratareas.setContentsMargins(0,0,0,0)
        layoutbarratareas.setSpacing(0)
        
        ### creamoslos widgets de la barra de control 
        
        self.titulo=QLabel(" ")
        self.titulo.setFixedHeight(25)

        self.botonOpciones=QPushButton()
        self.botonOpciones.setFixedHeight(25)
        self.botonOpciones.setFixedWidth(25)

        self.menuOpciones=QMenu("...")
        self.botonOpciones.setMenu(self.menuOpciones)

        self.accionGuardarTabla=QAction("Guardar Tabla")
        self.menuOpciones.addAction(self.accionGuardarTabla)
        self.accionGuardarTabla.triggered.connect(self.export_to_excel)

        ### agregamos los widigets a la barra 
        layoutbarratareas.addWidget(self.titulo)
        layoutbarratareas.addWidget(self.botonOpciones) 


        
    def agregaTabla(self,items):

        ### creo la tabla 
        self.tabla=QTableWidget()
        self.setWidget(self.tabla)
        ### extraigo los itemes  
        if items==None:
            self.items=[("Factor","Valor"),]
        else:
            self.items=items 
        ## extraigo informacion general de los items 
        self.Numfilas=len(self.items)
        self.Numcolumnas=len(self.items[0])
        
        ### configuraciones generales de la tabla  
        self.tabla.setRowCount(self.Numfilas)
        self.tabla.setColumnCount(self.Numcolumnas)

        ### agrego los itemsa la tabla
        fila=0
        for contadoruno in self.items:
            for i in range(self.Numcolumnas):
                self.tabla.setItem(fila,i,QTableWidgetItem(contadoruno[i]))
            fila+=1
         
        ## configutaciones de presentacion de  tabla 
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.horizontalHeader().setVisible(False)
        for col in range(self.tabla.columnCount()):
            self.tabla.setColumnWidth(col, 159)
    ### creo una funcion para poder modificar de manera facil los valores de la tabla
    def modificarItem(self,fila,columna,item="Texto"):
        self.tabla.setItem(fila,columna,QTableWidgetItem(item))
    def export_to_excel(self):
        # Crear un DataFrame con los datos de la tabla
        data = []
        for row in range(self.tabla.rowCount()):
            row_data = []
            for col in range(self.tabla.columnCount()):
                item = self.tabla.item(row, col)
                row_data.append(item.text())
            data.append(row_data)

        df = pd.DataFrame(data[1:], columns=data[0])

        # Crear un archivo Excel
        file_path = "tabla_excel.xlsx"
        writer = pd.ExcelWriter(file_path, engine="openpyxl")
        df.to_excel(writer, sheet_name="Sheet1", index=False)

        # Ajustar el ancho de las columnas para que se ajusten al contenido
        sheet = writer.sheets["Sheet1"]
        for column_cells in sheet.columns:
            length = max(len(str(cell.value)) for cell in column_cells)
            sheet.column_dimensions[column_cells[0].column_letter].width = length

        # Guardar el archivo y cerrar el writer
        writer.save()
        writer.close()
    
class VentanaDeTablas(Ventana):
    def __init__(self,accionagregar=None):
        super().__init__(accionagregar)
        #configutacion del objeto 
        self.setWindowTitle("Ventana de Tablas de Factores")
        self.setMinimumWidth(327)
        self.setMinimumHeight(240)
        if preferencias.tema=="oscuro":
            self.cargar_css("styles/dark/styleTableWindow.css")
        elif preferencias.tema=="claro":
            self.cargar_css("styles/clear/styleTableWindow.css")
        
        ### creamos los widgets contenedores
        self.contenido=QTabWidget()
        self.setWidget(self.contenido)
        ### Cargo los datos iniciales de las tablas 
        self.cargaritemsInicialTablas()
        self.crearTablas()
    def cargaritemsInicialTablas(self): 
        
        self.ItemsCarga=[
        ("Factor","Valor"),
        ("Nq",(str(round(datos.Nq,datos.unidades.decimales)))),
        ("Nc",(str(round(datos.Nc,datos.unidades.decimales)))),
        ("N\u03B3",(str(round(datos.Ny,datos.unidades.decimales))))
        ]  


        self.ItemsForma=[
        ("Factor","Valor"),
        ("Fq",(str(round(datos.Fqs,datos.unidades.decimales)))),
        ("Fc",(str(round(datos.Fcs,datos.unidades.decimales)))),
        ("F\u03B3s",(str(round(datos.Fys,datos.unidades.decimales))))
        ]


        self.ItemsProfundidad=[
        ("Factor","Valor"),
        ("Fqd",(str(round(datos.Fqd,datos.unidades.decimales)))),
        ("Fcd",(str(round(datos.Fcd,datos.unidades.decimales)))),
        ("F\u03B3d",(str(round(datos.Fyd,datos.unidades.decimales))))
        ]  

        self.ItemsInclinacion=[
        ("Factor","Valor"),
        ("Fqi",(str(round(datos.Fqi,datos.unidades.decimales)))),
        ("Fci",(str(round(datos.Fci,datos.unidades.decimales)))),
        ("F\u03B3i",(str(round(datos.Fyi,datos.unidades.decimales))))
        ] 


    def crearTablas(self):
        ## ficha Factores de forma 
        self.tablaFactoresForma=VentanaDeTabla(self.ItemsForma)
        self.contenido.addTab(self.tablaFactoresForma," Forma")
        self.tablaFactoresForma.titulo.setText("  Factores de Forma  ")

        #ficha factores de profundidad 
        self.tablaFactoresProfundidad=VentanaDeTabla(self.ItemsProfundidad)
        self.contenido.addTab(self.tablaFactoresProfundidad,"Profundidad")
        self.tablaFactoresProfundidad.titulo.setText("  Factores de Profundidad  ")

        ### ficha factor de carga 
        self.tablaFactoresCarga=VentanaDeTabla(self.ItemsCarga)  ### creamos el widget contenedor
        self.contenido.addTab(self.tablaFactoresCarga,"Carga")
        self.tablaFactoresCarga.titulo.setText("  Factores de Carga  ")

        #ficha factores de inclinacion 
        self.tablaFactoresInclinacion=VentanaDeTabla(self.ItemsInclinacion)
        self.contenido.addTab(self.tablaFactoresInclinacion," Inclinacion")
        self.tablaFactoresInclinacion.titulo.setText("  Factores de Inclinacion ")
    
    
    def cargar_css(self, archivo_css):
        file = QFile(archivo_css)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
            file.close() 
class VentanaContenedora(QWidget):
    def __init__(self):
        super().__init__()
        ### creanos los contenedores 
        self.layout=QHBoxLayout()
        self.setLayout(self.layout)

        self.splitter=QSplitter()
        self.layout.addWidget(self.splitter)
        
        ## creamos los widgets Ventana 
        self.VentanaDeGraficos=VentanaDeGraficos(acciones.accionAbrirVentanaGraficos)
        self.splitter.insertWidget(1,self.VentanaDeGraficos)

        self.widgetOrganizador=QWidget()
        self.splitter.insertWidget(2,self.widgetOrganizador)
        
        self.layoutorganizador=QVBoxLayout()
        self.widgetOrganizador.setLayout(self.layoutorganizador)
        self.layoutorganizador.setContentsMargins(0, 0, 0, 0)

        self.splitterdedivision=QSplitter(2)
        self.layoutorganizador.addWidget(self.splitterdedivision)
       
        ## creamos el resto de widgets 
        self.ventanadetablas=VentanaDeTablas(acciones.accionAbrirVentanaEntradasTablas)
        self.splitterdedivision.insertWidget(1,self.ventanadetablas)

        self.ventanadedatos=VentanaDeDatos(acciones.accionAbrirVentanaEntradasDatos)
        self.splitterdedivision.insertWidget(2,self.ventanadedatos)

class MainWindow(QMainWindow):
    def __init__(self): 
        super().__init__()
        self.setWindowTitle("Proyecto Cimentaciones ")
        self.setGeometry(50,50,1000,900)
        self.setObjectName("VentanaPrincipal") 
        self.setProperty("class", "VentanaPrincipal")
        if preferencias.tema=="oscuro":
            self.cargar_css("styles/dark/stylePrincipal.css")
        elif preferencias.tema=="claro":
            self.cargar_css("styles/clear/stylePrincipal.css")

        self.barradeestado=BarraEstado()
        self.setStatusBar(self.barradeestado)

        self.barramenu=BarraMenu()
        self.setMenuBar(self.barramenu)
        
        self.ventanacentral=VentanaContenedora()
        self.setCentralWidget(self.ventanacentral)





      ##conectamos con las funciones del menu archivo 
        acciones.accionSalir.triggered.connect(self.funcionSalir)
        acciones.accionAbrirPreferencias.triggered.connect(self.funcionPreferencias)
      
      
      

        
        

        ###╔ conecto con las funciones
        self.ventanacentral.ventanadedatos.entradaCohesion.valueChanged.connect(self.funcionEntradaCohesion)
        self.ventanacentral.ventanadedatos.entradaAnguloFriccion.valueChanged.connect(self.funcionEntradaAnguloFriccion)
        self.ventanacentral.ventanadedatos.entradaPesoEspecifico.valueChanged.connect(self.funcionEntradaPesoEspecifico)
        self.ventanacentral.ventanadedatos.entradaProfundidadFreatica.valueChanged.connect(self.funcionEntradaProfundidadFreatica)
        self.ventanacentral.ventanadedatos.entradaPesoEspecificoSaturado.valueChanged.connect(self.funcionEntradaPesoEspecificoSaturado)
        self.ventanacentral.ventanadedatos.entradaAncho.valueChanged.connect(self.funcionEntradaAncho)
        self.ventanacentral.ventanadedatos.entradaLongitud.valueChanged.connect(self.funcionEntradaLongitud)
        self.ventanacentral.ventanadedatos.entradaProfundidad.valueChanged.connect(self.funcionEntradaProfundidad)
        self.ventanacentral.ventanadedatos.entradaInclinacion.valueChanged.connect(self.funcionEntradaInclinacion)

       
       
       
    
       

        

    def cargar_css(self, archivo_css):
        file = QFile(archivo_css)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
            file.close()

              





#### funciones que implementar para la barra de menu 
    def funcionSalir(self):
        # Mostrar cuadro de diálogo de confirmación
        respuesta = QMessageBox.question(self, 'Confirmar Salida', '¿Estás seguro de que deseas salir?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if respuesta == QMessageBox.Yes:
            # Si el usuario hace clic en "Sí", cerrar la aplicación
            App.quit()
  
  
  
    #MENU PREFERENCIAS  
   
    def funcionPreferencias (self):
        self.preferencias=VentanaPreferencias()
        self.preferencias.show()     
                           
    #                                          FUNCIONES WIDGET CENTRALVENTANADEDATOS      
    def funcionEntradaCohesion(self):
        datos.cohesion=self.ventanacentral.ventanadedatos.entradaCohesion.value()    
    def funcionEntradaAnguloFriccion(self):
        datos.anguloFriccion = self.ventanacentral.ventanadedatos.entradaAnguloFriccion.value()
        
        ### reailizamos el calculo de los factores de carga 
        datos.Nq =calcularNq(datos.anguloFriccion,datos.unidades.angulos)
        datos.Nc=calcularNc(datos.anguloFriccion,datos.unidades.angulos)
        datos.Ny=calcularNy(datos.anguloFriccion,datos.unidades.angulos)

        ### imprimimos factores de carga 
        self.ventanacentral.ventanadetablas.tablaFactoresCarga.modificarItem(1,1,str(round(datos.Nq,datos.unidades.decimales)))
        self.ventanacentral.ventanadetablas.tablaFactoresCarga.modificarItem(2,1,str(round(datos.Nc,datos.unidades.decimales)))
        self.ventanacentral.ventanadetablas.tablaFactoresCarga.modificarItem(3,1,str(round(datos.Ny,datos.unidades.decimales)))   

        ### realizamos el calculo de los factores de forma
        datos.Fqs=calcularFqs(datos.ancho,datos.longitud,datos.anguloFriccion,unidadesangulos=datos.unidades.angulos, unidadesdistancia=datos.unidades.distancias)
        datos.Fcs=calcularFcs(datos.ancho,datos.longitud,datos.Nq, datos.Nc,unidadesdistancia=datos.unidades.distancias)

        ### imprimimos factores de forma 
        self.ventanacentral.ventanadetablas.tablaFactoresForma.modificarItem(1,1,str(round(datos.Fqs,datos.unidades.decimales)))
        self.ventanacentral.ventanadetablas.tablaFactoresForma.modificarItem(2,1,str(round(datos.Fcs,datos.unidades.decimales)))

        ###realizamos el calculo de los factores de profundidad 
        (datos.Fqd,datos.Fcd,datos.Fyd)=calcularFactoresprofundidad(datos.anguloFriccion,datos.profundidad,datos.ancho,datos.Nc,unidadesangulos=datos.unidades.angulos, unidadesdistancia=datos.unidades.distancias)

        ###imprimimos los factores de profundidad 
        self.ventanacentral.ventanadetablas.tablaFactoresProfundidad.modificarItem(1,1,str(round(datos.Fqd,datos.unidades.decimales)))
        self.ventanacentral.ventanadetablas.tablaFactoresProfundidad.modificarItem(2,1,str(round(datos.Fcd,datos.unidades.decimales)))
        self.ventanacentral.ventanadetablas.tablaFactoresProfundidad.modificarItem(3,1,str(round(datos.Fyd,datos.unidades.decimales))) 

        
        ###realizamos el calculo de los factores de inclinacion 
        datos.Fyi=calcularFyi(datos.inclinacion,datos.anguloFriccion,datos.unidades.angulos)
        ### imprimimos los factores de inclinacion 
        self.ventanacentral.ventanadetablas.tablaFactoresInclinacion.modificarItem(3,1,str(round(datos.Fyi,datos.unidades.decimales)))
    def funcionEntradaPesoEspecifico(self):
        datos.pesoEspecifico=self.ventanacentral.ventanadedatos.entradaPesoEspecifico.value()
    def funcionEntradaProfundidadFreatica(self):
        datos.profundidadFreatica=self.ventanacentral.ventanadedatos.entradaProfundidadFreatica.value()
    def funcionEntradaPesoEspecificoSaturado(self):
        datos.pesoEspecificoSaturado=self.ventanacentral.ventanadedatos.entradaPesoEspecificoSaturado.value()  
    def funcionEntradaAncho(self):
        datos.ancho=self.ventanacentral.ventanadedatos.entradaAncho.value()
        ### realizamos el calculo de los factores de forma
        datos.Fqs=calcularFqs(datos.ancho,datos.longitud,datos.anguloFriccion,unidadesangulos=datos.unidades.angulos, unidadesdistancia=datos.unidades.distancias)
        datos.Fcs=calcularFcs(datos.ancho,datos.longitud,datos.Nq, datos.Nc,unidadesdistancia=datos.unidades.distancias)
        datos.Fys=calcularFys(datos.ancho,datos.longitud,unidadesdistancia=datos.unidades.distancias)

        ### imprimimos el valor de Fqs en la tabla 
        self.ventanacentral.ventanadetablas.tablaFactoresForma.modificarItem(1,1,str(round(datos.Fqs,datos.unidades.decimales)))
        ### imprimimos el valor de Fcs en la tabla 
        self.ventanacentral.ventanadetablas.tablaFactoresForma.modificarItem(2,1,str(round(datos.Fcs,datos.unidades.decimales)))
        ### imprimimos el valor de Fys en la tabla 
        self.ventanacentral.ventanadetablas.tablaFactoresForma.modificarItem(3,1,str(round(datos.Fys,datos.unidades.decimales)))  

                ###realizamos el calculo de los factores de profundidad 
        (datos.Fqd,datos.Fcd,datos.Fyd)=calcularFactoresprofundidad(datos.anguloFriccion,datos.profundidad,datos.ancho,datos.Nc,unidadesangulos=datos.unidades.angulos, unidadesdistancia=datos.unidades.distancias)

        ###imprimimos los factores de profundidad 
        self.ventanacentral.ventanadetablas.tablaFactoresProfundidad.modificarItem(1,1,str(round(datos.Fqd,datos.unidades.decimales)))
        self.ventanacentral.ventanadetablas.tablaFactoresProfundidad.modificarItem(2,1,str(round(datos.Fcd,datos.unidades.decimales)))
        self.ventanacentral.ventanadetablas.tablaFactoresProfundidad.modificarItem(3,1,str(round(datos.Fyd,datos.unidades.decimales)))  
    def funcionEntradaLongitud(self):
        datos.longitud=self.ventanacentral.ventanadedatos.entradaLongitud.value()
        ###realizamo el calculo de los factores de forma 
        datos.Fqs=calcularFqs(datos.ancho,datos.longitud,datos.anguloFriccion,unidadesangulos=datos.unidades.angulos, unidadesdistancia=datos.unidades.distancias)
        datos.Fcs=calcularFcs(datos.ancho,datos.longitud,datos.Nq, datos.Nc,unidadesdistancia=datos.unidades.distancias)
        datos.Fys=calcularFys(datos.ancho,datos.longitud,unidadesdistancia=datos.unidades.distancias)
        
        ### actualizo en la tabla 
        ### imprimimos el valor de Fqs en la tabla 
        self.ventanacentral.ventanadetablas.tablaFactoresForma.modificarItem(1,1,str(round(datos.Fqs,datos.unidades.decimales)))
        ### imprimimos el valor de Fcs en la tabla 
        self.ventanacentral.ventanadetablas.tablaFactoresForma.modificarItem(2,1,str(round(datos.Fcs,datos.unidades.decimales)))
        ### imprimimos el valor de Fys en la tabla 
        self.ventanacentral.ventanadetablas.tablaFactoresForma.modificarItem(3,1,str(round(datos.Fys,datos.unidades.decimales)))     
    def funcionEntradaProfundidad(self):
        datos.profundidad=self.ventanacentral.ventanadedatos.entradaProfundidad.value()
        ###realizamos el calculo de los factores de profundidad 
        (datos.Fqd,datos.Fcd,datos.Fyd)=calcularFactoresprofundidad(datos.anguloFriccion,datos.profundidad,datos.ancho,datos.Nc,unidadesangulos=datos.unidades.angulos, unidadesdistancia=datos.unidades.distancias)

        ###imprimimos los factores de profundidad 
        self.ventanacentral.ventanadetablas.tablaFactoresProfundidad.modificarItem(1,1,str(round(datos.Fqd,datos.unidades.decimales)))
        self.ventanacentral.ventanadetablas.tablaFactoresProfundidad.modificarItem(2,1,str(round(datos.Fcd,datos.unidades.decimales)))
        self.ventanacentral.ventanadetablas.tablaFactoresProfundidad.modificarItem(3,1,str(round(datos.Fyd,datos.unidades.decimales))) 
    def funcionEntradaInclinacion(self):
        datos.inclinacion=self.ventanacentral.ventanadedatos.entradaInclinacion.value()
        ### realizamos el calculo de los factores de inclinacion 
        datos.Fqi=calcularFci(datos.inclinacion,datos.unidades.angulos)
        datos.Fci=datos.Fqi
        datos.Fyi=calcularFyi(datos.inclinacion,datos.anguloFriccion,datos.unidades.angulos)
        
        ### imprimimos los factores de inclinacion en la tabla 
        self.ventanacentral.ventanadetablas.tablaFactoresInclinacion.modificarItem(1,1,str(round(datos.Fqi,datos.unidades.decimales)))
        self.ventanacentral.ventanadetablas.tablaFactoresInclinacion.modificarItem(2,1,str(round(datos.Fci,datos.unidades.decimales)))
        self.ventanacentral.ventanadetablas.tablaFactoresInclinacion.modificarItem(3,1,str(round(datos.Fyi,datos.unidades.decimales))) 
      


 ## ejecucion del programa 

### 
if __name__=="__main__":
    
    App=QApplication([])
    ###abro los datos iniciales 
    datos=Cimentacion()
    acciones=Acciones()
    preferencias=Preferencias()
    ### creo la ventana principal y la conecto a los datos 
    ventanaprincipal= MainWindow()
    ventanaprincipal.show()
    
    sys.exit(App.exec_())
