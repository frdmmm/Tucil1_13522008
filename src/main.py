import numpy as np
import random
import time
def brute_force(matrix, currow, curcol, remaining_moves, route, allroute, visited, vertical=False):
    if remaining_moves == 0:
        if tuple(route) not in visited:
            allroute.append(route.copy())
            visited.add(tuple(route))
        return

    if (matrix[currow][curcol], (currow, curcol)) not in route:
        route.append((matrix[currow][curcol], (currow, curcol)))
    else:
        return

    nexdir = not vertical

    if nexdir:
        for i in range(len(matrix)):
            if i != currow:
                brute_force(matrix, i, curcol, remaining_moves - 1, route, allroute, visited, nexdir)
    else:
        for j in range(len(matrix[0])):
            if j != curcol:
                brute_force(matrix, currow, j, remaining_moves - 1, route, allroute, visited, nexdir)

    route.pop()

def calculatepoint(route, sequencedict):
    result=0
    for key, value in sequencedict.items():
        sub_len = len(key)
        for i in range(len(route) - sub_len + 1):
            if route[i:i + sub_len] == key:
                result+=value
    return result
def readtxt(filename):
    try:
        with open(filename, 'r')  as file:
            lines=file.readlines()
            buffer_size=int(lines[0])
            matrixsize = list(map(int, lines[1].split()))
            matrix=[list(map(str, line.strip().split()))for line in  lines[2:2+matrixsize[0]]]
            numberofsequence=int(lines[2+matrixsize[0]])
            listsequence=lines[3+matrixsize[0]:]
            sequencedict = {tuple(listsequence[i].strip().split()): int(listsequence[i + 1]) for i in range(0, 2*numberofsequence, 2)}
    except FileNotFoundError:
        print(f"File {filename} not  found.")
    return buffer_size, np.array(matrix), sequencedict

def random_matrix(tokens, m, n):
    matrix = [[random.choice(tokens) for _ in range(n)] for _ in range(m)]
    return matrix
def random_sequencedict(tokens, max_token, amount):
    sequencedict = {}
    for _ in range(amount):
        num_token = random.randint(1, max_token)
        rand_token = random.choices(tokens, k=num_token)
        value = random.randint(1, 100)
        sequencedict[tuple(rand_token)] = value
    return sequencedict
def printmatrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            print(matrix[i][j], end=' ')
        print()
def solution(max_key, start_time):
    print(f'{max_key[1]}')
    for i in range(len(max_key[0])):
        print(max_key[0][i][0], end=' ')
    print()
    for i in range(len(max_key[0])):
        print(f'{max_key[0][i][1][0]}, {max_key[0][i][1][1]}')
    print();print()
    end_time=time.time()
    print(f'{(end_time-start_time)*1000} ms')
    print();print()
    txt=input("Apakah ingin menyimpan solusi? (y/n) ")
    if txt=='y' or txt=='Y':
        fname=input("Masukkan nama file.txt : ")
        name=f'../test/{fname}'
        with open(name, 'w') as file:
            print(max_key[1], file=file)
            content=''
            for i in range(len(max_key[0])):
                content+=max_key[0][i][0]+' '
            print(content[:-1], file=file)
            for i in range(len(max_key[0])):
                print(f'{max_key[0][i][1][0]}, {max_key[0][i][1][1]}', file=file)
            print(file=file);print(file=file)
            print(f'{(end_time-start_time)*1000} ms', file=file)
if __name__ == "__main__":
    import sys

    if len(sys.argv) >2:
        print("Usage:  python main.py <txt_file>")
    elif len(sys.argv)==2:
        buffer_size, matrix, sequencedict=readtxt(sys.argv[1])
        allroute=[]
        visited=set()
        start_time = time.time()
        for i in range(len(matrix)):
            brute_force(matrix, 0, i, buffer_size, [],allroute, visited)
        hasil = {(tuple(route), calculatepoint(tuple(element[0] for element in route), sequencedict)) for route in allroute}
        max_key = max(hasil, key=lambda k: k[1])
        solution(max_key, start_time)
        
    else:
        tokencount=int(input("Masukkan jumlah token unik : "))
        token=input("Masukkan token yang dipisahkan spasi : ").strip().split()
        buffer_size=int(input("Masukkan ukuran buffer : "))
        matrixsize=input("Masukkan ukuran matriks : ").strip().split()
        sequencecount=int((input("Masukkan jumlah sekuens : ")))
        sequencesize=int(input("Masukkan ukuran maksimal sekuens : "))
        start_time = time.time()
        matrix=random_matrix(token, int(matrixsize[0]), int(matrixsize[1]))
        sequencedict=random_sequencedict(token, sequencesize, sequencecount)
        print("Matrix acak : ")
        printmatrix(matrix)
        print("Sekuens acak : ")
        for key, value in sequencedict.items():
            print(f"{key} : {value}")
        allroute=[]
        visited=set()
        for i in range(len(matrix)):
            brute_force(matrix, 0, i, buffer_size, [],allroute, visited)
        hasil = {(tuple(route), calculatepoint(tuple(element[0] for element in route), sequencedict)) for route in allroute}
        max_key = max(hasil, key=lambda k: k[1])
        solution(max_key, start_time)