from websockets import connect
import asyncio
import json
import ssl
import datetime


async def get_event():
       # type your node ip or hostname
   async with connect("ws://parity_json_rpc_node:8546") as ws:
       # send subscribe request
    await ws.send(json.dumps({"id": 1, "method": "eth_subscribe", "jsonrpc":"2.0", "params": ["newHeads"]}))
    subscription_response = await ws.recv()
    while True:
        try:
            message = await asyncio.wait_for(ws.recv(), timeout=20)
            pass
        except asyncio.TimeoutError:
            # No data in 20 seconds, check the connection.
            try:
                pong_waiter = await ws.ping()
                await asyncio.wait_for(pong_waiter, timeout=10)
            except asyncio.TimeoutError:
                # No response to ping in 10 seconds, disconnect.
                print("socket timeout")
                break
        else:
            ouput_file = 'Totle_newHeads_data_%s.json' % datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            with open(ouput_file, "w") as text_file:
               text_file.write(message)
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    while True:
        loop.run_until_complete(get_event())
