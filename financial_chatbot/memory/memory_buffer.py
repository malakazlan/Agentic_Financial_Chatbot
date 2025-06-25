class MemoryBuffer:
    def __init__(self):
        self.history = []

    def add(self, user_msg, agent_decision):
        self.history.append((user_msg, agent_decision))
        if len(self.history) > 5:
            self.history.pop(0)

    def get_context(self):
        return "\n".join(f"User: {u}\nAgent: {a}" for u, a in self.history)
