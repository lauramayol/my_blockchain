from django.db import models
from django.utils import timezone


class Chain(models.Model):
    '''
    Description:
        Each Chain holds a group of Blocks with a list of transactions associated.

    Attributes:
        timestamp (datetime): When chain was created.
    '''

    timestamp = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"{self.id} | {self.timestamp}"


class Block(models.Model):
    '''
    Description:
        Each block is part of a Chain (blockchain) and will have a list of transactions associated.

    Attributes:
        chain (Chain): date of trend
        proof (int): The proof given by the Proof of Work algorithm.
        previous_hash (char): Hash of previous Block.
        timestamp (datetime): When record was created in this database.
    '''
    chain = models.ForeignKey(Chain, on_delete=models.CASCADE)
    proof = models.IntegerField()
    previous_hash = models.CharField(max_length=300)
    timestamp = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"Block: {self.id} | Chain: {self.chain.id}"


class Transaction(models.Model):
    '''
    Attributes:
        block (Block): date of trend
        sender (char): Address of the Sender.
        recipient (char): Address of the Recipient.
        amount (dec): Amount being transferred.
        timestamp (datetime): When record was created in this database.
    '''
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    sender = models.CharField(max_length=300)
    recipient = models.CharField(max_length=300)
    amount = models.DecimalField(max_digits=25, decimal_places=10)
    timestamp = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"{self.block} | Sender: {self.sender} | Recipient: {self.recipient} | {self.amount}"
