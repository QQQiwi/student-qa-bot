from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Загрузка токенизатора и модели Llama 3.1
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-chat-hf",
    torch_dtype=torch.float16,
    device_map="auto"
)