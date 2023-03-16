import os
from flask import Flask, render_template
import hashlib
from random import Random
import sys, time, json, os
from ecdsa import VerifyingKey, SigningKey
from p2pnetwork.node import Node
from Crypto.Cipher import AES
from zc_client import startClient
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
    blocks = zcClient.blockchain[::-1]
    print(zcClient.blockchain[-1])
    return render_template('blocks.html', blocks=blocks, blockNumber=len(blocks))

# @app.route('/refresh-blocks')
# def refresh_blocks():
#     global zcClient
#     while (zcClient == None):
#         print("client is none")
#         zcClient = startClient("viewer", 42078)
#     blocks = zcClient.blockchain[::-1]
#     print("refreshed blocks")
#     return render_template('blocks.html', blocks=blocks, blockNumber=len(blocks))

@app.route('/accounts')
def public_keys():
    # blocks = getBlocks("viewer", 42078)
    global zcClient
    while (zcClient == None):
        print("client is none")
        zcClient = startClient("viewer", 42078)
    blocks = zcClient.blockchain[::-1]
    # Create a dictionary to store the balances for each public key
    balances = {}

    # Loop through each block in the blockchain and update the balances for each public key
    # Make sure to subtract from balances when the coins are used as input in a transaction
    for block in blocks:
        tx = block["tx"]
        for output in tx["output"]:
            if output["pub_key"] in balances:
                balances[output["pub_key"]] += output["value"]
            else:
                balances[output["pub_key"]] = output["value"]
        input = tx["input"]
        # get block with input["id"]
        for block in blocks:
            if block["id"] == input["id"]:
                tx = block["tx"]
                output = tx["output"][input["n"]]
                if output["pub_key"] in balances:
                    balances[output["pub_key"]] -= output["value"]

    # Render the template with the balances
    return render_template("accounts.html", public_keys=balances)

if __name__ == '__main__':
    app.run(host="localhost", port=5001, debug=True)
