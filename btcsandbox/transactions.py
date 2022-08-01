import requests

from settings import BTC_ADDR, USDT_ADDR, ETH_ADDR, ETH_API_KEY


offset_amount                   = lambda amount: amount * (1 - 0.003)

# BITCOIN
# Confirm a bitcoin transaction
def confirm_btc(_hash):
    url = f"https://blockchain.info/rawaddr/{BTC_ADDR}"
    data = requests.get(url).json()
    hashes = [i['hash'] for i in data['txs']]
    
    return True if _hash in hashes else False


# Get Amount of Bitcoin Transaction
def gaot_btc(_hash):
    url = f"https://blockchain.info/rawtx/{_hash}"
    data = requests.get(url).json()

    inputValue = 0
    for i in data['inputs']:
        inputValue += i['prev_out']['value']

    amount_in_btc = (inputValue - data['fee'])*0.00000001
    
    def convert_btc_to_usd(amount_in_btc):
        url = "https://api.alternative.me/v2/ticker/?convert=USD"
        data = requests.get(url).json()
        
        return amount_in_btc * data['data']["1"]['quotes']['USD']['price']
    
    usd = offset_amount(convert_btc_to_usd(amount_in_btc))
    btc = amount_in_btc
    
    return dict(usd=usd, btc=btc)


# ETHEREUM
# Confirm an ethereum transaction
def confirm_eth(_hash):
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={ETH_ADDR}&startblock=0&endblock=99999999&sort=desc&apikey={ETH_API_KEY}"
    data = requests.get(url).json()
    hashes = [i['hash'] for i in data['result']]
    
    for i in hashes:
        print(i)
        
    print(len(hashes))
    
    return True if _hash in hashes else False


# Get Amount of Ethereum Transaction
def gaot_eth(_hash):
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={ETH_ADDR}&startblock=0&endblock=99999999&sort=desc&apikey={ETH_API_KEY}"
    data = requests.get(url).json()
    hashes = [i['hash'] for i in data['result']]

    if _hash in hashes:
        for i in data['result']:
            if i['hash'] == _hash:
                amount = int(i['value']) * pow(10, -18)
                def convert_ethereum_to_usd(amount):
                    url = "https://api.alternative.me/v2/ticker/?convert=USD"
                    data = requests.get(url).json()
                    
                    return amount * data['data']["1027"]['quotes']['USD']['price']

                usd = convert_ethereum_to_usd(amount)
                eth = amount
                
                return dict(usd=usd, eth=eth)
            
    else:
        return "Transaction hash is invalid."



#############################################################################################
# USD TETHER
# Confirm a usd tether transaction
def confirm_usdt(_hash):
    url = f"https://apilist.tronscanapi.com/api/transaction?limit=50&count=true&address={USDT_ADDR}"
    data = requests.get(url).json()
    hashes = [i['hash'] for i in data['data']]
    
    return True if _hash in hashes else False


# Get Amount of USDT Transaction
def gaot_usdt(trnasaction_hash):
    url = f"https://apilist.tronscanapi.com/api/transaction?address={USDT_ADDR}"
    data = requests.get(url).json()
    hashes = [i['hash'] for i in data['data']]

    if trnasaction_hash in hashes:
        for i in data['data']:
            if i['hash'] == trnasaction_hash:
                amount = int(i['amount'])
                def convert_usdt_to_usd(amount):
                    url = "https://api.alternative.me/v2/ticker/?convert=USD"
                    data = requests.get(url).json()
                    
                    return amount * data['data']["825"]['quotes']['USD']['price']

                usd = convert_usdt_to_usd(amount)
                usdt = amount

                return dict(usd=usd, usdt=usdt)
            
    else:
        return "Transaction hash is invalid."