import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.fake import FakeListLLM
from langchain_core.runnables import RunnableSequence

class SimpleMemory:
    def __init__(self):
        self.chat_history = []

    def load_memory_variables(self):
        return {"chat_history": self.chat_history}

    def save_context(self, inputs, outputs):
        self.chat_history.append({"input": inputs, "output": outputs})


def create_chain(prompt_template: str, llm_class, memory_on: bool, responses: list):
    prompt = PromptTemplate(input_variables=["prompt"], template=prompt_template)

    memory = SimpleMemory() if memory_on else None

    llm = llm_class(responses=responses) 

    chain = RunnableSequence(first=prompt, last=llm)
    return chain


def main():

    st.title("LangChain Playground")

    prompt_template = st.text_area("Enter Prompt Template:", "What is the capital of {prompt}?")

    memory_on = st.checkbox("Enable Memory")

    output_parser = st.selectbox("Select Output Parser", ["BasicParser", "CustomParser"])

    responses = [
        "The capital of France is Paris",
        "The capital of Spain is Madrid",
        "The capital of Germany is Berlin"
    ]

    llm_class = FakeListLLM 
    chain = create_chain(prompt_template, llm_class, memory_on, responses)

    user_input = st.text_input("Enter a query to run the chain:")

    if user_input:
        result = chain.invoke({"prompt": user_input})

        st.write("Chain Output: ", result)

        if output_parser == "BasicParser":
            st.write("Parsed Output: ", result)
        elif output_parser == "CustomParser":
            st.write("Custom parsed output: ", result.upper()) 
        else:
            st.write("Output: ", result)


if __name__ == "__main__":
    main()
