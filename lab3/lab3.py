import requests

def pad_oracle():

    url= 'http://localhost:8080/'
    url2= 'http://localhost:8080/eavesdrop'


    req = requests.get(url2)
    check = requests.get(url)


    print(req)
    print(check)


pad_oracle()