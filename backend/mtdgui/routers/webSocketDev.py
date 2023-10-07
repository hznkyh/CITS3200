# from threading import Thread
# from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
# from fastapi.responses import HTMLResponse

# from dev.Sim import MySimulator

# router = APIRouter(
#     prefix="/devWebSocket",
#     tags=["devWebSocket"],
#     responses={404: {"description": "Not found"}}
# )


# html = """
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Chat</title>
#     </head>
#     <body>
#         <h1>WebSocket Chat</h1>
#         <h2>Your ID: <span id="ws-id"></span></h2>
#         <form action="" onsubmit="sendMessage(event)">
#             <input type="text" id="messageText" autocomplete="off"/>
#             <button>Send</button>
#         </form>
#         <ul id='messages'>
#         </ul>
#         <script>
#             var client_id = Date.now()
#             document.querySelector("#ws-id").textContent = client_id;
#             var ws = new WebSocket(`ws://localhost:8000/devWebSocket/ws/${client_id}`);
#             ws.onmessage = function(event) {
#                 var messages = document.getElementById('messages')
#                 var message = document.createElement('li')
#                 var content = document.createTextNode(event.data)
#                 message.appendChild(content)
#                 messages.appendChild(message)
#             };
#             function sendMessage(event) {
#                 var input = document.getElementById("messageText")
#                 ws.send(input.value)
#                 input.value = ''
#                 event.preventDefault()
#             }
#         </script>
#     </body>
# </html>
# """

# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: list[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#     async def send_personal_message(self, message: str, websocket: WebSocket):
#         await websocket.send_text(message)

#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)


# manager = ConnectionManager()


# @router.get("/")
# async def get():
#     return HTMLResponse(html)


# # @router.websocket("/ws/{client_id}")
# # async def websocket_endpoint(websocket: WebSocket, client_id: int):
# #     await manager.connect(websocket)
# #     # Start the simulator when a client connects
# #     sim = MySimulator()
# #     sim_thread:Thread = Thread(target=sim.run, args=(50,)).start()  # Run for a simulated time of 50 units
# #     try:
# #         print("try  Waiting for message")
# #         prev_message = None
# #         while True:
# #             print("Waiting for message")
# #             print(sim.message)
# #             if sim.message != prev_message:
# #                 await manager.send_personal_message(sim.message, websocket)
# #                 prev_message = sim.message
# #     except WebSocketDisconnect:
# #         manager.disconnect(websocket)
# #         sim_thread.join()
# #         await manager.broadcast(f"Client #{client_id} left the chat")




# @router.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: int):
#     await manager.connect(websocket)
    
#     async def websocket_callback(msg):
#         # This is a simple callback function that sends the message through the websocket
#         await manager.send_personal_message(msg, websocket)

#     # Pass the callback function when initializing the simulator
#     sim = MySimulator(callback=websocket_callback)
#     sim_thread: Thread = Thread(target=sim.run, args=(50,), daemon=True)
#     sim_thread.start()

#     try:
#         prev_message = None
#         while True:
#             if sim.message != prev_message:
#                 await manager.send_personal_message(sim.message, websocket)
#                 prev_message = sim.message
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         sim_thread.join()
#         await manager.broadcast(f"Client #{client_id} left the chat")