""" Bubble Sort Pseudo Código
1 - Receber o valor ao qual quero manipular
2 - Percorrer toda a lista que estou manipulando, verificando se é maior que todos os elementos.
3 - Se for maior por na posição anterior, caso não por na posição posterior.


 """

lista = [6,7,8,3,10,19,4,1,0,61,30,16,17,82,29,34,43,21,11,39,56,67,12]

def bubble_sort(arr):

    n = len(arr)

    """ Para cada elemento no array """
    for i in range(n):

        for j in range(0,n-i-1):

            if arr[j] > arr[j+1]:

                arr[j], arr[j+1] = arr[j+1], arr[j]

                return arr
            

print(bubble_sort(lista))
