from abc import ABC, abstractmethod

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

class Cliente:
    def __init__(self, endereco) -> None:
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

    def __str__(self):
        return f"{', '.join([f'{chave}: {valor}' for chave, valor in self.__dict__.items()])}"

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({"tipo": transacao.__class__.__name__, "valor": transacao.valor})

class Conta:
    def __init__(self, saldo=0, numero=None, agencia="0001", cliente=None, historico=Historico()):
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = historico

    def __str__(self) -> str:
        return f"Nº {self._numero} - R$ {self._saldo:.2f}"

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente, numero):
        return Conta(0, numero, None, cliente)
    
    def sacar(self, valor):
        if self._saldo < valor:
            print("Saldo insuficiente.")
            return False

        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado!")
            return True
        
        else:
            print("Valor inválido.")
            return False
        
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado!")
            return True
        
        else:
            print("Valor inválido!")
            return False
    
class ContaCorrente(Conta):
    def __init__(self, saldo=0, numero=None, agencia="0001", cliente=None, historico=Historico(), limite=500, limite_saques=3):
        super().__init__(saldo, numero, agencia, cliente, historico)
        self._limite = limite
        self._limite_saques = limite_saques

    @classmethod
    def nova_conta(cls, cliente, numero):
        return ContaCorrente(0, numero, None, cliente)

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        
        if numero_saques >= self._limite_saques:
            print("Limite de Saques excedido:", 3)

        else:
            if valor > self._limite:
                print("Limite de R$ 500.00 excedido.")
            else:
                return super().sacar(valor)
            
        return False


def identificador(cpf):
    cadastrado = None
    cliente = None

    if clientes:
        for pessoa in clientes:
            if cpf == pessoa.cpf:
                cadastrado = True
                cliente = pessoa
                break
            else:
                cadastrado = False
    else:
        cadastrado = False
    
    return cadastrado, cliente

def resgatar_conta(cliente):
    if cliente.contas:
        conta = cliente.contas[0]
        return conta

    else:
        print("Cliente não possui uma conta.")

def movimentacao(tipo_transacao):
    cpf = str(input("CPF: "))
    cadastrado, cliente = identificador(cpf)
        
    if cadastrado:
        conta = resgatar_conta(cliente)

        if conta == None:
            return
        
        valor = float(input(f"Valor para {str(tipo_transacao.__name__)}: "))
        transacao = tipo_transacao(valor)  
        cliente.realizar_transacao(conta, transacao)

    else:
        print("CPF não encontrado.")

def mostrar_extrato():
    cpf = str(input("CPF: "))
    cadastrado, cliente = identificador(cpf)

    if cadastrado:
        conta = resgatar_conta(cliente)

        if conta == None:
            return
        
        extrato = ""
        numero_saques = 0
        numero_depositos = 0
        total_saques = 0
        total_depositos = 0
        transacoes = conta.historico.transacoes
        
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\t\tR$ {transacao['valor']:.2f}"
            if transacao['tipo'] == "Saque":
                numero_saques += 1
                total_saques += transacao['valor']

            else:
                numero_depositos += 1
                total_depositos += transacao['valor']

        print("==============EXTRATO==============", end="")
        print("\nNão houveram movimentações." if extrato == "" else extrato)
        print(f"""===================================
Nº Depósitos: \t\t{numero_depositos}
Total Depositado: \tR$ {total_depositos:.2f}
===================================
Nº Saques: \t\t{numero_saques}
Total Sacado: \t\tR$ {total_saques:.2f}
===================================""")
        
        print(f"Saldo: \t\t\tR$ {conta._saldo}")

    else:
        print("CPF não encontrado.")

def cadastrar():
    nome = str(input("Nome: "))
    data_nascimento = str(input("Data de nascimento (DD/MM/AAAA): "))
    cpf = str(input("CPF (Somente Números): "))

    cadastrado, x = identificador(cpf)

    if cadastrado:
        print("CPF já cadastrado.")

    else:
        print("Informações do Endereço")
        logradouro = str(input("Logradouro: "))
        numero = int(input("Número: "))
        bairro = str(input("Bairro: "))
        cidade = str(input("Cidade: "))
        estado = str(input("Sigla do Estado: "))

        endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"
        
        cliente = PessoaFisica(endereco, cpf, nome, data_nascimento)
        
        print(cliente)

        clientes.append(cliente)
        print("Cadastro Realizado.")

def criar_conta():
    cpf = str(input("CPF: "))
    cadastrado, cliente = identificador(cpf)

    if cadastrado:
        global num
        num += 1

        conta = ContaCorrente.nova_conta(cliente, num)

        contas.append(conta)
        PessoaFisica.adicionar_conta(cliente, conta)

        print("Conta corrente criada.")
    
    else:
        print("CPF não encontrado")

num = 0
clientes = []
contas = []
operacao = -1

while operacao != 0:

    operacao = int(input(f"""
===========MENU===========
1 - Depósito
2 - Saque
3 - Extrato
4 - Criar Usuário
5 - Criar Conta Corrente

0 - Sair
==========================
"""))
    if operacao == 1:
        movimentacao(Deposito)

    elif operacao == 2:
        movimentacao(Saque)
        
    elif operacao == 3:
        mostrar_extrato()

    elif operacao == 4:
        cadastrar()
        
    elif operacao == 5:
        criar_conta()

    elif operacao == 6:
        for pessoa in clientes:
            print(pessoa)
            for conta in pessoa.contas:
                print(conta.saldo())

    elif operacao == 0:
        print("Obrigado por usar o programa!")

    else: print("Escolha uma das opções válidas.")