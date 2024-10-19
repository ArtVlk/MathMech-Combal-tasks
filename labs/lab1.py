from collections import deque, defaultdict


def merge(v, w, p, q, name, next_node, size):
    """
    Функция для слияния двух компонент графа.
    """
    name[w] = p
    u = next_node[w]
    while name[u] != p:
        name[u] = p
        u = next_node[u]
    size[p] += size[q]
    next_node[v], next_node[w] = next_node[w], next_node[v]


def Boruvka_Kruskal(V, E):
    """
        Алгоритм Борувки-Краскала для построения минимального остовного дерева во взвешенном графе.

        Параметры:
        V -- список вершин графа
        E -- список рёбер графа в формате (v, w, вес)

        Возвращает:
        T -- список рёбер, входящих в минимальное остовное дерево
        total_weight -- общий вес минимального остовного дерева
    """
    # Инициализация
    Q = deque(sorted(E, key=lambda x: x[2])) # Очередь с рёбрами, отсортированными по весу
    name = {} # Для хранения текущей компоненты для каждой вершины
    next_node = {} # Для хранения следующего узла в компоненте
    size = {} # Для хранения размера каждой компоненты

    # Инициализация начальных значений для каждой вершины
    for v in V:
        name[v] = v # Каждая вершина принадлежит своей компоненте
        next_node[v] = v # Следующая вершина в компоненте — сама вершина
        size[v] = 1 # Начальный размер компоненты — 1

    T = [] # Список для хранения рёбер минимального остовного дерева (MST)
    total_weight = 0 # Переменная для хранения общего веса MST# Переменная для хранения общего веса MST

    # Пока не найдено n-1 рёбер в минимальном остовном дереве или пока есть рёбра для обработки
    while len(T) != len(V) - 1 and Q:
        vw = Q.popleft() # Берём ребро с минимальным весом
        v, w, weight = vw
        p, q = name[v], name[w] # Компоненты, к которым принадлежат вершины v и w

        if p != q: # Если вершины принадлежат разным компонентам
            # Слияние меньшей компоненты с большей (или наоборот)
            if size[p] > size[q]:
                merge(w, v, q, p, name, next_node, size)
            else:
                merge(v, w, p, q, name, next_node, size)
            T.append(vw) # Добавляем ребро в минимальное остовное дерево
            total_weight += weight # Увеличиваем общий вес

    # Возвращаем список рёбер минимального остовного дерева и его общий вес
    return T, total_weight


def adjacency_list_output(V, T, total_weight):
    """
    Форматирование и вывод остова как списка смежностей.

    Параметры:
    V -- список вершин графа
    T -- список рёбер минимального остовного дерева
    total_weight -- общий вес минимального остовного дерева
    """
    # Словарь для хранения списков смежностей
    adj_list = defaultdict(list)

    # Построение списка смежностей на основе рёбер минимального остовного дерева
    for v, w, _ in T:
        adj_list[v].append(w)
        adj_list[w].append(v)

    # Форматированный вывод
    with open("out.txt", "w") as file:
        for v in sorted(V):
            neighbors = sorted(adj_list[v])  # Соседи вершины, отсортированные по возрастанию
            file.write(" ".join(map(lambda x: str(x + 1), neighbors)) + " 0" + '\n') # Выводим соседей с 0 в конце строки
        # Вывод общего веса остова
        file.write(str(total_weight))


def main():

    # Считываем данные
    with open("in.txt", "r") as file:
        n = int(file.readline())
        data = list(map(int, file.read().split()))

    # Избавляемся от "мусорной" вершины
    count_vertex = data[0]-1
    for i in range(0, count_vertex):
        if data[data[i] - 1] == 32767:
            data.remove(data[i])
    data.pop()
    count_vertex -= 1
    data[:data[0] - 2] = map(lambda x: x - 2, data[:data[0] - 2])

    # Создаём множество вершин и рёбер
    V = list(map(lambda x: x, range(0, count_vertex)))
    E = []
    for i in range(0, count_vertex-1):
        for j in range(data[i], data[i+1], 2):
            vertex, value = data[j]-1, data[j+1]
            if (vertex, i, value) not in E:
                edge = (i, vertex, value)
                E.append(edge)
    for i in range(data[count_vertex-1], len(data), 2):
        vertex, value = data[i] - 1, data[i + 1]
        if (vertex, count_vertex-1, value) not in E:
            edge = (count_vertex-1, vertex, value)
            E.append(edge)

    # Запускаем алгоритм и выводим ответик
    mst, total_weight = Boruvka_Kruskal(V, E)
    adjacency_list_output(V, mst, total_weight)


if __name__ == "__main__":
    main()
