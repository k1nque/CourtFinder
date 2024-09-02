import requests
# from bs4 import BeautifulSoup
from json import loads, dump
from aiohttp import ClientSession
from dadata import DadataAsync
from settings import settings


async def suggest(addr: str):
    async with DadataAsync(
        token=settings.TOKEN,
        secret=settings.SECRET
    ) as session:
        suggests = await session.suggest("address", addr)
        # return suggests
        return [{
            "address": el["value"],
            "fias": el["data"]["house_fias_id"]
        } for el in suggests]

def make_suggestion_address_request(suggestionAdress: str) -> dict[str, str]:

    URL = "https://sudrf.ru/suggestions/api/4_1/rs/suggest/address"

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru,en;q=0.9,ka;q=0.8",
        "Connection": "keep-alive",
        "Content-Length": "95",
        "Cookie": "PHPSESSID=uaa9lvsq33ics5pr85b0s83aj1",
        "Host": "sudrf.ru",
        "Origin": "https://sudrf.ru",
        "Referer": "https://sudrf.ru/index.php?id=300&var=true",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36",
        "content-type": "application/json",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
    }

    data = {
        "query": suggestionAdress,
        "from_bound": {"value": "region"},
        "to_bound": {"value": "house"},
    }
    
    # async with ClientSession() as session:
    #     async with session.post(url=URL, data=data, headers=headers) as r:
    #         content = await r.content.read()
    #         print(content)
    r = requests.post(URL, headers=headers, json=data)
    with open('out.json', 'w', encoding='utf-8') as f:
        dump([el for el in loads(r.content)['suggestions']], f, ensure_ascii=False)

    return {
        el["value"]: el["data"]["house_fias_id"]
        for el in loads(r.content)["suggestions"]
        if el["data"]["house_fias_id"] is not None
    }


def make_find_courts_request(id):
    URL = f"https://sudrf.ru/api.php?opt=court_list&action=getCourtListByFiasCode&fiasId={id}"
    print(URL)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36"}
    r = requests.get(URL, headers=headers)
    data = loads(r.text)['list']
    # return data # DEBUG
    return [{
        'NAME': el['ZNACHATR'],
        'ADDRESS': el['ADDRESS'],
        'LINK': el['PRIM']
    } for el in data]
    
    
async def find_courts(fias):
    URL=f"https://sudrf.ru/api.php?opt=court_list&action=getCourtListByFiasCode&fiasId={fias}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36"}

    async with ClientSession() as session:
        async with session.get(
            url=URL,
            headers=headers
        ) as r:
            data = await r.text()
            data = loads(data)
            print(type(data))
            # return data
            return [{
                'NAME': el['ZNACHATR'],
                'ADDRESS': el['ADDRESS'],
                'LINK': el['PRIM']
            } for el in data["list"]]
    

# addresses = asyncio.run(make_suggestion_address_request("Гурзуфская 5"))
# print(addresses)
# print(makeFindCourtsRequest(addresses['г Екатеринбург, ул Гурзуфская, д 5']))

# for address, id in addresses.items():
#     print(address)
#     print(makeFindCourtsRequest(id))
#     break
