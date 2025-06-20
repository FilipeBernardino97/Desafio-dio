class ContaBancaria:
    def __init__(self, numero_conta, titular, saldo_inicial=0):
        self.numero_conta = numero_conta
        self.titular = titular
        self.saldo = saldo_inicial
        self.extrato = [] 
        self.saques_diarios = 0 
        self.LIMITE_SAQUES_DIARIOS = 3 
        self.LIMITE_VALOR_SAQUE = 500 

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato.append(f"Depósito de R${valor:.2f}")
            print(f"Depósito de R${valor:.2f} realizado com sucesso. Novo saldo: R${self.saldo:.2f}")
        else:
            print("Operação falhou! O valor do depósito deve ser positivo.")

    def sacar(self, valor):
        if valor <= 0:
            print("Operação falhou! O valor do saque deve ser positivo.")
            return

        if self.saques_diarios >= self.LIMITE_SAQUES_DIARIOS:
            print(f"Operação falhou! Você atingiu o limite de {self.LIMITE_SAQUES_DIARIOS} saques diários.")
            return

        if valor > self.LIMITE_VALOR_SAQUE:
            print(f"Operação falhou! O valor máximo por saque é de R${self.LIMITE_VALOR_SAQUE:.2f}.")
            return

        if self.saldo < valor:
            print("Operação falhou! Saldo insuficiente para realizar o saque.") 
            return

    
        self.saldo -= valor
        self.extrato.append(f"Saque de R${valor:.2f}")
        self.saques_diarios += 1 
        print(f"Saque de R${valor:.2f} realizado com sucesso. Novo saldo: R${self.saldo:.2f}")
        print(f"Saques restantes hoje: {self.LIMITE_SAQUES_DIARIOS - self.saques_diarios}")


    def visualizar_extrato(self):
        print("\n--- EXTRATO ---")
        if not self.extrato:
            print("Nenhuma movimentação na conta.")
        else:
            for operacao in self.extrato:
                print(operacao)
        print(f"Saldo atual: R${self.saldo:.2f}")
        print("----------------\n")

    def __str__(self):
        return f"Conta: {self.numero_conta} | Titular: {self.titular} | Saldo: R${self.saldo:.2f}"

def criar_conta():
    numero = input("Digite o número da conta: ")
    titular = input("Digite o nome do titular: ")
    try:
        saldo_inicial = float(input("Digite o saldo inicial (opcional, padrão 0): ") or 0)
        if saldo_inicial < 0:
            print("Saldo inicial não pode ser negativo. Definindo para 0.")
            saldo_inicial = 0
    except ValueError:
        print("Valor inválido para saldo inicial. Usando 0.")
        saldo_inicial = 0
    return ContaBancaria(numero, titular, saldo_inicial)

def encontrar_conta(contas, numero_conta):
    for conta in contas:
        if conta.numero_conta == numero_conta:
            return conta
    return None

def main():
    contas = []
    while True:
        print("\n===== SISTEMA BANCÁRIO =====")
        print("1. Criar nova conta")
        print("2. Acessar conta existente")
        print("3. Listar todas as contas")
        print("4. Sair")
        print("============================")

        opcao_menu_principal = input("Escolha uma opção: ")

        if opcao_menu_principal == '1':
            nova_conta = criar_conta()
            contas.append(nova_conta)
            print(f"Conta {nova_conta.numero_conta} criada com sucesso para {nova_conta.titular}!")
        elif opcao_menu_principal == '2':
            if not contas:
                print("Nenhuma conta criada ainda. Crie uma primeiro.")
                continue

            num_conta_acesso = input("Digite o número da conta que deseja acessar: ")
            conta_selecionada = encontrar_conta(contas, num_conta_acesso)

            if conta_selecionada:
                while True:
                    print(f"\n--- Bem-vindo(a), {conta_selecionada.titular} (Conta: {conta_selecionada.numero_conta}) ---")
                    print("1. Depositar")
                    print("2. Sacar")
                    print("3. Visualizar Extrato")
                    print("4. Voltar ao menu principal")
                    print("-------------------------------------------------")

                    opcao_conta = input("Escolha uma operação: ")

                    if opcao_conta == '1':
                        try:
                            valor = float(input("Digite o valor para depositar: R$"))
                            conta_selecionada.depositar(valor)
                        except ValueError:
                            print("Valor inválido. Por favor, digite um número.")
                    elif opcao_conta == '2':
                        try:
                            valor = float(input("Digite o valor para sacar: R$"))
                            conta_selecionada.sacar(valor)
                        except ValueError:
                            print("Valor inválido. Por favor, digite um número.")
                    elif opcao_conta == '3':
                        conta_selecionada.visualizar_extrato()
                    elif opcao_conta == '4':
                        print("Voltando ao menu principal...")
                        break
                    else:
                        print("Opção inválida. Por favor, tente novamente.")
            else:
                print("Conta não encontrada. Verifique o número da conta.")
        elif opcao_menu_principal == '3':
            if not contas:
                print("Nenhuma conta criada ainda.")
            else:
                print("\n--- CONTAS CADASTRADAS ---")
                for conta in contas:
                    print(conta)
                print("--------------------------")
        elif opcao_menu_principal == '4':
            print("Saindo do sistema. Obrigado por usar nossos serviços!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    main()