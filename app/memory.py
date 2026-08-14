from collections import defaultdict

class ConversationMemory:

    def __init__(self, max_messages: int = 10):
        self.max_messages = max_messages
        self.sessions = defaultdict(list)

    def get_history(self, session_id: str) -> list[dict]:
        return self.sessions[session_id]

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ):

        self.sessions[session_id].append(
            {
                "role": role,
                "content": content,
            }
        )

        # Keep only the most recent messages
        self.sessions[session_id] = (
            self.sessions[session_id][-self.max_messages:]
        )

    def clear(self, session_id: str):

        self.sessions.pop(session_id, None)


conversation_memory = ConversationMemory()