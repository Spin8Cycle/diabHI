from websockets.sync.client import connect

with connect("ws://localhost:8000") as websocket:
    websocket.send("Eureka!")
    #assert websocket.recv() == "Eureka!"
    print(websocket.recv())

    websocket.send("I've found it!")
    #assert websocket.recv() == "I've found it!"
    print(websocket.recv())