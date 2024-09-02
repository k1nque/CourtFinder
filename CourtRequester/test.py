from court_requester import make_find_courts_request
import asyncio

# async def main():
#     sugg = await suggest("Учителей 8")
#     print(*sugg, sep="\n")
# asyncio.run(main())
    # 587a5c65-1fb6-4444-96ae-f3cde33daf5a -- House fias ID

# print(make_suggestion_address_request("Учителей 8").items(), sep="\n")

# data = {
#         "query": "Гурзуфская 5",
#         "from_bound": {"value": "region"},
#         "to_bound": {"value": "house"},
#     }

print(make_find_courts_request("587a5c65-1fb6-4444-96ae-f3cde33daf5a"))

# import json

# s = json.dumps(data, ensure_ascii=False)

# b = bytes(s, encoding='utf-8')
# print(s, b, sep='\n')