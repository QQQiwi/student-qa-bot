from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import os
import sys
from time import time
from datetime import datetime
import re

def print_progress(step, message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {step}: {message}", flush=True)

def display_results(results):
    """Отображает найденные результаты с их релевантностью"""
    total_score = sum(r.score for r in results)
    
    print("\nНайденные фрагменты:")
    print("=" * 80)
    for i, result in enumerate(results, 1):
        relative_score = (result.score / total_score) * 100
        print(f"\nФрагмент {i} (релевантность: {relative_score:.1f}%):")
        print("-" * 40)
        print(result.payload['text'])
    print("=" * 80)

def extract_key_phrases(text):
    """Извлекает ключевые фразы из текста для последующей проверки"""
    # Удаляем пунктуацию и приводим к нижнему регистру
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    # Разбиваем на слова и фильтруем короткие слова
    words = [w for w in text.split() if len(w) > 3]
    # Создаем фразы из последовательных слов
    phrases = [' '.join(words[i:i+3]) for i in range(len(words)-2)]
    return set(words + phrases)

def validate_response(answer, context_phrases):
    """Проверяет, что ответ основан на контексте"""
    answer_phrases = extract_key_phrases(answer)
    # Проверяем, что хотя бы 30% фраз из ответа есть в контексте
    common_phrases = answer_phrases.intersection(context_phrases)
    if len(answer_phrases) == 0:
        return False
    ratio = len(common_phrases) / len(answer_phrases)
    return ratio >= 0.3

def format_context(results):
    """Форматирует контекст для модели"""
    contexts = []
    total_score = sum(r.score for r in results)
    
    for i, r in enumerate(results, 1):
        text = r.payload['text']
        score = r.score
        relative_score = (score / total_score) * 100
        
        if relative_score >= 10:  # Игнорируем нерелевантные результаты
            context_entry = f"РАЗДЕЛ {i}:\n{text}"
            contexts.append(context_entry)
            
    return "\n\n".join(contexts)

try:
    start_time = time()
    print_progress("START", "Инициализация системы")

    # GPU setup
    os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print_progress("SYSTEM", f"Используется {device.upper()}")
    
    if device == "cuda":
        torch.cuda.empty_cache()
    
    # Подключение к БД
    print_progress("SYSTEM", "Подключение к базе данных...")
    client = QdrantClient(host='localhost', port=6333)
    
    # Загрузка модели для векторизации
    print_progress("SYSTEM", "Загрузка модели эмбеддингов...")
    sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
    sentence_model = sentence_model.to(device)

    # Получение запроса
    query_text = input('\nВаш вопрос: ').strip()
    if not query_text:
        print_progress("ERROR", "Пожалуйста, задайте вопрос")
        sys.exit(1)

    # Векторный поиск
    print_progress("PROCESS", "Поиск релевантной информации...")
    with torch.no_grad():
        query_vector = sentence_model.encode(query_text)

    results = client.search(
        collection_name="my_collection",
        query_vector=query_vector.tolist(),
        limit=5,
        score_threshold=0.2
    )

    if not results:
        print_progress("RESULT", "Не найдено релевантной информации")
        sys.exit(0)

    # Отображаем найденные вектора
    print_progress("PROCESS", f"Найдено {len(results)} релевантных фрагментов")
    display_results(results)

    # Подготовка контекста и ключевых фраз
    context = format_context(results)
    context_phrases = extract_key_phrases(context)

    # Инициализация генеративной модели
    print_progress("SYSTEM", "Загрузка языковой модели...")
    try:
        tokenizer = AutoTokenizer.from_pretrained("ai-forever/rugpt3small_based_on_gpt2")
        model = pipeline(
            "text-generation",
            model="ai-forever/rugpt3small_based_on_gpt2",
            tokenizer=tokenizer,
            device=0 if device == "cuda" else -1
        )

        system_prompt = """### Инструкция
Ты - ассистент для ответов на вопросы. Твоя задача - работать ТОЛЬКО с предоставленной информацией.
Не используй свои знания, опирайся ТОЛЬКО на предоставленный контекст.
Формат ответа:
1. Кратко суммируй основную информацию
2. Если есть конкретные детали - укажи их
3. Если информации недостаточно - так и скажи

### Требования
- Не добавляй информацию, которой нет в контексте
- Используй простой и понятный язык
- Будь краток и точен
- Указывай номера разделов, откуда берешь информацию"""

        prompt = f"""{system_prompt}

### Контекст:
{context}

### Вопрос:
{query_text}

### Ответ (строго из контекста выше):"""

        print_progress("PROCESS", "Генерация ответа...")
        
        # Попытки генерации с валидацией
        max_attempts = 3
        valid_response = False
        
        for attempt in range(max_attempts):
            with torch.no_grad():
                response = model(
                    prompt,
                    max_new_tokens=200,
                    temperature=0.3,
                    top_p=0.75,
                    top_k=30,
                    num_return_sequences=1,
                    do_sample=True,
                    no_repeat_ngram_size=3,
                    repetition_penalty=1.2,
                    pad_token_id=tokenizer.eos_token_id
                )

            # Извлекаем ответ
            full_text = response[0]["generated_text"]
            answer = full_text[len(prompt):].strip()
            
            # Проверяем валидность ответа
            if validate_response(answer, context_phrases):
                valid_response = True
                break
            else:
                print_progress("PROCESS", f"Попытка {attempt + 1}: ответ не соответствует контексту, повторяем...")

        if not valid_response:
            print_progress("RESULT", "Не удалось сгенерировать ответ на основе контекста")
            print("\nПожалуйста, используйте информацию из показанных выше фрагментов")
        else:
            print("\nСгенерированный ответ:")
            print("=" * 80)
            print(answer)
            print("=" * 80)

        total_time = time() - start_time
        print_progress("COMPLETE", f"Обработка заняла {total_time:.1f} секунд")

    except RuntimeError as e:
        if "out of memory" in str(e):
            print_progress("ERROR", "Недостаточно GPU памяти, переключаюсь на CPU...")
            torch.cuda.empty_cache()
            model.device = -1
            response = model(prompt, max_new_tokens=200, temperature=0.3)
            answer = response[0]["generated_text"][len(prompt):].strip()
            print("\nОтвет (сгенерирован на CPU):")
            print("=" * 80)
            print(answer)
            print("=" * 80)
        else:
            raise e

except Exception as e:
    print_progress("ERROR", str(e))
    if hasattr(e, '__traceback__'):
        import traceback
        traceback.print_exc()