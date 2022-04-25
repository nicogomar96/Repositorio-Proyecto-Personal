import os
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
pw = 'Contratra2030'

class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://instagram.com/")
        self.driver.fullscreen_window()
        sleep(3)
        e = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        e.send_keys(username)
        sleep(2)
        e = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        e.click()
        sleep(2)
        e.send_keys(pw[0])
        sleep(2)
        e.click()
        pw = pw[1:]
        e = e.send_keys(pw)
        try:
            self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        except Exception as e:
            print("No ingresó")
        sleep(5)

    # Método encargado de buscar una cuenta de usuario luego de hacer log-in

    def search_user(self, cuenta_a_buscar):
        return self.driver.get("https://instagram.com/" + cuenta_a_buscar)

    # Método encargado de obtener los seguidores y siguiendos de la cuenta correspondiente
    def get_unfollowers(self):
        """
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click() """
        following = self.following_users()
        followers = self.followers_users()
        for u in following:
            if u not in followers:
                print(u)
    # Método encargado de obtener los usuarios que siguen al perfil abierto
    def following_users(self):
        sleep(3)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]').click()
        following = self._get_names()
        self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[1]/div/div[3]/div/button').click()
        return following
    # Método encargado de obtener los usuarios a quienes sigue el perfil abierto
    def followers_users(self):
        sleep(3)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]').click()
        followers = self._get_names()
        self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[1]/div/div[3]/div/button').click()
        return followers

    # Método encargado hacer scroll en las ventanas
    def _get_names(self):
        sleep(3)
        try:
            scroll_box = self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div[3]")
        except Exception as e:
            scroll_box = self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(2)
            ht = self.driver.execute_script("""
                    arguments[0].scrollTo(0, arguments[0].scrollHeight);
                    return arguments[0].scrollHeight;
                    """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        return names

    # Método encargado de seguir a un usuario pasado por parametro
    def seguir_usuario(self, urlToFollow):
        urlToFollow = "https://instagram.com/" + urlToFollow
        self.driver.get(urlToFollow)
        sleep(3)
        try:
            self.driver.find_element_by_xpath('/html/body/div/section/main/div/header/section/div/div').click()
        except Exception as e:
            self.driver.find_element_by_class_name('button').click()

    # Deja de seguir a un usuario dada su url
    def dejar_de_seguir_usuario(self, urlToUnfollow):
        self.driver.get(urlToUnfollow)
        sleep(2)
        self.driver.find_element_by_xpath("//div[contains(@class,'YBx95')]").click()
        sleep(2)
        try:
            self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[1]").click()
        except:
            self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[1]").click()

    # Método encargado de comparar número de seguidores y seguidos de una cuenta y retorna True si esa cuenta sigue a mas personas que followers tiene, sino devuelve False
    def masSeguidos_Seguidores(self):
        try:    # Se intenta obtener el número de seguidores por id
            siguiendo = self.driver.find_element_by_xpath(
                "//a[contains(@href,'/following')]").text
            seguidores = self.driver.find_element_by_xpath(
                "//a[contains(@href,'/followers')]").text
        except Exception as e:
            try:  #  Si no se logra obtener el número por el método anterior se intenta con este xpath
                siguiendo = self.driver.find_element_by_xpath(
                    "//header[contains(@class,'vtbgv')]//li[3]//a[1]").text
                seguidores = self.driver.find_element_by_xpath(
                    "//main[contains(@class,'o64aR')]//li[2]//a[1]").text
            except Exception as e:
                try:    # Si no se ha podido encontrar con los anteriores buscadores, se intenta con este
                    siguiendo = self.driver.find_element_by_xpath(
                        "//main[contains(@class,'o64aR')]//li[3]").text
                    seguidores = self.driver.find_element_by_xpath(
                        " //main[contains(@class,'o64aR')]//li[2]").text
                except Exception as e:  # Finalmente no se ha encontrado. Se debe buscar solución
                    print("PROBLEMA masSeguidos_Seguidores")
        siguiendo = str(siguiendo).split()[0]
        seguidores = str(seguidores).split()[0]

        if(',' in siguiendo):       # Si la cadena obtenida tiene '.' es 'x' miles. Entonces se separa
            mil = int(siguiendo.split(',')[
                      0]) * 1000; decimal = int(siguiendo.split(',')[1]); siguiendo = str(mil + decimal)
        if(',' in seguidores):
            mil = int(seguidores.split(',')[
                      0]) * 1000; decimal = int(seguidores.split(',')[1]); seguidores = str(mil + decimal)

        if('k' in siguiendo):   # Si la cadena posee 'k' es > 10 mil, por lo que se separa
            siguiendo = str(siguiendo.split('k')[0])
            if(',' in siguiendo):
                siguiendo = int(siguiendo.split(',')[0]) * 1000
            else:
                siguiendo = int(siguiendo) * 1000
            siguiendo = str(siguiendo)
        if('m' in siguiendo):  # Si la cadena posee 'm' son millones, se separa correspondientemente
            siguiendo = str(siguiendo.split('m')[0])
            if(',' in siguiendo):
                siguiendo = int(siguiendo.split(',')[0]) * 1000000
            else:
                siguiendo = int(siguiendo) * 1000000
            siguiendo = str(siguiendo)
        if('k' in seguidores):  # Se repite el proceso anterior (seguidos) para los seguidores
            seguidores = str(seguidores.split('k')[0])
            if('.' in seguidores):
                seguidores = int(seguidores.split('.')[0]) * 1000
            else:
                seguidores = int(seguidores) * 1000
            seguidores = str(seguidores)
        if('m' in seguidores):  # Se repite el proceso anterior (seguidos) para los seguidores
            seguidores = str(seguidores.split('m')[0])
            if('.' in seguidores):
                seguidores = int(seguidores.split('.')[0]) * 1000000
            else:
                seguidores = int(seguidores) * 1000000
            seguidores = str(seguidores)

        # Sea cual sea el resultado anterior se transforma el valor final a NÚMERO
        siguiendo = int(siguiendo)
        # Sea cual sea el resultado anterior se transforma el valor final a NÚMERO
        seguidores = int(seguidores)

        if (siguiendo > seguidores):  # Se compara si se sigue a mas personas que quienes le siguen
            return True
        return False

    # Dados dos usuarios, devuelve todos los usuarios que son seguidos mutuamente por los dos pasados por parámetro
    def seguidos_en_comun(self, user1, user2):
        lista = []
        self.search_user(user1)  # Buscamos primer usuario
        f1 = self.following_users()  # GET usuarios a quienes sigue user1
        self.search_user(user2)  # Buscamos segundo usuario
        f2 = self.following_users()  # GET usuarios a quienes sigue user2
        for elem in f1:  #  Por cada seguido por user1 se compara con cada seguidor de user2
            for elem2 in f2:
                if elem == elem2:
                    lista.append(elem)
                    print(elem)
                    break
        return lista

    # Funcion encargada de obtener la lista de personas que le han gustado una foto dado su URL
    def get_likers(self, url_photo):
        self.driver.get(url_photo)  # Abrir url pasada por parametro
        sleep(3)
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div/a").click()  #  Click en 'x me gustas' botón
        sleep(1)
        lista = my_bot.scroll_likes()
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button").click()
        return lista

    def scroll_likes(self):
        sleep(2)
        try:
            scroll_box = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")  # Encuentra el scrollbox (ventana likers)
        except:
            scroll_box = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/div")  # Encuentra el scrollbox (ventana likers)
        last_ht, ht = 0, 1                              
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                    arguments[0].scrollTo(0, arguments[0].scrollHeight);
                    return arguments[0].scrollHeight;
                    """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        return names
            
##################### Fin Clase #####################



# BUSCAR UNFOLLOWERS DE MI CUENTA
def buscar_unfollowers_mi_cuenta():
    my_bot.search_user('nicoleishon96')
    sleep(2)
    my_bot.get_unfollowers()


# A partir del archivo 'fol.txt' recoge cada cuenta en cada fila y si following > followers , guarda esa cuenta en 'final.txt'
def mas_seguidos_masivo_a_partir_de_archivo():
    arch = open('fol.txt', 'r')
    contador = 10
    for s in arch :
        contador = contador -1
        s = s.strip()
        my_bot.search_user(s)
        sleep(3)
        if my_bot.masSeguidos_Seguidores():
            final = open ('final.txt', 'a')
            final.write("https://www.instagram.com/" + s + '\n')
            final.close()
        sleep(2)
        if(contador == 0):
            sleep(60)
            contador = 10
    arch.close()

def buscar_seguidos_por_cuenta(cuenta):
    my_bot.search_user(cuenta)
    sleep(2)
    lista = my_bot.following_users()
    arch = open('fol.txt', 'a')
    n = 0
    for i in lista :
        arch.write(i + '\n')
        n = n+1
    arch.close()

def seguir_a_partir_de_archivo():
    archivo = open('final.txt','r')
    contador = 10
    for s in archivo :
        contador = contador - 1
        s = s.strip()
        my_bot.seguir_usuario(s)
        sleep(2)
        if contador == 0 :
            sleep(60)
            contador = 10
    archivo.close()

def obtener_me_gustas(url_foto):
    likers = my_bot.get_likers(url_foto)
    archivo = open('fol.txt','a')
    for linea in likers:
        archivo.write(linea + '\n')
    archivo.close()

def unfullow_all_following():
    my_bot.search_user(my_bot.username)
    sleep(2)
    following = my_bot.following_users()
    sleep(2)
    contador = 0
    for fol in following:
        contador = contador + 1 
        my_bot.dejar_de_seguir_usuario("https://www.instagram.com/" + fol)
        if(contador == 10):
            sleep(60)
        sleep(1)
    
# ######### INVOCANDO FLUJO LLAMADAS #####################

def pedirNumeroEntero():
    correcto=False
    num=0
    while(not correcto):
        try:
            num = int(input("Introduce un numero entero: "))
            correcto=True
        except ValueError:
            print('Error, introduce un numero entero')
     
    return num


def hola():
    lista_flwME = []
    lista_Iflw = []
    arch = open('fol.txt', 'r')
    for i in arch :
        lista_flwME.append(i)
    arch.close()
    arch = open('final.txt', 'r')
    for i in arch :
        lista_Iflw.append(i)
    arch.close()

    for sigo in lista_Iflw :
        if sigo not in lista_flwME:
            print(sigo + "\n")



salir = False
opcion = 0
while not salir:
    print ("1. Imprimir Unfollowers de mi cuenta")
    print ("2. Buscar usuarios seguidos por una cuenta")
    print ("3. Buscar usuarios que siguen a una cuenta")
    print("4. Obtener los Likes de una fotografía")
    print("5. Obtener usuarios/ seguidos > seguidores, ARCHIVO")
    print("6. Seguir a todos los usuarios en archivo final.txt")
    print("7. Dejar de seguir todos los usuarios seguidos")
    print("8. Obtenr seguidos en común entre dos usuarios")
    print ("0. Salir")
    print ("Elige una opcion")
    opcion = pedirNumeroEntero()
    if opcion == 1:
        my_bot = InstaBot('ususu201', pw)   # INICIALZANDO BOT LOG-IN
        buscar_unfollowers_mi_cuenta()
        my_bot.driver.close()
    elif opcion == 2:
        usuario =  input("Ingrese nombre usuario: ")
        my_bot = InstaBot('ususu201', pw)   # INICIALZANDO BOT LOG-IN
        sleep(2)
        buscar_seguidos_por_cuenta(usuario)
        my_bot.driver.close()
    elif opcion == 3:
        usuario =  input("Ingrese nombre usuario: ")
        my_bot = InstaBot('ususu201', pw)   # INICIALZANDO BOT LOG-IN
        sleep(2)
        my_bot.search_user(usuario)
        sleep(2)
        followers = my_bot.followers_users()
        arch = open('fol.txt', 'a')
        for i in followers:
            arch.write(i + '\n')
        arch.close()
        my_bot.driver.close()
    elif opcion == 4:
        link = input("Ingrese URL foto: ")
        my_bot = InstaBot('ususu201', pw)   # INICIALZANDO BOT LOG-IN
        obtener_me_gustas(link)
        my_bot.driver.close()
    elif opcion == 5:
        my_bot = InstaBot('ususu201', pw)   # INICIALZANDO BOT LOG-IN
        mas_seguidos_masivo_a_partir_de_archivo()
        my_bot.driver.close()
    elif opcion == 6:
        my_bot = InstaBot('ususu201', pw)   # INICIALZANDO BOT LOG-IN
        seguir_a_partir_de_archivo()
        my_bot.driver.close()
    elif opcion == 7:
        my_bot = InstaBot('ususu201', pw)   # INICIALZANDO BOT LOG-IN
        unfullow_all_following()
        my_bot.driver.close()
    elif opcion == 8:
        my_bot = InstaBot('ususu201', pw)   # INICIALZANDO BOT LOG-IN
        user1 = input("Ingrese el nombre del usuario 1: ")
        user2 = input("Ingrese el nombre del usuario 2: ")
        my_bot.seguidos_en_comun(user1,user2)
        my_bot.driver.close()
    else:
        salir = True

pedirNumeroEntero()
print ("")
