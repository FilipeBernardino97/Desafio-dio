import textwrap

def menu():    
    menu_texto = """
------------------------------------
                MENU
------------------------------------
[d]\tDepositar
[s]\tSacar
[e]\tExtrato
[lc]\tListar contas
[nu]\tNovo usuário
[nc]\tNova conta
[q]\tSair
=> """   
    return input(textwrap.dedent(menu_texto))

def depositar(saldo, valor, extrato, /):    
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\nDepósito realizado com sucesso!")
    else:
        print("\nOperação falhou! O valor informado é inválido.")
        
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):  
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\nOperação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("\nOperação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("\nOperação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\nSaque realizado com sucesso!")
    else:
        print("\nOperação falhou! O valor informado é inválido.")
    
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):    
    print("\n---------------- EXTRATO ----------------")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("-----------------------------------------")

def criar_usuario(usuarios):    
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nJá existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("\nUsuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):   
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios, contas):   
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        contas.append({"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario})
        print("\nConta criada com sucesso!")
        return True
    
    print("\nUsuário não encontrado, fluxo de criação de conta encerrado!")
    return False

def listar_contas(contas):    
    if not contas:
        print("\nNenhuma conta cadastrada.")
        return
        
    print("\n------------- LISTA DE CONTAS -------------")
    for conta in contas:
        linha = f"""
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print(textwrap.dedent(linha))
        print("-----------------------------------------")


def main():    
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    
    usuarios = [
        {"nome": "Elara Vance", "data_nascimento": "01-01-1700", "cpf": "11122233344", "endereco": "Torre-Biblioteca de Ébano, Vale das Estrelas Cadentes"},
        {"nome": "Jax", "data_nascimento": "25-07-2045", "cpf": "55566677788", "endereco": "Setor 3, Docas do Porto Digital - Recife/PE - 2077"},
        {"nome": "Isadora Montenegro", "data_nascimento": "15-03-1905", "cpf": "99988877766", "endereco": "Livraria Montenegro, Rua da Aurora - Recife/PE - 1932"}
    ]
    
    contas = [
        {"agencia": AGENCIA, "numero_conta": 1, "usuario": usuarios[0]}, 
        {"agencia": AGENCIA, "numero_conta": 2, "usuario": usuarios[1]},
        {"agencia": AGENCIA, "numero_conta": 3, "usuario": usuarios[2]}  
    ]
    
    saldo = 0 
    limite = 500
    extrato = ""
    numero_saques = 0
    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(AGENCIA, numero_conta, usuarios, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("\nSaindo do sistema... Obrigado por usar nosso banco!\n")
            break

        else:
            print("\nOperação inválida, por favor selecione novamente a operação desejada.")
                     
main()