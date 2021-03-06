"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista .
"""

import config as cf
import sys
import csv
from ADT import list as lt
from DataStructures import listiterator as it
from DataStructures import liststructure as lt
from Sorting import mergesort as me

from time import process_time 


def loadCSVFile (file, sep=";"):
    """
    Carga un archivo csv a una lista
    Args:
        file
            Archivo csv del cual se importaran los datos
        sep = ";"
            Separador utilizado para determinar cada objeto dentro del archivo
        Try:
        Intenta cargar el archivo CSV a la lista que se le pasa por parametro, si encuentra algun error
        Borra la lista e informa al usuario
    Returns: None  
    """
    lst = lt.newList("ARRAY_LIST") #Usando implementacion arraylist
    #lst = lt.newList() #Usando implementacion linkedlist
    print("Cargando archivo ....")
    t1_start = process_time() #tiempo inicial
    dialect = csv.excel()
    dialect.delimiter=sep
    try:
        with open(file, encoding="utf-8") as csvfile:
            spamreader = csv.DictReader(csvfile, dialect=dialect)
            cantidad=0
            for row in spamreader: 
                lt.addLast(lst,row)
                cantidad+=1
                if cantidad==100000:
                    break
    except:
        print("Hubo un error con la carga del archivo")
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return lst

def encontrar_buenas_peliculas(peliculas,casting,director,needoflist):
    t1_start = process_time() #tiempo inicial
    iteradorcasting=it.newIterator(casting)
    idmovies=[]
    goodmovies=[0,0,[]]
    position=0
    while it.hasNext(iteradorcasting):
        movie=it.next(iteradorcasting)
        if director.lower() == movie["director_name"].lower():
            idmovies.append(position)
        position+=1
    for each in idmovies:
        movie=lt.getElement(peliculas,each)
        if not needoflist:
            if float(movie["vote_average"])>=6.0:
                goodmovies[0]+=1
                goodmovies[1]+=float(movie["vote_average"])
        elif needoflist:
            goodmovies[0]+=1
            goodmovies[1]+=float(movie["vote_average"])
            goodmovies[2].append(movie)
    if goodmovies[0]!=0:
        goodmovies[1]=round(goodmovies[1]/goodmovies[0],2)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return goodmovies

def conocer_autor(peliculas,casting,actor):
    t1_start = process_time() #tiempo inicial
    iteradorcasting=it.newIterator(casting)
    idmovies=[]
    most=["DirectorName",0]
    moviesautor=[0,0,[],{}]
    position=0
    while it.hasNext(iteradorcasting):
        movie=it.next(iteradorcasting)
        if actor == movie["actor1_name"] or actor == movie["actor2_name"] or actor == movie["actor3_name"] or actor == movie["actor4_name"] or actor == movie["actor5_name"]:
            idmovies.append((position,movie["director_name"]))
        position+=1
    for each in idmovies:
        movie=lt.getElement(peliculas,each[0])
        moviesautor[0]+=1
        moviesautor[1]+=float(movie["vote_average"])
        moviesautor[2].append(movie)
        if each[1] in moviesautor[3]:
            moviesautor[3][each[1]]+=1
        else:
            moviesautor[3][each[1]]=1 
        if moviesautor[3][each[1]]>most[1]:
            most[0]=each[1]
            most[1]=moviesautor[3][each[1]]
    moviesautor[1]=round(moviesautor[1]/moviesautor[0],2)
    t1_stop = process_time() #tiempo inicial
    print("Tardó "+str(t1_stop-t1_start)+" segundos")
    return [moviesautor[0],moviesautor[1],moviesautor[2],most[0]]
    
def ordenarAverageAsc(mov1:dict,mov2:dict)->bool:
    if float(mov1['vote_average'])>float(mov2['vote_average']):
        return True
    return False
def ordenarAverageDesc(mov1:dict,mov2:dict)->bool:
    if float(mov1['vote_average'])<float(mov2['vote_average']):
        return True
    return False
def ordenarCountAsc(mov1:dict,mov2:dict)->bool:
    if float(mov1['vote_count'])>float(mov2['vote_count']):
        return True
    return False
def ordenarCountDesc(mov1:dict,mov2:dict)->bool:
    if float(mov1['vote_count'])<float(mov2['vote_count']):
        return True
    return False


def crear_ranking_peliculas(peliculas,n_peliculas,CoA,ascOdesc):
    lista_return=[]
    iterador=it.newIterator(peliculas)
    if CoA == True:
        if ascOdesc == True:
            me.mergesort(peliculas,ordenarCountAsc)
        elif ascOdesc == False:
             me.mergesort(peliculas,ordenarCountDesc)   
    elif CoA== False:
        if ascOdesc ==True:
            me.mergesort(peliculas,ordenarAverageAsc)
        elif ascOdesc == False:
             me.mergesort(peliculas, ordenarAverageDesc)
    while n_peliculas != -1 and it.hasNext(iterador):
            n_peliculas-= 1
            movie = it.next(iterador)
            lista_return.append(movie)
    return lista_return

def entender_genero(peliculas,genero):
    t1_start = process_time() #tiempo final
    promedio_y_peliculas=[0,0,[]]
    iteradorpeliculas= it.newIterator(peliculas)

    while it.hasNext(iteradorpeliculas):
        pelicula=it.next(iteradorpeliculas)
        if genero.lower() in pelicula["genres"].lower():
            promedio_y_peliculas[2].append(pelicula)
            promedio_y_peliculas[0]+=1
            promedio_y_peliculas[1]+=float(pelicula["vote_average"])
    promedio_y_peliculas[1]=promedio_y_peliculas[1]/promedio_y_peliculas[0]
    t1_stop = process_time() #tiempo final
    print("Tardó "+str(t1_stop-t1_start)+" segundos")
    return promedio_y_peliculas


def crear_ranking_genero(peliculas,n_peliculas,genero,CoA,ascOdesc):
    lista_ranking=[0,0,[]]
    iterador=it.newIterator(peliculas)
    if CoA == True:
        if ascOdesc == True:
            me.mergesort(peliculas,ordenarCountAsc)
        elif ascOdesc == False:
             me.mergesort(peliculas,ordenarCountDesc)   
    elif CoA== False:
        if ascOdesc ==True:
            me.mergesort(peliculas,ordenarAverageAsc)
        elif ascOdesc == False:
             me.mergesort(peliculas, ordenarAverageDesc)
    while n_peliculas != -1 and it.hasNext(iterador):
            pelicula=it.next(iterador)
            if genero.lower() in pelicula["genres"].lower():
                n_peliculas-= 1
                lista_ranking[2].append(pelicula)
                lista_ranking[0]+=1
                lista_ranking[1]+=float(pelicula["vote_average"])
    lista_ranking[1]=lista_ranking[1]/lista_ranking[0]
    return lista_ranking

def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos Movies Casting")
    print("2- Cargar Datos Movies Details")
    print("3- Cargar buenas películas")
    print("4- Crear ranking de películas")
    print("5- Conocer a un director")
    print("6- Conocer a un actor")
    print("7- Entender un género cinematográgico")
    print("8- Crear ranking del género")
    print("9- Contar los elementos de la Lista")
    print("10- Contar elementos filtrados por palabra clave")
    print("11- Consultar elementos a partir de dos listas")
    print("0- Salir")

def countElementsFilteredByColumn(criteria, column, lst):
    """
    Retorna cuantos elementos coinciden con un criterio para una columna dada  
    Args:
        criteria:: str
            Critero sobre el cual se va a contar la cantidad de apariciones
        column
            Columna del arreglo sobre la cual se debe realizar el conteo
        list
            Lista en la cual se realizará el conteo, debe estar inicializada
    Return:
        counter :: int
            la cantidad de veces ue aparece un elemento con el criterio definido
    """
    if lst['size']==0:
        print("La lista esta vacía")  
        return 0
    else:
        t1_start = process_time() #tiempo inicial
        counter=0
        iterator = it.newIterator(lst)
        while  it.hasNext(iterator):
            element = it.next(iterator)
            if criteria.lower() in element[column].lower(): #filtrar por palabra clave 
                counter+=1           
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return counter

def countElementsByCriteria(criteria, column, lst):
    """
    Retorna la cantidad de elementos que cumplen con un criterio para una columna dada
    """
    return 0

def orderElementsByCriteria(function, column, lst, elements):
    """
    Retorna una lista con cierta cantidad de elementos ordenados por el criterio
    """
    return 0
def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """
    listacasting = None   # se require usar lista definida
    listamovies = None
    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:
            if int(inputs[0])==1: #opcion 1
                listacasting = loadCSVFile("Data/AllMoviesCastingRaw.csv") #llamar funcion cargar datos
                print("Datos cargados, ",listacasting['size']," elementos cargados")
            elif int(inputs[0])==2: #opcion2
                 listamovies = loadCSVFile("Data/AllMoviesDetailsCleaned.csv")
                 print("Datos cargados, ",listamovies['size']," elementos cargados")
            elif int(inputs[0])==3:#opcion3
                if listacasting == None or listamovies == None:
                    print("esta lista esta vacia:(" )
                else: 
                    director=input("Inserta el nombre del director a consultar: ")
                    goodmovies=encontrar_buenas_peliculas(listamovies,listacasting,director,False)
                    print("Las buenas películas de "+director+" son: "+str(goodmovies[0]))
                    print("Los votos promedio de las mismas es: "+str(goodmovies[1]))
            elif int(inputs[0])==4:#opcion4
                        cantidad = int(input("Escriba la cantidad de películas que quiere en el ranking, debe ser mayor o igual a 10: "))                        
                        while 10>cantidad:
                            print("La cantidad debe ser mayor a 10.")
                            cantidad=int(input("Escriba la cantidad de películas que quiere en el ranking: "))
                        AoC=input("Escriba Average, de lo contrario escriba Count: ").title()
                        ascOdesc= input("Según el orden que quiera escriba ascendente o descendente: ").title()
                        if AoC == "Average":
                            if ascOdesc == "Ascendente":
                                lista_final=crear_ranking_peliculas(listamovies,cantidad,False,False)
                            elif ascOdesc == "Descendente":
                                lista_final=crear_ranking_peliculas(listamovies,cantidad,False,True)                           
                        elif AoC == "Count":
                            if ascOdesc == "Ascendente":
                                lista_final=crear_ranking_peliculas(listamovies,cantidad,True,False)
                            elif ascOdesc == "Descendente":
                                lista_final=crear_ranking_peliculas(listamovies,cantidad,True,True)
                        if len(lista_final)>0:
                            print("El ranking de películas es: ",lista_final)
                          
            elif int(inputs[0])==5:#opcion5
                 if listacasting == None or listamovies == None:
                     print("esta lista esta vacia:(" )
                 else: 
                      director=input("Ingresa el nombre de un director: ")
                      conocerdirector=encontrar_buenas_peliculas(listamovies,listacasting,director,True)
                      print("La cantidad de películas dirigidas por "+director+" es "+str(conocerdirector[0]))
                      print("El promedio de las películas "+str(conocerdirector[1]))
                      answer=input("Deseas ver la lista de películas dirigidas por "+director+"?: Y/N")
                      while answer.lower()!="y"and"n":
                        answer=input("Deseas ver la lista de películas dirigidas por "+director+"?: Y/N")
                      if answer.lower()=="y":
                          print("Las películas dirigidas por "+director+" son:")
                          print(conocerdirector[2])
            elif int(inputs[0])==6:#opcion6
                if listacasting == None or listamovies == None:
                     print("esta lista esta vacia:(" )
                else: 
                     autor=input("Ingresa a un autor: ")
                     pelisautor=conocer_autor(listamovies,listacasting,autor)
                     if len(pelisautor)>0:
                         print(pelisautor)
            elif int(inputs[0])==7:#opcion7
                 if listacasting == None or listamovies == None:
                     print("Esta lista esta vacia:(" ) 
                 else:                        
                      genero=input("Escriba el género con el quiera crear el ranking: ")
                      entender_genero(listamovies,genero)
                      
                      
            elif int(inputs[0])==8:#opcion8
                if listacasting==None or listamovies==None or listacasting['size']==0 or listamovies['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")    
                else: print("La lista tiene ",lista['size']," elementos")
            elif int(inputs[0])==9: #opcion 9
                if listacasting==None or listamovies==None or listacasting['size']==0 or listamovies['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:   
                    criteria =input('Ingrese el criterio de búsqueda\n')
                    counter=countElementsFilteredByColumn(criteria, "nombre", lista) #filtrar una columna por criterio  
                    print("Coinciden ",counter," elementos con el crtierio: ", criteria  )
            elif int(inputs[0])==10: #opcion 10
                if listacasting==None or listamovies==None or listacasting['size']==0 or listamovies['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:
                    criteria =input('Ingrese el criterio de búsqueda\n')
                    counter=countElementsByCriteria(criteria,0,lista)
                    print("Coinciden ",counter," elementos con el crtierio: '", criteria ,"' (en construcción ...)")
            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                
if __name__ == "__main__":
    main()