from langchain.agents import create_agent
from core.llm import get_llm
from tools.odata_tools import *
from tools.retrieve_docs import * 
from config.agent_config import RETRIEVER_AGENT_PROMPT
from storage.global_store import get_global_store

def get_retriever_agent():
    retriever_agent = create_agent(
        model=get_llm(),
        tools=[
            retrieve_documents,
            retrieve_sap_transactions,
            retrieve_company_valuation,
            retrieve_carbon_emissions,
            retrieve_financial_postings,
            retrieve_sales,
            retrieve_purchase_orders,
            retrieve_production_orders,
            retrieve_bom_changes,
            retrieve_independent_requirements,
            retrieve_current_inventory_kpi,
            retrieve_market,
            retrieve_marketing_expenses,
            retrieve_production,
            retrieve_stock_transfers,
            retrieve_current_pricing_conditions,
            retrieve_current_inventory,
            retrieve_current_suppliers_prices
        ],
        store=get_global_store(),
        system_prompt=RETRIEVER_AGENT_PROMPT,
    )
    return retriever_agent