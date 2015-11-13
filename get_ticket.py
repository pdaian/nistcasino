from Crypto.PublicKey import RSA 
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
import uuid, json

def sign(key, message):
    rsakey = RSA.importKey(key)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(message)
    sign = signer.sign(digest)
    return b64encode(sign)

new_key = RSA.generate(2048, e=65537) 
public_key = new_key.publickey().exportKey("PEM") 
private_key = new_key.exportKey("PEM") 
id = str(uuid.uuid4())
open("lotto_ticket_" + id, "w").write(private_key)
message = raw_input("Enter the number of tickets you want, in dollars: ")
print "[+] Lotto ticket written to file lotto_ticket_" + id + "  DO NOT LOSE THIS FILE, YOU NEED IT TO CLAIM YOUR WINNINGS"
print "\n\nCopy and paste the following into the ticket request box on the NIST lottery site to play:\n"
print json.dumps({'key': public_key, 'signature': sign(private_key, message), 'ticket': message})
