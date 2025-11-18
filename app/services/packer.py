from typing import List, Dict
import uuid6

def generate_uuid7():
    """
    Gera um UUIDv7
    """
    return str(uuid6.uuid7())

def pack_groups(items: List[dict], capacity: int):
    """
    items: [{empresa, conta_contabil, qtd}]
    capacity: limite (ex. 1.000.000)

    Retorna:
    {
        "bins": [...],
        "oversized": [...]
    }
    """

    oversized = []
    normal_items = []

    # separa oversized
    for item in items:
        if item["qtd"] > capacity:
            oversized.append({
                "id": generate_uuid7(),
                "total": item["qtd"],
                "items": [item],
                "oversized": True
            })
        else:
            normal_items.append(item)

    # ordena desc para FFD
    normal_items.sort(key=lambda x: x["qtd"], reverse=True)

    bins = []

    for item in normal_items:
        placed = False
        for b in bins:
            if b["total"] + item["qtd"] <= capacity:
                b["items"].append(item)
                b["total"] += item["qtd"]
                placed = True
                break

        if not placed:
            bins.append({
                "id": generate_uuid7(),
                "total": item["qtd"],
                "items": [item],
                "oversized": False
            })

    return {
        "bins": bins,
        "oversized": oversized
    }
