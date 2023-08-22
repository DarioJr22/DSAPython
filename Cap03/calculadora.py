""" Passo á passo
1 - Pede para o caboclo falar oque ele quer Soma, Divisão, Subtração ou Multiplicação
2 - Pede para por os números
3 - Põe os resultados
 """

print("Bem vindo meu colega, me diga por gentileza oque vc quer")

operacao = input("Digite a operação")

num1 = float(input("Me diga o primeiro numero: "))

num2 = float(input("Digite o segundo número: "))

resultado = 0 

if operacao == "Soma":
    resultado = num1 + num2
elif operacao == "Divisão":
    resultado = num1 / num2
elif operacao == "Subtração":
    resultado = num1 - num2
elif operacao == "Multiplicação":
    resultado = num1 * num2
else: 
    resultado = "Operação inválida"

print("O resultado da sua operação foi: ", resultado)
