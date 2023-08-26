# Calculadora em Python

# Desenvolva uma calculadora em Python com tudo que você aprendeu nos capítulos até aqui no curso. 
# A solução será apresentada no próximo capítulo!
print("\n******************* Calculadora em Python *******************\n\n\n")

print("Selecione o numero da operação desejada: \n\n")
print("1 - Soma\n")
print("2 - Subtração\n")
print("3 - Multiplicação\n")
print("4 - Divisão\n")

opr = input("Digite sua opção (1/2/3/4): ")
signal = ''


def oprMat(num1,num2):
    global signal
    if opr == "1":
        signal = '+'
        return num1 + num2
    elif opr == "2":
        signal= '-'
        return num1 - num2
    elif opr == "3":
        signal = '*'
        return num1 * num2
    elif opr == "4":
        signal = '/'
        return num1 / num2
    else: 
        return "Operador inválido, digite outro meu parceiro"

num1 = float(input("Digite o primeiro número: "))

num2 =  float(input("Digite o segundo número: "))

result = oprMat(num1,num2)

if  type(result) == float:
    print("%s %r %a = %d" %(num1,str(signal),num2,result))
else:
    print('Sinal inválido meu chapa, tente mandar o sinal correto !')