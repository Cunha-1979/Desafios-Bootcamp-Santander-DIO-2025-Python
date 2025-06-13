#V1 - Criar um sistema bancário com as operações: sacar, depositar e visualizar extrato.
# V2 - Adicionado operações: criar usuário, criar conta, listar contas.

# Funções
def mostrar_moldura(texto, borda='=', largura=75):
    print("\n")
    print(borda * (largura + 8))
    print(borda * 4 + " " * largura + borda * 4)
    espaco_esq = (largura - len(texto)) // 2
    espaco_dir = largura - len(texto) - espaco_esq
    print(borda * 4 + " " * espaco_esq + texto + " " * espaco_dir + borda * 4)
    print(borda * 4 + " " * largura + borda * 4)
    print(borda * (largura + 8))
    print("\n")

def mostrar_moldura_multilinha(linhas, borda='@', largura=75):
    print("\n" + borda * (largura + 8))
    print(borda * 4 + " " * largura + borda * 4)
    for linha in linhas:
        linha = linha.strip()
        espaco_esq = (largura - len(linha)) // 2
        espaco_dir = largura - len(linha) - espaco_esq
        print(borda * 4 + " " * espaco_esq + linha + " " * espaco_dir + borda * 4)
    print(borda * 4 + " " * largura + borda * 4)
    print(borda * (largura + 8) + "\n")

def mostrar_aviso_legal(limite, limite_saques, numero_saques, largura=75):
    linhas = [
        "Avisos Legais:",
        f"O valor máximo permitido por saque é de R$ {limite:.2f}.",
        f"A quantidade máxima diária permitida é de {limite_saques} saques!",
        f"Você já efetuou {numero_saques} hoje."
    ]
    mostrar_moldura_multilinha(linhas, borda='=')

def menu():
    menu = """
    =======================================================
    ======== Bem Vindo ao Sistema Bancário XYZ v2 =========

    As operações disponíveis são:
                
                        [D] Depositar
                        [S] Sacar
                        [E] Extrato
                        [NC] Nova conta
                        [NU] Novo usuário
                        [LC] Listar contas
                        [Q] Sair

    =======================================================

    Selecione a opção desejada: """
    return input(menu)

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:     R$ {valor:.2f}\n"
        mostrar_moldura("Depósito realizado com sucesso!", borda='*')
    else:
        mostrar_moldura("Operação falhou! O valor informado é inválido.", borda='#')
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        mostrar_moldura("Operação não concluída! Você não possui saldo suficiente.", borda='#')
    elif excedeu_limite:
        mostrar_moldura("Operação não concluída! O valor do saque excede o limite.", borda='#')
    elif excedeu_saques:
        mostrar_moldura("Operação não concluída! Número máximo de saques excedido.", borda='#')
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:        R$ {valor:.2f}\n"
        numero_saques += 1
        mostrar_moldura("Operação realizada com sucesso, retire seu dinheiro!", borda='*')
    else:
        mostrar_moldura("Operação falhou! O valor informado é inválido.", borda='#')
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    conteudo = extrato if extrato else "Não foram realizadas movimentações!"
    linhas = conteudo.strip().split("\n")

    largura = 75
    borda = "="
    print("\n" + borda * (largura + 8))
    print(borda * 4 + " " * largura + borda * 4)

    titulo = "EXTRATO"
    espaco_esq = (largura - len(titulo)) // 2
    espaco_dir = largura - len(titulo) - espaco_esq
    print(borda * 4 + " " * espaco_esq + titulo + " " * espaco_dir + borda * 4)

    print(borda * 4 + " " * largura + borda * 4)

    for linha in linhas:
        if ":" in linha:
            tipo, valor = linha.split(":")
            tipo = tipo.strip()
            valor = valor.strip()
            texto_formatado = f"{tipo:<12} R$ {float(valor.split('R$')[-1]):>10.2f}"
        else:
            texto_formatado = linha.strip()

        espaco_esq = (largura - len(texto_formatado)) // 2
        espaco_dir = largura - len(texto_formatado) - espaco_esq
        print(borda * 4 + " " * espaco_esq + texto_formatado + " " * espaco_dir + borda * 4)

    print(borda * 4 + " " * largura + borda * 4)

    saldo_texto = f"Saldo: R$ {saldo:,.2f}"
    linha_formatada = f"{saldo_texto:>{largura}}"
    print(borda * 4 + linha_formatada + borda * 4)

    print(borda * 4 + " " * largura + borda * 4)
    print(borda * (largura + 8) + "\n")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    if len(cpf) == 11: # Válida quantidade de numero para CPF 11 numeros.
        usuario = filtrar_usuario(cpf, usuarios)
        if usuario:
            mostrar_moldura("Já existe usuário com esse CPF!", borda='#')
            return
        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
        mostrar_moldura("Usuário criado com sucesso!", borda='*')
    else:
        mostrar_moldura("CPF inválido! É obrigatório ter 11 números. Tente novamente!", borda='#')

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        mostrar_moldura("Conta criada com sucesso!", borda='*')
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    mostrar_moldura("Usuário não encontrado! Processo encerrado!", borda='#')

def listar_contas(contas):
    for conta in contas:
        linhas = [
            f"Agência: {conta['agencia']}",
            f"C/C: {conta['numero_conta']}",
            f"Titular: {conta['usuario']['nome']}"
        ]
        mostrar_moldura_multilinha(linhas, borda='@')

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        try:
            opcao = menu().upper()

            if opcao == "D":
                valor = float(input("Informe o valor do depósito: "))
                saldo, extrato = depositar(saldo, valor, extrato)

            elif opcao == "S":
                mostrar_aviso_legal(limite, LIMITE_SAQUES, numero_saques)

                valor = float(input("Informe o valor do saque: "))
                saldo, extrato, numero_saques = sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUES,
                )

            elif opcao == "E":
                exibir_extrato(saldo, extrato=extrato)

            elif opcao == "NU":
                criar_usuario(usuarios)

            elif opcao == "NC":
                numero_conta = len(contas) + 1
                conta = criar_conta(AGENCIA, numero_conta, usuarios)
                if conta:
                    contas.append(conta)

            elif opcao == "LC":
                listar_contas(contas)

            elif opcao == "Q":
                mostrar_moldura("Encerrando o Sistema! Obrigado por utilizar nossos serviços!", borda='=')
                break

            else:
                mostrar_moldura("Operação inválida! Selecione novamente.", borda='#')

        except ValueError:
            mostrar_moldura("Você está cometendo algum erro, por favor siga as instruções atentamente!", borda='#')

main()
