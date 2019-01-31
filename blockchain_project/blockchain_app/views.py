from uuid import uuid4
from django.http import JsonResponse
from blockchain_app.blockchain import Blockchain
from blockchain_app.models import Block, Transaction

bad_request_default = {"status_code": 400, "status": "Bad Request",
                       "message": "Please submit a valid request."}

blockchain = Blockchain()


def mine(request):
    """
        Mine transactions that haven't been assigned to a block yet and be rewarded with a coin.
    """

    if request.method == "POST":

        # We run the proof of work algorithm to get the next proof...
        last_block = blockchain.last_block
        proof = blockchain.proof_of_work(last_block)

        # Generate a globally unique address for this node
        node_identifier = str(uuid4()).replace('-', '')

        # We must receive a reward for finding the proof.
        # The sender is "0" to signify that this node has mined a new coin.
        blockchain.new_transaction(
            sender="0",
            recipient=node_identifier,
            amount=1,
        )

        # Forge the new Block by adding it to the chain
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        return JsonResponse(response)
    else:
        return JsonResponse(bad_request_default)


def new_transaction(request):
    """
        Creates a new transaction to go into the next mined Block

    """
    if request.method == "POST":
        values = request.GET

        # Check that the required fields are in the POST'ed data
        required = ['sender', 'recipient', 'amount']
        if not all(k in values for k in required):
            return 'Missing values', 400

        # Create a new Transaction
        index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

        response = {'message': f'Transaction will be added to Block {index}'}
        return JsonResponse(response)
    else:
        return JsonResponse(bad_request_default)


def full_chain(request):
    """
        Returns all Block and related Transaction objects.
    """
    if request.method == "GET":
        full_chain = []
        for b in blockchain.chain:
            b['transactions'] = list(Transaction.objects.filter(block__id=b['id']).values())
            full_chain.append(b)

        response = {
            'chain': full_chain,
            'length': len(blockchain.chain),
        }
        return JsonResponse(response)
    else:
        return JsonResponse(bad_request_default)


def register_nodes(request):
    """
        Add a new node to the list of nodes. Eg. 'http://192.168.0.5:5000'
    """
    if request.method == "POST":

        nodes = request.GET.get('node', None)
        if nodes is None:
            return JsonResponse(bad_request_default)

        blockchain.register_node(nodes)

        response = {
            'message': 'New node has been added',
            'total_nodes': list(blockchain.nodes),
        }
        return JsonResponse(response)
    else:
        return JsonResponse(bad_request_default)


def resolve_nodes(request):
    """
        Resolves conflicts by replacing our chain with the longest valid one in the network.
    """
    if request.method == "PATCH":
        replaced = blockchain.resolve_conflicts()

        if replaced:
            response = {
                'message': 'Our chain was replaced',
                'new_chain': blockchain.chain
            }
        else:
            response = {
                'message': 'Our chain is authoritative',
                'chain': blockchain.chain
            }

        return JsonResponse(response)
    else:
        return JsonResponse(bad_request_default)


def genesis_block(request):
    """
    Create the genesis block only if the chain is empty. This should only be done once for a brand new chain.
    """
    if request.method == "POST" and len(blockchain.chain) == 0:

        gen_block = blockchain.new_block(previous_hash=1, proof=100)

        response = {
            'message': "New Block Forged",
            'index': gen_block['index'],
            'transactions': gen_block['transactions'],
            'proof': gen_block['proof'],
            'previous_hash': gen_block['previous_hash'],
        }
        return JsonResponse(response)
    else:
        return JsonResponse(bad_request_default)
