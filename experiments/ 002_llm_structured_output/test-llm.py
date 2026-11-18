import time
from typing import List
import psutil
from pydantic import BaseModel, Field

from llama_cpp import Llama
import instructor
import outlines

# путь к скачанному файлу модели GGUF
MODEL_PATH = "qwen2.5-3b-instruct-q4_k_m.gguf"

# схема с json
class MedicalProtocol(BaseModel):
    chief_complaint: str = Field(description="Главная жалоба пациента")
    duration: str = Field(description="Длительность симптомов")
    symptoms: List[str] = Field(description="Список всех симптомов")
    medications: List[str] = Field(description="Принимаемые лекарства и дозировка")
    allergies: List[str] = Field(description="Аллергические реакции")
    diagnosis: str = Field(description="Предварительный диагноз")
    recommendations: List[str] = Field(description="Рекомендации и назначения врача")


# Тестовый диалог (твой кейс с ОРВИ и парацетамолом)
DIALOG_TEXT = """
Врач: Здравствуйте, на что жалуетесь?
Пациент: Добрый день. Три дня уже температура 38.5, сухой кашель, насморк и сильная слабость.
Врач: Что-то принимали уже? Аллергия на лекарства есть?
Пациент: Вчера вечером выпил парацетамол 500 мг. На пенициллин у меня сыпь.
Врач: Понятно, это ОРВИ, легкое течение. Пейте больше воды, парацетамол принимайте при температуре выше 38.5. Ко мне на прием через три дня.
"""

PROMPT = f"Извлеки медицинские данные из диалога строго по схеме JSON.\n\nДиалог:\n{DIALOG_TEXT}"


def get_ram_gb():
    process = psutil.Process()
    return process.memory_info().rss / (1024 ** 3)


def test_gbnf(llm: Llama):
    print("\n--- 1. Тест: llama-cpp + GBNF (JSON Schema) ---")
    schema = MedicalProtocol.model_json_schema()

    t0 = time.perf_counter()
    response = llm.create_chat_completion(
        messages=[{"role": "user", "content": PROMPT}],
        response_format={"type": "json_object", "schema": schema},
        temperature=0.1,
    )
    elapsed = time.perf_counter() - t0

    raw_json = response["choices"][0]["message"]["content"]
    tokens = response["usage"]["completion_tokens"]
    speed = tokens / elapsed

    try:
        parsed = MedicalProtocol.model_validate_json(raw_json)
        valid = True
    except Exception as e:
        parsed = str(e)
        valid = False

    print(f"Валидный JSON: {valid} | Время: {elapsed:.2f} сек | Скорость: {speed:.1f} tok/s | RAM: {get_ram_gb():.2f} ГБ")
    print("Результат:", parsed)


def test_instructor(llm: Llama):
    print("\n--- 2. Тест: llama-cpp + instructor ---")
    client = instructor.from_llama_cpp(llm)

    t0 = time.perf_counter()
    try:
        parsed = client.chat.completions.create(
            messages=[{"role": "user", "content": PROMPT}],
            response_model=MedicalProtocol,
            max_retries=2,
            temperature=0.1,
        )
        valid = True
    except Exception as e:
        parsed = str(e)
        valid = False
    elapsed = time.perf_counter() - t0

    print(f"Валидный JSON: {valid} | Общее время (с учетом retry): {elapsed:.2f} сек | RAM: {get_ram_gb():.2f} ГБ")
    print("Результат:", parsed)


def test_outlines(model_path: str):
    print("\n--- 3. Тест: llama-cpp + outlines ---")
    # Outlines использует свою обертку поверх llama-cpp
    model = outlines.models.llamacpp(model_path, n_ctx=2048)
    generator = outlines.generate.json(model, MedicalProtocol)

    t0 = time.perf_counter()
    try:
        parsed = generator(PROMPT)
        valid = True
    except Exception as e:
        parsed = str(e)
        valid = False
    elapsed = time.perf_counter() - t0

    print(f"Валидный JSON: {valid} | Общее время: {elapsed:.2f} сек | RAM: {get_ram_gb():.2f} ГБ")
    print("Результат:", parsed)


if __name__ == "__main__":
    print("Загрузка модели Qwen 2.5 3B...")
    base_llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_gpu_layers=-1,  # -1 выгрузит все слои на GPU (если есть), на CPU просто проигнорируется
        verbose=False,
    )

    test_gbnf(base_llm)
    test_instructor(base_llm)

    # Освобождаем память перед загрузкой модели через outlines
    del base_llm
    test_outlines(MODEL_PATH)
