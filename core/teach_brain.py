import os
import json

class TeachBrain:
    @staticmethod
    def get_memory_path():
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        memory_dir = os.path.join(base_dir, 'memory')
        os.makedirs(memory_dir, exist_ok=True)
        return os.path.join(memory_dir, 'custom_vocab.json')

    @staticmethod
    def load_vocab():
        """Returns a dict mapping custom words to base intents. e.g. {'yoink': 'extract'}"""
        path = TeachBrain.get_memory_path()
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    @staticmethod
    def save_vocab(word, intent):
        """Saves a new custom word mapping to memory"""
        vocab = TeachBrain.load_vocab()
        vocab[word.lower()] = intent.lower()
        
        path = TeachBrain.get_memory_path()
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(vocab, f, indent=4)
            return True
        except Exception:
            return False
