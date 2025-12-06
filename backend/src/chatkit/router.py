"""
ChatKit API router for the RAG chatbot backend
"""
from fastapi import APIRouter, Request
from fastapi.responses import Response, StreamingResponse

from .server import server

router = APIRouter()

@router.post("/chatkit")
async def chatkit_endpoint(request: Request):
    """ChatKit endpoint that handles requests from the ChatKit React frontend"""
    result = await server.process(await request.body(), {})
    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    return Response(content=result.json, media_type="application/json")

# Debug endpoint to inspect stored items
@router.get("/debug/threads")
async def debug_threads():
    """Debug endpoint to inspect stored conversation threads"""
    result = {}
    for thread_id, state in server.store._threads.items():
        items = []
        for item in state.items:
            item_data = {"id": item.id, "type": type(item).__name__}
            if hasattr(item, 'content') and item.content:
                content_parts = []
                for part in item.content:
                    if hasattr(part, 'text'):
                        content_parts.append(part.text)
                item_data["content"] = content_parts
            items.append(item_data)
        result[thread_id] = {"items": items, "count": len(items)}
    return result