"""GL Runtime V20 - 無限學習"""
class InfiniteLearner:
    def __init__(self):
        self._knowledge = {}
    
    def learn(self, data: dict) -> None:
        self._knowledge.update(data)
    
    def recall(self, key: str):
        return self._knowledge.get(key)
