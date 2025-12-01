# Persist knowledge over time

from langgraph.store.memory import InMemoryStore

_GLOBAL_STORE = None

def initialize_store(store: InMemoryStore):
    global _GLOBAL_STORE
    _GLOBAL_STORE = store

def get_global_store() -> InMemoryStore:
    if _GLOBAL_STORE is None:
        raise RuntimeError("Global store not initialized. Call initialize_store() first.")
    return _GLOBAL_STORE
