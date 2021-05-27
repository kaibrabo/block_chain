import blockchain

print("main file")
blockchain = blockchain.Blockchain()

print("***Mining 'Gold Dragons' about to start***")
print(blockchain.chain)

last_block = blockchain.latest_block
last_proof_no = last_block.proof_no
proof_no = blockchain.proof_of_work(last_proof_no)

blockchain.new_data(
    sender="0",  #it implies that this node has created a new block
    recipient="Kai Brabo",  #let's send Kai some coins!
    quantity=
    1,  #creating a new block (or identifying the proof number) is awarded with 1
)

last_hash = last_block.calculate_hash
block = blockchain.construct_block(proof_no, last_hash)

print("***Mining 'Gold Dragons' has been successful***")
print(blockchain.chain)