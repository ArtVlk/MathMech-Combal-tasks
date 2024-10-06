import sys
from collections import deque

def Ford_Fulkerson(A, s, t):
    n = len(A)
    F = [[0] * n for _ in range(n)]
    max_flow = 0

    def labeling():
        h = [-1] * n  # используем -1 для непройденных вершин
        h[s] = sys.maxsize
        prev = [-1] * n
        Q = deque([s])

        while Q:
            w = Q.popleft()
            for v in range(n):
                # проверка на возможность продвижения по прямому ребру
                if h[v] == -1 and A[w][v] - F[w][v] > 0:
                    h[v] = min(h[w], A[w][v] - F[w][v])
                    prev[v] = w
                    Q.append(v)
                # проверка на возможность продвижения по обратному ребру
                elif h[v] == -1 and F[v][w] > 0:
                    h[v] = min(h[w], F[v][w])
                    prev[v] = w
                    Q.append(v)
            if h[t] != -1:  # если дошли до стока, прерываем поиск
                break

        return h, prev

    while True:
        h, prev = labeling()
        if h[t] == -1:  # если нет пути до стока, завершаем алгоритм
            break

        # увеличиваем поток на найденном пути
        flow = h[t]
        max_flow += flow
        v = t
        while v != s:
            w = prev[v]
            if A[w][v] - F[w][v] >= flow:
                F[w][v] += flow
            else:
                F[v][w] -= flow
            v = w

    return F, max_flow

# Чтение данных из файла in.txt
with open('in.txt', 'r') as file:
    lines = file.readlines()

n = int(lines[0].strip())  # количество вершин
A = [list(map(int, lines[i + 1].strip().split())) for i in range(n)]  # матрица пропускных способностей
s = int(lines[n + 1].strip()) - 1  # источник (индексы начинаются с 0)
t = int(lines[n + 2].strip()) - 1  # сток (индексы начинаются с 0)

# Решение задачи
F, max_flow = Ford_Fulkerson(A, s, t)

# Форматируем вывод
output_fixed = '\n'.join(' '.join(map(str, row)) for row in F) + '\n' + str(max_flow)

# Запись результатов в файл out.txt
with open('out.txt', 'w') as file:
    file.write(output_fixed)
