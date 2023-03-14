import hashlib
from random import Random
import sys, time, json, os
from ecdsa import VerifyingKey, SigningKey
from p2pnetwork.node import Node
from Crypto.Cipher import AES

DIFFICULTY = 0x000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF


#===============================================================================

#===============================================================================
def generate_tx(client, sk, vk, input_block: dict, ):
    utx = {} # Create UTX

    utx["type"] = client.TRANSACTION # Set type to TRANSACTION

    utx["input"] = {} # Create input
    utx["input"]["id"] = 0 # Set input id to blockId of input block
    utx["input"]["n"] = 0 

    # utx.sig = 

    utx["output"] = [] # Create output
    utx["output"].append({}) # Create output[0]
    utx["output"][0]["value"] = 50 # Set output[0].value to 50
    utx["output"][0]["pub_key"] = vk.to_string().hex() # Set output[0].pub_key to vk

    utx["output"].append({}) # Create output[1]
    utx["output"][1]["value"] = 50 # Set output[1].value to 50
    utx["output"][1]["pub_key"] = vk.to_string().hex() # Set output[1].pub_key to vk

def validate_block_id(block: dict):
    expected_id = hashlib.sha256(json.dumps(block['tx'], sort_keys=True).encode('utf8')).hexdigest()
    return expected_id == block['id']

def compute_block_id(tx: dict):
    return hashlib.sha256(json.dumps(tx, sort_keys=True).encode('utf8')).hexdigest()

def mine_transaction(utx):
   nonce = Random.new().read(AES.block_size).hex()
   while( int( hashlib.sha256(json.dumps(utx, sort_keys=True).encode('utf8') + nonce.encode('utf-8')).hexdigest(), 16) > DIFFICULTY):
        nonce = Random.new().read(AES.block_size).hex()
   pow = hashlib.sha256(json.dumps(utx, sort_keys=True).encode('utf8') + nonce.encode('utf-8')).hexdigest()
   
   return pow, nonce

def validate_pow(block: dict):
    return int( hashlib.sha256(json.dumps(block['tx'], sort_keys=True).encode('utf8') + block['nonce'].encode('utf-8')).hexdigest(), 16) < DIFFICULTY

def generate_signature(sk, utx):
    sig = sk.sign(json.dumps(utx['input'], sort_keys=True).encode('utf8')).hex()
    return sig

def validate_signature(tx, pub_key):
    vk = VerifyingKey.from_string(bytes.fromhex(pub_key))
    assert vk.verify(bytes.fromhex(tx['sig']), json.dumps(tx['input'], sort_keys=True).encode('utf8'))



#===============================================================================
# ZachCoin™ Client
#===============================================================================

SERVER_ADDR = "zachcoin.net"
SERVER_PORT = 9067

class ZachCoinClient (Node):
    
    #ZachCoin Constants
    BLOCK = 0
    TRANSACTION = 1
    BLOCKCHAIN = 2
    UTXPOOL = 3
    COINBASE = 50
    DIFFICULTY = 0x000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

    #Hardcoded gensis block
    blockchain = [
        {
            "type": BLOCK,
            "id": "124059f656eb6b016ce36583b5d6e9fdaf82420355454a4e436f4ee2ff17dba7",
            "nonce": "5052bfab11df236c43a4d877d93e42a3",
            "pow": "000000be01b9e4b6fdd73985083174007c30a98dc0801eaa830e27bbbea0d705",
            "prev": "124059f656eb6b016ce36583b5d6e9fdaf82420355454a4e436f4ee2ff17dba7",
            "tx": {
                "type": TRANSACTION,
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
        }
    ]
    utx = []
  
    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(ZachCoinClient, self).__init__(host, port, id, callback, max_connections)

    def outbound_node_connected(self, connected_node):
        print("outbound_node_connected: " + connected_node.id)
        
    def inbound_node_connected(self, connected_node):
        print("inbound_node_connected: " + connected_node.id)

    def inbound_node_disconnected(self, connected_node):
        print("inbound_node_disconnected: " + connected_node.id)

    def outbound_node_disconnected(self, connected_node):
        print("outbound_node_disconnected: " + connected_node.id)

    def node_message(self, connected_node, data):
        print("node_message from " + connected_node.id + ": " + json.dumps(data,indent=2))

        if data != None:
            if 'type' in data:
                if data['type'] == self.TRANSACTION:
                    self.utx.append(data)
                elif data['type'] == self.BLOCKCHAIN:
                    self.blockchain = data['blockchain']
                elif data['type'] == self.UTXPOOL:
                    self.utx = data['utxpool']
                #TODO: Validate blocks

    def node_disconnect_with_outbound_node(self, connected_node):
        print("node wants to disconnect with oher outbound node: " + connected_node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")

    # Validate a block based on the following rules:
    # 1. the block contains all required fields
    # 2. The type field is the value 0
    # 3. the block id has been computed correctly
    # 4. The prev field stored the block id of the preceding block on the blockchain
    # 5. the proof of work validates and is less than the difficulty value
    # 6. the transaction within the block is valid, including: 
    #    a. the trasaction contains all required fields
    #    b. the transaction type is the value 1
    #    c. The transaction input refers to a valid unspent transaction output
    #    d. The transaction input has not been spent
    #    e. the value of the input equals the sum of the outputs 
    #    f. the coinbase output is valid
    #    g. the signature of the transaction is valid
    def validate_block(self, block)->bool:
        # 1. the block contains all required fields
        if not "type" in block:
            return False
        if not "id" in block:
            return False
        if not "nonce" in block:
            return False
        if not "pow" in block:
            return False
        if not "prev" in block:
            return False
        if not "tx" in block:
            return False

        # 2. The type field is the value 0
        if block["type"] != 0:
            return False

        # 3. the block id has been computed correctly
        if block["id"] != validate_block_id(block):
            return False

        # 4. The prev field stored the block id of the preceding block on the blockchain
        if block["prev"] != self.blockchain[-1]["id"]:
            return False

        # 5. the proof of work validates and is less than the difficulty value
        if not validate_pow(block["pow"]):
            return False

        # 6. the transaction within the block is valid, including: 
        #    a. the trasaction contains all required fields
        if not "type" in block["tx"]:
            return False
        if not "input" in block["tx"]:
            return False
        if not "sig" in block["tx"]:
            return False
        if not "output" in block["tx"]:
            return False

        #    b. the transaction type is the value 1
        if block["tx"]["type"] != 1:
            return False

        #    c. The transaction input refers to a valid unspent transaction output
        if not "id" in block["tx"]["input"]:
            return False
        if not "n" in block["tx"]["input"]:
            return False

        #    d. The transaction input has not been spent
        for b in self.blockchain:
            if b["tx"]["input"]["id"] == block["tx"]["input"]["id"] and b["tx"]["input"]["n"] == block["tx"]["input"]["n"]:
                return False

        #    e. the value of the input equals the sum of the outputs (arbitrary amount of outputs)
        sum = 0
        for output in block["tx"]["output"]:
            sum += output["value"]
        if sum != block["tx"]["input"]["value"]:
            return False
        
        #    f. the coinbase output is valid
        if block["tx"]["output"][-1]["value"] != 50:
            return False
        
        #    g. the signature of the transaction is valid
        #find input block in blockchain list
        for b in self.blockchain:
            if b["id"] == block["tx"]["input"]["id"]:
                if not validate_signature(block["tx"], b["tx"]["output"][block["tx"]["input"]["n"]]["pub_key"]):
                    return False
        
        return True

def getBlocks(username, port):
    #Create a client object
    client = ZachCoinClient("127.0.0.1", port, username)
    client.debug = False

    time.sleep(1)

    client.start()

    time.sleep(1)

    #Connect to server 
    client.connect_with_node(SERVER_ADDR, SERVER_PORT)
    # print("Starting ZachCoin™ Client:", sys.argv[1])
    time.sleep(2)

    blocks = client.blockchain

    client.stop()

    print("Blocks:", blocks)

    return blocks

def startClient(username, port):
    print("Creating client", username, "on port", port, "...")
    #Create a client object
    client = ZachCoinClient("127.0.0.1", port, username)
    client.debug = False

    time.sleep(1)

    client.start()

    time.sleep(1)

    #Connect to server 
    client.connect_with_node(SERVER_ADDR, SERVER_PORT)
    print("Starting ZachCoin™ Client:", username)
    time.sleep(2)

    return client

def main():

    if len(sys.argv) < 3:
        print("Usage: python3", sys.argv[0], "CLIENTNAME PORT")
        quit()

    #Load keys, or create them if they do not yet exist
    keypath = './' + sys.argv[1] + '.key'
    if not os.path.exists(keypath):
        sk = SigningKey.generate()
        vk = sk.verifying_key
        with open(keypath, 'w') as f:
            f.write(sk.to_string().hex())
            f.close()
    else:
        with open(keypath) as f:
            try:
                sk = SigningKey.from_string(bytes.fromhex(f.read()))
                vk = sk.verifying_key
            except Exception as e:
                print("Couldn't read key file", e)

    #Create a client object
    client = ZachCoinClient("127.0.0.1", int(sys.argv[2]), sys.argv[1])
    client.debug = False

    time.sleep(1)

    client.start()

    time.sleep(1)

    #Connect to server 
    client.connect_with_node(SERVER_ADDR, SERVER_PORT)
    print("Starting ZachCoin™ Client:", sys.argv[1])
    time.sleep(2)

    while True:
        os.system('cls' if os.name=='nt' else 'clear')
        slogan = " You can't spell \"It's a Ponzi scheme!\" without \"ZachCoin\" "
        print("=" * (int(len(slogan)/2) - int(len(' ZachCoin™')/2)), 'ZachCoin™', "=" * (int(len(slogan)/2) - int(len('ZachCoin™ ')/2)))
        print(slogan)
        print("=" * len(slogan),'\n')
        x = input("\t0: Print keys\n\t1: Print blockchain\n\t2: Print UTX pool\n\t3: Create a tx\n\t4: Mine tx\n\nEnter your choice -> ")
        try:
            x = int(x)
        except:
            print("Error: Invalid menu option.")
            input()
            continue
        if x == 0:
            print("sk: ", sk.to_string().hex())
            print("vk: ", vk.to_string().hex())
        elif x == 1:
            print(json.dumps(client.blockchain, indent=1))
        elif x == 2:
            print(json.dumps(client.utx, indent=1))
        elif x == 3: 
            print("Creating a transaction...")

            print("Collecting blocks containing output to vk: \"{}\"".format(vk.to_string().hex()))
            blocks = []
            for block in client.blockchain:
                # print("Checking block {}...".format(block["id"]))
                tx = block["tx"]
                for output in tx["output"]:
                    if output["pub_key"] == vk.to_string().hex():
                        blocks.append(block)
            if len(blocks) == 0:
                print("Error: No blocks found containing output to vk")
                input()
                continue
            print("Found {} blocks containing output to vk".format(len(blocks)))
            print("Selecting block with highest value...")

            # utx = {} # Create UTX

            # utx["type"] = client.TRANSACTION # Set type to TRANSACTION

            # utx["input"] = {} # Create input
            # utx["input"]["id"] = 0 # Set input id to blockId of input block
            # utx["input"]["n"] = 0 

            # # utx.sig = 

            # utx["output"] = [] # Create output
            # utx["output"].append({}) # Create output[0]
            # utx["output"][0]["value"] = 50 # Set output[0].value to 50
            # utx["output"][0]["pub_key"] = vk.to_string().hex() # Set output[0].pub_key to vk

            # utx["output"].append({}) # Create output[1]
            # utx["output"][1]["value"] = 50 # Set output[1].value to 50
            # utx["output"][1]["pub_key"] = vk.to_string().hex() # Set output[1].pub_key to vk

            # print(utx)

            # # client.connect_with_node(SERVER_ADDR, SERVER_PORT) # Connect to server
            # # client.send_to_nodes(utx) # Send utx to nodes

        elif x == 4: 
            print("Mining a block...")
            
            # Display utx pool for user to select from
            print("Select a transaction to mine:")
            for i in range(len(client.utx)):
                if not "type" in client.utx[i]:
                    print("Error: Invalid block type.")
                    continue
                if not "input" in client.utx[i]:
                    print("Error: Invalid block type.")
                    continue
                if not "sig" in client.utx[i]:
                    print("Error: Invalid block type.")
                    continue
                if not "output" in client.utx[i]:
                    print("Error: Invalid block type.")
                    continue
                print("\t{}: {}".format(i, client.utx[i]["id"]))
            if (len(client.utx) == 0):
                print("Error: No transactions to mine.")
                input()
                continue
            x = input("Enter your choice -> ")
            try:
                x = int(x)
            except:
                print("Error: Invalid menu option.")
                input()
                continue
            if x < 0 or x >= len(client.utx):
                print("Error: Invalid menu option.")
                input()
                continue
            utx = client.utx[x]
            print("Mining transaction: {}".format(utx["id"]))

            # Create block
            block = {}

            block["type"] = client.BLOCK # Set type to BLOCK
            
            block["id"] = compute_block_id(utx) # Set id to hash of utx

            block["prev"] = client.blockchain[-1]["id"] # Set prev to hash of last block in blockchain

            block["tx"] = utx # Set tx to utx

            # add coinbase tx to block
            coinbase = {}
            coinbase["value"] = 50
            coinbase["pub_key"] = vk.to_string().hex()
            block["tx"]["output"].append(coinbase)

            # sign block
            block["sig"] = generate_signature(vk, block["tx"])

            # calculate block proof of work
            (block["pow"], block["nonce"]) = mine_transaction(block["tx"])

            print("Block generated: {}".format(block["id"]))
            print("block: ", block)

            # get user confirmation to send block to server
            x = input("Send block to server? (y/n) -> ")
            if x == "y":
                client.send_to_nodes(block)
            else:
                print("Block discarded.")
        else:
            print("Error: Invalid menu option.")


        input()
        
if __name__ == "__main__":
    main()