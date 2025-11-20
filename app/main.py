import os
import json
from app.core.config import logger, settings
from app.services.fetcher_service import fetch_groups_from_csv
from app.services.packer_service import BinPacker
from app.services.serializer_service import Serializer


def main():
    logger.info("Iniciando processamento de conciliação...")

    # Carrega os grupos do CSV
    items = fetch_groups_from_csv(settings.INPUT_FILE)
    logger.info(f"Total de grupos carregados: {len(items)}")

    # Prepara o bin packer com o limite definido nas configs
    packer = BinPacker(capacity_limit=settings.CAPACITY_LIMIT)
    bins = packer.pack(items)
    logger.info(f"Total de bins gerados: {len(bins)}")

    # Serializa os bins para formato pronto para Spark
    serializer = Serializer(bins)
    spark_ready = serializer.to_spark_json()

    # Cria pasta de saída se não existir
    output_dir = "out"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "bins_spark.json")

    # Salva JSON final
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(spark_ready, f, indent=2, ensure_ascii=False)

    logger.info(f"JSON gerado em: {output_path}")


if __name__ == "__main__":
    main()
