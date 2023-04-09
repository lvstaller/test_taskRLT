from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from test_data import input_example, output_example
from config import mongoclient_uri


async def aggregate_data(collection, dt_from, dt_upto, group_type):

    # преобразуем входные данные в формат datetime
    dt_from = datetime.fromisoformat(dt_from)
    dt_upto = datetime.fromisoformat(dt_upto)

    # задаем параметры для группировки
    group_by = {}
    if group_type == "hour":
        group_by = {"$dateToString": {"format": "%Y-%m-%dT%H:00:00", "date": "$dt"}}
    elif group_type == "day":
        group_by = {"$dateToString": {"format": "%Y-%m-%dT00:00:00", "date": "$dt"}}
    elif group_type == "month":
        group_by = {"$dateToString": {"format": "%Y-%m-01T00:00:00", "date": "$dt"}}

    # формируем запрос на агрегацию данных
    pipeline = [
        {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
        {"$group": {"_id": group_by, "count": {"$sum": "$value"}}},
        {"$sort": {"_id": 1}},
    ]
    # выполняем запрос и получаем результат
    cursor = collection.aggregate(pipeline=pipeline)
    results = await cursor.to_list(length=1000)
    dataset = []
    labels = []
    # формируем подписи
    if group_type == "hour":
        current_time = dt_from
        while current_time <= dt_upto:
            labels.append(current_time.strftime("%Y-%m-%dT%H:00:00"))
            current_time += timedelta(hours=1)
    elif group_type == "day":
        current_day = dt_from.date()
        while current_day <= dt_upto.date():
            labels.append(current_day.strftime("%Y-%m-%dT%H:00:00"))
            current_day += timedelta(days=1)
    elif group_type == "month":
        current_month = datetime(dt_from.year, dt_from.month, 1)
        while current_month <= dt_upto:

            labels.append(current_month.strftime("%Y-%m-%dT%H:00:00"))
            current_month = datetime(
                current_month.year + (current_month.month // 12),
                ((current_month.month % 12) + 1),
                1,
            )
    for label in labels:
        count = None
        for item in results:
            if label == item["_id"]:
                count = item["count"]
        if count != None:
            dataset.append(count)
        else:
            dataset.append(0)

    # формируем и возвращаем ответ
    return {"dataset": dataset, "labels": labels}


if __name__ == "__main__":
    client = AsyncIOMotorClient(mongoclient_uri)
    db = client.sampleDB
    collection = db.sample_collection
    for i in range(len(input_example)):
        input_data = input_example[i]
        output_data = aggregate_data(
            collection,
            input_data["dt_from"],
            input_data["dt_upto"],
            input_data["group_type"],
        )
        print(output_data)
        if output_data == output_example[i]:
            print(f"Тест {i}- Пройден успешно")
        else:
            print(f"Тест {i}- Ошибка")

            for x in range(len(output_data["dataset"])):
                if output_data["dataset"][x] != output_example[i]["dataset"][x]:
                    print(x)
                    print(
                        output_data["dataset"][x], " ", output_example[i]["dataset"][x]
                    )
                if output_data["labels"][x] != output_example[i]["labels"][x]:
                    print(x)
                    print(output_data["labels"][x], " ", output_example[i]["labels"][x])
