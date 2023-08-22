""" 
Hello Word

"""

print('hello word')

""" 
# Criando uma lista de numeros de 0 a 100
- list transforma o conteúdo em uma lista 
"""

numeros = list(range(1,101))

for i in numeros:
    if i % 10 == 0:
       """  print(i) """



""" Usando list comprehention pela primeira vez """
"""
- List == Abre e fecha cochetes
- começa com o resultado (i)
- passa a expressão que retorna o resultado
- 
 """
divDez =  [i for i in numeros if i % 10 == 0 ]
print(type(divDez))
print(divDez)