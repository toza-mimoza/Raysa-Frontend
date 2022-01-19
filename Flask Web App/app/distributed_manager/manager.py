# manager for distributed system
# sends commands to nodes for:
#   triggering training of bots
#   file extraction (logs)
#   on the other end there is an HTTP RESTful API for offering files to download
#   SECURITY: implement token based authentication for RESTful service (API keys)
# #

import asyncio
import aiohttp
import concurrent
import logging
import sys
from typing import List
from app.util.constants import TIMEOUT

log = logging.getLogger(__name__)


# def create_conversation(app, db):
#     db.init_app(app)
#     session_uid = get_or_set_session_uid(session)
#
#     with app.app_context():
#         Conversations.create(session_uid=session_uid)


class DistributedManager:

    bot_base_urls = []
    results = []
    loop = asyncio.new_event_loop()

    def __init__(self, bot_base_urls: List[str]):
        self.bot_base_urls = bot_base_urls
        pass

    async def async_send_request_all(urls):

        # overwrite for testing purposes
        # urls = [
        #     "https://jsonplaceholder.typicode.com/todos/1",
        # ]
        try:
            async with aiohttp.ClientSession() as session:
                print("Making tasks...")
                tasks = []
                for url in urls:
                    tasks.append(session.get(url, timeout=TIMEOUT, ssl=False))
                print("Awaiting tasks...")
                responses = await asyncio.gather(*tasks)
                print("Response(s) awaited...")
                for response in responses:
                    DistributedManager.results.append(
                        await response.json(content_type=None)
                    )
                    print("Appending result to DS manager...")
                    print(f"Response: {DistributedManager.results}")
                pass
        except concurrent.futures._base.TimeoutError as timeout_error:
            type_, value_, traceback_ = sys.exc_info()
            # log.exception(f"{type_}: {value_}")
            log.exception(
                f"<concurrent.futures._base.TimeoutError > Timeout error: {timeout_error}"
            )
            pass
        except Exception as e:
            type_, value_, traceback_ = sys.exc_info()
            log.exception(f"{type_}: {value_}")
            log.exception(f"<aiohttp.ClientConnectorError> Connection error: {e}")
            raise
        pass

    def send_request_all(urls, endpoints=None, msg=None):
        if DistributedManager.bot_base_urls:
            DistributedManager.loop.run_until_complete(
                DistributedManager.async_send_request_all(urls)
            )

    def get_best_matched_response(self):
        if DistributedManager.results:
            pass

    def clear():
        DistributedManager.bot_base_urls = []
        DistributedManager.results = []
        pass
