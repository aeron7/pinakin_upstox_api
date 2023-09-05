import requests
import json
import logging
from websocket import create_connection

#This function is depreciated and does not work right now. I would not have shared it if it would've worked. Right?

def upstoxlogin(client_id, client_pass, client_pin, forcedlogin="0"):
    method = "v1"

    if method != "v1":
        if method == "v2":
            headers = {'Cookie': 'mode=login'}
            response = requests.get('https://classic-pro.upstox.com/', headers=headers).content
            app_data = json.loads(response.split('service(\'AppDataServ\', function(){ return')[1].split('});angular.module(\'upstoxApp\')')[0])
            api_Id = app_data['apiId']
            api_token = app_data['token']
        elif method == "v3":
            logging.critical("Logging with Upstox V3")
            js_name = requests.get('https://pro.upstox.com/').content
            js_name = str(js_name, "utf-8").split('<script src="/')[1].split('.js')[0]

            # Getting JS Data
            js_data = requests.get('https://pro.upstox.com/' + js_name + '.js').content

            # Extracting App ID and App Token
            api_Id = str(js_data).split('WS":{"apiId":"')[1].split('",')[0]
            api_token = str(js_data).split('.default.WS_LOGINLESS')[0]
            api_token = api_token[:-7].split('":"')

            api_token = api_token[-1] if len(api_token) == 240 else api_token[-2]

        wss_url = f'wss://ws.upstox.com/socket.io/?apiId={api_Id}&token={api_token}&client_id={client_id}&EIO=3&transport=websocket'
        q = create_connection(wss_url)
        logging.critical(q.recv())

        q.send(f'42["message",{{"method":"client_login","type":"interactive","data":{{"client_id":"{client_id}","password":"{client_pass}"}}}}]')
        response = q.recv()
        logging.critical(response)

        if response == "40":
            response = q.recv()
            logging.critical(response)
            if json.loads(response[2:])[1]['response_type'] == "client_login":
                q.send(f'42["message",{{"method":"client_login2fa","type":"interactive","data":{{"password":"{client_pin}"}}}}]')
                response = q.recv()
                logging.critical(response)
                if json.loads(response[2:])[1]['response_type'] == "client_login2fa":
                    logincookie = json.loads(response[13:-1])['data']['login_key']
                    response = "success"  # Fix cases for Password Change or Pin Block
    else:
        payload = {'password': client_pass, 'password2fa': client_pin, 'username': client_id}
        url = "https://pro2.upstox.com/trade/?place/"
        a = requests.post(url, json=payload).content
        a = str(a, "utf-8").split("hmac: ")[1].split(", lkfound:")[0]
        b = json.loads(a)
        api_Id = b['apiId']
        api_token = b['token']
        headers = {'referer': url}
        c = requests.post('https://api.upstox.com/index/publisher/login', headers=headers, json=payload)
        logincookie = c.json().get('loginKey')

    return api_Id, api_token, client_id, logincookie
