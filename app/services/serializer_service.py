import uuid
from collections import defaultdict
from app.core.config import logger

class Serializer:
    """
    Serializa os bins gerados pelo BinPacker para um formato pronto
    para Spark e, opcionalmente, para JSON.
    """

    def __init__(self, bins: list):
        self.bins = bins

    def to_spark_json(self) -> list:
        """
        Converte a lista de bins em um formato otimizado para Spark.
        Estrutura final:
        [
            {
                "id": <uuid>,
                "total_qtd": <soma de todas as contas>,
                "tabelas": [
                    {
                        "tabela_origem": <nome>,
                        "contas": [
                            {
                                "empresa": <empresa>,
                                "conta_contabil": <conta>,
                                "detalhes": [
                                    {"particao": <particao>, "qtd": <qtd>},
                                    ...
                                ]
                            },
                            ...
                        ]
                    },
                    ...
                ]
            },
            ...
        ]
        """
        spark_bins = []

        for b in self.bins:
            bin_dict = {
                "id": str(uuid.uuid4()),
                "total_qtd": b.get("total_qtd", 0),
                "tabelas": []
            }

            # Vamos reconstruir as contas a partir de 'detalhes'
            # Agrupamos por tabela_origem
            tabela_map = defaultdict(list)  # tabela_origem -> lista de contas

            for detalhe in b.get("detalhes", []):
                tabela = detalhe["tabela_origem"]
                empresa = detalhe["empresa"]
                conta_contabil = detalhe["conta_contabil"]
                particao = detalhe["particao"]
                qtd = detalhe["qtd"]

                # Procura se já existe uma conta com essa empresa+conta_contabil na tabela
                contas_list = tabela_map[tabela]
                conta_entry = next(
                    (c for c in contas_list if c["empresa"] == empresa and c["conta_contabil"] == conta_contabil),
                    None
                )

                detalhe_dict = {"particao": particao, "qtd": qtd}

                if conta_entry:
                    conta_entry["detalhes"].append(detalhe_dict)
                else:
                    contas_list.append({
                        "empresa": empresa,
                        "conta_contabil": conta_contabil,
                        "detalhes": [detalhe_dict]
                    })

            # Constrói a lista final de tabelas
            for tabela_origem, contas in tabela_map.items():
                bin_dict["tabelas"].append({
                    "tabela_origem": tabela_origem,
                    "contas": contas
                })

            spark_bins.append(bin_dict)

        logger.info(f"Total de bins serializados para Spark: {len(spark_bins)}")
        return spark_bins
