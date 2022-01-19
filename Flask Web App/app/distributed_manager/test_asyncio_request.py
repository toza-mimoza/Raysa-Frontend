import asyncio
import aiohttp

results = []


async def async_send_request_all(urls):

    # overwrite for testing purposes

    try:
        async with aiohttp.ClientSession() as session:
            print("Making tasks...")
            tasks = []
            for url in urls:
                tasks.append(session.get(url, ssl=False))
            print("Awaiting tasks...")
            responses = await asyncio.gather(*tasks)
            print("Responses awaited...")
            for response in responses:
                results.append(await response.json(content_type=None))
                print("Appending results to DS manager...")
            pass

    except Exception as e:
        raise
    pass


def send_request_all(urls, endpoints=None, msg=None):
    asyncio.run(async_send_request_all(urls))


if __name__ == "__main__":
    urls = ["https://jsonplaceholder.typicode.com/todos/1"]
    send_request_all(urls)
    print(results)
