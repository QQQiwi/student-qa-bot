from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM

# Инициализация клиента Qdrant
client = QdrantClient(host='localhost', port=6333)

# Подключение модели-переводчика в вектора
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

# Создание векторного запроса
querry = sentence_model.encode(input('Querry: '))

# Подключение llama 3.1 
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

# Поиск 5ти ближайших к запросу векторов
context = client.search(
    collection_name= "my_collection",
    query_vector=querry,
    limit = 5
)

# Вывод найденных ближайших векторов
for item in context:
    print(item) 

# prompt = f"Используя данный мною контекст, ответь на вопрос: \n {context}. Вопрос: {querry}"
# print(model(prompt, max_tokens = 512, temperature = 0))