from app.core.config import settings, logger
from app.core.db import fetch_groups_from_csv
from app.services.packer import pack_groups
from app.utils.utils import save_json


def main():
    logger.info("Iniciando processamento de conciliação...")

    logger.info(f"Lendo arquivo de entrada: {settings.INPUT_FILE}")
    items = fetch_groups_from_csv(settings.INPUT_FILE)

    logger.info(f"Total de grupos carregados: {len(items)}")
    logger.info(f"Iniciando bin packing com limite: {settings.CAPACITY_LIMIT}")

    result = pack_groups(items, settings.CAPACITY_LIMIT)

    save_json("out/bins_result.json", result)

    logger.info("Processo concluído com sucesso!")
    logger.info("Arquivo gerado em out/bins_result.json")


if __name__ == "__main__":
    main()
