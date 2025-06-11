# Criar um sistema bancário com as operalções: sacar, depositaar e visualizar extratp.

# Menu estatico 
menu = """
=======================================================
======== Bem Vindo ao Sistema Bancário XYZ v1 =========

As operações disponíveis são:
                
                    [D] Depositar
                    [S] Sacar
                    [E] Extrato
                    [Q] Sair

=======================================================

Selecione a opção desejada: """
# Declaração de variáveis com valores iniciais ou fixos.
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    try:
        opcao = input(menu).upper() #Colocado .upper() para caso o usuário digitar em minusculo converte para maiusculo para não dar erro no sistema.

        if opcao == "D":
            valor = float(input("\nInforme o valor do depósito: R$ "))

            if valor > 0:
                print("\nOperação realizada com sucesso!")
                saldo += valor
                extrato += f"Depósito: R$ {valor:.2f}\n"

            else:
                print("Operação não concluída! O valor informado é inválido.")

        elif opcao == "S":
            print("\nAvisos Legais:")
            print(f"O Valor máximo permitido por saque é de R$ {limite}.")
            print(f"A quantidade máxima diária permitida é de {LIMITE_SAQUES} saques!")
            print(f"Você já efetuou {numero_saques} hoje.")
        
            valor = float(input("\nInforme o valor do saque: R$ "))

            excedeu_saldo = valor > saldo

            excedeu_limite = valor > limite

            excedeu_saques = numero_saques >= LIMITE_SAQUES

            if excedeu_saldo:
                print("\nOperação não concluída! Você não possui saldo suficiente.")

            elif excedeu_limite:
                print("\nOperação não concluída! O valor do saque excede o limite.")

            elif excedeu_saques:
                print("\nOperação não concluída! Número máximo de saques excedido.")

            elif valor > 0:
                print("\n Opração realizada com sucesso, retire seu dinheiro!")
                saldo -= valor
                extrato += f"Saque: R$ {valor:.2f}\n"
                numero_saques += 1

            else:
                print("Operação não concluída! O valor informado é inválido.")

        elif opcao == "E":
            print("\n================ EXTRATO ================")
            print("Não foram realizadas movimentações." if not extrato else extrato)
            print(f"\nSaldo: R$ {saldo:.2f}")
            print("==========================================")

        elif opcao == "Q":
            print("\n\nEncerrando o Sistema!")
            print("\nObrigado por utilizar nossos serviços!\n\n\n")
            break;

        else:
            print("\nOpção inválida, por favor selecione novamente a operação desejada.")
    except ValueError:
        print("\n\n######################################################################################################")
        print("####                                                                                              ####")
        print('#### Valor informado esta no formato incorreto, não utilize  " , " para valores! Tente novamente! ####')
        print("####                                                                                              ####")
        print("######################################################################################################\n\n")
