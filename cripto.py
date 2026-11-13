import os
import random
from datetime import datetime

ARQUIVO_USUARIOS = "usuarios.txt"
ARQUIVO_CRIPTOMOEDAS = "criptomoedas.txt"
ARQUIVO_EXTRATO = "extrato.txt"

arquivos = [
    ARQUIVO_USUARIOS,
    ARQUIVO_CRIPTOMOEDAS,
    ARQUIVO_EXTRATO
]

for arquivo in arquivos:
    if not os.path.exists(arquivo):
        open(arquivo, "w").close()

usuarios = []
criptomoedas = []
extrato = []

USUARIO_PADRAO = ["Investidor", "12345678900", "123456", "0", "0", "0", "0"]

CRIPTOMOEDAS_PADRAO = [
    ["Bitcoin", "350000", "2", "3"],
    ["Ethereum", "18000", "1", "2"],
    ["Ripple", "3", "1", "1"]
]

def carregar_dados():
    global usuarios
    global criptomoedas
    global extrato

    usuarios = []
    criptomoedas = []
    extrato = []

    with open(ARQUIVO_USUARIOS, "r") as arquivo:
        for linha in arquivo:
            dados = linha.strip().split(";")
            if len(dados) == 7:
                usuarios.append(dados)

    if len(usuarios) == 0:
        usuarios.append(USUARIO_PADRAO)
        salvar_usuarios()

    with open(ARQUIVO_CRIPTOMOEDAS, "r") as arquivo:
        for linha in arquivo:
            dados = linha.strip().split(";")
            if len(dados) == 4:
                criptomoedas.append(dados)

    if len(criptomoedas) == 0:
        criptomoedas.extend(CRIPTOMOEDAS_PADRAO)
        salvar_criptomoedas()

    with open(ARQUIVO_EXTRATO, "r") as arquivo:
        for linha in arquivo:
            dados = linha.strip().split(";")
            if len(dados) == 12:
                extrato.append(dados)

def salvar_usuarios():
    with open(ARQUIVO_USUARIOS, "w") as arquivo:
        for usuario in usuarios:
            arquivo.write(";".join(usuario) + "\n")

def salvar_criptomoedas():
    with open(ARQUIVO_CRIPTOMOEDAS, "w") as arquivo:
        for moeda in criptomoedas:
            arquivo.write(";".join(moeda) + "\n")

def salvar_extrato():
    with open(ARQUIVO_EXTRATO, "w") as arquivo:
        for operacao in extrato:
            arquivo.write(";".join(operacao) + "\n")

def logo():
    print("=" * 70)
    print(" " * 25 + "EXCHANGE")
    print("=" * 70)
    print(" " * 18 + "Plataforma de Criptomoedas")
    print("=" * 70)

def converter_valor(valor):
    return float(valor.replace(",", "."))

def formatar_valor(valor):
    return f"{valor:.2f}".replace(".", ",")

def formatar_quantidade(valor):
    return f"{valor:.8f}".replace(".", ",")

def buscar_moeda(nome):
    for moeda in criptomoedas:
        if moeda[0].lower() == nome.lower():
            return moeda
    return None

def mostrar_cotacoes():
    print("\n" + "=" * 65)
    print(f'| {"CRIPTOMOEDA":^20} | {"COTAÇÃO (R$)":^18} | {"COMPRA":^8} | {"VENDA":^8} |')
    print("=" * 65)
    for moeda in criptomoedas:
        print(f'| {moeda[0]:^20} | {formatar_valor(float(moeda[1])):^18} | {moeda[2] + "%":^8} | {moeda[3] + "%":^8} |')
    print("=" * 65)

def verificar_senha(usuario):
    senha = input("Digite sua senha de 6 dígitos: ")
    if senha == usuario[2]:
        return True
    print("\nSenha incorreta!")
    return False

def registrar_operacao(usuario, tipo, moeda, quantidade, cotacao, taxa):
    data = datetime.now().strftime("%d-%m-%Y %H:%M")
    registro = [
        usuario[1],
        data,
        tipo,
        moeda,
        str(quantidade),
        str(cotacao),
        str(taxa),
        usuario[3],
        usuario[4],
        usuario[5],
        usuario[6],
        "R$"
    ]
    extrato.append(registro)
    salvar_extrato()

def consultar_saldo(usuario):
    if not verificar_senha(usuario):
        return

    print("\n" + "=" * 50)
    print(f"Nome: {usuario[0]}")
    print(f"CPF: {usuario[1]}")
    print(f"Reais: R$ {formatar_valor(float(usuario[3]))}")
    print(f"Bitcoin: {formatar_quantidade(float(usuario[4]))}")
    print(f"Ethereum: {formatar_quantidade(float(usuario[5]))}")
    print(f"Ripple: {formatar_quantidade(float(usuario[6]))}")
    print("=" * 50)

def consultar_extrato(usuario):
    if not verificar_senha(usuario):
        return

    print("\n" + "=" * 100)
    print(f"Nome: {usuario[0]}")
    print(f"CPF: {usuario[1]}")
    print("=" * 100)

    encontrou = False

    for operacao in extrato:
        if operacao[0] == usuario[1]:
            encontrou = True
            print(f"{operacao[1]} | {operacao[2]} | {operacao[3]} | Quantidade: {operacao[4]} | Cotação: R$ {formatar_valor(float(operacao[5]))} | Taxa: R$ {formatar_valor(float(operacao[6]))}")
            print(f"Saldo em reais: R$ {formatar_valor(float(operacao[7]))} | BTC: {operacao[8]} | ETH: {operacao[9]} | XRP: {operacao[10]}")
            print("-" * 100)

    if not encontrou:
        print("\nNenhuma operação realizada!")

def depositar(usuario):
    print("\n===== DEPÓSITO =====")

    try:
        valor = converter_valor(input("Digite o valor do depósito: R$ "))
    except ValueError:
        print("\nDigite um valor válido!")
        return

    if valor <= 0:
        print("\nO valor deve ser maior que zero!")
        return

    usuario[3] = str(float(usuario[3]) + valor)
    salvar_usuarios()
    registrar_operacao(usuario, "DEPOSITO", "REAL", valor, 0, 0)

    print("\nDepósito realizado com sucesso!")
    print(f"Saldo em reais: R$ {formatar_valor(float(usuario[3]))}")

def sacar(usuario):
    print("\n===== SAQUE =====")

    try:
        valor = converter_valor(input("Digite o valor do saque: R$ "))
    except ValueError:
        print("\nDigite um valor válido!")
        return

    if valor <= 0:
        print("\nO valor deve ser maior que zero!")
        return

    if valor > float(usuario[3]):
        print("\nSaldo insuficiente!")
        return

    usuario[3] = str(float(usuario[3]) - valor)
    salvar_usuarios()
    registrar_operacao(usuario, "SAQUE", "REAL", valor, 0, 0)

    print("\nSaque realizado com sucesso!")
    print(f"Saldo em reais: R$ {formatar_valor(float(usuario[3]))}")

def comprar_criptomoeda(usuario):
    if not verificar_senha(usuario):
        return

    mostrar_cotacoes()

    print("\n1 - Bitcoin")
    print("2 - Ethereum")
    print("3 - Ripple")

    opcao = input("\nEscolha a criptomoeda: ")

    if opcao == "1":
        moeda = buscar_moeda("Bitcoin")
        indice = 4
    elif opcao == "2":
        moeda = buscar_moeda("Ethereum")
        indice = 5
    elif opcao == "3":
        moeda = buscar_moeda("Ripple")
        indice = 6
    else:
        print("\nOpção inválida!")
        return

    try:
        valor = converter_valor(input("\nQuanto deseja investir em reais? R$ "))
    except ValueError:
        print("\nDigite um valor válido!")
        return

    if valor <= 0:
        print("\nO valor deve ser maior que zero!")
        return

    taxa = valor * (float(moeda[2]) / 100)
    total = valor + taxa63

    if total > float(usuario[3]):
        print("\nSaldo em reais insuficiente!")
        return

    quantidade = valor / float(moeda[1])
    usuario[3] = str(float(usuario[3]) - total)
    usuario[indice] = str(float(usuario[indice]) + quantidade)

    salvar_usuarios()
    registrar_operacao(usuario, "COMPRA", moeda[0], quantidade, float(moeda[1]), taxa)

    print("\nCompra realizada com sucesso!")
    print(f"Quantidade comprada: {formatar_quantidade(quantidade)}")
    print(f"Taxa: R$ {formatar_valor(taxa)}")
    print(f"Total descontado: R$ {formatar_valor(total)}")
    print(f"Saldo em reais: R$ {formatar_valor(float(usuario[3]))}")

def vender_criptomoeda(usuario):
    if not verificar_senha(usuario):
        return

    mostrar_cotacoes()

    print("\n1 - Bitcoin")
    print("2 - Ethereum")
    print("3 - Ripple")

    opcao = input("\nEscolha a criptomoeda: ")

    if opcao == "1":
        moeda = buscar_moeda("Bitcoin")
        indice = 4
    elif opcao == "2":
        moeda = buscar_moeda("Ethereum")
        indice = 5
    elif opcao == "3":
        moeda = buscar_moeda("Ripple")
        indice = 6
    else:
        print("\nOpção inválida!")
        return

    try:
        quantidade = converter_valor(input("\nQuanto deseja vender? "))
    except ValueError:
        print("\nDigite uma quantidade válida!")
        return

    if quantidade <= 0:
        print("\nA quantidade deve ser maior que zero!")
        return

    if quantidade > float(usuario[indice]):
        print("\nSaldo de criptomoeda insuficiente!")
        return

    valor = quantidade * float(moeda[1])
    taxa = valor * (float(moeda[3]) / 100)
    total = valor - taxa

    usuario[indice] = str(float(usuario[indice]) - quantidade)
    usuario[3] = str(float(usuario[3]) + total)

    salvar_usuarios()
    registrar_operacao(usuario, "VENDA", moeda[0], quantidade, float(moeda[1]), taxa)

    print("\nVenda realizada com sucesso!")
    print(f"Valor da venda: R$ {formatar_valor(valor)}")
    print(f"Taxa: R$ {formatar_valor(taxa)}")
    print(f"Valor recebido: R$ {formatar_valor(total)}")
    print(f"Saldo em reais: R$ {formatar_valor(float(usuario[3]))}")

def atualizar_cotacao():
    print("\n===== ATUALIZAR COTAÇÕES =====")

    for moeda in criptomoedas:
        cotacao_anterior = float(moeda[1])
        variacao = random.uniform(-0.05, 0.05)
        nova_cotacao = cotacao_anterior + (cotacao_anterior * variacao)
        moeda[1] = str(round(nova_cotacao, 2))

    salvar_criptomoedas()
    mostrar_cotacoes()
    print("\nCotações atualizadas com sucesso!")

def menu_usuario(usuario):
    while True:
        print("\n" + "=" * 60)
        print("1 - Consultar saldo")
        print("2 - Consultar extrato")
        print("3 - Depositar reais")
        print("4 - Sacar reais")
        print("5 - Comprar criptomoedas")
        print("6 - Vender criptomoedas")
        print("7 - Atualizar cotação")
        print("8 - Sair")
        print("=" * 60)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            consultar_saldo(usuario)
        elif opcao == "2":
            consultar_extrato(usuario)
        elif opcao == "3":
            depositar(usuario)
        elif opcao == "4":
            sacar(usuario)
        elif opcao == "5":
            comprar_criptomoeda(usuario)
        elif opcao == "6":
            vender_criptomoeda(usuario)
        elif opcao == "7":
            atualizar_cotacao()
        elif opcao == "8":
            print("\nLogout realizado!")
            break
        else:
            print("\nDigite uma opção válida!")

def login():
    print("\n===== LOGIN =====")
    cpf = input("Digite seu CPF (somente números): ")
    senha = input("Digite sua senha de 6 dígitos: ")

    if not cpf.isdigit() or len(cpf) != 11:
        print("\nCPF inválido! Digite os 11 números sem pontos ou traços.")
        return None

    if not senha.isdigit() or len(senha) != 6:
        print("\nSenha inválida! Digite 6 números.")
        return None

    for usuario in usuarios:
        if usuario[1] == cpf and usuario[2] == senha:
            print(f"\nBem-vindo(a), {usuario[0]}!")
            return usuario

    print("\nCPF ou senha incorretos!")
    return None

def menu_inicial():
    while True:
        print("\n1 - Fazer login")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            usuario = login()
            if usuario:
                menu_usuario(usuario)
        elif opcao == "0":
            print("\nSistema encerrado!")
            break
        else:
            print("\nDigite uma opção válida!")

carregar_dados()
logo()
menu_inicial()
