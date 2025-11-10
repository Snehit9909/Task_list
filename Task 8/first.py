from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.runnables import RunnableSequence
from langchain_core.language_models.llms import LLM


class LocalMockLLM(LLM):
    """
    A mock LLM that simulates a language model by reversing the input string.
    This is useful for local testing without any external API calls.
    """
    def _call(self, prompt: str, stop=None) -> str:
        print(f"\n[MockLLM] Received prompt:\n{prompt}")
        reversed_prompt = prompt[::-1]
        print(f"[MockLLM] reversed prompt:\n{reversed_prompt}")
        return reversed_prompt

    @property
    def _llm_type(self) -> str:
        return "local_mock_llm"


prompt_template = PromptTemplate.from_template("User said: {text}")

class SimpleOutputParser(BaseOutputParser):
    """
    A simple parser that formats the output from the LLM.
    """
    def parse(self, text: str):
        print(f"\n[OutputParser] Raw LLM output:\n{text}")
        parsed = f" Final Parsed Output:\n{text}"
        print(f"Parsed output:\n{parsed}")
        return parsed

chain = prompt_template | LocalMockLLM() | SimpleOutputParser()


if __name__ == "__main__":
    user_input = {"text": "Hello LangChain running locally!"}
    print(f"[Main] Input to chain: {user_input}")
    
    result = chain.invoke(user_input)
    
    
