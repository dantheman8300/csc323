import os
from flask import Flask, render_template
from zc_client import getBlocks, startClient
app = Flask(__name__)

zcClient = None

# Example array of blockchain blocks
blocks = []

@app.route('/')
def index():
    return render_template('index.html', blocks=blocks)

@app.route('/blocks')
def view_blocks():
    # blocks = getBlocks("viewer", 42078)
    global zcClient
    while (zcClient == None):
        print("client is none")
        zcClient = startClient("viewer", 42078)
    blocks = zcClient.blockchain
    return render_template('blocks.html', blocks=blocks)

@app.route('/accounts')
def public_keys():
    # blocks = getBlocks("viewer", 42078)
    global zcClient
    while (zcClient == None):
        print("client is none")
        zcClient = startClient("viewer", 42078)
    blocks = zcClient.blockchain
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
