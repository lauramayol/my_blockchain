import hashlib
import json
import requests

from urllib.parse import urlparse


from blockchain_app.models import Block, Transaction, Node


class Blockchain(object):
    # def __init__(self):

    @property
    def chain(self):
        return list(Block.objects.all().values().order_by('id'))

    def current_transactions_obj(self):
        return Transaction.objects.filter(block__isnull=True)

    @property
    def current_transactions(self):
        return list(self.current_transactions_obj.values())

    @property
    def nodes(self):
        return list(Node.objects.values_list('address', flat=True))

    @property
    def last_block(self):
        return self.chain[-1]

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        # Create the block
        my_block = Block(proof=proof,
                         previous_hash=previous_hash or self.hash(self.last_block))
        my_block.save()

        # Update current_transactions with this new block.
        my_block_trans = self.current_transactions_obj

        for trans in Transaction.objects.filter(block__isnull=True):
            trans.block = my_block
            trans.save()

        block = {
            'index': my_block.id,
            'timestamp': my_block.timestamp,
            'transactions': list(Transaction.objects.filter(block=my_block).values()),
            'proof': my_block.proof,
            'previous_hash': my_block.previous_hash,
        }

        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """

        new_trans = Transaction(sender=sender,
                                recipient=recipient,
                                amount=amount)

        new_trans.save()

        return self.last_block['id'] + 1

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_block: <dict>
        :return: <int>
        """

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """

        Validates the Proof
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.

        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
        :return: None
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            new_address = parsed_url.netloc
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            new_address = parsed_url.path
        else:
            raise ValueError('Invalid URL')

        new_node = Node(address=new_address)
        new_node.save()

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.rewrite_chain(new_chain)
            return True

        return False

    def rewrite_chain(self, new_chain):
        # Deleting Block objects will also delete Transaction objects.
        Block.objects.all().delete()

        for block in new_chain:
            new_block = Block(proof=block['proof'],
                              previous_hash=block['previous_hash'],
                              timestamp=block['timestamp'])
            new_block.save()

            for trans in block['transactions']:
                new_trans = Transaction(block=new_block,
                                        sender=trans['sender'],
                                        recipient=trans['recipient'],
                                        amount=trans['amount'],
                                        timestamp=trans['timestamp'])

                new_trans.save()
