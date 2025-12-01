from langchain.tools import tool, ToolRuntime
from storage.global_odata_manager import get_odata_manager
from storage.global_store import get_global_store
from config.agent_config import MAX_RETRIEVAL
from tools.helpers import get_retrieve_call_count, increment_retrieve_call_count
from datetime import datetime


def get_odata_tool_by_name(tool_name: str, odata_tools):
    tool_dict = {tool.name: tool for tool in odata_tools}
    my_tool = tool_dict.get(tool_name)
    return my_tool


# COMPANY VALUATION
@tool
def retrieve_company_valuation(runtime: ToolRuntime):
    """
    Get the current Company Valuation, Profit, Bank Cash Account,
    Accounts Receivable, Accounts Payable, and Financial Metrics.
    Use for questions about company worth, stock performance, profits,
    bank balances, and overall financial health.
    """
    try:
      odata_manager = get_odata_manager()
      tool = get_odata_tool_by_name("get_company_valuation", odata_manager.get_odata_tools())
      
      if tool is None:
          print( "Company Valuation doesn't exist")
          return "Company Valuation doesn't exist"

      config = runtime.config
      user_id = config.get("configurable", {}).get("user_id")
      if not user_id:
          raise ValueError("user_id is missing in runtime.config['configurable']")
      namespace = ("retrieved_tools", user_id)
      store = get_global_store()
      retrieve_call_count = get_retrieve_call_count(store, user_id)
      if retrieve_call_count >= MAX_RETRIEVAL:
        print("Maximum retrieval reached.")
        return f"⚠️ retrieve_tools has already been called {retrieve_call_count} times. Please reuse existing data."
      else:
        new_count = increment_retrieve_call_count(store, user_id)
        print(f"🔧 Comp Val DEBUG: Incremented call count to: {new_count}")
      content = tool.invoke("")
      print(f"Comp Val Debug: Retrieved content:\n {content}\n")
      existing_items = store.search(namespace)
      exist = False
      for item in existing_items:
        if item.value.get("content") == content:
          print(f"🧠 Content already retrieved, skipping store.")
          exist = True

      if not exist:
          # Store new content
          timestamp_key = str(datetime.now().timestamp())
          new_content = {
            "ts": datetime.now().isoformat(),
            "content": content
          }
          store.put(namespace, timestamp_key, new_content)
      return content
    
    except Exception as e:
      return f"Error retrieving company valuation: {str(e)}"
    
    
    # CARBON EMISSIONS
@tool
def retrieve_carbon_emissions(runtime: ToolRuntime):
    """
    Track the company's activities generating CO2 emissions.
    Contains Total CO2 Emissions and Emissions.
    The Emissions column may differ from the Total CO2 Emissions column
    when the Type is Products Purchased or Overstock.
    Use for questions about sustainability, CO2 footprint,
    environmental impact, and green initiatives.
    """
    odata_manager = get_odata_manager()
    tool = get_odata_tool_by_name("get_carbon_emissions", odata_manager.get_odata_tools())
      
    if tool is None:
        return "Carbon Emissions doesn't exist"

    config = runtime.config
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        raise ValueError("user_id is missing in runtime.config['configurable']")
    namespace = ("retrieved_tools", user_id)
    store = get_global_store()
    retrieve_call_count = get_retrieve_call_count(store, user_id)
    if retrieve_call_count >= MAX_RETRIEVAL:
      print("Maximum retrieval reached.")
      return f"⚠️ retrieve_tools has already been called {retrieve_call_count} times. Please reuse existing data."
    else:
      new_count = increment_retrieve_call_count(store, user_id)
      print(f"🔧 DEBUG: Incremented call count to: {new_count}")
    content = tool.invoke("")
    existing_items = store.search(namespace)
    exist = False
    for item in existing_items:
      if item.value.get("content") == content:
        print(f"🧠 Content already retrieved, skipping store.")
        exist = True

    if not exist:
        # Store new content
        timestamp_key = str(datetime.now().timestamp())
        new_content = {
          "ts": datetime.now().isoformat(),
          "content": content
        }
        store.put(namespace, timestamp_key, new_content)
    return content


# FINANCIAL POSTINGS
@tool
def retrieve_financial_postings(runtime: ToolRuntime):
    """
    Get current accounting entries and financial transactions.
    Use for detailed financial analysis, journal entries,
    debit/credit postings, and accounting records.
    """
    odata_manager = get_odata_manager()
    tool = get_odata_tool_by_name("get_financial_postings", odata_manager.get_odata_tools())
    
    if tool is None:
        return "Financial Postings doesn't exist"
    config = runtime.config
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        raise ValueError("user_id is missing in runtime.config['configurable']")
    namespace = ("retrieved_tools", user_id)
    store = get_global_store()
    retrieve_call_count = get_retrieve_call_count(store, user_id)
    if retrieve_call_count >= MAX_RETRIEVAL:
      print("Maximum retrieval reached.")
      return f"⚠️ retrieve_tools has already been called {retrieve_call_count} times. Please reuse existing data."
    else:
      new_count = increment_retrieve_call_count(store, user_id)
      print(f"🔧 DEBUG: Incremented call count to: {new_count}")
    content = tool.invoke("")
    existing_items = store.search(namespace)
    exist = False
    for item in existing_items:
      if item.value.get("content") == content:
        print(f"🧠 Content already retrieved, skipping store.")
        exist = True

    if not exist:
        # Store new content
        timestamp_key = str(datetime.now().timestamp())
        new_content = {
          "ts": datetime.now().isoformat(),
          "content": content
        }
        store.put(namespace, timestamp_key, new_content)
    return content

# SALES
@tool
def retrieve_sales(runtime: ToolRuntime):
    """
    Get current sales transactions and revenue data.
    Use for questions about sales performance, customer orders,
    revenue metrics, and sales trends.
    """
    odata_manager = get_odata_manager()
    tool = get_odata_tool_by_name("get_sales", odata_manager.get_odata_tools())
    if tool is None:
        return "Sales doesn't exist"
    config = runtime.config
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        raise ValueError("user_id is missing in runtime.config['configurable']")
    namespace = ("retrieved_tools", user_id)
    store = get_global_store()
    retrieve_call_count = get_retrieve_call_count(store, user_id)
    if retrieve_call_count >= MAX_RETRIEVAL:
      print("Maximum retrieval reached.")
      return f"⚠️ retrieve_tools has already been called {retrieve_call_count} times. Please reuse existing data."
    else:
      new_count = increment_retrieve_call_count(store, user_id)
      print(f"🔧 DEBUG: Incremented call count to: {new_count}")
    content = tool.invoke("")
    existing_items = store.search(namespace)
    exist = False
    for item in existing_items:
      if item.value.get("content") == content:
        print(f"🧠 Content already retrieved, skipping store.")
        exist = True

    if not exist:
        # Store new content
        timestamp_key = str(datetime.now().timestamp())
        new_content = {
          "ts": datetime.now().isoformat(),
          "content": content
        }
        store.put(namespace, timestamp_key, new_content)
    return content


# PURCHASE ORDERS
@tool
def retrieve_purchase_orders(runtime: ToolRuntime):
    """
    Get the latest purchase orders documents generated and their status.
    Contains Quantity (Product quantity in the purchase order).
    Use for questions about supplier orders, purchase quantities,
    and sales order item quantity purchased by the customer.
    """
    odata_manager = get_odata_manager()
    tool = get_odata_tool_by_name("get_purchase_orders", odata_manager.get_odata_tools())
    
    if tool is None:
        return "Purchase Orders doesn't exist"
    config = runtime.config
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        raise ValueError("user_id is missing in runtime.config['configurable']")
    namespace = ("retrieved_tools", user_id)
    store = get_global_store()
    retrieve_call_count = get_retrieve_call_count(store, user_id)
    if retrieve_call_count >= MAX_RETRIEVAL:
      print("Maximum retrieval reached.")
      return f"⚠️ retrieve_tools has already been called {retrieve_call_count} times. Please reuse existing data."
    else:
      new_count = increment_retrieve_call_count(store, user_id)
      print(f"🔧 DEBUG: Incremented call count to: {new_count}")
    content = tool.invoke("")
    existing_items = store.search(namespace)
    exist = False
    for item in existing_items:
      if item.value.get("content") == content:
        print(f"🧠 Content already retrieved, skipping store.")
        exist = True

    if not exist:
        # Store new content
        timestamp_key = str(datetime.now().timestamp())
        new_content = {
          "ts": datetime.now().isoformat(),
          "content": content
        }
        store.put(namespace, timestamp_key, new_content)
    return content


# PRODUCTION ORDERS
@tool
def retrieve_production_orders(runtime:ToolRuntime):
    """
    Get the latest production orders documents generated and their status,
    available for all Manufacturing games.
    Contains Target Quantity (total quantity to be produced to complete
    the production order) and Confirmed Quantity (Current quantity produced
    for the production order).
    Use for questions about production orders, manufacturing orders,
    factory scheduling, and production efficiency.
    """
    odata_manager = get_odata_manager()
    tool = get_odata_tool_by_name("get_production_orders", odata_manager.get_odata_tools())
    if tool is None:
        return "Production Orders doesn't exist"
    config = runtime.config
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        raise ValueError("user_id is missing in runtime.config['configurable']")
    namespace = ("retrieved_tools", user_id)
    store = get_global_store()
    retrieve_call_count = get_retrieve_call_count(store, user_id)
    if retrieve_call_count >= MAX_RETRIEVAL:
      print("Maximum retrieval reached.")
      return f"⚠️ retrieve_tools has already been called {retrieve_call_count} times. Please reuse existing data."
    else:
      new_count = increment_retrieve_call_count(store, user_id)
      print(f"🔧 DEBUG: Incremented call count to: {new_count}")
    content = tool.invoke("")
    existing_items = store.search(namespace)
    exist = False
    for item in existing_items:
      if item.value.get("content") == content:
        print(f"🧠 Content already retrieved, skipping store.")
        exist = True

    if not exist:
        # Store new content
        timestamp_key = str(datetime.now().timestamp())
        new_content = {
          "ts": datetime.now().isoformat(),
          "content": content
        }
        store.put(namespace, timestamp_key, new_content)
    return content


# BOM CHANGES
@tool
def retrieve_bom_changes(runtime: ToolRuntime):
    """
    Get Bill of Materials changes, only available for Manufacturing Extended
    and Advanced game.
    Use when Quantity of components required to produce one unit of
    finished goods is asked.
    """
    odata_manager = get_odata_manager()
    tool = get_odata_tool_by_name("get_bom_changes", odata_manager.get_odata_tools())
    if tool is None:
        return "BOM Changes doesn't exist"
    config = runtime.config
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        raise ValueError("user_id is missing in runtime.config['configurable']")
    namespace = ("retrieved_tools", user_id)
    store = get_global_store()
    retrieve_call_count = get_retrieve_call_count(store, user_id)
    if retrieve_call_count >= MAX_RETRIEVAL:
      print("Maximum retrieval reached.")
      return f"⚠️ retrieve_tools has already been called {retrieve_call_count} times. Please reuse existing data."
    else:
      new_count = increment_retrieve_call_count(store, user_id)
      print(f"🔧 DEBUG: Incremented call count to: {new_count}")
    content = tool.invoke("")
    existing_items = store.search(namespace)
    exist = False
    for item in existing_items:
      if item.value.get("content") == content:
        print(f"🧠 Content already retrieved, skipping store.")
        exist = True

    if not exist:
        # Store new content
        timestamp_key = str(datetime.now().timestamp())
        new_content = {
          "ts": datetime.now().isoformat(),
          "content": content
        }
        store.put(namespace, timestamp_key, new_content)
    return content


# INDEPENDENT REQUIREMENTS
@tool
def retrieve_independent_requirements(runtime: ToolRuntime):
    """
    Get the daily production planning and demand forecasts.
    Use for questions about demand planning, production requirements,
    and manufacturing forecasts.
    """
    odata_manager = get_odata_manager()
    tool = get_odata_tool_by_name("get_independent_requirements", odata_manager.get_odata_tools())
    if tool is None:
        return "Independent Requirements doesn't exist"
    config = runtime.config
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        raise ValueError("user_id is missing in runtime.config['configurable']")
    namespace = ("retrieved_tools", user_id)
    store = get_global_store()
    retrieve_call_count = get_retrieve_call_count(store, user_id)
    if retrieve_call_count >= MAX_RETRIEVAL:
      print("Maximum retrieval reached.")
      return f"⚠️ retrieve_tools has already been called {retrieve_call_count} times. Please reuse existing data."
    else:
      new_count = increment_retrieve_call_count(store, user_id)
      print(f"🔧 DEBUG: Incremented call count to: {new_count}")
    content = tool.invoke("")
    existing_items = store.search(namespace)
    exist = False
    for item in existing_items:
      if item.value.get("content") == content:
        print(f"🧠 Content already retrieved, skipping store.")
        exist = True

    if not exist:
        # Store new content
        timestamp_key = str(datetime.now().timestamp())
        new_content = {
          "ts": datetime.now().isoformat(),
          "content": content
        }
        store.put(namespace, timestamp_key, new_content)
    return content


# CURRENT INVENTORY KPI
@tool
def retrieve_current_inventory_kpi(runtime: ToolRuntime):
    """
    Get key indicators to better manage inventory, stock transfer and forecast.
    Contains Current Inventory, Quantity Sold, Nb Steps Available.
    Nb Steps Available describes the number of steps for which the product
    was in inventory.
    Use for questions about stock turnover, stockout frequency,
    inventory efficiency, and KPI metrics.
    """
    odata_manager = get_odata_manager()
    tool = get_odata_tool_by_name("get_current_inventory_kpi", odata_manager.get_odata_tools())
    if tool is None:
        return "Current Inventory KPI doesn't exist"
    config = runtime.config
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        raise ValueError("user_id is missing in runtime.config['configurable']")
    namespace = ("retrieved_tools", user_id)
    store = get_global_store()
    retrieve_call_count = get_retrieve_call_count(store, user_id)
    if retrieve_call_count >= MAX_RETRIEVAL:
      print("Maximum retrieval reached.")
      return f"⚠️ retrieve_tools has already been called {retrieve_call_count} times. Please reuse existing data."
    else:
      new_count = increment_retrieve_call_count(store, user_id)
      print(f"🔧 DEBUG: Incremented call count to: {new_count}")
    content = tool.invoke("")
    existing_items = store.search(namespace)
    exist = False
    for item in existing_items:
      if item.value.get("content") == content:
        print(f"🧠 Content already retrieved, skipping store.")
        exist = True

    if not exist:
        # Store new content
        timestamp_key = str(datetime.now().timestamp())
        new_content = {
          "ts": datetime.now().isoformat(),
          "content": content
        }
        store.put(namespace, timestamp_key, new_content)
    return content


# MARKET
@tool
def retrieve_market(runtime: ToolRuntime):
    """
    Analyze market shares based on sales quantity or net value.
    Contains total product quantity sold to each market area for the period,
    the average price of goods sold in each market area, and the
    generated net value for each good sold in each market area.
    Use for questions about market conditions.
    """
    odata_manager = get_odata_manager()
    tool = get_odata_tool_by_name("get_market", odata_manager.get_odata_tools())
    if tool is None:
        return "Market doesn't exist"
    config = runtime.config
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        raise ValueError("user_id is missing in runtime.config['configurable']")
    namespace = ("retrieved_tools", user_id)
    store = get_global_store()
    retrieve_call_count = get_retrieve_call_count(store, user_id)
    if retrieve_call_count >= MAX_RETRIEVAL:
      print("Maximum retrieval reached.")
      return f"⚠️ retrieve_tools has already been called {retrieve_call_count} times. Please reuse existing data."
    else:
      new_count = increment_retrieve_call_count(store, user_id)
      print(f"🔧 DEBUG: Incremented call count to: {new_count}")
    content = tool.invoke("")
    existing_items = store.search(namespace)
    exist = False
    for item in existing_items:
      if item.value.get("content") == content:
        print(f"🧠 Content already retrieved, skipping store.")
        exist = True

    if not exist:
        # Store new content
        timestamp_key = str(datetime.now().timestamp())
        new_content = {
          "ts": datetime.now().isoformat(),
          "content": content
        }
        store.put(namespace, timestamp_key, new_content)
    return content


# MARKETING EXPENSES
@tool
def retrieve_marketing_expenses(runtime: ToolRuntime):
    """
    Get daily investments in marketing and advertising per product and region.
    Use for questions about marketing budgets, campaign costs,
    advertising expenses, and marketing ROI.
    """
    odata_manager = get_odata_manager()
    tool = get_odata_tool_by_name("get_marketing_expenses", odata_manager.get_odata_tools())
    if tool is None:
        return "Marketing Expenses doesn't exist"
    config = runtime.config
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        raise ValueError("user_id is missing in runtime.config['configurable']")
    namespace = ("retrieved_tools", user_id)
    store = get_global_store()
    retrieve_call_count = get_retrieve_call_count(store, user_id)
    if retrieve_call_count >= MAX_RETRIEVAL:
      print("Maximum retrieval reached.")
      return f"⚠️ retrieve_tools has already been called {retrieve_call_count} times. Please reuse existing data."
    else:
      new_count = increment_retrieve_call_count(store, user_id)
      print(f"🔧 DEBUG: Incremented call count to: {new_count}")
    content = tool.invoke("")
    existing_items = store.search(namespace)
    exist = False
    for item in existing_items:
      if item.value.get("content") == content:
        print(f"🧠 Content already retrieved, skipping store.")
        exist = True

    if not exist:
        # Store new content
        timestamp_key = str(datetime.now().timestamp())
        new_content = {
          "ts": datetime.now().isoformat(),
          "content": content
        }
        store.put(namespace, timestamp_key, new_content)
    return content


# PRODUCTION
@tool
def retrieve_production(runtime: ToolRuntime):
    """
    Get current production output and efficiency metrics.
    Use for questions about factory output, production rates,
    manufacturing efficiency, and production costs.
    """
    odata_manager = get_odata_manager()
    tool = get_odata_tool_by_name("get_production", odata_manager.get_odata_tools())
    if tool is None:
        return "Production doesn't exist"
    config = runtime.config
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        raise ValueError("user_id is missing in runtime.config['configurable']")
    namespace = ("retrieved_tools", user_id)
    store = get_global_store()
    retrieve_call_count = get_retrieve_call_count(store, user_id)
    if retrieve_call_count >= MAX_RETRIEVAL:
      print("Maximum retrieval reached.")
      return f"⚠️ retrieve_tools has already been called {retrieve_call_count} times. Please reuse existing data."
    else:
      new_count = increment_retrieve_call_count(store, user_id)
      print(f"🔧 DEBUG: Incremented call count to: {new_count}")
    content = tool.invoke("")
    existing_items = store.search(namespace)
    exist = False
    for item in existing_items:
      if item.value.get("content") == content:
        print(f"🧠 Content already retrieved, skipping store.")
        exist = True

    if not exist:
        # Store new content
        timestamp_key = str(datetime.now().timestamp())
        new_content = {
          "ts": datetime.now().isoformat(),
          "content": content
        }
        store.put(namespace, timestamp_key, new_content)
    return content


# STOCK TRANSFERS
@tool
def retrieve_stock_transfers(runtime: ToolRuntime):
    """
    Get current inventory movements between locations.
    Use for questions about stock transfers, warehouse movements,
    and internal logistics.
    """
    odata_manager = get_odata_manager()
    tool = get_odata_tool_by_name("get_stock_transfers", odata_manager.get_odata_tools())
    if tool is None:
        return "Stock Transfers doesn't exist"
    config = runtime.config
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        raise ValueError("user_id is missing in runtime.config['configurable']")
    namespace = ("retrieved_tools", user_id)
    store = get_global_store()
    retrieve_call_count = get_retrieve_call_count(store, user_id)
    if retrieve_call_count >= MAX_RETRIEVAL:
      print("Maximum retrieval reached.")
      return f"⚠️ retrieve_tools has already been called {retrieve_call_count} times. Please reuse existing data."
    else:
      new_count = increment_retrieve_call_count(store, user_id)
      print(f"🔧 DEBUG: Incremented call count to: {new_count}")
    content = tool.invoke("")
    existing_items = store.search(namespace)
    exist = False
    for item in existing_items:
      if item.value.get("content") == content:
        print(f"🧠 Content already retrieved, skipping store.")
        exist = True

    if not exist:
        # Store new content
        timestamp_key = str(datetime.now().timestamp())
        new_content = {
          "ts": datetime.now().isoformat(),
          "content": content
        }
        store.put(namespace, timestamp_key, new_content)
    return content


# CURRENT PRICING CONDITIONS
@tool
def retrieve_current_pricing_conditions(runtime: ToolRuntime):
    """
    Get the current price for each product.
    """
    odata_manager = get_odata_manager()
    tool = get_odata_tool_by_name("get_current_pricing_conditions", odata_manager.get_odata_tools())
    if tool is None:
        return "Current Pricing Conditions doesn't exist"
    config = runtime.config
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        raise ValueError("user_id is missing in runtime.config['configurable']")
    namespace = ("retrieved_tools", user_id)
    store = get_global_store()
    retrieve_call_count = get_retrieve_call_count(store, user_id)
    if retrieve_call_count >= MAX_RETRIEVAL:
      print("Maximum retrieval reached.")
      return f"⚠️ retrieve_tools has already been called {retrieve_call_count} times. Please reuse existing data."
    else:
      new_count = increment_retrieve_call_count(store, user_id)
      print(f"🔧 DEBUG: Incremented call count to: {new_count}")
    content = tool.invoke("")
    existing_items = store.search(namespace)
    exist = False
    for item in existing_items:
      if item.value.get("content") == content:
        print(f"🧠 Content already retrieved, skipping store.")
        exist = True

    if not exist:
        # Store new content
        timestamp_key = str(datetime.now().timestamp())
        new_content = {
          "ts": datetime.now().isoformat(),
          "content": content
        }
        store.put(namespace, timestamp_key, new_content)
    return content

# CURRENT INVENTORY
@tool
def retrieve_current_inventory(runtime: ToolRuntime):
    """
    Get real-time current stock levels for each product.
    Use for questions about immediate stock availability,
    current warehouse quantities, and real-time inventory.
    """
    odata_manager = get_odata_manager()
    tool = get_odata_tool_by_name("get_current_inventory", odata_manager.get_odata_tools())
    if tool is None:
        return "Current Inventory doesn't exist"
    config = runtime.config
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        raise ValueError("user_id is missing in runtime.config['configurable']")
    namespace = ("retrieved_tools", user_id)
    store = get_global_store()
    retrieve_call_count = get_retrieve_call_count(store, user_id)
    if retrieve_call_count >= MAX_RETRIEVAL:
      print("Maximum retrieval reached.")
      return f"⚠️ retrieve_tools has already been called {retrieve_call_count} times. Please reuse existing data."
    else:
      new_count = increment_retrieve_call_count(store, user_id)
      print(f"🔧 DEBUG: Incremented call count to: {new_count}")
    content = tool.invoke("")
    existing_items = store.search(namespace)
    exist = False
    for item in existing_items:
      if item.value.get("content") == content:
        print(f"🧠 Content already retrieved, skipping store.")
        exist = True

    if not exist:
        # Store new content
        timestamp_key = str(datetime.now().timestamp())
        new_content = {
          "ts": datetime.now().isoformat(),
          "content": content
        }
        store.put(namespace, timestamp_key, new_content)
    return content


# CURRENT SUPPLIERS PRICES
@tool
def retrieve_current_suppliers_prices(runtime: ToolRuntime):
    """
    Get current supplier pricing information.
    Use for questions about product costs per unit, purchase prices,
    and product information.
    """
    odata_manager = get_odata_manager()
    tool = get_odata_tool_by_name("get_current_suppliers_prices", odata_manager.get_odata_tools())
    if tool is None:
        return "Current Suppliers Prices doesn't exist"
    config = runtime.config
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        raise ValueError("user_id is missing in runtime.config['configurable']")
    namespace = ("retrieved_tools", user_id)
    store = get_global_store()
    retrieve_call_count = get_retrieve_call_count(store, user_id)
    if retrieve_call_count >= MAX_RETRIEVAL:
      print("Maximum retrieval reached.")
      return f"⚠️ retrieve_tools has already been called {retrieve_call_count} times. Please reuse existing data."
    else:
      new_count = increment_retrieve_call_count(store, user_id)
      print(f"🔧 DEBUG: Incremented call count to: {new_count}")
    content = tool.invoke("")
    existing_items = store.search(namespace)
    exist = False
    for item in existing_items:
      if item.value.get("content") == content:
        print(f"🧠 Content already retrieved, skipping store.")
        exist = True

    if not exist:
        # Store new content
        timestamp_key = str(datetime.now().timestamp())
        new_content = {
          "ts": datetime.now().isoformat(),
          "content": content
        }
        store.put(namespace, timestamp_key, new_content)
    return content