from fastapi import FASTAPI
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate

def transform_text(task: str, text: str) -> str:
    if task == "reverse":
        return text[::-1]
    elif task == "keywords":
        return ", ".join(text.split()[:5])  
    elif task == "summarize":
        return "Summary: " + text[:50] + "..." 
    else:
        return f"Unknown task '{task}'"

class LocalChain:
    def __init__(self, prompt: PromptTemplate):
        self.prompt = prompt

    def run(self, task: str, text: str):
        formatted = self.prompt.format(task=task, text=text)
        result = transform_text(task, text)
        return {"input": formatted, "output": result}

app = FastAPI()

class ChainRequest(BaseModel):
    task: str
    text: str

prompt = PromptTemplate(
    input_variables=["task", "text"],
    template="Perform the task '{task}' on the following text:\n{text}"
)

chain = LocalChain(prompt)

@app.post("/run_chain")
async def run_chain(req: ChainRequest):
    result = chain.run(req.task, req.text)
    return result
