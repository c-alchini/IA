"""
Trabalho Inteligência Artificial
Algoritmo A*
Autores: Cristian Alexandre Alchini, José Daniel Alves do Prado e Victor do Valle Cunha.
Ano: 2024
"""


graph = {
    'A': {'B': 73, 'C': 64, 'D': 89, 'E': 104},
    'B': {'A': 73, 'K': 83},
    'C': {'A': 64, 'I': 64},
    'D': {'A': 89, 'N': 89,},
    'E': {'A': 104, 'J': 40},
    'F': {'I': 31, 'N': 84},
    'G': {'J': 35, 'Q': 113},
    'H': {'K': 35, 'L': 36},
    'I': {'F': 31, 'L': 28, 'M': 20, 'C': 64},
    'J': {'G': 35, 'N': 53, 'E': 40, 'Q': 80},
    'K': {'B': 83, 'H': 35},
    'L': {'H': 36, 'I': 28, 'P': 63},
    'M': {'I': 20, 'O': 50},
    'N': {'D': 89, 'F': 84, 'J': 53},
    'O': {'M': 50, 'P': 41, 'R': 72},
    'P': {'R': 65, 'L': 63, 'O': 41},
    'Q': {'G': 113, 'J': 80, 'R': 65},
    'R': {'O': 72, 'Q': 65, 'P': 65}
}

# Tabela de distâncias
h = {
    "A": 240,
    "B": 186,
    "C": 182,
    "D": 163,
    "E": 170,
    "F": 150,
    "G": 165,
    "H": 139,
    "I": 120,
    "J": 130,
    "K": 122,
    "L": 104,
    "M": 100,
    "N": 77,
    "O": 72,
    "P": 65,
    "Q": 65,
    "R": 0
}

# Retorna o elemento da lista com o menor valor de f.
def getMinF(open: list) -> tuple:
    minF = float('inf')
    minEl = tuple()
    for el in open:
        currentF = el[2] + el[3] # f = g + h
        if currentF < minF:
            minF = currentF
            minEl = el
    
    return minEl

def addOrUpdateNode(newElement, open, closed):
    nodeID, _, newG, newH = newElement

    for el in open:
        # Verifica se o novo elemento está presente em open
        if el[0] == nodeID:
            newF = newG + newH
            existingF = el[2] + el[3]
            if (newF < existingF):
                open.remove(el)
                open.append(newElement)
            return True

    for el in closed:
        # Verifica se o novo elemento está presente em open
        if el[0] == nodeID:
            newF = newG + newH
            existingF = el[2] + el[3]
            if (newF < existingF):
                closed.remove(el)
                open.append(newElement)
            return True
    
    return False

def findElementInList(elementID, searchList):
    for el in searchList:
        if el[0] == elementID:
            return el
    
    return None

def reconstructPath(current, closed):
    nodeID, parentID, gValue, hValue = current
    fValue = gValue + hValue
    path = [(nodeID, gValue, fValue)]
    
    while len(closed) != 0:
        parent = findElementInList(parentID, closed)
        if parent == None:
            break
        
        nodeID, parentID, gValue, hValue = parent
        closed.remove(parent)
        fValue = gValue + hValue
        path = [(nodeID, gValue, fValue)] + path
    
    return path

def printPathTree(path, goalID):
    print(f"\nEncontrado caminho para {goalID}")
    print("ID  - G_Acc - F(ID)")
    for ID, g, f in path:
        print(f" {ID:<2} -  {g:>3}  -  {f:<2}")

def printIterationInfo(iteration, open, closed, current):
    print(f"\n\nIteração: {iteration}")
    
    print(f"Open: ", end="")
    for ID, _, g, hVal in open:
        print(f"({ID}, f:{g+hVal}), ", end="")
    
    
    print(f"\nClosed: ", end="")
    for ID, _, g, hVal in closed:
        print(f"({ID}, f:{g+hVal}), ", end="")
    
    print(f"\nNó selecionado: {current[0]}")

def printExpandedNodes(expanded):
    print(f"Nós verificados (expansão): ", end="")
    for ID, _, g, hVal in expanded:
        print(f"({ID} = g:{g}, h:{hVal}, f:{g+hVal}), ", end="")

def searchByAStar(startID: str, goalID: str):
    # Cada elemento é um tupla: (Nó do grafo, nó pai, distância g, distância h)
    initialState = (startID, None, 0, h[startID])
    open = [initialState]
    closed = []
    i = 0
    while len(open) != 0:
        current = getMinF(open)
        printIterationInfo(i, open, closed, current)
        
        closed.append(current)
        open.remove(current)

        currentID = current[0]
        if currentID == goalID:
            path = reconstructPath(current, closed)
            printPathTree(path, goalID)
            return
        
        expanded = []
        for neighborID in graph[currentID].keys(): # Percorre os nós vizinhos
            g = current[2] + graph[currentID][neighborID] # g = g(pai) + aresta do novo elemento
            newElement = (neighborID, currentID, g, h[neighborID])
            expanded.append(newElement)

            if not addOrUpdateNode(newElement, open, closed):
                open.append(newElement)
        
        printExpandedNodes(expanded)        
        i = i+1

def main():
    searchByAStar('A', 'R')

if __name__ == "__main__":
    main()
