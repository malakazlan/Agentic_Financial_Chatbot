class MemoryBuffer:
    def __init__(self):
        self.chat_history = []

    def add(self, user, bot):
        self.chat_history.append({"user": user, "bot": bot})

    def get_context(self, last_n=5):
        history = self.chat_history[-last_n:]
        context = ""
        for turn in history:
            context += f"User: {turn['user']}\nBot: {turn['bot']}\n"
        return context.strip()
