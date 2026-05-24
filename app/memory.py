class ChatMemory:
    def __init__(self):
        self.history = []

    def add_message(self, user_query, bot_response):
        self.history.append({
            "user": user_query,
            "bot": bot_response
        })

    def get_history(self):
        """
        Convert history into LLM-readable format
        """
        formatted = ""

        for chat in self.history[-5:]:  # keep last 5 turns
            formatted += f"User: {chat['user']}\nBot: {chat['bot']}\n"

        return formatted