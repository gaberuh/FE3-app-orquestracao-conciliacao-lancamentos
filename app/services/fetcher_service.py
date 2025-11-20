import pandas as pd
from app.core.config import logger

def fetch_groups_from_csv(path: str):
    logger.info(f"Lendo CSV agrupado: {path}")

    df = pd.read_csv(path, dtype=str)

    # Convertendo qtd para int
    df["qtd"] = df["qtd"].astype(int)

    # Agrupamento completo por todas as chaves
    grouped = (
        df.groupby(["empresa", "conta_contabil", "tabela_origem", "particao"], as_index=False)
          .agg({"qtd": "sum"})
    )

    results = grouped.to_dict(orient="records")

    logger.info(f"Total de grupos consolidados: {len(results)}")

    return results



# ================================
# Athena real para o futuro
# ================================

def fetch_groups_from_athena(query: str, athena_client, output_s3: str):
    """
    Mantido como referência para futura implementação real.
    """
    response = athena_client.start_query_execution(
        QueryString=query,
        ResultConfiguration={"OutputLocation": output_s3},
    )

    execution_id = response["QueryExecutionId"]

    # Você fará polling até SUCCEEDED...
    # Depois consumirá os resultados com get_query_results()
    # e mapeará empresa, conta_contabil, qtd.

    raise NotImplementedError(
        "Integração real com Athena ainda não habilitada."
    )
