from pinakin.ravan import *

def upstox_login(creds):
  client_id = creds["auth"]["client_id"]
  client_pass = creds["auth"]["client_pass"]
  client_pin = creds["auth"]["client_pin"]
  api_key = creds["auth"]["api_key"]
  api_secret = creds["auth"]["api_secret"]
  redirect_uri = creds["auth"]["redirect_uri"]

  login_url = "https://api-v2.upstox.com/login/authorization/dialog?response_type=code&client_id={}&redirect_uri={}".format(api_key, redirect_uri)

  print(f"Visit this URL: {login_url}. Then, Paste the code from the redirect browser.")

  auth_code = input("Paste the code from the redirect browser here: ")

  # API endpoint URL
  url = "https://api-v2.upstox.com/login/authorization/token"

  # Request headers
  headers = {
      'accept': 'application/json',
      'Api-Version': '2.0',
      'Content-Type': 'application/x-www-form-urlencoded'
  }

  # Request data
  data = {
      'code': auth_code,
      'client_id': api_key,
      'client_secret': api_secret,
      'redirect_uri': redirect_uri,
      'grant_type': 'authorization_code'
  }

  # Make the POST request
  response = requests.post(url, headers=headers, data=data)

  # Check the response
  if response.status_code == 200:
      # Request was successful
      print("Access Token:", response.json().get('access_token'))
      creds["auth"]["access_token"]=response.json().get('access_token')
      creds["api"]["headers"]=headers = {
                                        'accept': 'application/json',
                                        'Api-Version': '2.0',
                                        'Authorization': f'Bearer {creds["auth"]["access_token"]}'
                                    }
      print("Logged in : "+ creds["auth"]["client_id"])
  else:
      # Request failed
      print("Error:", response.status_code, response.text)
      print("Unable to Login in : "+ creds["auth"]["client_id"])

  creds["api"]["last_updated"]=str(datetime.datetime.now().strftime('%H:%M%S'))
  creds["api"]["last_function"]="login"
  return creds

def upstox_auth(creds):
  try:
    url = "https://api-v2.upstox.com/user/profile"

    # Make the GET request
    response = requests.get(url, headers=creds["api"]["headers"])

    # Check the response
    if response.status_code == 200:
        # Request was successful
        json_data = response.json()
        if json_data["status"]=="success":
          print("Authentication Successful: " + creds["auth"]["client_id"])
          return creds
    else:
        # Request failed
        print("Authentication Failed: " + creds["auth"]["client_id"])
        raise KeyError

  except(ValueError, KeyError):
    logging.critical(response)
    print("Logging into: "+ creds["auth"]["client_id"])
    return upstox_login(creds)

def upstox_margin(creds):
  try:
    url = "https://api-v2.upstox.com/user/get-funds-and-margin?segment=SEC"

    # Make the GET request
    response = requests.get(url, headers=creds["api"]["headers"])

    # Check the response
    if response.status_code == 200:
        # Request was successful
        json_data = response.json()
        if json_data["status"]=="success":
          creds["api"]["margin"]=json_data["data"]
        else:
            # Request failed
            print("Status Failed")
            raise KeyError
    else:
      url = "https://api-v2.upstox.com/user/profile" 
      response = requests.get(url, headers=creds["api"]["headers"])
      if response.status_code != 200:
        print(f"Failed to retriece data. Status Code: {response.status_code}") 
        raise KeyError
      else: 
        #Upstox is down in Margin API but rest everything is working.
        return creds

  except(ValueError, KeyError):
    logging.critical("Errors in Margins Module: "+ creds["auth"]["client_id"])
    logging.critical(json_data)
    logging.critical("Curlify Data...")
    logging.critical(curlify.to_curl(response.request))
    print(response)
  
  creds["api"]["last_updated"]=str(datetime.datetime.now().strftime('%H:%M%S'))
  creds["api"]["last_function"]="margin"
  return creds

def upstox_positions(creds):
  try:
    url = "https://api-v2.upstox.com/portfolio/short-term-positions"

    # Make the GET request
    response = requests.get(url, headers=creds["api"]["headers"])

    # Check the response
    if response.status_code == 200:
        # Request was successful
        json_data = response.json()
        if json_data["status"]=="success":
          creds["api"]["positions"]=json_data["data"]
        else:
            # Request failed
            print("Status Failed")
            raise KeyError
    else:
      url = "https://api-v2.upstox.com/user/profile" 
      response = requests.get(url, headers=creds["api"]["headers"])
      if response.status_code != 200:
        print(f"Failed to retriece data. Status Code: {response.status_code}") 
        raise KeyError
      else: 
        #Upstox is down in Position API but rest everything is working.
        return creds

  except(ValueError, KeyError):
    logging.critical("Errors in Margins Module: "+ creds["auth"]["client_id"])
    logging.critical(json_data)
    logging.critical("Curlify Data...")
    logging.critical(curlify.to_curl(response.request))
    print(response)
  
  creds["api"]["last_updated"]=str(datetime.datetime.now().strftime('%H:%M%S'))
  creds["api"]["last_function"]="positions"
  return creds
