#codigo para probar al API de pushbullet que mandara una alerta a cualquier dispositivo Android o iOs
#podemos pedir al usuario que nos introduzca su email que ha usado en su cuenta de pushbullet y le podemos mandar todas las alertas y notificaciones que queramos

import requests
import json
 
def send_notification_via_pushbullet(title, body):
    """ Sending notification via pushbullet.
        Args:
            title (str) : title of text.
            body (str) : Body of text.
    """
    data_send = {"type": "note", "title": title, "body": body, "email": "andre.luque.c@gmail.com"} #aqui especificamos la informacion que ira en el mensaje 
    #https://docs.pushbullet.com/#list-pushes en esta pagina salen todos los parametros que puedes introducir
 
    ACCESS_TOKEN = 'o.KqZ4Geric6A6ybdlQtl0EGupexU4OUyA' #se necesita un token de accesso para acceder a la pagina y realizar un push
    #usamos el modulo request para acceder al API y despues introducirnos nuestro token de accesso y la informacion que queremos mandar
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 'Content-Type': 'application/json'}) 

    if resp.status_code != 200:
        raise Exception('Something wrong')
    else:
        print(resp.text)


