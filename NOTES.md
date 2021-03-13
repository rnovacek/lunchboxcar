
## Installation from upip (not necessary at the moment)

```
import upip
upip.install('uasyncio.websocket.server')
```

## Precompiling (not necessary at the moment)

Clone micropython, build mpy-cross and use it on tineweb.py

```
git clone https://github.com/micropython/micropython
cd micropython/mpy-cross/
make
./mpy-cross <PATH>/tinyweb.py
```
