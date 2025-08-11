from ..utils.vector_store import vectorstore
from langchain_core.tools import create_retriever_tool

retriver = vectorstore.as_retriever()

retriever_tool = create_retriever_tool(retriever=retriver, name="retriever_tool", description="This tool is used to fetch information regrading the business. Information related to replacements, refunds, inventory discovery details can be found here")