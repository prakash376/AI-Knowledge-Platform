from agent.calculator_tool import calculator_tool
from rag.pipeline import answer_query

def decide_tool(query:str)->str:
    query_lower = query.lower()
    math_symbols = ["+","-","*","/" , "calculate" , "what is"]
    has_numbers = any(char.isdigit() for char in query)

    has_math_numbers = any(symbols in query_lower for symbols in math_symbols)

    if has_numbers and has_math_numbers:
        return "Calculator"
    return "rag"

def run_agent(query:str)-> str:
    tool = decide_tool(query)

    if tool == "Calculator":
        result = calculator_tool(query)
        return {"answer":result , "tool_used":"Calculator" , "Sources":[]}

    else : 
        rag_result = answer_query(query)
        rag_result["tool_used"] = "rag"
        return rag_result