from transformers import AutoModelForCausalLM, AutoTokenizer

class LlamaModel:
    def __init__(self, model_name='llama-3.1'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def generate_response(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors='pt')
        outputs = self.model.generate(**inputs)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
    model = LlamaModel()
    prompt = "What is the capital of France?"
    response = model.generate_response(prompt)
    print(response)
