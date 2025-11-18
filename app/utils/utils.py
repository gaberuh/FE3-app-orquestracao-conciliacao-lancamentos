import json
import os
from app.core.config import logger  # usando imports corretos

def ensure_out_dir():
    if not os.path.exists("out"):
        os.makedirs("out")
        logger.info("Criada pasta out/")

def save_json(path, data):
    ensure_out_dir()
    # Garantir que todas as strings sejam salvas sem alterar
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info(f"Arquivo salvo em {path}")
