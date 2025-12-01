from datetime import datetime
from functools import partial
from langchain_core.tools import Tool
import requests
import pyodata

class ODataToolManager:
    ENTITY_TOOL_DESCRIPTIONS = {
            'Company_Valuation':
                "Get the current Company Valuation, Profit, Bank Cash Account",

            'Carbon_Emissions':
                "Track the company's activities generating CO2 emissions.",

            'Financial_Postings':
                "Get current accounting entries and financial transactions.",

            'Sales':
                "Get current sales transactions and revenue data.",

            'Purchase_Orders':
                "Get current procurement and purchasing data.",

            'Production_Orders':
                "Get current manufacturing and production schedules.",

            'BOM_Changes':
                "Get current Bill of Materials changes and revisions.",

            'Independent_Requirements':
                "Get current production planning and demand forecasts.",

            'Current_Inventory_KPI':
                "Get key indicators to better manage inventory, stock transfer and forecast.",

            'Market':
                "Analyze market shares based on sales quantity or net value.",

            'Marketing_Expenses':
                "Get current marketing and advertising costs.",

            'Production':
                "Get current production output and efficiency metrics.",

            'Stock_Transfers':
                "Get current inventory movements between locations.",

            'Current_Pricing_Conditions':
                "Get current pricing conditions.",

            'Current_Inventory':
                "Get real-time current Stock levels for each product.",

            'Current_Suppliers_Prices':
                "Get unit cost for each products."
        }

    def __init__(self, url, username, password):
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.odata_service = pyodata.Client(url, self.session)
        self.odata_tools = self.create_individual_entity_tools()

    def create_individual_entity_tools(self, selected_entities=None):
        if selected_entities is None:
            selected_entities = [es.name for es in self.odata_service.schema.entity_sets]
        tools = []
        for entity_name in selected_entities:
            if not self.has_data(entity_name):
                print(f"✗ Skipping {entity_name}: No data available")
                continue
            tool_name = f"get_{entity_name.lower()}"
            entity_tool = Tool(
                func=partial(self.query_specific_entity, entity_name=entity_name),
                name=tool_name,
                description=self.ENTITY_TOOL_DESCRIPTIONS.get(entity_name, "")
            )
            tools.append(entity_tool)
            print(f"✓ Created tool: {tool_name}")
        return tools

    def has_data(self, entity_name, top_n=1):
        try:
            entity_set = getattr(self.odata_service.entity_sets, entity_name)
            entities = entity_set.get_entities().order_by("ROW_ID desc").top(top_n).execute()
            return bool(entities)
        except Exception as e:
            print(f"✗ Error checking {entity_name}: {str(e)}")
            return False

    def query_specific_entity(self, query="", entity_name=None, top_n=3):
        try:
            entity_set = getattr(self.odata_service.entity_sets, entity_name)
            entities = entity_set.get_entities().order_by("ROW_ID desc").top(top_n).execute()
            if not entities:
                return f"No current data found in {entity_name}."
            result = f"📊 CURRENT {entity_name.replace('_', ' ').upper()} DATA\n"
            result += f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            for i, entity in enumerate(entities, 1):
                result += f"📍 Record {i}:\n{self.format_entity_content(entity)}\n"
                if i < len(entities):
                    result += "─" * 50 + "\n"
            print(f"OData result: {result}")
            return result
        except Exception as e:
            return f"Error accessing {entity_name}: {str(e)}"

    @staticmethod
    def format_entity_content(entity):
        content_parts = []
        for attr_name in dir(entity):
            if attr_name == "_cache":
                try:
                    attr_value = getattr(entity, attr_name)
                    if isinstance(attr_value, dict):
                        for key, value in attr_value.items():
                            if value is not None and not callable(value):
                                content_parts.append(f"  {key}: {value}")
                except Exception:
                    continue
        return "\n".join(content_parts) if content_parts else "  No data available"
    
    def test_odata_connection(self):
        """Test OData connection and list available entities"""
        try:
            entity_sets = [es.name for es in self.odata_service.schema.entity_sets]
            print(f"Available entities: {entity_sets}")
            
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
    
    
    # def get_odata_tools(self):
    #     if _odata_tools is None:
    #         odata_tools = self.create_individual_entity_tools()
    #         initialize_odata_tools(odata_tools)
    #     else:
    #         odata_tools = get_gl_odata_tools()
    #     return odata_tools
    
    def get_odata_tools(self):
        return self.odata_tools

    # Example usage:

    # if **name** == "**main**":
    # manager = ODataToolManager(
    # url="[https://e05.bi.ucc.cit.tum.de/odata/943](https://e05.bi.ucc.cit.tum.de/odata/943)",
    # username="Admin1",
    # password="uccBAMA2024##"
    # )
    # odata_tools = manager.create_individual_entity_tools()
