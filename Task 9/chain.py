import string
from langchain_core.runnables import Runnable, RunnableSequence

class ToLowercase(Runnable):
    def invoke(self, input: str, config=None, **kwargs) -> str:
        result = input.lower()
        print("Step 1 - Lowercase:", result)
        return result

class RemovePunctuation(Runnable):
    def invoke(self, input: str, config=None, **kwargs) -> str:
        result = input.translate(str.maketrans('', '', string.punctuation))
        print("Step 2 - No Punctuation:", result)
        return result

class ReplaceSynonyms(Runnable):
    synonyms = {
        "quick": "fast",
        "happy": "joyful",
        "sad": "unhappy",
        "smart": "clever"
    }

    def invoke(self, input: str, config=None, **kwargs) -> str:
        words = input.split()
        replaced = [self.synonyms.get(word, word) for word in words]
        result = " ".join(replaced)
        print("Step 3 - Synonyms Replaced:", result)
        return result

class CountUniqueWords(Runnable):
    def invoke(self, input: str, config=None, **kwargs) -> str:
        words = input.split()
        unique_count = len(set(words))
        print("Step 4 - Unique Word Count:", unique_count)
        return f"Final Text: {input}\nUnique Words: {unique_count}"


pipeline = RunnableSequence(
    ToLowercase(),
    RemovePunctuation(),
    ReplaceSynonyms(),
    CountUniqueWords()
)

if __name__ == "__main__":
    user_input = input("Enter your text: ")
    print("\n Processing Pipeline ")
    result = pipeline.invoke(user_input)
    print("\n Final Output")
    print(result)
