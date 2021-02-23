# A_star_algorithm


### Wprowadzenie:

Plik a_star.py zawiera implementację algorytmu A* oraz funkcjonalności pozwalające na wizualizację jego działania.

Program korzysta z modułu pygame, który jest niezbędny do jego uruchomienia.

### Opis algorytmu:

Serce programu to sam algorytm A*, który służy do znajdowania najkrótszej scieżki pomiędzy dwoma punktami.
Algorytm wybiera scieżkę spośród nieodwiedzonych jeszcze wierzchołków tak aby minimalizować funkcję f(x), która jest 
zadana wzorem:
f(x) = g(x) + h(x)
gdzie x jest wierzchołkiem sąsiadującym z aktualnie odwiedzanym wierzchołkiem.
g(x) to funkcja, która oblicza odległość/koszt drogi od punktu startowego do wierzchołka x
h(x) to funkcja heurystyczna, która oblicza odległość/koszt drogi od wierzchołka x do wierzchołka docelowego.

W tym przypadku funkcja heurystyczna została zaimplementowana jako "Manhatan distance". To znaczy odległość pomiędzy dwoma 
punktami obliczona jest jako suma bezwzględnych różnic odpowiadających wzspółrzędnych:
```
def h(p1, p2): 
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)
```

Funkcja g(x) w tym przypadku dla każdego kolejnego odwiedzonego wierzchołka będzie wynosić tyle co dla poprzedniego 
wierzchołka + 1.

Każdy z wierzchołków posiada pole będące listą sąsiadujących z nim wierzchołków. Dla każdego wierzchołka jest aktualizowana
przed uruchomieniem algorytmu.

Implementacja samego algorytmu bazuje na kolejce priorytetowej, do której dodawane są kolejne wierzchołki. 
Priorytet wierzchołków określany jest na podstawie wartości funkcji f(x), dodatkowo wy celu rozstrzygnięcia 
konfliktów w przypadku identycznej wartości f(x) brana pod uwagę jest kolejność dodawania do kolejki.
W tym celu obecna jest zmienna count.

cameFrom to słownik zapisujący dla każdego wierzchołka wierzchołek poprzedzający.

gScore to słownik przechowywujący dla każdego wierzchołka wartość g(x), początkowo zainicjowany dla 
wszystkich wierzchołków jako nieskończoność. Wyjątek stanowi wierzchołek startowy inicjowany na 0.

fScore to słownik przechowujący dla każdego wierzchołka wartość f(x), podonie jak g(x) zainicjowany
dla wszystkich wierzchołków jako nieskończoność. Z wyjątkiem wierzchołka startowego, który 
zainicjowany jest wartością h(x).

hashSet to strutura pomocnicza w postaci zbioru. Umożliwia sprawdzenie zawartości kolejki priorytetowej, ponieważ 
pythonowa implementacja kolejki nie ma takiej funkcjonalności, w momencie dodawania obiektu do kolejki obiekt dodawany
jest do hashSet i odwrotnie w przypadku usuwania obiektu.

Główna pętla algorytmu działa dopóki w kolejce znajdują się obiekty.
Dodatkowo istnieje wewnętrzna pętla, która sprawdza wszystkich sąsiadów dla danego węzła.
Algorytm kończy działanie w momencie dotarcia do węzła, który jest węzłem docelowym lub kiedy 
kolejka przechowująca kolejne węzły zostanie opróżniona. Zwraca w tedy odpowiednio wartość True, w przypadku 
sukcesu, i False w przypadku porażki.

W przypadku sukcesu, najoptymalniejsza ścieżka zostaje wyznaczona.




```
def a_star(draw, start, grid, goal):
    """ A* path finding algorithm """
    count = 0
    openSet = PriorityQueue()
    openSet.put((0, count, start))
    cameFrom = {}
    gScore = {node : float("inf") for row in grid for node in row}
    gScore[start] = 0  
    fScore = {node : float("inf") for row in grid for node in row}
    fScore[start] = h(start.get_pos(), goal.get_pos())

    hashSet = {start}

    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = openSet.get()[2]
        hashSet.remove(current)


        if current == goal:
            reconstructPath(cameFrom, current, draw)
            goal.make_end()
            return True

        for neighbor in current.neighbors:
            tmp_gScore = gScore[current] + 1

            if tmp_gScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tmp_gScore
                fScore[neighbor] = gScore[neighbor] + h(neighbor.get_pos(), goal.get_pos())
                if neighbor not in hashSet:
                    count += 1
                    openSet.put((fScore[neighbor], count, neighbor))
                    hashSet.add(neighbor)
                    neighbor.make_open()
        draw()
        if current != start:
            current.make_closed()
    
    return False
```

### Obsługa:

Program obsługuje się myszką. 

Pierwsze kliknięcie lewego przycisku myszy ustawia start, kolejne pole docelowe.

Następne kliknięcia (można rysować przytrzymując lewy przycisk myszy) rysują ściany/przeszkody.

W celu usunięcia zaznaczeń można posłużyć się prawym przyciskiem myszy, bądź zresetować całą planszę 
klikając przycisk 'n' na klawiaturze.

W celu uruchomienia algorytmu należy wcisnąć spację. Aby algorytm się uruchomił na planszy muszą być zaznaczone pola start i stop.
