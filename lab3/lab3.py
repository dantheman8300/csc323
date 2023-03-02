import requests

def pad_oracle():

    url= 'http://localhost:8080/'
    url2= 'http://localhost:8080/eavesdrop'
    url3= 'http://localhost:8080/submit'

    guess = '9'
    val = "h"
# open ssl - speed test (how many hashes you can do per sec)

    # get leaked cipher text
    req = requests.get(url2).text
    cipher = req.split("<font color=\"red\"> ")[1].split(" </font></p>")[0]
    print("Leaked cipher text:" + cipher)

    t = cipher[len(cipher) - 1] ^ "h" ^ "\x01"


    # check for 404 (not found) or 403 (forbidden)
    check = requests.get(url, {"enc": t}).text
    if ("403" in check):
        print("Fail")
    if ("404" in check):
        print("Success")
    # print(check)



    
    # submit = requests.post(url3, {"guess" : guess}).text.split("<font color=\"red\"> ")[1].split(" </font></p>")[0]
    # print("result: " + submit)


pad_oracle()