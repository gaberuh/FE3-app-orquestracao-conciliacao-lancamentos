from app.services.packer import pack_groups

def test_basic_pack():
    items = [
        {"empresa": "A", "conta_contabil": "1", "qtd": 400_000},
        {"empresa": "A", "conta_contabil": "2", "qtd": 300_000},
        {"empresa": "B", "conta_contabil": "3", "qtd": 200_000},
        {"empresa": "B", "conta_contabil": "4", "qtd": 800_000},
    ]

    result = pack_groups(items, 1_000_000)

    assert len(result["oversized"]) == 0
    assert len(result["bins"]) == 2
