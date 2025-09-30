from typing import List, Dict, Any
from fastapi import WebSocket
import json

class ConnectionManager:
    def __init__(self):
        # Список активных соединений
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        # Принимаем новое соединение
        await websocket.accept()
        # Добавляем соединение в список активных
        self.active_connections.append(websocket)
        print(f"Новое подключение. Всего подключений: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        # Удаляем соединение из списка при отключении
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print(f"Подключение закрыто. Осталось подключений: {len(self.active_connections)}")

    async def broadcast_comment(self, comment: Dict[str, Any]):
        """Отправляет новый комментарий всем подключенным клиентам"""
        # Преобразуем комментарий в JSON
        message = json.dumps({
            "type": "new_comment",
            "data": comment
        })
        
        # Отправляем сообщение всем подключенным клиентам
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")
                self.disconnect(connection)

# Создаем глобальный экземпляр менеджера соединений
manager = ConnectionManager()
