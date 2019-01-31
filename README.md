# Create your Custom Blockchain in Django
*Release 1.0*

The goal of this project is to set up a simple blockchain stored in sqlitedb. Inspired by https://github.com/dvf/blockchain


## Features

#### This release
- [x] Mine transactions that haven't been assigned to a block yet and be rewarded with a coin. Simple Proof of Work Algorithm used:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
- [x] Create new transactions to be mined.
- [x] Query full chain and transaction list.
- [x] Register and resolve conflicts with other nodes in the network that hold a copy of same blockchain.

#### Next release
- [ ] Test Consensus algorithm by creating a conflicting blockchain on another node.

### Endpoints

| Method | Description | Endpoint | Query Sample |
| :-- | :-- | :-- | :-- |
| `GET` | Chain | `/chain`| `n/a` |
| `POST` | Mine | `/mine`| `n/a` |
| `POST` | Register transaction | `/transactions/new`| `?sender=1&recipient=some-other-address&amount=1` |
| `POST` | Register Node | `/nodes/register`| `?node=http://192.168.0.5:5000` |
| `PATCH` | Resolve Conflict between Nodes | `/nodes/resolve`| `n/a` |
| `POST` | Creates genesis block (new chain only) | `/blocks/genesis`| `n/a` |



### Running project locally

1. Clone repo to your development environment
```
git clone https://github.com/lauramayol/my_blockchain.git
```
2. Install [virtualenv](https://virtualenv.pypa.io/en/latest/)
```
pip install virtualenv
```
3. Change directory to project folder
```
cd blockchain_project
```
4. Start virtualenv
```
virtualenv --python=/usr/local/bin/python3 env
```
5. Run virtualenv
```
source env/bin/activate
```
6. Install dependencies using [pip](https://pip.pypa.io/en/latest/installing.html)
```
pip3 install -r requirements.txt
```
7. Run development server
```
python blockchain_project/manage.py runserver
```
8. Check <http://127.0.0.1:8000/chain> on your browser.



### Contribute

- Issue Tracker: https://github.com/lauramayol/my_blockchain/issues
- Source Code: https://github.com/lauramayol/my_blockchain


### Support


If you are having issues, please let me know by posting on Issue Tracker.
