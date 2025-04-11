from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from transformers import AutoModel, AutoTokenizer, AutoModelForCausalLM, pipeline

import os
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"  # Для точного определения места ошибки
# Инициализация клиента Qdrant
client = QdrantClient(host='localhost', port=6333)

# Подключение модели-переводчика в вектора
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

# Создание векторного запроса
query = sentence_model.encode(input('Querry: '))

# Подключение llama 3.1 
# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
# model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

# Поиск 5ти ближайших к запросу векторов
context = client.search(
    collection_name= "my_collection",
    query_vector=query,
    limit = 5
)

# Перезагрузка модели
# model = AutoModel.from_pretrained(
#     "ai-forever/rugpt3small_based_on_gpt2",
#     force_download=True,  # Принудительно скачать заново
#     resume_download=False # Не продолжать прерванную загрузку
# )

# Вывод найденных ближайших векторов
# for item in context:
#     print(item) 

# Генерация ответа
model = pipeline("text-generation", model="ai-forever/rugpt3small_based_on_gpt2")
prompt = f"""Используй только контекст ниже. Не придумывай ответ, если его нет в тексте.
Контекст: {context}
Вопрос: {query}
Ответ:"""
print(model(
    prompt, 
    max_new_tokens=512,  # Максимальное количество новых токенов для генерации
    max_length=2048,     # Общий максимум (промпт + сгенерированный ответ)
    temperature=0.1
)[0]["generated_text"])