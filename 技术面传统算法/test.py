from bigchaindb_driver.crypto import generate_keypair
from bigchaindb_driver import BigchainDB

kinds = 'stock'
predictions = [600001, 600002]
user_id = 'admin'
key=generate_keypair()
pub_key = Public_key(account_number=user_id,public_key=key.public_key)
pri_key=Private_key(account_number=user_id,private_key=key.private_key)


trans_asset = {
            'data':{
                'transaction':{
                    'kinds':kinds,
                    'predictions': predictions
                }
            }
        }

prepared_creation_tx = bdb.transactions.prepare(
    operation='CREATE',
    signers=admin.public_key,#gongyao
    asset=tran_asset,
    metadata={'msg':'开辟一条新的预测链','recorder':session.get('name')}
)
fulfilled_creation_tx = bdb.transactions.fulfill(
    prepared_creation_tx,
    private_keys=admin.private_key
)
sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)
#.....
transfer_asset = {
            'id': fulfilled_creation_tx['id'],
        }
output_index = 0
output = fulfilled_creation_tx['outputs'][output_index]

transfer_input = {
    'fulfillment': output['condition']['details'],
    'fulfills': {
        'output_index': output_index,
        'transaction_id': fulfilled_creation_tx['id']
    },
    'owners_before': output['public_keys']
}

tran_metadata = {'msg': '新一期的预测',
                 'recorder': session.get('name'),
                 'predictions': predictions,
                 'time': time.strftime('%Y-%m-%d', time.localtime(time.time()))}

prepared_transfer_tx = bdb.transactions.prepare(
    operation='TRANSFER',
    asset=transfer_asset,
    inputs=transfer_input,
    recipients=Public_key,
    metadata=tran_metadata
)

fulfilled_transfer_tx = bdb.transactions.fulfill(
    prepared_transfer_tx,
    private_keys=private_key,
)

sent_transfer_tx = bdb.transactions.send_commit(fulfilled_transfer_tx)
