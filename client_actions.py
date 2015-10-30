import bitjws
from bravado_bitjws.client import BitJWSSwaggerClient

privkey = bitjws.PrivateKey()

my_pubkey = privkey.pubkey.serialize()
my_address = bitjws.pubkey_to_addr(my_pubkey)

print("My key address: {}".format(my_address))

host = "0.0.0.0"
url = "http://0.0.0.0:8002/"
specurl = "%sstatic/swagger.json" % url
username = str(my_address)[0:8]

client = BitJWSSwaggerClient.from_url(specurl, privkey=privkey)

# register a new user
print "registering a new user for this session"
user = client.get_model('user')(username=username)
print client.user.addUser(user=user).result()

# create two coins
print "creating two new coins"
coin = client.get_model('coin')(metal='ub', mint='uranus')
coin2 = client.get_model('coin')(metal='bn', mint='billworld')
print client.coin.addCoin(coin=coin).result()
print client.coin.addCoin(coin=coin2).result()

# server accepts this command but client throws error,
# because spec defines an array of coins response
print "attempt to get a list of coins"
print client.coin.findCoin().result()

