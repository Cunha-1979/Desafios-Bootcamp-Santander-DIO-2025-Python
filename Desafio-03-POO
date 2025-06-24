# V1 - Criar um sistema bancário com as operações: sacar, depositar e visualizar extrato.
# V2 - Adicionado operações: criar usuário, criar conta, listar contas.
# V3 - Modelando sistema com Programação Orientada a objeto (POO).

from abc import ABC, abstractmethod
from datetime import datetime

# Funções Estéticas "molduras"

def calcular_largura_ideal(linhas, largura_minima=45, padding=8):
    comprimento_max = max(len(l.strip()) for l in linhas)
    return max(comprimento_max, largura_minima) + padding

def mostrar_moldura(texto, borda='=', largura=None):
    if largura is None:
        largura = calcular_largura_ideal([texto])
    print("\n")
    print(borda * (largura + 8))
    print(borda * 4 + " " * largura + borda * 4)
    espaco_esq = (largura - len(texto)) // 2
    espaco_dir = largura - len(texto) - espaco_esq
    print(borda * 4 + " " * espaco_esq + texto + " " * espaco_dir + borda * 4)
    print(borda * 4 + " " * largura + borda * 4)
    print(borda * (largura + 8))
    print("\n")

def mostrar_moldura_multilinha(linhas, borda='@', largura=None):
    if largura is None:
        largura = calcular_largura_ideal(linhas)
    print("\n" + borda * (largura + 8))
    print(borda * 4 + " " * largura + borda * 4)
    for linha in linhas:
        linha = linha.strip()
        espaco_esq = (largura - len(linha)) // 2
        espaco_dir = largura - len(linha) - espaco_esq
        print(borda * 4 + " " * espaco_esq + linha + " " * espaco_dir + borda * 4)
    print(borda * 4 + " " * largura + borda * 4)
    print(borda * (largura + 8) + "\n")

def mostrar_aviso_legal(limite, limite_saques, numero_saques):
    linhas = [
        "Avisos Legais:",
        f"O valor máximo permitido por saque é de R$ {limite:.2f}.",
        f"A quantidade máxima diária permitida é de {limite_saques} saques!",
        f"Você já efetuou {numero_saques} hoje."
    ]
    mostrar_moldura_multilinha(linhas, borda='=')

def mostrar_menu_moldurado(linhas, borda='=', largura_total=84, largura_conteudo=50):
    print("\n" + borda * (largura_total))
    margem = (largura_total - largura_conteudo - 8) // 2
    for linha in linhas:
        texto = linha.strip()
        texto_formatado = texto.ljust(largura_conteudo)
        print(f"{borda*4}{' ' * margem}{texto_formatado}{' ' * margem}{borda*4}")
    print(borda * (largura_total))
    print()

# Classes

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

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

    def sacar(self, valor):
        if valor <= 0:
            mostrar_moldura("Operacao falhou! Valor invalido.", borda='#')
            return False
        if valor > self._saldo:
            mostrar_moldura("Operacao falhou! Saldo insuficiente.", borda='#')
            return False
        self._saldo -= valor
        mostrar_moldura("Saque realizado com sucesso!", borda='*')
        return True

    def depositar(self, valor):
        if valor <= 0:
            mostrar_moldura("Operacao falhou! Valor invalido.", borda='#')
            return False
        self._saldo += valor
        mostrar_moldura("Deposito realizado com sucesso!", borda='*')
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([
            t for t in self.historico.transacoes if t["tipo"] == "Saque"
        ])
        if valor > self._limite:
            mostrar_moldura("Operacao falhou! Valor excede limite.", borda='#')
            return False
        if numero_saques >= self._limite_saques:
            mostrar_moldura("Operacao falhou! Limite de saques excedido.", borda='#')
            return False
        return super().sacar(valor)

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })

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

# Funções

def menu():
    linhas_menu = [
        "Bem Vindo ao Sistema Bancário XYZ v3",
        "",
        "As operações disponíveis são:",
        "",
        "[D] Depositar",
        "[S] Sacar",
        "[E] Extrato",
        "[NC] Nova conta",
        "[NU] Novo usuário",
        "[LC] Listar contas",
        "[Q] Sair",
        ""
    ]
    mostrar_menu_moldurado(linhas_menu)
    return input("Selecione a opção desejada: ")

def ler_valor_numerico(msg):
    valor_str = input(msg)
    try:
        valor = float(valor_str)
        if valor <= 0:
            mostrar_moldura("Valor inválido! Deve ser maior que zero.", borda='#')
            return None
        return valor
    except ValueError:
        mostrar_moldura("Valor inválido! Tente novamente.", borda='#')
        return None

def validar_cpf(cpf):
    if not cpf.isdigit() or len(cpf) != 11:
        mostrar_moldura("CPF inválido! Deve conter exatamente 11 dígitos numéricos.", borda='#')
        return False
    return True

def solicitar_cpf():
    while True:
        cpf = input("CPF (somente números): ")
        if validar_cpf(cpf):
            return cpf

def solicitar_numero_conta(cliente):
    while True:
        numero_conta_str = input("Número da conta: ")
        if not numero_conta_str.isdigit():
            mostrar_moldura("Conta inválida! Digite apenas números.", borda='#')
            continue
        numero_conta = int(numero_conta_str)
        conta = recuperar_conta_cliente(cliente, numero_conta)
        if conta:
            return conta
        else:
            mostrar_moldura("Número da conta não pertence ao cliente. Tente novamente.", borda='#')

def filtrar_cliente(cpf, clientes):
    return next((c for c in clientes if c.cpf == cpf), None)

def recuperar_conta_cliente(cliente, numero_conta):
    return next((c for c in cliente.contas if c.numero == numero_conta), None)

def depositar(clientes):
    cpf = solicitar_cpf()
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        mostrar_moldura("Cliente não encontrado!", borda='#')
        return
    conta = solicitar_numero_conta(cliente)
    valor = ler_valor_numerico("Valor do depósito: ")
    if valor is None:
        return
    cliente.realizar_transacao(conta, Deposito(valor))

def sacar(clientes):
    cpf = solicitar_cpf()
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        mostrar_moldura("Cliente não encontrado!", borda='#')
        return
    conta = solicitar_numero_conta(cliente)
    if isinstance(conta, ContaCorrente):
        numero_saques = len([t for t in conta.historico.transacoes if t["tipo"] == "Saque"])
        mostrar_aviso_legal(conta._limite, conta._limite_saques, numero_saques)
    valor = ler_valor_numerico("Valor do saque: ")
    if valor is None:
        return
    cliente.realizar_transacao(conta, Saque(valor))

def exibir_extrato(clientes):
    cpf = solicitar_cpf()
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        mostrar_moldura("Cliente nao encontrado!", borda='#')
        return
    conta = solicitar_numero_conta(cliente)
    if not conta:
        return
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    linhas = [
        f"EXTRATO - Gerado em {timestamp}",
        "-" * 60,
        f"Nome: {cliente.nome}",
        f"CPF: {cliente.cpf}",
        f"Agência: {conta.agencia}",
        f"Nº Conta: {conta.numero}",
        "-" * 60,
        f"{'Data':<20} | {'Tipo':<10} | {'Valor':>15}",
        "-" * 60
    ]
    transacoes = conta.historico.transacoes
    if not transacoes:
        linhas.append("Nao foram realizadas movimentacoes.")
    else:
        for t in transacoes:
            data = t["data"]
            tipo = t["tipo"]
            valor = t["valor"]
            linhas.append(f"{data:<20} | {tipo:<10} | R$ {valor:>12.2f}")
    linhas.append("-" * 60)
    linhas.append(f"{'Saldo atual:':>47} R$ {conta.saldo:>10.2f}")
    mostrar_moldura_multilinha(linhas, borda='=')

def criar_cliente(clientes):
    cpf = solicitar_cpf()
    if filtrar_cliente(cpf, clientes):
        mostrar_moldura("Cliente já existe!", borda='#')
        return
    nome = input("Nome completo: ")
    nasc = input("Data de nascimento (dd/mm/aaaa): ")
    endereco = input("Endereço completo: ")
    clientes.append(PessoaFisica(nome, nasc, cpf, endereco))
    mostrar_moldura("Cliente criado com sucesso!", borda='*')

def criar_conta(contas, clientes):
    cpf = solicitar_cpf()
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        mostrar_moldura("Cliente nao encontrado!", borda='#')
        return
    numero = len(contas) + 1
    conta = ContaCorrente.nova_conta(cliente, numero)
    cliente.adicionar_conta(conta)
    contas.append(conta)
    mostrar_moldura("Conta criada com sucesso!", borda='*')

def listar_contas(contas):
    if not contas:
        mostrar_moldura("Nenhuma conta foi encontrada!", borda='@')
        return
    linhas = ["CONTAS CADASTRADAS:"]
    for conta in contas:
        linhas.extend([
            "-" * 45,
            f"Agência: {conta.agencia}",
            f"Número da Conta: {conta.numero}",
            f"Titular: {conta.cliente.nome}",
            f"Saldo Atual: R$ {conta.saldo:.2f}"
        ])
    mostrar_moldura_multilinha(linhas, borda='@')

def main():
    clientes = []
    contas = []
    while True:
        try:
            opcao = menu().strip().upper()
            if opcao == 'D':
                depositar(clientes)
            elif opcao == 'S':
                sacar(clientes)
            elif opcao == 'E':
                exibir_extrato(clientes)
            elif opcao == 'NU':
                criar_cliente(clientes)
            elif opcao == 'NC':
                criar_conta(contas, clientes)
            elif opcao == 'LC':
                listar_contas(contas)
            elif opcao == 'Q':
                mostrar_moldura("Encerrando o sistema...", borda='=')
                break
            else:
                mostrar_moldura("Opcao invalida!", borda='#')
        except ValueError:
            mostrar_moldura("Erro de entrada! Tente novamente.", borda='#')

main()
