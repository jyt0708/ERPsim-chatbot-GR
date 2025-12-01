def get_retrieve_call_count(store, user_id) -> int:
    """Get the number of times tools have been retrieved"""
    namespace = ("retrieve_tools_count", user_id)
    items = store.search(namespace)

    if not items:
        return 0

    # The counter is stored as the value of the first item
    # Since we're using a dedicated namespace, just use the first item
    return items[0].value

def increment_retrieve_call_count(store, user_id) -> int:
    """Increment and return the retrieve call count for a user"""
    namespace = ("retrieve_tools_count", user_id)
    new_count = get_retrieve_call_count(store, user_id) + 1

    # Store/update the counter - use a fixed key "counter"
    store.put(namespace, "counter", new_count)
    return new_count