import sqlite3
mantener_interfaz="0"
con=sqlite3.connect('DB_Cadify.sqlite')
cursor=con.cursor()
salir= "0"
i=0
usuario_actual= None
conductor_actual= None
cat_dic= ["B1","b1","B2","b2","D1","d1","D2","d2","D3","d3","E1","e1","E2","e2"]
from datetime import datetime

def menu(opcion):
    menu_principal={"A":"A", "B":"B"}
    return menu_principal.get(opcion, "Solo se permiten las letras A,B")


def comprobacion_NO_Num (x):
    while any(chr.isdigit() for chr in x) == True :
        if any(chr.isdigit() for chr in x) == True:
            print ("No puede contener numeros.")
            x=input("Por favor intente devuelta: ")
            
        elif any(chr.isdigit() for chr in x) == False:
            break
    return x

def comprobacion_numeros(x):
    while any(chr.isdigit() for chr in x) == True :
        if any(chr.isalpha() for chr in x) == False:
            break
        elif any(chr.isalpha() for chr in x) == True:
            print("No puede contener letras o caracteres que no sean números.")
            x=input("Intente devuelta: ")
    return x

def comprobacion_patente(x):
    while True :
        if len (x) > 7 or len (x) < 6:
            print ("La patente tiene que tener formato de AAA111 o AA111AA (1)")
            x=input ("Ingrese la patente de su vehiculo: ")
        elif len(x) == 7 and (any(chr.isdigit() for chr in x[:2]) == True or any(chr.isdigit() for chr in x[3:5]) == False or any(chr.isdigit() for chr in x[6:7]) == True )  :
            print ("La patente tiene que tener formato de AAA111 o AA111AA (2)")
            x=input ("Ingrese la patente de su vehiculo: ")
        elif len (x) == 6 and (any(chr.isdigit() for chr in x[:3]) == True or any(chr.isdigit() for chr in x[4:]) == False):
            print  ("La patente tiene que tener formato de AAA111 o AA111AA (3)")
            x=input ("Ingrese la patente de su vehiculo: ")
        else:
            print ("Patente cargada con exito.")
            break
    return  x

def comprobacion_categorias(x,y):
    while True:
        if len (x) > 2  or len (x) < 2:
            print (" Fomato permito :B1,B2,D1,D2,D3,E1,E2 " )
            x= input ("Ingrese la categoria de su licencia: ")
        elif x not in y:
            print (" Fomato permito :B1,B2,D1,D2,D3,E1,E2 " )
            x= input ("Ingrese la categoria de su licencia: ")
        else:
            break
    return x

def comprobar_dia (x):
    while True:
        if any(chr.isalpha() for chr in x) == True:
            print ("solo puede contener numeros.")
            x=input("ingrese nuevamente su día de vencimiento: ")
        elif int(x) >31 or int(x) <0 :
            print ("El día debe estar entre 1 y 31")
            x=input("Por favor ingrese nuevamente el día de vencimiento: ")
        else:
            break
    return x

def comprobar_mes (y):
    while True:
        if any(chr.isalpha() for chr in y) == True:
            print ("solo puede contener numeros.")
            y=input("Ingrese nuevamente su mes de vencimiento: ")
        if int(y) >12 or int(y) < 0:
            print ("El día debe estar entre 1 y 12")
            y=input("Por favor ingrese nuevamente el mes de vencimiento: ")
        else:
            break
    return y

def comprobar_año (z):
    while True:
        if any(chr.isalpha() for chr in z) == True:
            print ("solo puede contener numeros.")
            z=input("Ingrese nuevamente su día de vencimiento: ")
            lon=len(z)
        elif len(z) == 2:
            if int(z) > 36:
                z= str("19")+str(z)
                print (z)
                break
            elif int(z)< 35:
                z="20"+z
                print (z)
                break
            print (z)
        elif len(z) == 3:
            print ("Año no valido")
            z=input("Ingrese nuevamente su año de vencimiento: ")
        elif len(z) ==1:
            print ("Año no valido")
            z=input("Ingrese nuevamente su año de vencimieto: ")
        elif len(z) ==4:
            break
        elif len (z) >4:
            print ("Año no valido")
            z=input("Ingrese nuevamente su año de vencimiento: ")
    print (z)
            
    return z

def alta_usuario (x):    #no incluyo tarjeta porque puede ser null, la pido en un menu separado con una funcion separada
    dni=input("Ingrese su DNI: ")
    comprobacion_numeros(dni)
    largo_d_usuario=len(dni)
    cursor.execute(x,(dni,))
    usuarios=cursor.fetchone()

    while True:
            if usuarios: 
                print("El usuario ",dni," ya ha sido creado")
                dni=input("Ingrese su nuevo usario: ")
                cursor.execute(x,(dni,))
                usuarios=cursor.fetchone()
            elif largo_d_usuario  > 8 and largo_d_usuario < 7:
                print ("Su usuario es demasiado largo. No puede tener mas de 8 numeros o menos de 7")
                dni=input("Ingrese su nuevo usario: ")
            else:
                break
    nombre=input("Ingrese su nombre: ")
    comprobacion_NO_Num(nombre)
    tel=input("Ingrese su teléfono: ")
    comprobacion_numeros(tel)
    tarjeta=None
    
    print (""" ---- """*6)
    
    return (dni, nombre, tel, tarjeta)

def comprobacion_largo(x,y,z1,z2,name):
    x=comprobacion_numeros(x)
    while True:
        largo_d_usuario=len(x)
        cursor.execute(y,(x,))
        usuarios=cursor.fetchone()
        if usuarios: 
            print("El ", name," ", x," ya ha sido registrado.")
            x=input("Por favor ingrese nuevamente su "+name+" : ")
            cursor.execute(y,(x,))
            usuarios=cursor.fetchone()
        elif int(largo_d_usuario) >= z1 or int(largo_d_usuario) <= z2:
            print ("Su "+name+" es demasiado largo/corto. No puede tener mas de ",z1," numeros o menos de ",z2,".")
            x= input("Por favor ingrese nuevamente su "+name+" : ")
            largo_d_usuario=len(x)
        else:
            break

    return x
def alta_conductor(x):
    #Comprobar CUIL
    cuil=input("Ingrese su numero de CUIL: ")
    name= "CUIL"
    z1=12
    z2=10
    y=x
    cuil=comprobacion_largo(cuil,y,z1,z2,name)
    #Comprobar Licencia
    licencia= input ("Ingrese su numero de licencia: ")
    y="SELECT C_Licencia FROM Conductores where C_Licencia=?;"
    name="Licencia"
    z1=9
    z2=6
    licencia= comprobacion_largo(licencia, y, z1,z2, name)
    



    categoria=input("Ingrese la categoria de su licencia: ")
    categoria=comprobacion_categorias(categoria,cat_dic)
    patente= input ("Ingrese la patente de su vehiculo: ")
    patente=comprobacion_patente(patente)
    nombre=input("Ingrese su nombre: ")
    nombre=comprobacion_NO_Num(nombre)
    apellido=input("Ingrese su apellido: ")
    apellido=comprobacion_NO_Num(apellido)
    año=input("Ingres el año de vencimiento de su licencia: ")
    año=comprobar_año(año)
    mes=input("Ingrese el mes de vencimiento de su licencia: ")
    mes=comprobar_mes(mes)
    dia=input("Ingrese el día de vencimiento de su licencia: ")
    dia=comprobar_dia(dia)
    vencimiento= (dia+"/"+mes+"/"+año)
    tarjeta=None

    print ('------------------------')
    print ('DATOS DE USUARIO:')
    print ('CUIL: ', cuil)
    print ('NOMBRE: ', nombre)
    print ('APELLIDO: ', apellido)
    print ('CATEGORIA DE LICENCIA: ', categoria)
    print ('VENCIMIENTO DE LICENCIA: ', vencimiento)
    print ('N° DE LICENCIA: ', licencia)
    print ('PATENTE DEL VEHICULO: ', patente)
    comprobacion_datos=input("Los datos son correctos? S/N: ")
    if comprobacion_datos == "s" or comprobacion_datos == "S" or comprobacion_datos == "Si" or comprobacion_datos == "si" or comprobacion_datos== "Sí" or comprobacion_datos=="SI" or comprobacion_datos=="Sí":
        pass
    elif comprobacion_datos == "n" or comprobacion_datos == "N" or comprobacion_datos == "No" or comprobacion_datos == "NO" or comprobacion_datos== "no":
        return alta_conductor(x)
    else:
        print ("La respuuesta solo puede ser SI o NO")
    print (""" ---- """*6)
    
    return (cuil,nombre,apellido,categoria,vencimiento,licencia,patente)


#agregar tarjeta
def agregar_tarjeta():
        tarjeta=input("Ingrese su tarjeta (opcional): ")
        comprobacion_numeros(tarjeta)
        while True:
            if len(tarjeta)>16 or len(tarjeta)<10:
                print("Su número de tarjeta es inválido,  tiene que tener entre10 a 16 numeros.")
                tarjeta=input("Ingrese su tarjeta (opcional): ")
                comprobacion_numeros(tarjeta)
            else:
                print ("Tarjeta agregada con exito")
                break
        return tarjeta
    
def historial (x,y):
    if int(x) <= len(y):
        x= int(x)-1
        print ('ID: ', y [int(x)][0])
        print ('Distancia: ', y [int(x)][1])
        print ('Tarifa: ', y [int(x)][2])
        print ('Patente del auto: ', y [int(x)][3])
        print ('CUIL: ', y [int(x)][4])
        print ('DNI: ', y [int(x)][5])
        print ('Fecha: ', y [int(x)][6])
        return True
    elif int(x) > len(y):
        print ("numero incorrecto")
        return False

def opc_pasajero(x):
    if x == "a" or x == "A":
        print ("Hola bienvenido a la App-Pasajeros")
        print ("A traves de acá va a poder gestionar sus viajes!")
        print ("Usted posee un usario dentro la app?. Ingrese una de las opciones.")
        opcion_usuario= input ("Posee un usario? S/N: ")
        opcion_usuario= comprobacion_NO_Num(opcion_usuario)
        print (""" ---- """*10)
        #Alta de datos
        if opcion_usuario == "n" or opcion_usuario == "N" or opcion_usuario == "No" or opcion_usuario == "NO" or opcion_usuario== "no":
            sql_alta_usuario= "SELECT cl_dni FROM Clientes where cl_dni=?;"
            usuarios=alta_usuario(sql_alta_usuario)
            print (usuarios)
            cursor.execute("INSERT INTO clientes VALUES (?,?,?,?)", usuarios)
            con.commit()
            usuario_actual=usuarios[1]
            print ("El usuario",usuario_actual," ha creado con exito. ")
            return usuarios
        else:
            ("La respuesta solo puede ser S/N.")



        #Comprobación de datos        
        if opcion_usuario == "s" or opcion_usuario == "S" or opcion_usuario == "Si" or opcion_usuario == "si" or opcion_usuario== "Sí" or opcion_usuario=="SI" or opcion_usuario=="Sí":
            ingreso = input ('INGRESE SU USUARIO: ')
            comprobacion_numeros(ingreso)
            sql_usuario="select CL_DNI, CL_Nombre, CL_Telefono, CL_Tarjeta from Clientes WHERE CL_DNI = ?"
            cursor.execute(sql_usuario,(ingreso,))
            usuario=cursor.fetchone()
            while True:
                if usuario:
                    print ('INGRESANDO....')
                    break
                else:
                    print ('USUARIO INVALIDO')
                    ingreso = input ('INGRESE SU USUARIO: ')
                    cursor.execute(sql_usuario,(ingreso,))
                    usuario=cursor.fetchone()
            return usuario

def opc_conductor(x):
    if x == "b" or x == "B":
        print ("Hola bienvenido a la App-Conductores")
        print ("A traves de acá va a poder gestionar sus viajes!")
        print ("Usted posee un usario dentro la app?. Ingrese una de las opciones.")
        opcion_conductor= input ("Posee un usario? S/N: ")
        opcion_conductor= comprobacion_NO_Num(opcion_conductor)
        print (""" ---- """*10)
        #Alta de datos
        if opcion_conductor == "n" or opcion_conductor == "N" or opcion_conductor == "No" or opcion_conductor == "NO" or opcion_conductor== "no":
            sql_alta_conductor= "SELECT C_Cuil FROM Conductores where C_Cuil=?;"
            conductor=alta_conductor(sql_alta_conductor)
            print (conductor)
            cursor.execute("INSERT INTO Conductores VALUES (?,?,?,?,?,?,?)", conductor)
            cursor.execute("INSERT INTO Vehiculos(V_Patente) VALUES (?)", (conductor[6],))
            con.commit()
            usuario_actual= conductor[2]+" "+conductor[1]
            print ("Bienvenido a nuestra app ",usuario_actual," ha creado con exito. ")
            return conductor
        else:
            ("La respuesta solo puede ser S/N.")



        #Comprobación de datos
        if opcion_conductor == "s" or opcion_conductor == "S" or opcion_conductor == "Si" or opcion_conductor == "si" or opcion_conductor== "Sí" or opcion_conductor=="SI" or opcion_conductor=="Sí":
            ingreso = input ('INGRESE SU CUIL: ')
            comprobacion_numeros(ingreso)
            sql_conductor="select C_Cuil, C_Nombre, C_Apellido, C_Categoria, C_Vencimiento, C_Licencia, C_Patente from Conductores WHERE C_CUIL = ?"
            cursor.execute(sql_conductor,(ingreso,))
            conductor=cursor.fetchone()
            while True:
                if conductor:
                    print ('INGRESANDO....')
                    break
                else:
                    print ('USUARIO INVALIDO')
                    ingreso = input ('INGRESE NUEVAMENTE SU CUIL: ')
                    cursor.execute(sql_conductor,(ingreso,))
                    conductor=cursor.fetchone()
            return conductor

def conductor_int (x,y,z):
    mantener_interfaz=z
    est_cond= "0"
    while z == "1":
        if (x == "b" or x == "B") and (y is not None) and (mantener_interfaz== "1"):
            print ("Bienvenido ",y [1] ,", que desea hacer hoy? ")
            if est_cond == "0" :
                print ("""      A- Habilitarme para conducir""")
            if est_cond == "1" :
                print ("""      A- Desabilitarme para conducir """)
            print ("""      B- Revisar historial""")
            sql="SELECT CL_Tarjeta FROM Clientes WHERE CL_DNI = ?;"
            cursor.execute(sql,(y[0],))
            tarjeta=cursor.fetchone()
            print ("""      C- Modificar datos de usuario""")
            print ("""      D- Modificar datos del vehiculo  """)
            print ("""      E- Balance de ganancias """)
            print ("""      F- Salir
                """)
            opcion=input ("Elija su opcion (A,B,C,D,E,F): ")
            comprobacion_NO_Num(opcion)
            
            #online/ofline del conductor
            if (opcion == "a" or opcion == "A") and (y is not None) and (est_cond == "0"):
                est_cond = "1"
                print ("*---------------------------------------------------------------------------------------------*")
                print ("|Ya estas habilitado para conducir, recibiras una alerta cuando tengas un viaje para realizar.|")
                print ("*---------------------------------------------------------------------------------------------*")
            elif (opcion == "a" or opcion == "A") and (y is not None) and (est_cond == "1"):
                est_cond = "0"
                print ("*--------------------------------------------------------------------------------*")
                print ("|Se desahbilito la conducción. No recibiras viajes hasta que vuelvas a activarla.|")
                print ("*--------------------------------------------------------------------------------*")
                
            #historial del conductor
            elif (opcion == "b" or opcion == "B") and (y is not None):
                RH=False
                sql="SELECT * FROM historial WHERE H_Cuil = ?;"
                cursor.execute(sql,(y[0],))
                HISTORIAL= cursor.fetchall()
                while True:
                    if len(HISTORIAL) >= 1 :
                        print ("Historial de ",y[1],":")
                        for ID,H_Distancia,H_tarifa,H_patente,H_Cuil,H_DNI,H_Fecha, in HISTORIAL:
                            if y:
                                i=1
                                print("Numero de historial: ",i,"--- ","Numero de ID:", ID, "  Fecha: ", H_Fecha )
                                i+=1
                            else:
                                pass
                    
                        opcion_historial= input("Seleccione su numero de historial: ")
                        comprobacion_numeros(opcion_historial)
                        RH=historial (opcion_historial,HISTORIAL)
                        break
                    elif  not HISTORIAL :
                        print ("Usted todavia no ha realizado ningún viaje.")
                        break
                    continue
                
            #Modificación de datos (Usuario)
            elif (opcion == "c" or opcion == "C") and (y is not None):
                print ("Sus datos son estos por el momento: ")
                print ("Cuil: ", y[0])
                print ("Nombre: ", y[1])
                print ("Apellido: ", y[2])
                print ("Categoria: ", y[3])
                print ("Vencimiento de la licencia: ", y[4])
                print ("Numero de licencia: ", y[5])
                print ("Patente: ", y[6])
                opcion_mod= input("Desea cambiar algún dato? S/N: ")
                print ("\n")
                if opcion_mod == "s" or opcion_mod == "S" or opcion_mod == "Si" or opcion_mod == "si" or opcion_mod== "Sí" or opcion_mod=="SI" or opcion_mod=="Sí":
                    print (" Elije la opcion que seas modificar:")
                    print (" 1 - Cuil")
                    print (" 2 - Nombre")
                    print (" 3 - Apellido")
                    print (" 4 - Categoria")
                    print (" 5 - Vencimiento de la licencia")
                    print (" 6 - Numero de licencia")
                    print (" 7 - Patente")
                    print (" 8 - Todos los datos")
                    opc_Modificar_usu= input ("Elija una opción: ")
                    print ("\n")
                    match opc_Modificar_usu:
                        case 1 | "1":
                            new_Cuil= int(input ("Ingrese su nuevo CUIL: "))
                            sql= "UPDATE Conductores SET C_Cuil=? where C_Cuil=?;"
                            cursor.execute(sql,(new_Cuil,y[0],))
                            sql= "Select * FROM Conductores where C_Cuil=?;"
                            cursor.execute(sql,(new_Cuil,))
                            y=cursor.fetchone()
                            con.commit ()
                            print ("Datos cambiados correctamente!")
                            print ("\n")
                        case 2 | "2":
                            new_name= input ("Ingrese su nuevo Nombre: ")
                            comprobacion_NO_Num(new_name)
                            sql= "UPDATE Conductores SET C_Nombre=? where C_Nombre=?;"
                            cursor.execute(sql,(new_name,y[1],))
                            sql= "Select * FROM Conductores where C_Nombre=?;"
                            cursor.execute(sql,(new_name,))
                            y=cursor.fetchone()
                            con.commit ()
                            print ("Datos cambiados correctamente!")
                            print ("\n")
                        case 3 | "3":
                            new_lastname= input ("Ingrese su nuevo Apellido: ")
                            comprobacion_NO_Num(new_lastname)
                            sql= "UPDATE Conductores SET C_Apellido=? where C_Apellido=?;"
                            cursor.execute(sql,(new_lastname,y[2],))
                            sql= "Select * FROM Conductores where C_Apellido=?;"
                            cursor.execute(sql,(new_lastname,))
                            y=cursor.fetchone()
                            con.commit ()
                            print ("Datos cambiados correctamente!")
                            print ("\n")
                        case 4 | "4":
                            new_categoria=input("Ingrese su nueva categoria: ")
                            comprobacion_categorias(new_categoria,cat_dic)
                            sql="UPDATE Conductores SET C_Categoria=? where C_Categoria=?;"
                            cursor.execute(sql,(new_categoria,y[3],))
                            sql= "Select * FROM Conductores where C_Categoria=?;"
                            cursor.execute(sql,(new_categoria,))
                            y=cursor.fetchone()
                            con.commit()
                            print ("Datos cambiados correctamente!")
                            print ("\n")
                        case 5 | "5":
                            año=input("Ingres el año de vencimiento de su licencia: ")
                            año=comprobar_año(año)
                            mes=input("Ingrese el mes de vencimiento de su licencia: ")
                            mes=comprobar_mes(mes)
                            dia=input("Ingrese el día de vencimiento de su licencia: ")
                            dia=comprobar_dia(dia)
                            vencimiento= (dia+"/"+mes+"/"+año)
                            sql="UPDATE Conductores SET C_Vencimiento=? WHERE C_Vencimiento=?;"
                            cursor.execute(sql,(vencimiento,y[4]))
                            sql= "Select * FROM Conductores where C_Vencimiento=?;"
                            cursor.execute(sql,(vencimiento,))
                            y=cursor.fetchone()
                            con.commit()
                            print ("Datos cambiados correctamente!")
                            print ("\n")
                        case 6 | "6":
                            licencia= input ("Ingrese su numero de licencia: ")
                            y="SELECT C_Licencia FROM Conductores where C_Licencia=?;"
                            name="Licencia"
                            z1=8
                            z2=7
                            licencia= comprobacion_largo(licencia, y, z1,z2, name)
                            sql="UPDATE Conductores SET C_Licencia=? WHERE C_Licencia=?;"
                            cursor.execute(sql,(licencia,y[5]))
                            sql= "Select * FROM Conductores where C_Apellido=?;"
                            cursor.execute(sql,(licencia,))
                            y=cursor.fetchone()
                            con.commit()
                            print ("Datos cambiados correctamente!")
                            print ("\n")
                        case 7 | "7":
                            patente= input ("Ingrese la patente de su vehiculo: ")
                            patente=comprobacion_patente(patente)
                            sql="UPDATE Conductores SET C_Patente=? WHERE C_Patente=?;"
                            cursor.execute(sql,(patente,y[6]))
                            sql= "Select * FROM Conductores where C_Apellido=?;"
                            cursor.execute(sql,(patente,))
                            y=cursor.fetchone()
                            con.commit()
                            print ("Datos cambiados correctamente!")
                            print ("\n")
                        case 8 | "8":
                            new_Cuil= int(input ("Ingrese su nuevo CUIL: "))
                            sql= "UPDATE Conductores SET C_Cuil=? where C_Cuil=?;"
                            cursor.execute(sql,(new_Cuil,y[0],))
                            sql= "Select * FROM Conductores where C_Cuil=?;"
                            cursor.execute(sql,(new_Cuil,))
                            y=cursor.fetchone()
                            con.commit ()
                            new_name= input ("Ingrese su nuevo Nombre: ")
                            comprobacion_NO_Num(new_name)
                            sql= "UPDATE Conductores SET C_Nombre=? where C_Nombre=?;"
                            cursor.execute(sql,(new_name,y[1],))
                            sql= "Select * FROM Conductores where C_Nombre=?;"
                            cursor.execute(sql,(new_name,))
                            y=cursor.fetchone()
                            con.commit ()
                            new_lastname= input ("Ingrese su nuevo Apellido: ")
                            comprobacion_NO_Num(new_lastname)
                            sql= "UPDATE Conductores SET C_Apellido=? where C_Apellido=?;"
                            cursor.execute(sql,(new_lastname,y[2],))
                            sql= "Select * FROM Conductores where C_Apellido=?;"
                            cursor.execute(sql,(new_lastname,))
                            y=cursor.fetchone()
                            con.commit ()
                            new_categoria=input("Ingrese su nueva categoria: ")
                            comprobacion_categorias(new_categoria,cat_dic)
                            sql="UPDATE Conductores SET C_Categoria=? WHERE C_Categoria=?;"
                            cursor.execute(sql,(new_categoria,y[3]))
                            sql= "Select * FROM Conductores where C_Categoria=?;"
                            cursor.execute(sql,(new_lastname,))
                            y=cursor.fetchone()
                            con.commit()
                            año=input("Ingres el año de vencimiento de su licencia: ")
                            año=comprobar_año(año)
                            mes=input("Ingrese el mes de vencimiento de su licencia: ")
                            mes=comprobar_mes(mes)
                            dia=input("Ingrese el día de vencimiento de su licencia: ")
                            dia=comprobar_dia(dia)
                            vencimiento= (dia+"/"+mes+"/"+año)
                            sql="UPDATE Conductores SET C_Vencimiento=? WHERE C_Vencimiento=?;"
                            cursor.execute(sql,(vencimiento,y[4]))
                            sql= "Select * FROM Conductores where C_Vencimiento=?;"
                            cursor.execute(sql,(new_lastname,))
                            y=cursor.fetchone()
                            con.commit()
                            licencia= input ("Ingrese su numero de licencia: ")
                            y="SELECT C_Licencia FROM Conductores where C_Licencia=?;"
                            name="Licencia"
                            z1=8
                            z2=7
                            licencia= comprobacion_largo(licencia, y, z1,z2, name)
                            sql="UPDATE Conductores SET C_Licencia=? WHERE C_Licencia=?;"
                            cursor.execute(sql,(licencia,y[5]))
                            y=cursor.fetchone()
                            sql= "Select * FROM Conductores where C_Licencia=?;"
                            cursor.execute(sql,(new_lastname,))
                            con.commit()
                            patente= input ("Ingrese la patente de su vehiculo: ")
                            patente=comprobacion_patente(patente)
                            sql="UPDATE Conductores SET C_Patente=? WHERE C_Patente=?;"
                            cursor.execute(sql,(patente,y[6]))
                            sql= "Select * FROM Conductores where C_Patente=?;"
                            cursor.execute(sql,(new_lastname,))
                            y=cursor.fetchone()
                            con.commit()
                            print ("Datos cambiados correctamente!")
                            print ("\n")
                        case _:
                            print ("El caracter ingresado no es una opción.")
                            print ("\n")

            elif (opcion == "d" or opcion == "D") and (y is not None):
                cursor.execute("Select * FROM Vehiculos WHERE V_Patente=?;",(y[6],))
                v=cursor.fetchone()
                print (v)
                print ("Estos son los datos de su vehiculo por el momento: ")
                print ("Patente: ", v[0])
                if v[1] == None:
                    print ("Marca: Sin información.")
                else:
                    print ("Marca: ", v[1])
                if v[2] == None:
                    print ("Modelo: Sin información.")
                else:
                    print ("Modelo: ", v[2])
                if v[3] == None:
                    print ("Color: Sin información.")
                else:
                    print ("Color: ", v[3])
                if v[4] == None:
                    print ("Cedula: Sin información.")
                else:
                    print ("Cedula: ", v[4])
                if v[5] == None:
                    print ("Categoria: Sin información.")
                else:
                    print ("Categoria: ", v[5])
                opcion_mod= input("Desea cambiar algún dato? S/N: ")
                print ("\n")
                if opcion_mod == "s" or opcion_mod == "S" or opcion_mod == "Si" or opcion_mod == "si" or opcion_mod== "Sí" or opcion_mod=="SI" or opcion_mod=="Sí":
                    print (" Elije la opcion que seas modificar:")
                    print (" 1 - Marca")
                    print (" 2 - Modelo")
                    print (" 3 - Color")
                    print (" 4 - Cedula")
                    print (" 5 - Categoria")
                    print (" 6 - Todos los datos")
                    mod_vehiculo_info= input ("Elija una opción: ")
                    print ("\n")
                    match mod_vehiculo_info:
                        case 1 | "1":
                            Marca= input("Ingrese la Marca del vehiculo: ")
                            comprobacion_NO_Num (Marca)
                            cursor.execute ("UPDATE Vehiculos SET V_Marca=? WHERE V_Patente=?;", (Marca,v[0]))
                            cursor.execute ("SELECT * FROM Vehiculos WHERE V_Patente=?;", (v[0],))
                            v=cursor.fetchone()
                            con.commit ()
                            print ("¡Dato cambiado con Exito!")
                            print ("\n")
                        case 2 | "2":
                            Modelo= input("Ingrese la Modelo del vehiculo: ")
                            cursor.execute ("UPDATE Vehiculos SET V_Modelo=? WHERE V_Patente=?;", (Modelo,v[0]))
                            cursor.execute ("SELECT * FROM Vehiculos WHERE V_Patente=?;", (v[0],))
                            v=cursor.fetchone()
                            con.commit()
                            print ("¡Dato cambiado con Exito!")
                            print ("\n")
                        case 3 | "3":
                            Color= input("Ingrese el color del vehiculo: ")
                            comprobacion_NO_Num (Color)
                            cursor.execute ("UPDATE Vehiculos SET V_Color=? WHERE V_Patente=?;", (Color,v[0]))
                            cursor.execute ("SELECT * FROM Vehiculos WHERE V_Patente=?;", (v[0],))
                            v=cursor.fetchone()
                            con.commit()
                            print ("¡Dato cambiado con Exito!")
                            print ("\n")
                        case 4 | "4":
                            Cedula= input("Ingrese el color del vehiculo: ")
                            cursor.execute ("UPDATE Vehiculos SET V_Cedula=? WHERE V_Patente=?;", (Cedula,v[0]))
                            cursor.execute ("SELECT * FROM Vehiculos WHERE V_Patente=?;", (v[0],))
                            v=cursor.fetchone()
                            con.commit()
                            print ("¡Dato cambiado con Exito!")
                            print ("\n")
                        case 5 | "5":
                            Categoria= input("Ingrese el color del vehiculo: ")
                            comprobacion_categorias(Categoria,cat_dic)
                            cursor.execute ("UPDATE Vehiculos SET V_Categoria=? WHERE V_Patente=?;", (Categoria,v[0]))
                            cursor.execute ("SELECT * FROM Vehiculos WHERE V_Patente=?;", (v[0],))
                            v=cursor.fetchone()
                            con.commit()
                            print ("¡Dato cambiado con Exito!")
                            print ("\n")
                        case 6 | "6":
                            #Marca
                            Marca= input("Ingrese la Marca del vehiculo: ")
                            comprobacion_NO_Num (Marca)
                            cursor.execute ("UPDATE Vehiculos SET V_Marca=? WHERE V_Patente=?;", (Marca,v[0]))
                            cursor.execute ("SELECT * FROM Vehiculos WHERE V_Patente=?;", (v[0],))
                            v=cursor.fetchone()
                            con.commit ()
                            print ("¡Dato cambiado con Exito!")
                            print ("\n")
                            #Modelo
                            Modelo= input("Ingrese la Modelo del vehiculo: ")
                            cursor.execute ("UPDATE Vehiculos SET V_Modelo=? WHERE V_Patente=?;", (Modelo,v[0]))
                            cursor.execute ("SELECT * FROM Vehiculos WHERE V_Patente=?;", (v[0],))
                            v=cursor.fetchone()
                            con.commit()
                            print ("¡Dato cambiado con Exito!")
                            print ("\n")
                            #Color
                            Color= input("Ingrese el color del vehiculo: ")
                            comprobacion_NO_Num (Color)
                            cursor.execute ("UPDATE Vehiculos SET V_Color=? WHERE V_Patente=?;", (Color,v[0]))
                            cursor.execute ("SELECT * FROM Vehiculos WHERE V_Patente=?;", (v[0],))
                            v=cursor.fetchone()
                            con.commit()
                            print ("¡Dato cambiado con Exito!")
                            print ("\n")
                            #Cedula
                            Cedula= input("Ingrese el cedula del vehiculo: ")
                            cursor.execute ("UPDATE Vehiculos SET V_Cedula=? WHERE V_Patente=?;", (Cedula,v[0]))
                            cursor.execute ("SELECT * FROM Vehiculos WHERE V_Patente=?;", (v[0],))
                            v=cursor.fetchone()
                            con.commit()
                            print ("¡Dato cambiado con Exito!")
                            print ("\n")
                            #Categoria
                            Categoria= input("Ingrese el categoria del vehiculo: ")
                            comprobacion_categorias(Categoria,cat_dic)
                            cursor.execute ("UPDATE Vehiculos SET V_Categoria=? WHERE V_Patente=?;", (Categoria,v[0]))
                            cursor.execute ("SELECT * FROM Vehiculos WHERE V_Patente=?;", (v[0],))
                            v=cursor.fetchone()
                            con.commit()
                            print ("¡Dato cambiado con Exito!")
                            print ("\n")
                        case _:
                            print ("not ok")
            elif (opcion == "e" or opcion == "E") and (y is not None):
                print( "Usuario ", y[2], ":")
                cursor.execute("SELECT COUNT (H_Tarifa) FROM Historial WHERE H_Patente=?;", (y[6],))
                Conteo= cursor.fetchone()
                print ("Ha hecho un total de ", Conteo [0], " viajes.")
                if int(Conteo[0]) > 0:
                    cursor.execute ("select SUM (H_Tarifa) from Historial where H_Patente=?;",(y[6],))
                    Pago_total=cursor.fetchone()
                    print("Se le ha pagado un total de $", Pago_total[0])
                    print ("Tarifa de la aplicación 10%.")
                    ganancia= int(Pago_total[0])* 90 //100
                    print ("Ganancia total de: $",ganancia )
                    print ("\n")
                else:
                    print ("Necesita al menos un viaje para calcular un balance")
                    print ("\n")
            elif (opcion == "f" or opcion == "F") and ( y is not None):
                comprobacion_salir=input ("Esta seguro que quiere salir (S/N):")
                if comprobacion_salir == "s" or comprobacion_salir == "S" or comprobacion_salir == "Si" or comprobacion_salir == "si" or comprobacion_salir== "Sí" or comprobacion_salir=="SI" or comprobacion_salir=="Sí":
                    mantener_interfaz="0"
                    return mantener_interfaz
                else:
                    pass
                if comprobacion_salir == "n" or comprobacion_salir == "N" or comprobacion_salir == "No" or comprobacion_salir == "NO" or comprobacion_salir== "no":
                    pass
def pasajero_int(x, y,z):
    mantener_interfaz=z
    while z == "1":
        if (x == "a" or x == "A") and (y is not None) and (mantener_interfaz== "1"):
            print ("Bienvenido ",y [1] ,", que desea hacer hoy? ")
            print ("""      A- Comenzar un viaje
      B- Revisar historial""")
            sql="SELECT CL_Tarjeta FROM Clientes WHERE CL_DNI = ?;"
            cursor.execute(sql,(y[0],))
            tarjeta=cursor.fetchone()
            if tarjeta[0] is not None:
                print ("""      C- Modificar N° de tarjeta""")
            else:
                print ("""      C- Agregar tarjeta  """)
               
            print ("""      D- Salir
                """)
            opcion=input ("Elija su opcion (A,B,C,D): ")
            comprobacion_NO_Num(opcion)
            if (opcion == "a" or opcion == "A") and (y is not None):    
                print("Ingrese la ubicación en la que se encuentra: ")
                sql=cursor.execute("SELECT id, origen FROM kilometros;") 
                for origen in sql:
                    a=int(origen[0])
                    print(a, ": ", origen[1])
                    continue
                opcion_origen=input("Ingrese la opcion deseada: ")
                comprobacion_numeros(opcion_origen)
                sql="SELECT origen FROM kilometros WHERE id=?"
                cursor.execute(sql,(opcion_origen,))
                origen_sql=cursor.fetchone()
                origen=origen_sql[0]
                print("Su origen es: ", origen)
                print ("Por el momento estos son los lugares al que puede ir: ")
                sql="SELECT id, destino FROM kilometros WHERE origen = ?;"
                cursor.execute(sql, (origen,))
                destino_sql=cursor.fetchall()
                for destino in destino_sql:
                    a=destino[0]
                    print(a, ": ", destino[1])
                    continue
                opcion_destino=input("Ingrese el destino deseado: ")
                comprobacion_numeros(opcion_destino)
                sql="SELECT destino FROM kilometros WHERE id=?;"
                cursor.execute(sql,(opcion_destino,))
                destino_sql=cursor.fetchone()
                destino=destino_sql[0]

                #calculo el precio:
                sql="select preciokm * distancia from kilometros where origen = ? and destino = ?"
                precio=cursor.execute(sql,(origen,destino))
                precio=cursor.fetchone()
                print("El precio de su viaje será de: ", precio)
                #----------------------------------------------#
                comprobar_viaje= input("Desea pagar ese viaje? (S/N): ")
                if comprobar_viaje == "s" or comprobar_viaje == "S" or comprobar_viaje == "Si" or comprobar_viaje == "si" or comprobar_viaje== "Sí" or comprobar_viaje=="SI" or comprobar_viaje=="Sí":
                    ID=cursor.execute ("select COUNT (id) from historial;")
                    ID=cursor.fetchone()
                    ID=list(ID)
                    ID=[x+1 for x in ID]
                    ID=tuple(ID)
                    distancia=cursor.execute("select distancia from kilometros where origen = ? and destino = ?", (origen,destino))
                    distancia=cursor.fetchone()
                    auto_random= cursor.execute("select C_Patente from Conductores order by random() LIMIT 1")
                    auto_random=cursor.fetchone()
                    conductor_cuil= cursor.execute("select C_Cuil from Conductores where C_Patente = ?", auto_random)
                    conductor_cuil=cursor.fetchone()
                    DNI = y[0]
                    fecha= datetime.today().strftime('%Y/%m/%d')
                    valores=(ID[0],distancia[0],precio[0],auto_random[0],conductor_cuil[0],DNI,fecha)
                    cursor.execute("INSERT INTO historial (ID,H_distancia,H_tarifa,H_patente,H_Cuil,H_DNI,H_Fecha)VALUES (?,?,?,?,?,?,?)", valores)
                    con.commit()
                    print ("Viaje hecho con exito!")
                    print("Puede revisar su viaje en el historial.")

                elif comprobar_viaje == "n" or comprobar_viaje== "N" or comprobar_viaje== "No" or comprobar_viaje== "NO" or comprobar_viaje== "no":
                    pass
                else:
                    print ("La respuesta solo puede ser S/N.")
                        
       
            #Revisar el historial.
            elif (opcion == "b" or opcion == "B") and (y is not None):
                sql="SELECT * FROM historial WHERE H_DNI = ?;"
                cursor.execute(sql,(y[0],))
                HISTORIAL= cursor.fetchall()
                print ("Historial de ",y[1],":")
                while True:
                    for ID,H_Distancia,H_tarifa,H_patente,H_Cuil,H_DNI,H_Fecha, in HISTORIAL:
                        if y:
                            i=1
                            print("Numero de historial: ",i,"--- ","Numero de ID:", ID, "  Fecha: ", H_Fecha )
                            i+=1
                        else:
                            pass
                    opcion_historial= input("Seleccione su numero de historial: ")
                    comprobacion_numeros(opcion_historial)
                    RH=historial (opcion_historial,HISTORIAL)
                    if RH == True:
                        break
                    else:
                        pass
                    continue
                    
            #agregar tarjeta
            elif (opcion == "c" or opcion == "C") and (y is not None):
                tarjeta=agregar_tarjeta()
                query="UPDATE clientes SET CL_Tarjeta = ? WHERE CL_DNI = ?"
                cursor.execute(query,(tarjeta, y[0]))
                con.commit()
            #salir 
            elif (opcion == "d" or opcion == "D") and (y is not None):
                comprobacion_salir=input ("Esta seguro que quiere salir (S/N):")
                if comprobacion_salir == "s" or comprobacion_salir == "S" or comprobacion_salir == "Si" or comprobacion_salir == "si" or comprobacion_salir== "Sí" or comprobacion_salir=="SI" or comprobacion_salir=="Sí":
                    mantener_interfaz="0"
                    return mantener_interfaz
                else:
                    pass
                if comprobacion_salir == "n" or comprobacion_salir == "N" or comprobacion_salir == "No" or comprobacion_salir == "NO" or comprobacion_salir== "no":
                    pass
                else:
                    pass
            else:
                print ("Incorrecto. Por favor seleccione A,B,C o D")
                opcion=input ("Elija su opcion (A,B,C): ")
                print (""" ---- """*6)
        else:
            break
    else:
        pass



def estructura(x):
    mantener_interfaz=x
    while salir == "0" and (mantener_interfaz == "0"):
        print (""" ---- """*10)
        print ("Bienvenido a  Cadify-App")

        print("A travez de esta aplicación podra coordinar sus viajes a cualquier parte de la ciudad")

        print ("Comencemos, por favor escriba la letra de  una de las siguentes opciones")

        print ("""          A- Soy Pasajero!
          B- Soy Conductor!
          C- Salir""")

        opcion=input ("Elija su opcion (A,B o C): ")
        menu(opcion)
        print (""" ---- """*6)
        if opcion == "a" or opcion == "A":
            usuario_info= opc_pasajero(opcion)
            mantener_interfaz="1"
            usuario_actual= usuario_info [1]
        if opcion == "b" or opcion == "B":
            usuario_info=opc_conductor(opcion)
            mantener_interfaz="1"
            usuario_actual= usuario_info [1]
        if opcion == "c" or opcion == "C":
            mantener= "z"
            print ("Cerrando programa....")
            break
        if opcion == "a" or opcion == "A":
            mantener_interfaz=pasajero_int(opcion,usuario_info,mantener_interfaz)
        if opcion == "b" or opcion == "B":
            mantener_interfaz=conductor_int (opcion,usuario_info,mantener_interfaz)


        



estructura(mantener_interfaz)
