# IMPORTS NECESARIOS (BIBLIOTECA SELENIUM)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import warnings
from tqdm import tqdm
import sys
import os
import wget


warnings.filterwarnings('ignore')


# ESPECIFICAMOS EL DRIVER
def abrir_ig():
    # ABRIMOS LA PÁGINA WEB
    print('Abriendo el buscador...')
    driver.get("http://www.instagram.com")
    # ACEPTAMOS LAS COOKIES
    print('Aceptando las cookies...')
    cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/button[1]'))).click()
        

def credenciales_ig():
    # INTRODUCIMOS LAS CREDENCIALES
    time.sleep(1)
    print('Introduciendo credenciales de instagram...')
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    # INTRODUCIMOS EL USUARIO (INVENTADO)
    username.clear()
    username.send_keys("alex.martinez5229")
    password.clear()
    password.send_keys("patata")

    # CLICKAMOS EN BOTÓN DE LOG IN
    button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()


def busqueda_ig():
    # BUSCAMOS EL USUARIO DEL QUE EXTRAER INFORMACIÓN
    time.sleep(2)
    keyword = input('Escribe el nombre del usuario del que quieres Scrapear: ')
    print('Buscando...', keyword)
    searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Busca']")))
    searchbox.clear()
    searchbox.send_keys(keyword)
    usuario_encontrado = False
    while not usuario_encontrado:
        #SE HAN ENCONTRADO PERFILES
        try:
            time.sleep(5)
            nombre_usuario = driver.find_element(by=By.XPATH,value='/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a/div/div[2]/div[1]/div/div/div').text
            #EL PERFIL COINCIDE CON EL BUSCADO
            if keyword != nombre_usuario:
                print(
                    'No se ha encontrado el usuario con nombre ' + keyword + ', sin embargo se ha encontrado el siguiente con nombre similar: ' + nombre_usuario)
                keyword = input('Escribe el nombre del usuario del que quieres Scrapear: ')
                searchbox.clear()
                searchbox.send_keys(keyword)
            #EL PERFIL NO COINCIDE CON EL BUSCADO
            else:
                print('¡Se ha encontrado el perfil de '+keyword+'!')
                usuario_encontrado = True
        #NO SE HAN ENCONTRADO PERFILES
        except:
            print("La cuenta no ha sido encontrada o no existe, asegúrate de escribir bien el nombre.")
            keyword = input('Escribe el nombre del usuario del que quieres extraer la información: ')
            searchbox.clear()
            searchbox.send_keys(keyword)
            time.sleep(3)

    time.sleep(3)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(3)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(3)
    return keyword


def info_perfil(keyword):
    # NÚMERO DE SEGUIDORES
    time.sleep(3)
    seguidores = driver.find_element(by=By.XPATH,
                                     value='/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/div/span')
    seguidores = seguidores.get_attribute('title')
    print(keyword + ' tiene: ' + seguidores + ' seguidores.')

    # NÚMERO DE SEGUIDOS
    seguidos = driver.find_element(by=By.XPATH,
                                   value='/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/div/span').text
    print(keyword + ' tiene: ' + seguidos + ' seguidos.')

    # URL DE LA FOTO DE PERFIL
    profile_photo = driver.find_element(by=By.TAG_NAME, value='img')
    profile_photo = profile_photo.get_attribute('src')
    print('Esta es su foto de perfil (URL): ' + profile_photo)

    # INFO TABLÓN
    tablon = driver.find_element(by=By.CLASS_NAME, value='QGPIr').text
    print('En su tablón tiene la siguiente información: \n' + tablon)


def scroll_posts_ig():
    # SCROLL HASTA TENER TODOS LOS POSTS
    time.sleep(5)
    posts = []
    scrolldown = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
    match = False
    scrolls = 0
    print('Procedemos a hacer scroll hasta el primer post, esto puede tardar unos segundos...')
    while (match == False):
        links_posts = driver.find_elements(by=By.TAG_NAME, value='a')
        for link in links_posts:
            #TOMAMOS LA URL DE LOS POSTS
            post = link.get_attribute('href')
            if (post not in posts) and ('/p/' in post):
                posts.append(post)
        last_count = scrolldown
        time.sleep(5)
        scrolldown = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
        scrolls += 1
        print(str(scrolls)+' scrolls realizados.')
        time.sleep(2)
        #YA HEMOS LLEGADO AL FONDO
        if last_count == scrolldown:
            match = True
    print('Encontrados ' + str(len(posts)) + ' posts distintos.')
    return posts


#TOMA LIKES DEL POST
likes_posts = []
def likes_post():
    print('Me gusta')
    try:
        likes_posts.append(driver.find_element(by=By.XPATH,
                                      value='/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/div/a/div').text)
    except:
        try:
            likes_posts.append(driver.find_element(by=By.XPATH,
                                          value='/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/div/a/div').text)
        except:
            try:
                likes_posts.append(driver.find_element(by=By.XPATH,
                                           value='/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[2]/div/span/div/span').text)
            except:
                likes.append('No se pudieron encontrar los likes')



#TOMA LA DESCRIPCIÓN DEL POST
descrip_posts = []
def descrip_post():
    print('Descripcion')
    try:
        descrip = driver.find_element(by=By.XPATH, value=
            '/html/body/div[1]/section/main/div/div/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/span').text
        descrip_posts.append(descrip)
    except:
        descrip_posts.append('No se ha encontrado niguna descripción')

#TOMA LA FECHA DEL POST
fecha_posts = []
def fecha_post():
    print('Fecha')
    try:
        fecha1 = driver.find_element(by=By.XPATH, value=
            '/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[2]/div/a/div/time').text
        fecha_posts.append(fecha)
    except:
        try:
            fecha2 = driver.find_element(by=By.XPATH, value=
                    '/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/div[2]/div/a/div/time').text
        except:
            fecha_posts.append('No se ha encontrado niguna fecha')

#CREA Y ESCRIBE EN EL FICHERO .TXT
def show_info_post(posts, keyword):
    path = os.getcwd()
    ruta_f = keyword + '.txt'
    sys.stdout = open(ruta_f, "w")

    #AHORA LA SALIDA ESTÁNDAR ES EL FICHERO
    for p in range(len(posts)):
        print('Post :'+str(p))
        print(posts[p])
        print(likes_posts[p])
        print(descrip_posts[p])
        print(fecha_posts[p])
        print('\n\n')


def get_urls_ig(posts):
    images = []
    for p in tqdm(range(len(posts))):
        driver.get(posts[p])
        time.sleep(6)
        likes_post()
        descrip_post()
        fecha_post()
        #MIRAMOS SI ES UN VIDEO
        try:
            vid = driver.find_element(by=By.TAG_NAME, value='video')
            vid=vid.get_attribute('poster')
            images.append(vid)

        # ES UNA FOTO
        except:
            try:
                img = driver.find_element(by=By.TAG_NAME, value='img')
                img = img.get_attribute('src')
                images.append(img)
            except:
                print('No se ha identificado la publicación')
    return images


def menu_descarga():
    print('¿Desea descargar las imágenes del usuario? (yes/no): ', end="")
    descarga = input()
    while (descarga != 'yes' and descarga != 'no'):
        print('Escriba "yes" o "no" si desea descargar las imágenes: ', end="")
        descarga = input()
    return 'yes' == descarga


def descarga_images_ig(keyword, urls, descarga):
    if descarga:
        #TOMAMOS LA RUTA ACTUAL
        path = os.getcwd()
        path = os.path.join(path, keyword)

        # CREAMOS EL DIRECTORIO
        try:
            os.mkdir(path)
            print(path)
        except:
            print('El directorio con nombre '+ keyword+ ', ya existe, por ello no se ha vuelto a crear.')

        # DESCARGAMOS LAS IMÁGENES
        counter = 0
        for u in urls:
            save_as = os.path.join(path, keyword + str(counter) + '.jpg')
            wget.download(u, save_as)
            counter += 1
    else:
        print('Mostramos las URLs sin descargarlas:')
        [print(u) for u in urls]

#PROGRAMA PRINCIPAL
def main():
    try:
        abrir_ig()
        credenciales_ig()
        usuario = busqueda_ig()
        info_perfil(usuario)
        posts = scroll_posts_ig()
        urls = get_urls_ig(posts)
        descarga = menu_descarga()
        descarga_images_ig(usuario, urls, descarga)
        show_info_post(posts, usuario)
    except:
        print('Ha ocurrido un problema durante la extracción. Lo más probable es que sea debido a un error de conexión, por favor comprueba tu estado de red')


#COMPROBAMOS QUE LOS ARGUMENTOS SON CORRECTOS ANTES DE EMPEZAR
if len(sys.argv) != 2:
    print('Introduce la ruta completa donde se encuentra tu driver, ejemplo: /Users/user/Documents/chromedriver')
else:
    try:
        driver = webdriver.Chrome(sys.argv[1])
        main()
    except:
        print('La ruta '+sys.argv[1]+ ' no es correcta.')

