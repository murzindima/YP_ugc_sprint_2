import asyncio

from config import mongo_service, pg_service


async def run_operations(*services):
    tasks = [asyncio.create_task(service.run()) for service in services]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(run_operations(pg_service, mongo_service))
