import hashlib
import time


class Block:
    def __init__(self, index: int, proof_no, prev_hash, data, timestamp=None) -> None:
        """
        :param index: keeps track of the position of the block within the blockchain
        :param proof_no: number produced during the creation of a new block
        :param prev_hash: hash of the previous block within the chain
        :param data: gives a record of all transactions completed
        :param timestamp: timestamp for the transactions
        """
        self.index = index
        self.proof_no = proof_no
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp or time.time()

    @property
    def calculate_hash(self) -> str:
        # calculates the cryptographic hash of every block
        block_of_string = "{}{}{}{}{}".format(self.index, self.proof_no, self.prev_hash, self.data, self.timestamp)
        return hashlib.sha256(block_of_string.encode()).hexdigest()

    def __repr__(self) -> str:
        return "{}-{}-{}-{}-{}".format(self.index, self.proof_no, self.prev_hash, self.data, self.timestamp)


class Blockchain:
    def __init__(self) -> None:
        self.chain = []  # keeps all blocks
        self.current_data = []  # keeps all the completed transactions in the block
        self.nodes = set()
        self.construct_genesis()  # will take care of constructing the initial block

    def construct_genesis(self) -> None:
        # construct initial block
        self.construct_block(proof_no=0, prev_hash=0)

    def construct_block(self, proof_no, prev_hash) -> Block:
        # constructs a new block and adds it to the chain
        block = Block(len(self.chain), proof_no, prev_hash, self.current_data)
        self.current_data = []
        self.chain.append(block)
        return block

    @staticmethod
    def check_validity(block: Block, prev_block: Block) -> bool:
        # checks whether the blockchain is valid
        if prev_block.index + 1 != block.index:
            # check index
            return False
        elif prev_block.timestamp >= block.timestamp:
            # check timestamp
            return False
        elif prev_block.calculate_hash != block.prev_hash:
            # check hash
            return False
        elif not Blockchain.verify_proof(block.proof_no, prev_block.proof_no):
            # check verify_proof() -> bool
            return False

        return True

    def new_data(self, sender, recipient, quantity) -> bool:
        # adds a new transaction to the data of the transactions
        self.current_data.append({
            'sender': sender,
            'recipient': recipient,
            'quantity': quantity
        })
        return True

    @staticmethod
    def proof_of_work(prev_proof) -> int:
        """
        this simple algorithm identifies a number f' such that hash(ff') contain 4 leading zeroes
        f is the previous f'
        f' is the new proof
        """
        # protects the blockchain from attack
        proof_no = 0
        while Blockchain.verifying_proof(proof_no, prev_proof) is False:
            proof_no += 1

        return proof_no

    @staticmethod
    def verifying_proof(last_proof, proof) -> bool:
        # verifying the proof: does hash(last_proof, proof) contain 4 leading zeroes?
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @property
    def latest_block(self):
        # returns last block in the chain
        return self.chain[-1]

    def block_mining(self, details_miner):
        self.new_data(
            sender="0",
            receiver=details_miner,
            quanntity=1,
        )

        last_block = self.latest_block

        last_proof_no = last_block.proof_no
        proof_no = self.proof_of_work(last_proof_no)

        last_hash = last_block.calculate_hash
        block = self.construct_block(proof_no, last_hash)

        return vars(block)

    def create_node(self, address):
        self.nodes.add(address)
        return True

    @staticmethod
    def obtain_block_object(block_data):

        return Block(
            block_data['index'],
            block_data['proof_no'],
            block_data['prev_hash'],
            block_data['data'],
            timestamp=block_data['timestamp']
        )