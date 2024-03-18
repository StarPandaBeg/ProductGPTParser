from g4f.client import Client
from g4f.providers.retry_provider import RetryProviderError
from config import config
from util import *
import json

SYSTEM_PROMPT = "[Output only JSON][no prose]Ты - помощник для парсинга JSON-данных из постов в сообществах. Твоя задача - анализировать каждое мое присланное сообщение и вытягивать из него максимум информации в JSON-формат. Ты должен достать по возможности наименование товара, цену, характеристики, ключевые слова, номер телефона. Формат - JSON со следующими полями: name, description, keywords, price, contact, attributes. Все указанные поля должны быть. Не пиши никаких дополнительных сообщений, отвечай только JSON-содержимым. Не форматируй ответ. Если ты видишь несколько товаров - присылай массив с данными о каждом товаре. Цену выводи как число без сокращений: например '10тыс.р' -> '10000'"
_gpt = Client()


def parse(item):
    i = 0.0
    while i < 3:
        try:
            response = run_gpt(item['text'])
            if (response == None):
                continue
            parsed = parse_response(response)
            return True, process_response(item, parsed)
        except RetryProviderError as er1:
            continue
        except Exception as e:
            i += 1
            continue
    return False, item


def run_gpt(text):
    # prev_messages = []
    # for p in prev:
    #     prev_messages.append({"role": "assistant", "content": p})
    #     prev_messages.append(
    #         {"role": "client", "content": "Твой ответ оборван, продолжай"})

    gpt_response = _gpt.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "client", "content": text}
        ]  # + prev_messages
    )

    if (gpt_response.choices[0].finish_reason == "stop"):
        return gpt_response.choices[0].message.content
    return None


def parse_response(text):
    text = trim_json(text).replace("\n", "")
    data = json.loads(text)
    return data


def process_response(item, response):
    if (isinstance(response, list)):
        processed = [process_response(item, i) for i in response]
        return processed

    if not check_keys(response, ["name", "price"]):
        raise Exception("Not all required keys are presented")

    if (isinstance(response["price"], str)):
        response["price"] = filter_int(response["price"])
    response["post_date"] = item["date"]
    response["post_attachments"] = item["attachments"]
    response["post_id"] = item["id"]
    response["post_owner_id"] = item["owner_id"]
    return response
