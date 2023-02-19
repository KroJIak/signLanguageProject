m = list(map(int, input('Массив:\n').split()))
m1 = [i for i in m if i < 50]
m2 = [i for i in m if i >= 50]
print(f'Ср. арифм. элементов [0,50): {sum(m1)/len(m1)}')
print(f'Ср. арифм. элементов [50,100]: {sum(m2)/len(m2)}')