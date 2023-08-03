from  numpy import  tan,cos,sin,arctan,e,pi ,log10
def radianes(x):
    x=x*pi/180
    return x

def grados(x):
    x=x*180/pi
    return x


### factores de Carga
def calcularNq(a,unidadesangulos="Radianes"):  ###ecuacion  3.20 
    if unidadesangulos=="Grados":
        a=radianes(a)
    Nq=((tan((pi/4)+a/2))**2)*(e**(pi*tan(a)))
    return Nq
def calcularNc(a,unidadesangulos="Radianes"):   ## ecuacion  3.21 
    if unidadesangulos=="Grados":
        a=radianes(a)
    if a==0 :
        Nc=5.14
    else: 
        Nq=calcularNq(a)
        Nc=((Nq-1)*(1/tan(a)))
    return Nc
def calcularNy(a,unidadesangulos="Radianes"):   ## ecuacion  3.22 
    if unidadesangulos=="Grados":
        a=radianes(a)
    Nq=calcularNq(a)
    Ny=(2*(Nq+1)*(tan(a)))
    return Ny


### factores de forma 
def calcularFqs(B,L,a,unidadesangulos="Radianes",unidadesdistancia="Metros"):

    if unidadesangulos=="Grados":
        a=radianes(a)
    
    if L==0:
        print("ERROR ZERO DIVISION L=0")
    else:
        Fqs=1+(B/L)*tan(a)
        return Fqs
def calcularFcs(B,L,Nq,Nc,unidadesdistancia="Metros"):
    if L==0: 
       print("ERROR ZERO DIVISION L=0")
    else:
        Fcs=1+(B/L)*(Nq/Nc)
        return Fcs
def calcularFys(B,L,unidadesdistancia="Metros"):
    if L==0: 
        print("ERROR ZERO DIVISION L=0")
    else:
        Fys =1-0.4*(B/L)
        return Fys

def calcularFactoresprofundidad(a,Df,B,Nc,unidadesangulos="Radianes",unidadesdistancia="Metros"):
    if unidadesangulos=="Grados":
        a=radianes(a)
    if Df/B<=1:
        if a==0:
            Fcd=1+0.4*(Df/B)
            Fqd=1
            Fyd=1
        elif a>0:
            Fyd=1
            Fqd=1+(2*tan(a)*(1-sin(a))**2)*(Df/B)
            Fcd=Fqd-((1-Fqd)/(Nc*(tan(a))))
        
    elif Df/B>1:
        if a==0:
            Fcd=1+0.4*arctan((Df/B))
            Fqd=1
            Fyd=1 
        elif a>0:
            Fyd=1
            Fqd=1+2*tan(a)*((1-sin(a))**2)*(arctan(Df/B))
            Fcd=Fqd-((1-Fqd)/(Nc*(tan(a))))
    factoresprofundidad=(Fqd,Fcd,Fyd)
    return (factoresprofundidad)

### Factores de inclinacion 

def calcularFci(Bi,unidadesangulos="Radianes"):                    ###Fqi=Fci
    if unidadesangulos=="Grados": 
        Bi=radianes(Bi)
    Fci= (1-(Bi*180/pi)/90)**2
    return Fci


 #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! tiene un problema cuando a es cero  
def calcularFyi(Bi,a,unidadesangulos="Radianes"):
    if unidadesangulos=="Grados":
        a=radianes(a)
        Bi=radianes(Bi)
    if a==0:
        Fyi=1
    else:
        Fyi=(1-Bi/a)
    return Fyi