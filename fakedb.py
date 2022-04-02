from decimal import Decimal

fake_db = {
    "motoboys": [
        {
            "id": 1,
            "nome": "Moto 1",
            "taxa": Decimal(2),
            "exclusivo": False,
            "loja_id": None,
            "pedidos_entregues": list(),
            "saldo":Decimal(0)
        },
        {
            "id": 2,
            "nome": "Moto 2",
            "taxa": Decimal(2),
            "exclusivo": False,
            "loja_id": None,
            "pedidos_entregues": list(),
            "saldo":Decimal(0)
        },
        {
            "id": 3,
            "nome": "Moto 3",
            "taxa": Decimal(2),
            "exclusivo": False,
            "loja_id": None,
            "pedidos_entregues": list(),
            "saldo":Decimal(0)
        },
        {
            "id": 4,
            "nome": "Moto 4",
            "taxa": Decimal(2),
            "exclusivo": True,
            "loja_id": 1,
            "pedidos_entregues": list(),
            "saldo":Decimal(0)
        },
        {
            "id": 5,
            "nome": "Moto 5",
            "taxa": Decimal(3),
            "exclusivo": False,
            "loja_id": None,
            "pedidos_entregues": list(),
            "saldo":Decimal(0)
        },
    ],
    "lojas": [
        {
            "id": 1,
            "nome": "Loja 1",
            "taxa": 5,
            "pedidos": [
                {"id": 1, "valor": Decimal(50)},
                {"id": 2, "valor": Decimal(50)},
                {"id": 3, "valor": Decimal(50)},
            ],
        },
        {
            "id": 2,
            "nome": "Loja 2",
            "taxa": 5,
            "pedidos": [
                {"id": 1, "valor": Decimal(50)},
                {"id": 2, "valor": Decimal(50)},
                {"id": 3, "valor": Decimal(50)},
                {"id": 4, "valor": Decimal(50)},
            ],
        },
        {
            "id": 3,
            "nome": "Loja 3",
            "taxa": 15,
            "pedidos": [
                {"id": 1, "valor": Decimal(50)},
                {"id": 2, "valor": Decimal(50)},
                {"id": 3, "valor": Decimal(100)},
            ],
        },
    ],
}
