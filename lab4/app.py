from flask import Flask, render_template

app = Flask(__name__)

# Example array of blockchain blocks
blocks = [
 {
  "type": 0,
  "id": "124059f656eb6b016ce36583b5d6e9fdaf82420355454a4e436f4ee2ff17dba7",
  "nonce": "5052bfab11df236c43a4d877d93e42a3",
  "pow": "000000be01b9e4b6fdd73985083174007c30a98dc0801eaa830e27bbbea0d705",
  "prev": "124059f656eb6b016ce36583b5d6e9fdaf82420355454a4e436f4ee2ff17dba7",
  "tx": {
   "type": 1,
   "input": {
    "id": "0000000000000000000000000000000000000000000000000000000000000000",
    "n": 0
   },
   "sig": "33399ed9ba1cc40eb1395ef8826955398446badb9c7c84113d545806714809a013c73d71b3326041853638b1190443af",
   "output": [
    {
     "value": 50,
     "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa"
    }
   ]
  }
 },
 {
  "type": 0,
  "id": "ec45827288181e0b3e6cee0712c5770943fce7431c681a6bf0b102efdf18a716",
  "nonce": "4f24b201dcbfc4083f30b495b740275f",
  "pow": "000000ebad2c43c0e1ff9102d2bd606727a71433c716aa0cdb5d35b35ed9c289",
  "prev": "124059f656eb6b016ce36583b5d6e9fdaf82420355454a4e436f4ee2ff17dba7",
  "tx": {
   "type": 1,
   "input": {
    "id": "124059f656eb6b016ce36583b5d6e9fdaf82420355454a4e436f4ee2ff17dba7",
    "n": 0
   },
   "sig": "9dcea2453c136463a5354eff0d28db9c3a1c7a93d7f9ec24be436afb3b534c20181657062122c356d81b37e69e7e3e6d",
   "output": [
    {
     "value": 35,
     "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa"
    },
    {
     "value": 15,
     "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa"
    },
    {
     "value": 50,
     "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa"
    }
   ]
  }
 },
 {
  "type": 0,
  "id": "2c9cf34f507f03dca81825e10f29e4bdf6048f44d0a533f6aec1f60b0087b274",
  "nonce": "cfceeaf77080023e8d4fa11f8f02296a",
  "pow": "000000f2591a4cb72cad825a7b8e9def1ef0e658fc9020fbfb54829b414f8e5a",
  "prev": "ec45827288181e0b3e6cee0712c5770943fce7431c681a6bf0b102efdf18a716",
  "tx": {
   "type": 1,
   "input": {
    "id": "ec45827288181e0b3e6cee0712c5770943fce7431c681a6bf0b102efdf18a716",
    "n": 1
   },
   "sig": "c62b3d57bc49b71bb54b80d8023c735850a3bc60e599b94bebab57aad97923a860de28845fc9bae43f865880874d8449",
   "output": [
    {
     "value": 8,
     "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa"
    },
    {
     "value": 7,
     "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa"
    },
    {
     "value": 50,
     "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa"
    }
   ]
  }
 },
 {
  "type": 0,
  "id": "b4f69646932313fe9b08652c2005c5276616408ed4053a831a8742846b15182b",
  "nonce": "3338c58ef34d6aeb89fc124c9f2ed809",
  "pow": "000000a83fc388ad09485b366d519fe3ee1c210cb4dee0b1cce80b1e4c045fe4",
  "prev": "2c9cf34f507f03dca81825e10f29e4bdf6048f44d0a533f6aec1f60b0087b274",
  "tx": {
   "type": 1,
   "input": {
    "id": "ec45827288181e0b3e6cee0712c5770943fce7431c681a6bf0b102efdf18a716",
    "n": 2
   },
   "sig": "678ece0e4a8fefe20f2136b81ebb3cccc3f90deddfb0b8369115d321ed621cffaa12d9862666e52c191c91ab655e5244",
   "output": [
    {
     "value": 50,
     "pub_key": "ac95f8bb55e2afc2a7a6fa22d0458e65c0903bf5ec6fbde04604680c37d74de3077b0efff889191e269e467024cf609a"
    },
    {
     "value": 50,
     "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa"
    }
   ]
  }
 },
 {
  "type": 0,
  "id": "99f1009b8fb4dd46781f0fd45bcf905480353c4656200e2d91e55bdc181631d1",
  "nonce": "738edca8324fd13d989b1d9771820371",
  "pow": "0000001f6e7ea1dfbe618156b2641f4b81608dee54ba09b034d041a65e30696e",
  "prev": "b4f69646932313fe9b08652c2005c5276616408ed4053a831a8742846b15182b",
  "tx": {
   "type": 1,
   "input": {
    "id": "b4f69646932313fe9b08652c2005c5276616408ed4053a831a8742846b15182b",
    "n": 1
   },
   "sig": "eaf6fdc72c64bc72d36bcb86489e9975ef6b85924e0fb7ef208cae37ae664a2076d63264da417cf58d23d133c87c0396",
   "output": [
    {
     "value": 25,
     "pub_key": "84cf319ea250369a4bc4c03fd8487bc5b017e94dc2c743a49169e5bebb83c0a31362847e739b67bd1b12494009e77dea"
    },
    {
     "value": 25,
     "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa"
    },
    {
     "value": 50,
     "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa"
    }
   ]
  }
 },
 {
  "type": 0,
  "id": "95b36089dbff5b59ce608bcc93c381e63a8d491e8e10ef1df310d5c31b18f301",
  "nonce": "7711f0eba69d5d2e2f1031c9a9b56d42",
  "pow": "0000003192e761d0301dd4c893cbb44256ed5e226cca2812b14c5de0e4c8f7e9",
  "prev": "99f1009b8fb4dd46781f0fd45bcf905480353c4656200e2d91e55bdc181631d1",
  "tx": {
   "type": 1,
   "input": {
    "id": "99f1009b8fb4dd46781f0fd45bcf905480353c4656200e2d91e55bdc181631d1",
    "n": 1
   },
   "sig": "3a7e8cfa4c84a4616f1357a3abfd81bc8875d9fb0413b35d827082b5244c07f70d9f47c3acd6d74b4475ac22668761e7",
   "output": [
    {
     "value": 25,
     "pub_key": "1f39f7a37527c5c895c4c253200ebcb4d0aac29e91d0e34318777ae9a79adfefb2ab10ef5d065f275ad37a1ab6a84730"
    },
    {
     "value": 50,
     "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa"
    }
   ]
  }
 }
]

@app.route('/')
def index():
    return render_template('index.html', blocks=blocks)

@app.route('/blocks')
def view_blocks():
    return render_template('blocks.html', blocks=blocks)

@app.route('/accounts')
def public_keys():
    # Create a dictionary to store the balances for each public key
    balances = {}

    # Loop through each block in the blockchain and update the balances for each public key
    for block in blocks:
        for output in block['tx']['output']:
            pub_key = output['pub_key']
            value = output['value']
            if pub_key in balances:
                balances[pub_key] += value
            else:
                balances[pub_key] = value

    # Render the template with the balances
    return render_template("accounts.html", public_keys=balances)

if __name__ == '__main__':
    app.run(host="localhost", port=5001, debug=True)
