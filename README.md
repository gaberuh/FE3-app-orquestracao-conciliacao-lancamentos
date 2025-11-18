# conciliacao-binner

Este projeto implementa uma solução de agrupamento de lotes (bin packing)
para agrupar registros de conciliação retornados via Athena.

Cada item é uma linha com:
- empresa
- conta_contabil
- qtd

Regra:
- se qtd > limite (ex.: 1.000.000), vira um grupo individual
- senão: agrupamos itens até não exceder o limite

## Rodar localmente

1. Criar ambiente
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

2. Criar .env
cp .env.example .env

3. Rodar exemplo local (CSV em examples/)
python app/main.py --input examples/sample_input.csv --capacity 1000000

O resultado será salvo em:
out/bins_result.json

## Estrutura

/app
  core/         → config boto3, Athena stub, SQS writer
  services/     → lógica de bin packing
  main.py       → fluxo principal

No futuro: substituir stub Athena por chamada real.

