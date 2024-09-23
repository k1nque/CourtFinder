from aiohttp import ClientSession
from json import loads

from settings import settings

import asyncio


async def get_suggestions(address: str):
    # print(f"http://0.0.0.0:8000/suggestion/{address}")
    async with ClientSession() as session:
        async with session.get(
            f"{settings.get_api_url()}suggestion?addr={address}"
            # f"http://0.0.0.0:8000/suggestion?addr={address}"
        ) as r:
            text = await r.text()
            data = loads(text)
            return data
        
        
async def get_courts(fias: str):
    async with ClientSession() as session:
        try:
            r = await session.get(
                f"{settings.get_api_url()}find_courts?fias={fias}"
                # f"http://0.0.0.0:8000/find_courts?fias={fias}"
            )
        except Exception as e:
            pass
        while r.status != 200:
            try:
                r = await session.get(
                    f"{settings.get_api_url()}find_courts?fias={fias}"
                    # f"http://0.0.0.0:8000/find_courts?fias={fias}"
                )
            except Exception as e:
                pass
        text = await r.text()
        data = loads(text)
        return data
    
    
async def get_arbitration_subject_court(region: str):
    print(region)
    async with ClientSession() as session:
        r = await session.get(
            f"{settings.get_api_url()}get_arbitration_subject_court?region={region}"
            # f"http://0.0.0.0:8000/get_arbitration_subject_court?region={region}"
        )
        while r.status != 200:
            r = await session.get(
                f"{settings.get_api_url()}get_arbitration_subject_court?region={region}"
                # f"http://0.0.0.0:8000/get_arbitration_subject_court?region={region}"
            )
        text = await r.text()
        print(text)
        data = loads(text)
        return data
       
    
       
# async def main():
#     data = await get_suggestions("Учителей 8") 
#     fias = data[1]["fias"]
#     print(fias)
#     data = await get_courts(fias)  
#     print(data)
      
            
# if __name__ == "__main__":
#     asyncio.run(main())