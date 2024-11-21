import asyncio

from config import data_manager, mongo_service, pg_service


async def prepare_databases(*services):
    tasks = [asyncio.create_task(service.prepare_database()) for service in services]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(data_manager.clear_directory_with_data())
    asyncio.run(data_manager.save_initial_data_to_csv())
    asyncio.run(prepare_databases(pg_service, mongo_service))
