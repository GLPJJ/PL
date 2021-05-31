#eth模块

#设定pip下载镜像地址
#pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
#下面的命令执行可能会失败，需要多次执行。确保成功安装web3
#pip3 install web3

'''
一.下载安装geth作为本地服务器节点 https://geth.ethereum.org/downloads/
二.添加到环境变量
三.运行节点
    移除之前的区块链数据:
    geth --ropsten removedb
    启动:
    geth --ropsten --datadir F:\\eth --ethash.dagdir F:\\eth\\dagdir --bootnodes "enode://6332792c4a00e3e4ee0926ed89e0d27ef985424d97b6a45bf0f23e51f0dcb5e66b875777506458aea7af6f9e4ffb69f43f3778ee73c81ed9d34c51c4b16b0b0f@52.232.243.152:30303,enode://94c15d1b9e2fe7ce56e458b9a3b672ef11894ddedd0c6f247e0f1d3487f52b66208fb4aeb8179fce6e3a749ea93ed147c37976d67af557508d199d9594c35f09@192.81.208.223:30303"

    1.启动，
        注意其中的日志信息
            IPC endpoint opened                      url=\\.\pipe\geth.ipc
            HTTP server started                      endpoint=127.0.0.1:8545 prefix= cors= vhosts=localhost
        这里的url就是我们下面需要的attach endpoint节点或者用http
        geth --ropsten -http --datadir F:\\eth --ethash.dagdir F:\\eth\\dagdir --bootnodes "enode://6332792c4a00e3e4ee0926ed89e0d27ef985424d97b6a45bf0f23e51f0dcb5e66b875777506458aea7af6f9e4ffb69f43f3778ee73c81ed9d34c51c4b16b0b0f@52.232.243.152:30303,enode://94c15d1b9e2fe7ce56e458b9a3b672ef11894ddedd0c6f247e0f1d3487f52b66208fb4aeb8179fce6e3a749ea93ed147c37976d67af557508d199d9594c35f09@192.81.208.223:30303"

        geth --ropsten --datadir F:\\eth --ethash.dagdir F:\\eth\\dagdir --nodiscover
        geth --ropsten --http --port 9999 --datadir F:\\eth --nodiscover
        geth --ropsten --ipcpath glp.rpc --datadir F:\\eth --ethash.dagdir F:\\eth\\dagdir --nodiscover
    2.
    geth attach \\.\pipe\geth.ipc
        对应可以使用的模块不一样，ipc权限高一点。
        admin:1.0 debug:1.0 eth:1.0 ethash:1.0 miner:1.0 net:1.0 personal:1.0 rpc:1.0 txpool:1.0 web3:1.0
    geth attach F:\\eth/geth.ipc
    geth attach http://127.0.0.1:8545   
        eth:1.0 net:1.0 rpc:1.0 web3:1.0
'''
from web3 import Web3
from pathlib import (
    Path,
)

def testEth()->bool:
    print("test eth")

    #通过IPC连接eth节点
    #这个url[\\.\pipe\geth.ipc]只能是用geth attach,用在python不行.
    # 自己本地节点同步太难了，还是用公用的https://infura.io/dashboard方便一点
    # w3 = Web3(Web3.IPCProvider('\\.\pipe\geth.ipc'))#这种连接方式会连不上。
    # w3 = Web3(Web3.IPCProvider())#用默认的可以连上 尼玛。
    # print("w3=",w3)
    # print("w3.isConnected()",w3.isConnected())

    #通过http连接本地的节点
    #request_kwargs参数字典key由session.py的request的参数名字
    w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/4f41b9c0250244df9d7e3aae137bb160'))
    # w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/4f41b9c0250244df9d7e3aae137bb160'
        # ,{'auth': ('','ee8ec64a0ce14fc6a632e4a11e60e23c')}))
    # w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/4f41b9c0250244df9d7e3aae137bb160'))
    print("w3=",w3)
    print(w3.isConnected())
    if not w3.isConnected():
        return False

    # #通过websocket连接本地节点
    # w3Test3 = Web3(Web3.WebsocketProvider('ws://127.0.0.1:8546'))
    # print("w3Test3=",w3Test3)
    # print(w3Test3.isConnected())

    #获取最新的区块信息
    eth = w3.eth
    # block = eth.get_block('latest')
    # print(block)
    # print("区块高度",block.number)
    print("gas_price",eth.gas_price)
    print("当前地址列表",eth.accounts)
    print("chain id=",eth.chain_id)
    
    ethToAddress = "0x572E492ccA2508A12e97308d0F91a7371acbfDAD"
    ethFromAddress = '0xb6B146651b69C8bA7EE5e8dFA64a051fE06565a4'
    value = Web3.toWei(1, 'ether') #1个ETH
    print("获取接收地址的eth余额",eth.get_balance(ethToAddress))
    print("获取指定地址的eth余额",eth.get_balance(ethFromAddress))
    try:
        gas = 21000 #eth.estimate_gas({'to': ethToAddress, 'from':ethFromAddress, 'value': value})
        print("eth.gas_price=",eth.gas_price)
        # print("last gas=",block.gasUsed)
        print("estimate_gas",gas)

        signed_txn = eth.account.sign_transaction(dict(
            #注意：这个nonce必须是这个用法，否则交易会失败，取的是当前这个地址已经交易的数量
            nonce=eth.get_transaction_count(ethFromAddress) , 
            gasPrice=eth.gas_price, #1GWEI=e3MWEI=e6KWEI=e9WEI
            gas=gas, #使用估算的gas
            to=ethToAddress,
            value=value,
            data=b'',
          ),
          'e1e65f7c8b900b4f92a0ac58207c3e43b1c2c163eed003fa04b8404dd3aad234',
        )
        print("signed_txn.hash=",signed_txn.hash.hex())
        sendResult = eth.send_raw_transaction(signed_txn.rawTransaction)
        print("wait for transaction...")
        # waitResult = eth.wait_for_transaction_receipt(sendResult,timeout=60)
        # print(waitResult)
    except Exception as e:
        print("Exception:",e)
        return False
    return True


if __name__ == '__main__':
    testEth()
    # 4.999979 000000000000
    #       21 000 000000000
    # 100000 * 21000