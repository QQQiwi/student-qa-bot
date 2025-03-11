from qdrant_client import QdrantClient

# Инициализация клиента Qdrant
client = QdrantClient(host='localhost', port=6333)

# Получение информации о коллекции
collection_info = client.get_collection(collection_name='my_collection')
print("Информация о коллекции:", collection_info)

# Поиск векторов
search_result = client.search(
    collection_name='my_collection',
    query_vector=[0.1] * collection_info.config.params.vectors.size,  # Пример запроса с нулевым вектором
    limit=5
)
print("Результаты поиска:", search_result)