from typing import List
import uuid6
from app.core.config import logger


class BinPacker:
    def __init__(self, capacity_limit: int):
        self.capacity_limit = capacity_limit

    def generate_uuid7(self) -> str:
        """Gera um UUIDv7"""
        return str(uuid6.uuid7())

    def pack(self, items: List[dict]) -> List[dict]:
        """
        items: [{empresa, conta_contabil, tabela_origem, particao, qtd}]
        Retorna lista de bins
        """
        bins = []

        # Agrupa por empresa+conta_contabil
        grupos = {}
        for item in items:
            key = (item["empresa"], item["conta_contabil"])
            if key not in grupos:
                grupos[key] = []
            grupos[key].append(item)

        # Itera sobre cada grupo
        for (empresa, conta), detalhes in grupos.items():
            total_qtd = sum(d["qtd"] for d in detalhes)

            # Cria um bin próprio se ultrapassa capacity_limit
            if total_qtd > self.capacity_limit:
                bins.append({
                    "id": self.generate_uuid7(),
                    "total_qtd": total_qtd,
                    "detalhes": detalhes
                })
                continue

            # Tenta colocar em algum bin existente que não ultrapasse capacity
            placed = False
            for b in bins:
                if b["total_qtd"] + total_qtd <= self.capacity_limit:
                    b["total_qtd"] += total_qtd
                    b.setdefault("detalhes", []).extend(detalhes)
                    placed = True
                    break

            if not placed:
                bins.append({
                    "id": self.generate_uuid7(),
                    "total_qtd": total_qtd,
                    "detalhes": detalhes
                })

        return bins
