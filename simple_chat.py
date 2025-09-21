from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from duckduckgo_search import DDGS
import asyncio

import os 
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

class simple_chat:
    def __init__(self):
        self.llm = ChatGroq(temperature=0.2, model="moonshotai/kimi-k2-instruct")

        self.merge_prompt = ChatPromptTemplate.from_template("""
        You are a helpful project guide assistant specializing in engineering, technology, and educational projects.
        
        Your role is to help users refine their project ideas by:
        1. Understanding their interests and skill level
        2. Asking clarifying questions to make vague ideas more specific
        3. Suggesting improvements and practical considerations
        4. Focusing on projects that are educational and achievable
        
        User's query: {query}
        
        Web search results: {search_result}
        
        Guidelines:
        - Only help with technology, engineering, science, and educational projects
        - Ask 2-3 specific questions if the idea needs clarification
        - Suggest realistic scope based on skill level and resources
        - Encourage learning-focused projects
        - Be encouraging and educational
        
        Provide a helpful response that guides the user toward a well-defined project.
        """)
        

    def duckduckgo_search(self, query: str) -> str:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=5)
            return "\n".join([f"- {r['title']}: {r['href']}" for r in results])


    async def fusion_answer(self, user_query):
   
        loop = asyncio.get_event_loop()
        search_task = loop.run_in_executor(None, self.duckduckgo_search, user_query) 
        llm_task = loop.run_in_executor(None, self.llm.predict, user_query)
        search_result, llm_output = await asyncio.gather(search_task, llm_task)

        final_input = self.merge_prompt.format_messages(
            query=user_query,
            search_result=search_result + "\n\nLLM Thought:\n" + llm_output
        )

        final_response = self.llm.invoke(final_input)
        return final_response.content
    
    def __call__(self, user_query):
        return asyncio.run(self.fusion_answer(user_query))
        

if __name__ == "__main__":
    chat = simple_chat()
    user_query = "What are the best AI projects for a final year student?"
    result = chat(user_query)
    print("\n🧠 Final Answer:\n", result)
