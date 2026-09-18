import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv

load_dotenv()

client = QdrantClient(
    url = os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
    timeout=60
)

COLLECTION_NAME = "pyq_Collection"


def create_collection():
    try:
        collections = client.get_collections().collections
    except Exception as exc:
        print(f"⚠️ Qdrant unavailable during startup; skipping collection initialization: {exc}")
        return False

    collection_names = [c.name for c in collections]

    if COLLECTION_NAME in collection_names:
        try:
            collection_info = client.get_collection(collection_name=COLLECTION_NAME)
            if collection_info.config.params.vectors.size != 3072:
                print(f"Dimension mismatch in {COLLECTION_NAME}. Deleting and recreating...")
                client.delete_collection(collection_name=COLLECTION_NAME)
                collection_names.remove(COLLECTION_NAME)
        except Exception as exc:
            print(f"⚠️ Qdrant collection check failed: {exc}")
            return False

    if COLLECTION_NAME not in collection_names:
        try:
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=3072,
                    distance=Distance.COSINE
                ),
            )
        except Exception as exc:
            print(f"⚠️ Qdrant collection creation failed: {exc}")
            return False

    return True


def insert_vector(question_id, vector, payload):
    if not create_collection():
        return False

    try:
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=question_id,
                    vector=vector,
                    payload=payload,
                )
            ]
        )
        return True
    except Exception as exc:
        print(f"⚠️ Qdrant insert failed: {exc}")
        return False


def search_vector(query_vector, limit=5, offset=0):
    if not create_collection():
        return []

    try:
        response = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=limit,
            offset=offset
        )
        return [(point.id, point.score) for point in response.points]
    except Exception as exc:
        print(f"⚠️ Qdrant search failed: {exc}")
        return []

