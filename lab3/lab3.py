import requests

def pad_oracle():

    url= 'http://localhost:8080/'
    url2= 'http://localhost:8080/eavesdrop'
    url3= 'http://localhost:8080/submit'

    guess = '9'

# open ssl - speed test (how many hashes you can do per sec)
    req = requests.get(url2).text
    check = requests.get(url)

    cipher = req.split("<font color=\"red\"> ")[1].split(" </font></p>")[0]
    print("Leaked cipher text:" + cipher)


    


    # print(check)



    
    # submit = requests.post(url3, {"guess" : guess}).text.split("<font color=\"red\"> ")[1].split(" </font></p>")[0]
    # print("result: " + submit)


pad_oracle()