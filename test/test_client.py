import pytest
import bitjws
from bravado_bitjws.client import BitJWSSwaggerClient

privkey = bitjws.PrivateKey()

my_pubkey = privkey.pubkey.serialize()
my_address = bitjws.pubkey_to_addr(my_pubkey)

host = "0.0.0.0"
url = "http://0.0.0.0:8002/"
specurl = "%sstatic/swagger.json" % url
username = str(my_address)[0:8]

client = BitJWSSwaggerClient.from_url(specurl, privkey=privkey)

luser = client.get_model('User')(username=username)
user = client.user.addUser(user=luser).result()


def test_register_user():
    # register a new user
    privkey2 = bitjws.PrivateKey()
    my_pubkey2 = privkey2.pubkey.serialize()
    my_address2 = bitjws.pubkey_to_addr(my_pubkey2)

    username2 = str(my_address2)[0:8]

    client2 = BitJWSSwaggerClient.from_url(specurl, privkey=privkey2)

    luser2 = client2.get_model('User')(username=username2)
    user2 = client2.user.addUser(user=luser2).result()
    assert hasattr(user2, 'id')


def test_create_coin():
    print "creating a new coin"
    lcoin = client.get_model('Coin')(metal='ub', mint='uranus')
    coin = client.coin.addCoin(coin=lcoin).result()
    assert hasattr(coin, 'id')
    assert coin.user.id == user.id

    print "attempt to get a list of coins"
    coins = client.coin.findCoin().result()
    found = False
    for c in coins:
        if c.id == coin.id:
            found = True
    assert found


def test_user_can_only_get_own_coins():
    """Tests that user cannot get other users' coins throught the server"""
    print "creating a new user"
    privkey2 = bitjws.PrivateKey()
    my_pubkey2 = privkey2.pubkey.serialize()
    my_address2 = bitjws.pubkey_to_addr(my_pubkey2)

    username2 = str(my_address2)[0:8]

    client2 = BitJWSSwaggerClient.from_url(specurl, privkey=privkey2)

    luser2 = client2.get_model('User')(username=username2)
    user2 = client2.user.addUser(user=luser2).result()
    assert user.id != user2.id

    print "creating coins for both users"
    lcoin = client.get_model('Coin')(metal='ub', mint='uranus')
    client.coin.addCoin(coin=lcoin)

    lcoin2 = client2.get_model('Coin')(metal='ub', mint='uranus')
    client2.coin.addCoin(coin=lcoin2)

    print "checking users cannot get each others's coins"
    coins = client.coin.findCoin().result()
    coins2 = client2.coin.findCoin().result()

    def get_others_coins(user, coins):
        for c in coins:
            if c.user.id != user.id:
                return True
            return False

    assert not get_others_coins(user, coins)
    assert not get_others_coins(user2, coins2)
