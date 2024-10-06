import sys
from collections import deque


def Ford_Fulkerson(F, s, t):
    n = len(F)
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
                if h[v] == -1 and F[w][v] - F[w][v] > 0:
                    h[v] = min(h[w], F[w][v] - F[w][v])
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
            if F[w][v] - F[w][v] >= flow:
                F[w][v] += flow
            else:
                F[v][w] -= flow
            v = w

    return F, max_flow


def main():
    with open('in.txt', 'r') as f:
        n = int(f.readline())
        graph = [list(map(int, f.readline().split())) for _ in range(n)]
        s = int(f.readline()) - 1
        t = int(f.readline()) - 1

    F, max_flow = Ford_Fulkerson(graph, s, t)

    with open('out.txt', 'w') as f:
        for row in F:
            f.write(' '.join(map(str, row)) + '\n')
        f.write(str(max_flow))


if __name__ == '__main__':
    main()
