# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 13:01:23 2020

@author: Don
"""

#importing libraries

import datetime
import hashlib
import json
from flask import Flask, jsonify

#Defining the blockchain

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
    
    def create_block(self, proof, previous_hash):
        block = {'index' : len(self.chain)+1,
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash' : previous_hash
                 }
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self):
        previous_block = self.chain[0]
        block_index = 1
        while block_index < len(self.chain):
            block = self.chain[block_index]
            if (block['previous_hash'] != self.hash(previous_block)):
                return False
            previous_proof = previous_block['proof']
            new_proof = block['proof']
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    

#Mining the blockchain
        
#WebApplication
app = Flask(__name__)

#Creating the Blockchain
blockchainobj  = Blockchain()

#Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchainobj.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchainobj.proof_of_work(previous_proof)
    previous_hash = blockchainobj.hash(previous_block)
    block = blockchainobj.create_block(proof, previous_hash)
    response = {'message' : 'You have mined a block',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash']}
    return jsonify(response), 200 #httpstatuscode

#Getting the full Blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain' : blockchainobj.chain,
                'length' : len(blockchainobj.chain)}
    return jsonify(response), 200

#Checking if blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchainobj.is_chain_valid()
    if is_valid:
        response = {'message' : 'Blockchain is Valid'}
    else:
        response = {'message' : 'Blockchain is not valid'}
    return jsonify(response), 200

#Running the App
app.run(host='0.0.0.0', port='5000')