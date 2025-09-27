from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.core.websocket_manager import manager

router = APIRouter()

@router.websocket("/ws/comments")
async def websocket_endpoint(websocket: WebSocket):
    # Принимаем новое соединение
    await manager.connect(websocket)
    
    try:
        # Бесконечный цикл для поддержания соединения
        while True:
            # Ожидаем любое сообщение от клиента
            # (здесь можно добавить обработку входящих сообщений, если нужно)
            await websocket.receive_text()
            
    except WebSocketDisconnect:
        # При разрыве соединения удаляем его из списка активных
        manager.disconnect(websocket)
