import pandas as pd

def fetch_groups_from_csv(path: str):
    """
    Carrega dados no formato:
    empresa,conta_contabil,qtd
    """
    df = pd.read_csv(path)
    df["qtd"] = df["qtd"].astype(int)

    return df.to_dict(orient="records")


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
