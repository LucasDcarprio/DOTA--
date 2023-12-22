from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException
import json
import time
import random
def DOTA(key):
        # 连接到 Polkadot 节点，这里使用公共节点，您也可以使用自己的节点
    substrate = SubstrateInterface(
        url="wss://rpc.polkadot.io",
        ss58_format=0,
        type_registry_preset='polkadot'
    )
    # 创建密钥对，您需要替换成您自己的助记词或私钥
    keypair = Keypair.create_from_mnemonic(key,ss58_format=0)
    print(f"Address: {keypair.ss58_address}")
    exit
    # 替换为您要查询的账户地址
    account_address = keypair.ss58_address

    # 查询账户信息
    result = substrate.query(
        module='System',
        storage_function='Account',
        params=[account_address]
    )

    # 如果查询成功，打印账户余额
    if result:
        # 在Polkadot中，余额是以最小单位（plank）表示的
        balance = result.value['data']['free']
        # 转换为DOT（Polkadot的主要货币单位，1 DOT = 10^10 plank）
        balance_dot = balance / 10**10
        print(f"账户余额: {balance_dot} DOT")
    else:
        print("无法查询到账户余额。")


        # 构建transfer_keep_alive调用
    transfer_call = substrate.compose_call(
        call_module='Balances',
        call_function='transfer_keep_alive',
        call_params={
            'dest': account_address,
            'value': 0  # 注意：这里的值是0，通常应该是一个正数
        }
    )

    # 构建remark调用
    remark_call = substrate.compose_call(
        call_module='System',
        call_function='remark',
        call_params={
            'remark': bytes(json.dumps({"p":"dot-20","op":"mint","tick":"DOTA"}), encoding='utf-8')
        }
    )
    
    # 构建批处理调用
    batch_call = substrate.compose_call(
        call_module='Utility',
        call_function='batch_all',
        call_params={
            'calls': [transfer_call, remark_call]
        }
    )

    # 构建并签名交易
    extrinsic = substrate.create_signed_extrinsic(call=batch_call, keypair=keypair)

    # 发送交易
    try:
        receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        print(f"交易已发送，哈希值：{receipt.extrinsic_hash}")

        if receipt.is_success:
            print("交易成功")
        else:
            print("交易失败:", receipt.error_message)

    except SubstrateRequestException as e:
        print("交易失败:", str(e))

if __name__ == '__main__':
    key=input('请输入助记词')
    while True:
        try:
            DOTA(key)
            time.sleep(2)
        except Exception as e:
            print('================================AWAIT======================================')
            print(e)
            time.sleep(5)
  
       
