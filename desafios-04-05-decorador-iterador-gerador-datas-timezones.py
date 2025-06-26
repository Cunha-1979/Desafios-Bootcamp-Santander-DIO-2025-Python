# V1 - Criar um sistema bancário com as operações: sacar, depositar e visualizar extrato.
# V2 - Adicionado operações: criar usuário, criar conta, listar contas.
# V3 - Modelando sistema com Programação Orientada a objeto (POO).
# V4 - Sistema Bancário com POO, Decoradores, Iterador, Gerador, Datas, TimeZones.

from abc import ABC, abstractmethod
from datetime import datetime
from pytz import timezone, all_timezones
from collections import defaultdict


# TZ default utilizado pelo sistema
TIMEZONE_ATUAL = timezone("America/Sao_Paulo")

# Decorador de log
def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        texto_log = f"{get_horario_atual().strftime('%d-%m-%Y %H:%M:%S')}: {func.__name__.upper()} executada."
        mostrar_moldura(texto_log, borda='=')
        return resultado
    return envelope

# Molduras visuais personalizadas
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

#def mostrar_aviso_legal(limite, limite_saques, numero_saques):
    #linhas = [
    #    "Avisos Legais:",
    #    f"O valor máximo permitido por saque é de R$ {limite:.2f}.",
    #    f"A quantidade máxima diária permitida é de {limite_saques} saques!",
    #    f"Você já efetuou {numero_saques} hoje."
    #]
    #mostrar_moldura_multilinha(linhas, borda='=')

def mostrar_menu_moldurado(linhas, borda='=', largura_total=84, largura_conteudo=50):
    print("\n" + borda * (largura_total))
    margem = (largura_total - largura_conteudo - 8) // 2
    for linha in linhas:
        texto = linha.strip()
        texto_formatado = texto.ljust(largura_conteudo)
        print(f"{borda*4}{' ' * margem}{texto_formatado}{' ' * margem}{borda*4}")
    print(borda * (largura_total))
    print()

# Montar o mapa completo de timezones categorizado
def construir_mapa_timezones():
    categorias = defaultdict(list)
    for tz in all_timezones:
        if '/' in tz and not tz.startswith("Etc/"):
            regiao = tz.split('/')[0]
            categorias[regiao].append(tz)

    letras = "abcdefghijklmnopqrstuvwxyz"
    mapa_final = {}
    for i, (regiao, zonas) in enumerate(sorted(categorias.items())):
        letra = letras[i]
        zonas_ordenadas = sorted(zonas)
        grupos_numerados = {str(idx + 1): zona for idx, zona in enumerate(zonas_ordenadas)}
        mapa_final[letra] = (regiao, grupos_numerados)
    return mapa_final

MAPA_TIMEZONES = construir_mapa_timezones()

# Função para configurar TZ via menu oculto
def configurar_timezone():
    global TIMEZONE_ATUAL

    mostrar_moldura("CONFIGURAÇÃO DE TIMEZONE", borda='=')
    
    print("Categorias disponíveis:")
    for letra, (regiao, _) in MAPA_TIMEZONES.items():
        print(f"[{letra.upper()}] {regiao}")
    
    letra = input("Escolha a letra da categoria: ").lower()
    if letra not in MAPA_TIMEZONES:
        mostrar_moldura("Categoria inválida!", borda='#')
        return

    regiao, zonas = MAPA_TIMEZONES[letra]
    print(f"\nTimezones disponíveis na categoria {regiao}:")
    
    for numero, zona in zonas.items():
        print(f"{letra}{numero} - {zona}")
    
    escolha = input("\nDigite o código do timezone desejado (ex: b147): ").strip().lower()
    if not escolha.startswith(letra):
        mostrar_moldura("Código inválido para a categoria escolhida!", borda='#')
        return

    numero = escolha[len(letra):]
    if numero not in zonas:
        mostrar_moldura("Número de timezone inválido!", borda='#')
        return

    selecionado = zonas[numero]
    TIMEZONE_ATUAL = timezone(selecionado)
    mostrar_moldura(f"Timezone configurado para {selecionado}", borda='*')

# Classes
class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self.contas):
            raise StopIteration
        conta = self.contas[self._index]
        self._index += 1
        return f"Agência: {conta.agencia}\nConta: {conta.numero}\nTitular: {conta.cliente.nome}\nSaldo: R$ {conta.saldo:.2f}"

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
        #self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([
            t for t in self.historico.transacoes if t["tipo"] == "Saque"
        ])
        if valor > self._limite:
            mostrar_moldura("Operacao falhou! Valor excede limite.", borda='#')
            return False
        #if numero_saques >= self._limite_saques:
            #mostrar_moldura("Operacao falhou! Limite de saques excedido.", borda='#')
            #return False
        return super().sacar(valor)

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        hoje = get_horario_atual().strftime("%d-%m-%Y")
        transacoes_hoje = [t for t in self._transacoes if t["data"].startswith(hoje)]

        if len(transacoes_hoje) >= 10:
            mostrar_moldura("Limite diário de 10 transações atingido!", borda='#')
            return

        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": get_horario_atual().strftime("%d-%m-%Y %H:%M:%S")
        })

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao

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

# Funções e operações

def menu():
    linhas_menu = [
        "Bem Vindo ao Sistema Bancário XYZ v4",
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

def get_horario_atual():
    return datetime.now(TIMEZONE_ATUAL)

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
    return cpf.isdigit() and len(cpf) == 11

def solicitar_cpf():
    while True:
        cpf = input("CPF (somente números): ")
        if validar_cpf(cpf):
            return cpf
        else:
            mostrar_moldura("CPF inválido! Deve conter 11 dígitos.", borda='#')

def filtrar_cliente(cpf, clientes):
    return next((c for c in clientes if c.cpf == cpf), None)

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        mostrar_moldura("Cliente não possui contas!", borda='#')
        return None
    return cliente.contas[0]

def excedeu_limite_transacoes(conta):
    hoje = get_horario_atual().strftime("%d-%m-%Y")
    transacoes_hoje = [t for t in conta.historico.transacoes if t["data"].startswith(hoje)]
    return len(transacoes_hoje) >= 10

@log_transacao
def depositar(clientes):
    cpf = solicitar_cpf()
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        mostrar_moldura("Cliente não encontrado!", borda='#')
        return
    
    conta = recuperar_conta_cliente(cliente)
    
    if conta is None:
        return
    if excedeu_limite_transacoes(conta):
        mostrar_moldura("Limite diário de transações atingido!", borda='#')
        return
        
    valor = ler_valor_numerico("Valor do depósito: ")
    
    if valor is not None:
        cliente.realizar_transacao(conta, Deposito(valor))

@log_transacao
def sacar(clientes):
    cpf = solicitar_cpf()
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        mostrar_moldura("Cliente não encontrado!", borda='#')
        return
    
    conta = recuperar_conta_cliente(cliente)
    
    if conta is None:
        return
    
    #mostrar_aviso_legal(conta._limite, conta._limite_saques, numero_saques
    
    if excedeu_limite_transacoes(conta):
        mostrar_moldura("Limite diário de transações atingido!", borda='#')
        return
            
    valor = ler_valor_numerico("Valor do saque: ")
    
    if valor is not None:
        cliente.realizar_transacao(conta, Saque(valor))

@log_transacao
def exibir_extrato(clientes):
    cpf = solicitar_cpf()
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        mostrar_moldura("Cliente não encontrado!", borda='#')
        return
    conta = recuperar_conta_cliente(cliente)
    linhas = [
        f"EXTRATO - {get_horario_atual().strftime('%d/%m/%Y %H:%M:%S')}",
        "-" * 60
    ]
    for t in conta.historico.gerar_relatorio():
        linhas.append(f"{t['data']} | {t['tipo']} | R$ {t['valor']:.2f}")
    if not conta.historico.transacoes:
        linhas.append("Não foram realizadas movimentações.")
    linhas.append("-" * 60)
    linhas.append(f"Saldo atual: R$ {conta.saldo:.2f}")
    mostrar_moldura_multilinha(linhas, borda='=')

@log_transacao
def criar_cliente(clientes):
    cpf = solicitar_cpf()
    if filtrar_cliente(cpf, clientes):
        mostrar_moldura("Cliente já existe!", borda='#')
        return
    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    endereco = input("Endereço completo: ")
    cliente = PessoaFisica(nome, nascimento, cpf, endereco)
    clientes.append(cliente)
    mostrar_moldura("Cliente criado com sucesso!", borda='*')

@log_transacao
def criar_conta(clientes, contas):
    cpf = solicitar_cpf()
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        mostrar_moldura("Cliente não encontrado!", borda='#')
        return
    
    numero = len(contas) + 1
    conta = ContaCorrente.nova_conta(cliente, numero)
    cliente.adicionar_conta(conta)
    contas.append(conta)
    mostrar_moldura("Conta criada com sucesso!", borda='*')

def listar_contas(contas):
    if not contas:
        mostrar_moldura("Nenhuma conta encontrada!", borda='@')
        return
    linhas = [str(conta) for conta in ContasIterador(contas)]
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
                criar_conta(clientes, contas)
            elif opcao == 'LC':
                listar_contas(contas)
            elif opcao == 'Q':
                mostrar_moldura("Encerrando o sistema...", borda='=')
                break
            elif opcao == 'TZ': # Menu oculto para setar o TZ
                configurar_timezone()
            else:
                mostrar_moldura("Opção inválida!", borda='#')
        except Exception as e:
            mostrar_moldura(f"Erro: {e}", borda='#')

main()
