"""
ChatKit server implementation for the RAG chatbot backend
Implements the OpenAI ChatKit server interface to work with the ChatKit React frontend
"""
import os
import uuid
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List
from dataclasses import dataclass, field

from dotenv import load_dotenv
from fastapi import Request
from fastapi.responses import Response, StreamingResponse

from chatkit.server import ChatKitServer, StreamingResult
from chatkit.store import Store  # SINGULAR, not 'stores'
from chatkit.types import ThreadMetadata, ThreadItem, Page
from chatkit.types import UserMessageItem, AssistantMessageItem, MessageContentPart
from chatkit.types import ThreadItemAddedEvent, ThreadItemDoneEvent, ThreadItemUpdatedEvent
from chatkit.agents import ThreadItemConverter, stream_agent_response, AgentContext

from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel

from ..api.chat import get_answer_with_citations  # Import our existing RAG functionality
from ..services.embedding_service import get_gemini_embedding_client

ROOT_DIR = Path(__file__).parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

@dataclass
class ThreadState:
    """Represents the state of a conversation thread"""
    id: str
    created_at: datetime
    metadata: Dict[str, Any]
    items: List[ThreadItem] = field(default_factory=list)

class MemoryStore(Store[Dict[str, Any]]):
    """In-memory store for ChatKit threads"""

    def __init__(self):
        self._threads: Dict[str, ThreadState] = {}

    def generate_thread_id(self, context: Dict[str, Any]) -> str:
        return str(uuid.uuid4())

    def generate_item_id(self, item_type: str, thread: ThreadMetadata, context: Dict[str, Any]) -> str:
        return str(uuid.uuid4())

    async def load_thread(self, thread_id: str, context: Dict[str, Any]) -> ThreadMetadata:
        if thread_id not in self._threads:
            # Create a new thread if it doesn't exist
            thread_state = ThreadState(
                id=thread_id,
                created_at=datetime.now(timezone.utc),
                metadata={"title": "New Chat", "created_at": datetime.now(timezone.utc).isoformat()}
            )
            self._threads[thread_id] = thread_state

        thread_state = self._threads[thread_id]
        return ThreadMetadata(
            id=thread_state.id,
            created_at=thread_state.created_at,
            metadata=thread_state.metadata
        )

    async def save_thread(self, thread: ThreadMetadata, context: Dict[str, Any]) -> None:
        if thread.id not in self._threads:
            self._threads[thread.id] = ThreadState(
                id=thread.id,
                created_at=thread.created_at,
                metadata=thread.metadata,
                items=[]
            )
        else:
            existing = self._threads[thread.id]
            existing.metadata = thread.metadata

    async def load_thread_items(self, thread_id: str, after: str | None, limit: int, order: str, context: Dict[str, Any]) -> Page[ThreadItem]:
        if thread_id not in self._threads:
            return Page(data=[], has_more=False, first_id=None, last_id=None)

        thread_state = self._threads[thread_id]
        items = thread_state.items

        # Apply after filter if provided
        if after:
            after_idx = next((i for i, item in enumerate(items) if item.id == after), -1)
            if after_idx != -1:
                items = items[after_idx + 1:]

        # Apply limit
        items = items[:limit]

        # Apply ordering
        if order == "desc":
            items = list(reversed(items))

        return Page(
            data=items,
            has_more=False,  # For simplicity, not implementing pagination
            first_id=items[0].id if items else None,
            last_id=items[-1].id if items else None
        )

    async def add_thread_item(self, thread_id: str, item: ThreadItem, context: Dict[str, Any]) -> None:
        if thread_id not in self._threads:
            thread_state = ThreadState(
                id=thread_id,
                created_at=datetime.now(timezone.utc),
                metadata={"title": "New Chat", "created_at": datetime.now(timezone.utc).isoformat()}
            )
            self._threads[thread_id] = thread_state

        self._threads[thread_id].items.append(item)

    async def save_item(self, thread_id: str, item: ThreadItem, context: Dict[str, Any]) -> None:
        # For in-memory store, we don't need to do anything special
        pass

    async def load_item(self, thread_id: str, item_id: str, context: Dict[str, Any]) -> ThreadItem:
        if thread_id not in self._threads:
            raise ValueError(f"Thread {thread_id} not found")

        thread_state = self._threads[thread_id]
        for item in thread_state.items:
            if item.id == item_id:
                return item

        raise ValueError(f"Item {item_id} not found in thread {thread_id}")

    async def delete_thread_item(self, thread_id: str, item_id: str, context: Dict[str, Any]) -> None:
        if thread_id not in self._threads:
            raise ValueError(f"Thread {thread_id} not found")

        thread_state = self._threads[thread_id]
        thread_state.items = [item for item in thread_state.items if item.id != item_id]

    async def load_threads(self, limit: int, after: str | None, order: str, context: Dict[str, Any]) -> Page[ThreadMetadata]:
        thread_metadatas = []
        for thread_state in self._threads.values():
            thread_metadatas.append(ThreadMetadata(
                id=thread_state.id,
                created_at=thread_state.created_at,
                metadata=thread_state.metadata
            ))

        # Apply limit
        thread_metadatas = thread_metadatas[:limit]

        # Apply ordering
        if order == "desc":
            thread_metadatas = list(reversed(thread_metadatas))

        return Page(
            data=thread_metadatas,
            has_more=False,
            first_id=thread_metadatas[0].id if thread_metadatas else None,
            last_id=thread_metadatas[-1].id if thread_metadatas else None
        )

    async def delete_thread(self, thread_id: str, context: Dict[str, Any]) -> None:
        if thread_id in self._threads:
            del self._threads[thread_id]

    async def save_attachment(self, attachment: Any, context: Dict[str, Any]) -> None:
        # For simplicity, not implementing attachments
        pass

    async def load_attachment(self, attachment_id: str, context: Dict[str, Any]) -> Any:
        # For simplicity, not implementing attachments
        return None

    async def delete_attachment(self, attachment_id: str, context: Dict[str, Any]) -> None:
        # For simplicity, not implementing attachments
        pass

class ChatKitServerImpl(ChatKitServer[Dict[str, Any]]):
    """ChatKit server implementation with RAG functionality using OpenAI Agents SDK and LiteLLM for Gemini"""

    def __init__(self, store: MemoryStore):
        super().__init__(store)
        self.converter = ThreadItemConverter()

    async def respond(self, thread, input, context):
        """Respond to a user input with RAG-augmented response using OpenAI Agents SDK"""
        try:
            # Load all items from the thread to build conversation history
            page = await self.store.load_thread_items(thread.id, None, 100, "asc", context)
            all_items = list(page.data)
            if input:
                all_items.append(input)

            # Extract the user's query from the latest message
            user_query = ""
            selected_text = ""

            # Find the latest user message
            for item in reversed(all_items):
                if isinstance(item, UserMessageItem) and item.content:
                    # Extract text from content parts
                    for part in item.content:
                        if hasattr(part, 'text'):
                            user_query = part.text
                            break
                    break

            # Check if the query is a greeting or related to the book content first
            query_lower = user_query.lower().strip()
            greeting_keywords = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'how are you', 'what\'s up', 'sup', 'morning', 'afternoon', 'evening']

            is_greeting = any(greeting in query_lower for greeting in greeting_keywords)

            if is_greeting:
                # Return a friendly greeting message
                full_response = "Hello! I'm your Physical AI & Humanoid Robotics book assistant. I'm here to help you with questions about the book content. How can I assist you today?"
            else:
                # Check if the query is related to the book topic
                book_related_keywords = ['physical ai', 'humanoid robotics', 'robot', 'ai', 'artificial intelligence', 'machine learning', 'ros2', 'digital twin', 'ai robot', 'vla', 'vision language action', 'hardware', 'software', 'capstone', 'module', 'chapter', 'textbook', 'book', 'learning', 'education', 'course', 'topic']

                is_book_related = any(keyword in query_lower for keyword in book_related_keywords)

                if not is_book_related:
                    full_response = "I apologize, but I can only respond to greetings and queries related to Physical AI & Humanoid Robotics content. Please ask a question related to the book's content."
                else:
                    # Use our existing RAG functionality to get the answer with citations
                    answer, citations = get_answer_with_citations(
                        query=user_query,
                        selected_text=selected_text
                    )

                    # Add citations to the response
                    citation_text = ""
                    if citations:
                        citation_text = "\n\nSources: " + ", ".join([f"[{i+1}]({citation.get('url', '#')})" for i, citation in enumerate(citations)])

                    full_response = answer + citation_text

            # Create the assistant message item
            assistant_item = AssistantMessageItem(
                id=self.store.generate_item_id("message", thread, context),
                created_at=datetime.now(timezone.utc),
                content=[MessageContentPart(type="text", text=full_response)]
            )

            # Yield the response as a streaming result
            yield ThreadItemAddedEvent(item=assistant_item)

        except Exception as e:
            # Handle errors gracefully
            error_item = AssistantMessageItem(
                id=self.store.generate_item_id("message", thread, context),
                created_at=datetime.now(timezone.utc),
                content=[MessageContentPart(type="text", text=f"Sorry, I encountered an error processing your request: {str(e)}")]
            )
            yield ThreadItemAddedEvent(item=error_item)

# Create the store and server instances
store = MemoryStore()
server = ChatKitServerImpl(store)