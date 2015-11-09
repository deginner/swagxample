##### Example of generating bitjws key to use for communicating with the server.
import bitjws
privkey = bitjws.PrivateKey()

my_pubkey = privkey.pubkey.serialize()
my_address = bitjws.pubkey_to_addr(my_pubkey)
print "Created bitjws (Bitcoin) address %s" % my_address

##### Example User registration using bravado-bitjws client
# https://github.com/deginner/bravado-bitjws
from bravado_bitjws.client import BitJWSSwaggerClient

host = "swagxample.deginner.com"
url = "http://swagxample.deginner.com/"
specurl = "%sstatic/swagger.json" % url
username = str(my_address)[0:8]

client = BitJWSSwaggerClient.from_url(specurl, privkey=privkey)

luser = client.get_model('User')(username=username)
user = client.user.addUser(user=luser).result()

print "registered as user\n%s" % user

##### Example of creating a coin with the more common requests package
import requests
import time

rawcoin = {'metal': 'I_approve_CTF1_game_for_1_BTC',
           'mint': '1AVV83Xa8E4yQGKrE4bZgi9rB2fDAEmySE'}
jwsdata = bitjws.sign_serialize(privkey, requrl="/coin",
                                iat=time.time(), data=rawcoin)
resp = requests.post("http://swagxample.deginner.com/coin", data=jwsdata,
                     headers={'content-type': 'application/jose'})
rawresp = resp.content.decode('utf8')
print "raw response\n%s" % rawresp
headers, payload = bitjws.validate_deserialize(rawresp, requrl="/response")
print "bitjws response body\n%s" % payload
print "bitjws response headers\n%s" % headers

