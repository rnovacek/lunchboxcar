import os

try:
    import uasyncio as asyncio
    import uhashlib as hashlib
    import ubinascii as binascii
except ImportError:
    import asyncio
    import hashlib
    import binascii

import websock

from motor import motor_a, motor_b

try:
    import network
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('Azuryt', 'jdu1na2sever3jdu4na5jih')
    while not sta_if.isconnected():
        pass
    print('network config:', sta_if.ifconfig())
except ImportError:
    print('Network connect skipped')


def make_respkey(webkey):
    d = hashlib.sha1(webkey)
    d.update(b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11')
    respkey = d.digest()
    return binascii.b2a_base64(respkey)[:-1]


async def handle(ws, client_id):
    print('[%s] CONNECTED' % client_id)

    try:
        async for msg in ws:
            print('[%s] <<< %s' % (client_id, msg))
            if msg[0] == 'M':
                left, right = msg[1:].split(',')
                motor_a.set_speed(int(left))
                motor_b.set_speed(int(right))

            msg = 'OK'
            print('[%s] >>> %s' % (client_id, msg))
            await ws.send(msg)
    except Exception as e:
        print('[%s] ERROR: %s' % (client_id, e))
    finally:
        print('[%s] DISCONNECTED' % client_id)
        motor_a.set_speed(0)
        motor_b.set_speed(0)


last_client_id = 0
clients = {}


async def server(reader, writer):
    print('SERVER')
    # Consume GET line
    get_line = await reader.readline()

    if not get_line:
        writer.close()
        await writer.wait_closed()
        return

    print(get_line)

    websocket_key = None
    while True:
        line = await reader.readline()
        if line == b'\r\n':
            break
        elif line.startswith(b'Sec-WebSocket-Key:'):
            websocket_key = line[len(b'Sec-WebSocket-Key:'):]

    if get_line.startswith(b'GET / '):
        stat = os.stat('index.html')
        with open('index.html', 'rb') as f:
            writer.write(b'HTTP/1.0 200 OK\r\n')
            writer.write(b'Content-Type: text/html\r\n')
            writer.write(b'Content-Length: %d\r\n' % stat[6])
            writer.write(b'Connection: close\r\n')
            writer.write(b'\r\n')

            while True:
                buffer = f.read(256)
                writer.write(buffer)
                await writer.drain()
                if len(buffer) == 0:
                    break

    elif get_line.startswith(b'GET /ws '):
        assert websocket_key
        print('Key', websocket_key.strip())
        respkey = make_respkey(websocket_key.strip())

        writer.write(b'HTTP/1.1 101 Switching Protocols\r\n')
        writer.write(b'Upgrade: websocket\r\n')
        writer.write(b'Connection: Upgrade\r\n')
        writer.write(b'Sec-WebSocket-Accept: %s\r\n' % respkey)
        writer.write(b'\r\n')
        await writer.drain()

        ws = websock.Websocket(writer)

        global last_client_id
        client_id = last_client_id
        last_client_id += 1
        clients[id] = ws

        asyncio.create_task(handle(ws, client_id))
        return

    else:
        writer.write(b'HTTP/1.0 404 Not Found\r\n')
        writer.write(b'Content-Length: 0\r\n')
        writer.write(b'Connection: close\r\n')
        writer.write(b'\r\n')
        await writer.drain()
    writer.close()
    await writer.wait_closed()


loop = asyncio.get_event_loop()
loop.create_task(asyncio.start_server(server, "0.0.0.0", 8080, backlog=20))
loop.run_forever()
loop.close()
