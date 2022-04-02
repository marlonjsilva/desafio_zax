import argparse
from fakedb import fake_db
from decimal import *
import locale

# Configurar o número de casas decimais a ser utilizado pela classe Decimal 
getcontext().prec = 2

#Configurar o locale para pt_BR para formatação da moeda em BRL
locale.setlocale(locale.LC_ALL, "pt_BR.utf-8")

# Função lambda para formatar Decimal para BRL
formatar_valor = lambda x: locale.currency(x, grouping=True)


def pegar_todos_pedidos(inverter = True) -> list:
    """
    Esse método itera por todos os pedidos de todas as lojas e 
    cria uma lista de pedidos adicionando as informações loja_id e taxa
    junto ao pedido.
    
    Ex: {"loja_id":1,"taxa":5,"id":1,"valor":50}
    
    Por padrão retorna a lista em ordem inversa, dessa forma é possível
    filtrar pedidos para os motoboys que tenham exclusividade com lojas.

    :param inverter: Inverte a lista de pedidos, por padrão é True
    :type inverter: bool, optional
    :return: Uma lista de dicionários contendo todos os pedidos de todas as lojas
    :rtype: list
    """
    total_pedidos = list()
    for loja in fake_db["lojas"]:
        for pedido in loja["pedidos"]:
            total_pedidos.append(
                {"loja_id": loja["id"], "taxa": loja["taxa"], **pedido}
            )
    
    if inverter:
        total_pedidos.reverse()
        
    return total_pedidos


def calcular_taxas_pedidos(todos_pedidos:list) -> list:
    """Esse método calcula o valor adicional da taxa fixa de comissão que a loja paga
    ao motoboy por cada pedido entregue, e adiciona esse valor no atributo valor_taxa

    :param todos_pedidos: Lista de pedidos
    :type todos_pedidos: list
    :return: Lista de dicionário contendo os pedidos com o campo adicional
    :rtype:list
    """
    for pedido in todos_pedidos:
        pedido["valor_taxa"] = pedido["valor"] * pedido["taxa"] / 100
    return todos_pedidos


def filtrar_pedidos(lista_pedidos: list, loja_id: int) -> list:
    """Este método itera pela lista de pedidos e retorna uma lista de 
    indexes dos pedidos cujo valor seja igual ao parametro loja_id.

    :param lista_pedidos: Lista de pedidos  a ser pesquisada
    :type lista_pedidos: list
    :param loja_id: Id da loja a ser pesquisado na lista de pedidos
    :type loja_id: int
    :return: Lista contendo os indexes de posição dos pedidos na lista de pedidos
    :rtype: list
    """
    indexes = list()
    for index, pedido in enumerate(lista_pedidos):
        if pedido["loja_id"] == loja_id:
            indexes.append(index)
    return indexes


def distribuir_pedidos(total_pedidos: list, total_motoboys: list) -> list:
    """Esse método distribui a lista de pedidos entre a lista de motoboys,
    dando prioridade para os motoboys que tem exclusividade de entrega com
    as lojas.

    :param total_pedidos: Uma lista de dicionários contendo todos os pedidos
    :type total_pedidos: list
    :param total_motoboys: Uma lista de dicionários contendo todos os motoboys disponíveis
    :type total_motoboys: list
    :return: Uma lista de dicionário contendo todos motoboys os com pedidos realizados por eles.
    :rtype: list
    """
    while len(total_pedidos) > 1:
        for motoboy in total_motoboys:
            if motoboy["exclusivo"]:
                pedidos_prioritarios = filtrar_pedidos(
                    total_pedidos, motoboy["loja_id"]
                )
                if len(pedidos_prioritarios) > 0:
                    motoboy["pedidos_entregues"].append(
                        total_pedidos.pop(pedidos_prioritarios.pop(0))
                    )
                else:
                    motoboy["pedidos_entregues"].append(total_pedidos.pop(0))
            else:
                motoboy["pedidos_entregues"].append(total_pedidos.pop(0))
    return total_motoboys


def calcular_valor_entrega(total_motoboys: list) -> list:
    """Esse método adiciona o valor da taxa de entrega ao pedido,
    calcula do valor de saldo do motoboy pelas entregas realizadas,
    incluido o valor da taxa de comissão paga pela loja e soma esses
    valores no campo saldo.

    :param total_motoboys: Uma lista de dicionários contendo todos os motoboys com os pedidos entregues
    :type total_motoboys: list
    :return: Retorna uma lista de dicionários contendo os valores de taxas 
    :rtype: list
    """
    for motoboy in total_motoboys:
        for pedido in motoboy["pedidos_entregues"]:
            pedido["taxa_entrega"] = motoboy["taxa"]
            motoboy["saldo"] += motoboy["taxa"]
            motoboy["saldo"] += pedido["valor_taxa"]
    return total_motoboys


def relatorio_entregas(total_motoboys: list, ids_motoboys: list) -> None:
    """
    Esse método apresenta as informações de entrega de cada um dos
    motoboys, exibindo o nome, pedidos entregues junto com seus respectivos valores,
    e o saldo final do motoboy.
    
    :param total_motoboys: Lista de motoboys
    :type total_motoboys: list
    :param ids_motoboys: Lista de Ids dos motoboys para serem exibidos no relatório
    :type ids_motoboys: list
    """
    for motoboy in sorted(total_motoboys, key=lambda moto: moto["id"]):
        if motoboy["id"] in ids_motoboys:
            print(f'{motoboy["nome"]}:')
            for pedido in motoboy["pedidos_entregues"]:
                print(f'- Loja {pedido["loja_id"]} - Comissão {pedido["taxa"]} %')
                print(
                    f'  + Pedido {pedido["id"]} Valor: {formatar_valor(pedido["valor"])} Taxa de Comissão: {formatar_valor(pedido["valor_taxa"])} Taxa de Entrega: {formatar_valor(pedido["taxa_entrega"])}'
                )
            print(f'Saldo: {formatar_valor(motoboy["saldo"])}')
            print("----------------------------------------------")


if __name__ == "__main__":
    parse = argparse.ArgumentParser(
        prog="main",
        description="Gerencia a distribuição de pedido de lojas entre os motoboys disponíveis.",
        usage="main -m ",
    )
    parse.add_argument(
        "-m",
        "--motoboys",
        default=[],
        nargs="*",
        help="Lista dos Ids dos Motoboys",
        type=int,
    )
    parse.add_argument("-v", "--version", action="version", version=f"{parse.prog} 1.0")

    args = parse.parse_args()

    total_motoboys = sorted(fake_db["motoboys"], key=lambda moto: not moto["exclusivo"])

    total_pedidos = pegar_todos_pedidos()

    total_pedidos = calcular_taxas_pedidos(total_pedidos)

    total_motoboys = distribuir_pedidos(total_pedidos, total_motoboys)

    total_motoboys = calcular_valor_entrega(total_motoboys)

    if len(args.motoboys) == 0:
        relatorio_entregas(total_motoboys, range(1, 6))
    else:
        relatorio_entregas(total_motoboys, args.motoboys)
