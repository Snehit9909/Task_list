import json
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

def load_templates(path="temp.json"):
    with open(path, "r") as f:
        return json.load(f)

def match_templates(user_input, templates):
    matched = []
    for name, data in templates.items():
        if any(keyword in user_input.lower() for keyword in data["keywords"]):
            matched.append((name, data["template"]))
    return matched


def apply_template(template_str, variables):
    prompt = PromptTemplate.from_template(template_str)
    return prompt.format(**variables)

def chain_transformations(user_input, templates):
    text = user_input
    context = {"tone": "formal"}

    if "clean_text" in templates:
        clean_template = templates["clean_text"]["template"]
        prompt = PromptTemplate.from_template(clean_template)
        text = prompt.format(text=text)

    if "tone_adjustment" in templates:
        tone_template = templates["tone_adjustment"]["template"]
        prompt = PromptTemplate.from_template(tone_template)
        text = prompt.format(text=text, tone=context["tone"])

    if "summarization" in templates:
        summary_template = templates["summarization"]["template"]
        prompt = PromptTemplate.from_template(summary_template)
        text = prompt.format(text=text)

    return text
    
if __name__ == "__main__":
    templates = load_templates()
    user_input = input("Enter your prompt: ")

    matched_templates = match_templates(user_input, templates)

    if len(matched_templates) == 1:
        name, template_str = matched_templates[0]
        print("\nMatched Template:", name)
        if name == "tone_adjustment":
            output = apply_template(template_str, {"text": user_input, "tone": "formal"})
        elif name == "summarization":
            output = apply_template(template_str, {"text": user_input})
        elif name == "polite_rephrasing":
            output = apply_template(template_str, {"task": user_input})
        else:
            output = apply_template(template_str, {"text": user_input})
        print("Reformulated Prompt:", output)

    else:
        print("\nNo direct match found or multiple matches. Applying chained transformations...")
        output = chain_transformations(user_input, templates)
        print("Final Output:", output)

