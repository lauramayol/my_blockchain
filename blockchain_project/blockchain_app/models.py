from django.db import models
from time import time


class Block(models.Model):
    '''
    Description:
        Each block is part of a chain (blockchain) and will have a list of transactions associated. This database will manage one chain.

    Attributes:
        proof (int): The proof given by the Proof of Work algorithm.
        previous_hash (char): Hash of previous Block.
        timestamp (datetime): When record was created in this database.
    '''

    proof = models.IntegerField()
    previous_hash = models.CharField(max_length=300)
    timestamp = models.FloatField(default=time())

    def __str__(self):
        return f"Block: {self.id} | proof: {self.proof}"


class Transaction(models.Model):
    '''
    Attributes:
        block (Block): Block object that holds the Transaction.
        sender (char): Address of the Sender.
        recipient (char): Address of the Recipient.
        amount (dec): Amount being transferred.
        timestamp (datetime): When record was created in this database.
    '''
    block = models.ForeignKey(Block, on_delete=models.CASCADE, null=True)
    sender = models.CharField(max_length=300)
    recipient = models.CharField(max_length=300)
    amount = models.DecimalField(max_digits=25, decimal_places=10)
    timestamp = models.FloatField(default=time())

    def __str__(self):
        return f"{self.block} | Sender: {self.sender} | Recipient: {self.recipient} | {self.amount}"


class Node(models.Model):
    '''
    Attributes:
        address (char): Address of another location for the same chain. In the format of 'http://{node}/chain'
        timestamp (datetime): When record was created in this database.
    '''
    address = models.CharField(primary_key=True, max_length=300)
    timestamp = models.FloatField(default=time())

    def __str__(self):
        return f"{self.block} | Sender: {self.sender} | Recipient: {self.recipient} | {self.amount}"
