# The only OData manager used in the whole chat.

from storage.odata_source import ODataToolManager

_odata_manager = None
# _odata_tools = None


def ensure_odata_manager(url, username, password) -> ODataToolManager:
    manager = get_odata_manager()

    if manager:
        return manager
    manager = ODataToolManager(url, username, password)
    initialize_odata_manager(manager)
    return manager


def get_odata_manager():
    return _odata_manager

def initialize_odata_manager(manager):
    global _odata_manager
    _odata_manager = manager
    
# def get_gl_odata_tools():
#     return _odata_tools 
    
# def initialize_odata_tools(tools):
#     global _odata_tools
#     _odata_tools = tools