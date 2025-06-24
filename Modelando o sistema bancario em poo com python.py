from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
from enum import Enum


# 1. ENUM para Tipos de Transação
class TipoTransacao(Enum):
    DEPOSITO = "Depósito"
    SAQUE = "Saque"


class Cliente:
    """
    Representa um cliente do banco.
    Um cliente possui um endereço e uma lista de contas.
    """
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        """
        Realiza uma transação em uma conta específica.

        Args:
            conta (Conta): A conta onde a transação será realizada.
            transacao (Transacao): A transação a ser registrada.
        """
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """
        Adiciona uma nova conta ao cliente.

        Args:
            conta (Conta): A conta a ser adicionada.
        """
        self.contas.append(conta)


class PessoaFisica(Cliente):
    """
    Representa uma pessoa física, que é um tipo de cliente.
    """
    def __init__(self, nome: str, data_nascimento: str, cpf: str, endereco: str):
        """
        Inicializa uma nova instância de PessoaFisica.

        Args:
            nome (str): O nome completo da pessoa física.
            data_nascimento (str): A data de nascimento da pessoa (formato DD-MM-AAAA).
            cpf (str): O Cadastro de Pessoas Físicas (CPF).
            endereco (str): O endereço completo da pessoa.
        """
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    """
    Classe base para representar uma conta bancária.
    Gerencia saldo, número, agência, cliente e histórico de transações.
    """
    def __init__(self, numero: int, cliente: Cliente):
        """
        Inicializa uma nova instância de Conta.

        Args:
            numero (int): O número da conta.
            cliente (Cliente): O cliente associado a esta conta.
        """
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int):
        """
        Cria uma nova instância de conta.

        Args:
            cliente (Cliente): O cliente para associar à conta.
            numero (int): O número da nova conta.

        Returns:
            Conta: Uma nova instância da classe Conta.
        """
        return cls(numero, cliente)

    @property
    def saldo(self) -> float:
        """Retorna o saldo atual da conta."""
        return self._saldo

    @property
    def numero(self) -> int:
        """Retorna o número da conta."""
        return self._numero

    @property
    def agencia(self) -> str:
        """Retorna o número da agência."""
        return self._agencia

    @property
    def cliente(self) -> Cliente:
        """Retorna o cliente associado à conta."""
        return self._cliente

    @property
    def historico(self):
        """Retorna o histórico de transações da conta."""
        return self._historico

    def sacar(self, valor: float) -> bool:
        """
        Realiza um saque na conta.

        Args:
            valor (float): O valor a ser sacado.

        Returns:
            bool: True se o saque for bem-sucedido, False caso contrário.
        """
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n❌ Operação falhou! Saldo insuficiente. ❌")
        elif valor <= 0:
            print("\n❌ Operação falhou! O valor informado é inválido. ❌")
        else:
            self._saldo -= valor
            print("\n✅ Saque realizado com sucesso! ✅")
            return True
        return False

    def depositar(self, valor: float) -> bool:
        """
        Realiza um depósito na conta.

        Args:
            valor (float): O valor a ser depositado.

        Returns:
            bool: True se o depósito for bem-sucedido, False caso contrário.
        """
        if valor > 0:
            self._saldo += valor
            print("\n✅ Depósito realizado com sucesso! ✅")
            return True
        else:
            print("\n❌ Operação falhou! O valor informado é inválido. ❌")
            return False


class ContaCorrente(Conta):
    """
    Representa uma conta corrente, um tipo específico de conta.
    Possui limite de saque e limite de número de saques diários.
    """
    def __init__(self, numero: int, cliente: Cliente, limite: float = 500, limite_saques: int = 3):
        """
        Inicializa uma nova instância de ContaCorrente.

        Args:
            numero (int): O número da conta corrente.
            cliente (Cliente): O cliente associado.
            limite (float): O limite máximo por saque.
            limite_saques (int): O número máximo de saques permitidos por dia.
        """
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        """
        Realiza um saque na conta corrente, considerando limites e número de saques.

        Args:
            valor (float): O valor a ser sacado.

        Returns:
            bool: True se o saque for bem-sucedido, False caso contrário.
        """
        # Uso do Enum para filtrar transações de saque
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == TipoTransacao.SAQUE.value]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print(f"\n❌ Operação falhou! O valor do saque (R$ {valor:.2f}) excede o limite de R$ {self.limite:.2f}. ❌")
        elif excedeu_saques:
            print(f"\n❌ Operação falhou! Número máximo de saques ({self.limite_saques}) excedido. ❌")
        else:
            return super().sacar(valor)
        return False

    def __str__(self) -> str:
        """
        Retorna uma representação em string da conta corrente.
        """
        return f"""\
            Agência:\t\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
            Saldo:\t\tR$ {self.saldo:.2f}
        """


class Historico:
    """
    Gerencia o histórico de transações de uma conta.
    """
    def __init__(self):
        """Inicializa um novo histórico de transações."""
        self._transacoes = []

    @property
    def transacoes(self) -> list:
        """Retorna a lista de transações."""
        return self._transacoes

    def adicionar_transacao(self, transacao):
        """
        Adiciona uma transação ao histórico.

        Args:
            transacao (Transacao): A transação a ser adicionada.
        """
        self._transacoes.append(
            {
                "tipo": transacao.tipo.value,  # Acessa o valor do Enum
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    """
    Classe abstrata base para todas as transações.
    Define a interface para transações (valor e registro).
    """
    @property
    @abstractproperty
    def valor(self) -> float:
        """Retorna o valor da transação."""
        pass

    @property
    @abstractproperty
    def tipo(self) -> TipoTransacao:
        """Retorna o tipo da transação (Enum)."""
        pass

    @abstractmethod
    def registrar(self, conta):
        """
        Registra a transação em uma conta.

        Args:
            conta (Conta): A conta onde a transação será registrada.
        """
        pass


class Saque(Transacao):
    """
    Representa uma transação de saque.
    """
    def __init__(self, valor: float):
        """
        Inicializa uma nova transação de saque.

        Args:
            valor (float): O valor do saque.
        """
        self._valor = valor
        self._tipo = TipoTransacao.SAQUE

    @property
    def valor(self) -> float:
        """Retorna o valor do saque."""
        return self._valor

    @property
    def tipo(self) -> TipoTransacao:
        """Retorna o tipo da transação (Saque)."""
        return self._tipo

    def registrar(self, conta: Conta):
        """
        Registra o saque na conta.

        Args:
            conta (Conta): A conta onde o saque será registrado.
        """
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    """
    Representa uma transação de depósito.
    """
    def __init__(self, valor: float):
        """
        Inicializa uma nova transação de depósito.

        Args:
            valor (float): O valor do depósito.
        """
        self._valor = valor
        self._tipo = TipoTransacao.DEPOSITO

    @property
    def valor(self) -> float:
        """Retorna o valor do depósito."""
        return self._valor

    @property
    def tipo(self) -> TipoTransacao:
        """Retorna o tipo da transação (Depósito)."""
        return self._tipo

    def registrar(self, conta: Conta):
        """
        Registra o depósito na conta.

        Args:
            conta (Conta): A conta onde o depósito será registrado.
        """
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


# --- Função principal para demonstrar o uso do sistema bancário ---
def main():
    """Função principal para demonstrar o uso do sistema bancário."""
    print("--- INICIANDO SIMULAÇÃO BANCÁRIA ---")

    # Criando os clientes fictícios
    ana = PessoaFisica(nome="Ana Paula Rodrigues", data_nascimento="15-03-1988", cpf="456.789.012-34", endereco="Rua das Palmeiras, 75 - Boa Viagem - Recife, PE")
    carlos = PessoaFisica(nome="Carlos Eduardo Souza", data_nascimento="20-07-1975", cpf="123.456.789-00", endereco="Avenida Boa Viagem, 1200 - Apto 501 - Boa Viagem - Recife, PE")
    mariana = PessoaFisica(nome="Mariana Costa Lima", data_nascimento="03-11-1995", cpf="987.654.321-01", endereco="Travessa do Forte, 10 - Olinda - PE")
    roberto = PessoaFisica(nome="Roberto Almeida Santos", data_nascimento="28-02-1960", cpf="321.654.987-77", endereco="Rua do Sol, 300 - Casa Forte - Recife, PE")

    # Criando as contas para cada cliente
    # Ana com conta padrão
    conta_ana = ContaCorrente.nova_conta(cliente=ana, numero=1001)
    ana.adicionar_conta(conta_ana)

    # Carlos com limite de saque maior
    conta_carlos = ContaCorrente.nova_conta(cliente=carlos, numero=1002, limite=1500)
    carlos.adicionar_conta(conta_carlos)

    # Mariana com conta padrão
    conta_mariana = ContaCorrente.nova_conta(cliente=mariana, numero=1003)
    mariana.adicionar_conta(conta_mariana)

    # Roberto com conta padrão
    conta_roberto = ContaCorrente.nova_conta(cliente=roberto, numero=1004)
    roberto.adicionar_conta(conta_roberto)

    print("\n--- Informações Iniciais das Contas ---")
    print(conta_ana)
    print(conta_carlos)
    print(conta_mariana)
    print(conta_roberto)

    print("\n--- Realizando Operações (Ana) ---")
    deposito_ana = Deposito(valor=2000.00)
    ana.realizar_transacao(conta_ana, deposito_ana)
    print(f"Saldo atual da {conta_ana.cliente.nome}: R$ {conta_ana.saldo:.2f}")

    saque_ana_1 = Saque(valor=300.00)
    ana.realizar_transacao(conta_ana, saque_ana_1)
    print(f"Saldo atual da {conta_ana.cliente.nome}: R$ {conta_ana.saldo:.2f}")

    saque_ana_2 = Saque(valor=600.00) # Excede o limite de 500 da conta_ana
    ana.realizar_transacao(conta_ana, saque_ana_2)
    print(f"Saldo atual da {conta_ana.cliente.nome}: R$ {conta_ana.saldo:.2f}")


    print("\n--- Realizando Operações (Carlos) ---")
    deposito_carlos = Deposito(valor=5000.00)
    carlos.realizar_transacao(conta_carlos, deposito_carlos)
    print(f"Saldo atual do {conta_carlos.cliente.nome}: R$ {conta_carlos.saldo:.2f}")

    saque_carlos_1 = Saque(valor=1200.00) # Dentro do limite de 1500
    carlos.realizar_transacao(conta_carlos, saque_carlos_1)
    print(f"Saldo atual do {conta_carlos.cliente.nome}: R$ {conta_carlos.saldo:.2f}")

    saque_carlos_2 = Saque(valor=1600.00) # Excede o limite de 1500 da conta_carlos
    carlos.realizar_transacao(conta_carlos, saque_carlos_2)
    print(f"Saldo atual do {conta_carlos.cliente.nome}: R$ {conta_carlos.saldo:.2f}")


    print("\n--- Realizando Operações (Mariana) ---")
    deposito_mariana = Deposito(valor=300.00)
    mariana.realizar_transacao(conta_mariana, deposito_mariana)
    print(f"Saldo atual da {conta_mariana.cliente.nome}: R$ {conta_mariana.saldo:.2f}")

    # Realizando múltiplos saques para testar o limite de saques (3)
    saque_mariana_1 = Saque(valor=50.00)
    mariana.realizar_transacao(conta_mariana, saque_mariana_1)
    print(f"Saldo atual da {conta_mariana.cliente.nome}: R$ {conta_mariana.saldo:.2f}")

    saque_mariana_2 = Saque(valor=70.00)
    mariana.realizar_transacao(conta_mariana, saque_mariana_2)
    print(f"Saldo atual da {conta_mariana.cliente.nome}: R$ {conta_mariana.saldo:.2f}")

    saque_mariana_3 = Saque(valor=80.00)
    mariana.realizar_transacao(conta_mariana, saque_mariana_3)
    print(f"Saldo atual da {conta_mariana.cliente.nome}: R$ {conta_mariana.saldo:.2f}")

    saque_mariana_4 = Saque(valor=20.00) # Deve falhar por exceder número de saques
    mariana.realizar_transacao(conta_mariana, saque_mariana_4)
    print(f"Saldo atual da {conta_mariana.cliente.nome}: R$ {conta_mariana.saldo:.2f}")


    print("\n--- Histórico de Transações da Conta da Ana ---")
    for transacao in conta_ana.historico.transacoes:
        print(f"  - Tipo: {transacao['tipo']}, Valor: R$ {transacao['valor']:.2f}, Data: {transacao['data']}")

    print("\n--- FIM DA SIMULAÇÃO ---")


# Garante que a função main() seja chamada apenas quando o script for executado diretamente
if __name__ == "__main__":
    main()