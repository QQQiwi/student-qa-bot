from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

# Инициализация модели для преобразования текста в векторы
model = SentenceTransformer('all-MiniLM-L6-v2')

# Функция для создания иерархического текста
def create_hierarchical_text(direction, document, section, details=None):
    base_text = f"{direction['name']} -> {document['type']} -> {section['category']}"
    if details:
        base_text += f" -> {details}"
    return base_text

# Извлечение иерархических текстов
hierarchical_texts = []
for direction in data['directions']:
    for document in direction['documents']:
        for section in document['sections']:
            if section['category'] == 'Общие сведения':
                for key, value in section['details'].items():
                    hierarchical_text = create_hierarchical_text(direction, document, section, f"{key}: {value}")
                    hierarchical_texts.append(hierarchical_text)
            elif section['category'] == 'Образовательные стандарты':
                for standard in section['standards']:
                    hierarchical_text = create_hierarchical_text(direction, document, section, f"{standard['code']}: {standard['name']}")
                    hierarchical_texts.append(hierarchical_text)
            elif section['category'] == 'Курсы':
                for course in section['courses']:
                    hierarchical_text = create_hierarchical_text(direction, document, section, course['name'])
                    hierarchical_texts.append(hierarchical_text)
            elif section['category'] == 'Практики':
                for practice in section['practices']:
                    hierarchical_text = create_hierarchical_text(direction, document, section, practice['name'])
                    hierarchical_texts.append(hierarchical_text)
            elif section['category'] == 'Экзамены и зачеты':
                for key, value in section['details'].items():
                    hierarchical_text = create_hierarchical_text(direction, document, section, f"{key}: {value}")
                    hierarchical_texts.append(hierarchical_text)
            elif section['category'] == 'Календарь':
                for year, semesters in section['schedule'].items():
                    for semester, dates in semesters.items():
                        date_info = f"{semester}: {dates['start_date']} - {dates['end_date']}"
                        hierarchical_text = create_hierarchical_text(direction, document, section, date_info)
                        hierarchical_texts.append(hierarchical_text)

# Преобразование иерархических текстов в векторы
vectors = model.encode(hierarchical_texts)

# Инициализация клиента Qdrant
client = QdrantClient(host='localhost', port=6333)

# Создание коллекции в Qdrant
client.recreate_collection(
    collection_name='my_collection',
    vector_size=vectors.shape[1]  # Размерность векторов
)

# Загрузка векторов в Qdrant
for i, vector in enumerate(vectors):
    client.upsert(
        collection_name='my_collection',
        points=[
            {
                'id': i,
                'vector': vector.tolist(),
                'payload': {'text': hierarchical_texts[i]}
            }
        ]
    )

print("Векторы успешно загружены в Qdrant!")
