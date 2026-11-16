import asyncio

from app.pipeline.fetcher import fetch_catalog


async def main():
    records = await fetch_catalog()
    print(f"Fetched {len(records)} records from Space-Track.")

    for record in records[:5]:  # Print the first 5 records for demonstration
        print(
            f"NORAD_CAT_ID: {record.NORAD_CAT_ID}, OBJECT_NAME: {record.OBJECT_NAME}, EPOCH: {record.EPOCH}"
        )


if __name__ == "__main__":
    asyncio.run(main())
