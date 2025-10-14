from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import Dict, List, Set
import json
from datetime import datetime
import uuid

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.room_connections: Dict[str, Set[WebSocket]] = {}
        self.message_history: Dict[str, List[dict]] = {}
        self.room_users: Dict[str, Set[str]] = {}
    
    async def connect(self, room_id: str, user_id: str, websocket: WebSocket):
        await websocket.accept()
        
        if room_id not in self.room_connections:
            self.room_connections[room_id] = set()
            self.message_history[room_id] = []
            self.room_users[room_id] = set()
        
        self.room_connections[room_id].add(websocket)
        self.room_users[room_id].add(user_id)
        
        join_message = {
            "type": "user_join",
            "user_id": user_id,
            "room_id": room_id,
            "timestamp": datetime.now().isoformat(),
            "message": f"User {user_id} joined the room",
            "online_count": len(self.room_users[room_id])
        }
        
        await self.broadcast(room_id, json.dumps(join_message), websocket)
        
        for message in self.message_history[room_id][-50:]:
            await websocket.send_text(json.dumps(message))
    
    async def disconnect(self, room_id: str, user_id: str, websocket: WebSocket):
        """Отключение пользователя"""
        if room_id in self.room_connections:
            self.room_connections[room_id].discard(websocket)
            self.room_users[room_id].discard(user_id)
            
            if not self.room_connections[room_id]:
                if room_id in self.room_connections:
                    del self.room_connections[room_id]
                if room_id in self.message_history:
                    del self.message_history[room_id]
                if room_id in self.room_users:
                    del self.room_users[room_id]
    
    async def broadcast(self, room_id: str, message: str, exclude_websocket: WebSocket = None):
        """Отправка сообщения всем в комнате"""
        if room_id in self.room_connections:
            disconnected = []
            for websocket in self.room_connections[room_id]:
                if websocket != exclude_websocket:
                    try:
                        await websocket.send_text(message)
                    except:
                        disconnected.append(websocket)
            
            for ws in disconnected:
                self.room_connections[room_id].discard(ws)
    
    async def save_message(self, room_id: str, message: dict):
        """Сохранение сообщения в историю"""
        if room_id not in self.message_history:
            self.message_history[room_id] = []
        
        self.message_history[room_id].append(message)
        if len(self.message_history[room_id]) > 100:
            self.message_history[room_id] = self.message_history[room_id][-100:]
    
    def get_room_users(self, room_id: str) -> List[str]:
        if room_id in self.room_users:
            return list(self.room_users[room_id])
        return []
    
    def get_rooms(self) -> List[str]:
        return list(self.room_connections.keys())

# Глобальный менеджер соединений
manager = ConnectionManager()

@app.websocket("/ws/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id: str):
    """WebSocket endpoint для чата"""
    await manager.connect(room_id, user_id, websocket)
    
    try:
        while True:
            # Получаем сообщение от клиента
            data = await websocket.receive_text()
            
            # Создаем структурированное сообщение
            message_data = {
                "type": "message",
                "user_id": user_id,
                "room_id": room_id,
                "message": data,
                "timestamp": datetime.now().isoformat(),
                "message_id": str(uuid.uuid4())
            }
            
            # Сохраняем в историю
            await manager.save_message(room_id, message_data)
            
            # Отправляем всем в комнате
            await manager.broadcast(room_id, json.dumps(message_data), websocket)
            
    except WebSocketDisconnect:
        # Уведомляем о выходе пользователя
        leave_message = {
            "type": "user_leave",
            "user_id": user_id,
            "room_id": room_id,
            "timestamp": datetime.now().isoformat(),
            "message": f"User {user_id} left the room",
            "online_count": len(manager.room_users.get(room_id, set())) - 1
        }
        
        await manager.broadcast(room_id, json.dumps(leave_message))
        await manager.disconnect(room_id, user_id, websocket)

# REST API endpoints
@app.get("/rooms")
async def get_rooms():
    """Получить список всех активных комнат"""
    return {"rooms": manager.get_rooms()}

@app.get("/room/{room_id}/users")
async def get_room_users(room_id: str):
    """Получить пользователей комнаты"""
    return {"room_id": room_id, "users": manager.get_room_users(room_id)}

@app.get("/room/{room_id}/history")
async def get_room_history(room_id: str, limit: int = 50):
    """Получить историю сообщений комнаты"""
    if room_id in manager.message_history:
        history = manager.message_history[room_id][-limit:]
        return {"room_id": room_id, "history": history}
    return {"room_id": room_id, "history": []}

# HTML интерфейс для тестирования
@app.get("/")
async def get():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WebSocket Chat без Redis</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .chat-container { border: 1px solid #ccc; border-radius: 8px; padding: 20px; }
            .messages { height: 400px; overflow-y: auto; border: 1px solid #eee; padding: 10px; margin-bottom: 10px; }
            .message { margin-bottom: 10px; padding: 8px; border-radius: 4px; }
            .message.user { background-color: #e3f2fd; }
            .message.system { background-color: #f3e5f5; font-style: italic; }
            .online-users { background-color: #f5f5f5; padding: 10px; border-radius: 4px; margin-bottom: 10px; }
            .input-group { display: flex; gap: 10px; margin-bottom: 10px; }
            input, button { padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
            button { background-color: #007bff; color: white; cursor: pointer; }
            button:disabled { background-color: #ccc; }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <h1>WebSocket Chat</h1>
            
            <div class="input-group">
                <input type="text" id="roomInput" placeholder="Room ID" value="general">
                <input type="text" id="userInput" placeholder="Your Name" value="User1">
                <button onclick="connect()">Connect</button>
                <button onclick="disconnect()">Disconnect</button>
            </div>

            <div class="online-users">
                <h3>Online: <span id="onlineCount">0</span></h3>
                <div id="usersList"></div>
            </div>

            <div class="messages" id="messages"></div>

            <div class="input-group">
                <input type="text" id="messageInput" placeholder="Type your message..." disabled>
                <button onclick="sendMessage()" disabled id="sendBtn">Send</button>
            </div>
        </div>

        <script>
            let ws = null;
            let currentRoom = '';
            let currentUser = '';

            function connect() {
                currentRoom = document.getElementById('roomInput').value;
                currentUser = document.getElementById('userInput').value;
                
                if (ws) {
                    ws.close();
                }
                
                ws = new WebSocket(`ws://${window.location.host}/ws/${currentRoom}/${currentUser}`);
                
                ws.onopen = function() {
                    console.log('Connected to room:', currentRoom);
                    document.getElementById('messageInput').disabled = false;
                    document.getElementById('sendBtn').disabled = false;
                };
                
                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    displayMessage(data);
                    
                    // Обновляем онлайн список
                    if (data.type === 'user_join' || data.type === 'user_leave') {
                        updateOnlineUsers(data);
                    }
                };
                
                ws.onclose = function() {
                    console.log('Disconnected');
                    document.getElementById('messageInput').disabled = true;
                    document.getElementById('sendBtn').disabled = true;
                };
                
                ws.onerror = function(error) {
                    console.error('WebSocket error:', error);
                };
            }
            
            function disconnect() {
                if (ws) {
                    ws.close();
                    ws = null;
                }
            }
            
            function sendMessage() {
                const input = document.getElementById('messageInput');
                if (ws && ws.readyState === WebSocket.OPEN && input.value.trim()) {
                    ws.send(input.value.trim());
                    input.value = '';
                }
            }
            
            function displayMessage(data) {
                const messagesDiv = document.getElementById('messages');
                const messageDiv = document.createElement('div');
                
                if (data.type === 'user_join' || data.type === 'user_leave') {
                    messageDiv.className = 'message system';
                    messageDiv.innerHTML = '<strong>' + data.message + '</strong>';
                } else {
                    messageDiv.className = 'message user';
                    messageDiv.innerHTML = `
                        <strong>${data.user_id}:</strong> ${data.message}
                        <small style="color: #666; margin-left: 10px;">${new Date(data.timestamp).toLocaleTimeString()}</small>
                    `;
                }
                
                messagesDiv.appendChild(messageDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
            
            function updateOnlineUsers(data) {
                document.getElementById('onlineCount').textContent = data.online_count || 0;
                
                // Запрос к API для получения списка пользователей
                fetch(`/room/${currentRoom}/users`)
                    .then(response => response.json())
                    .then(data => {
                        const usersList = document.getElementById('usersList');
                        usersList.innerHTML = data.users.map(user => 
                            '<span style="margin-right: 10px;">' + user + '</span>'
                        ).join('');
                    })
                    .catch(error => {
                        console.error('Error fetching users:', error);
                    });
            }
            
            // Enter для отправки
            document.getElementById('messageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)