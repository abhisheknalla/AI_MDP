import copy

def print_nice(U):#####PRINTING UTILITIES OF GRID
    print
    for i in range(N):
        for j in range(M):
            print '% 7.3f ' % U[i][j],
        print
    print

# UT = [[0 for j in range(M)] for i in range(N)]
# U[0][3] = X#POSITIVE TERMIAllDirL STATE
# U[1][3] = -X#NEGATIVE TERMIAllDirL STATE

INF = 1000099
X = 0.0000
N, M = map(int, raw_input().split())

U = [[0 for j in range(M)] for i in range(N)]#UTILITY MATRIX ALL ZEROES

board2 = [[0]*N for _ in range(M)]

for i in range(N):
    board2[i] = [float(j) for j in raw_input().strip().split(" ")]

#print(board2)
E, W =  map(int, raw_input().split())
Y = 0.0000
endStates = []
for i in range (0, E):
        xx, yy = map(int, raw_input().split())
        X = (board2[xx][yy])
        Y = abs(X)
        U[xx][yy]=X;
X = Y


wallStates = []

for i in range (0, W):
        xxx, yyy = map(int, raw_input().split())
        #wallStates.append(xxx,yyy)
        board2[xxx][yyy]=INF;

startx, starty = map(int, raw_input().split())

def_reward = float(raw_input())

board = [['0.00' for i in range(M)]for j in range(N)]

for i in range(N):
    for j in range(M):
        if board2[i][j]==0:
            board[i][j]='.'
        elif board2[i][j]==INF:
            board[i][j]='-'
        elif board2[i][j]==X:
            board[i][j]='g'
        elif board2[i][j]==-X:
            # print "came here!"
            # print (i,j)
            board[i][j]='b'
        elif board2[i][j]==X/10:
            U[i][j] = X/10
            board[i][j]='oa'
        elif board2[i][j]==-X/10:
            U[i][j] = -X/10
            board[i][j]='ob'
print board

h = {}
h[0] = (-1, 0)
h[1] = (0, 1)
h[2] = (1, 0)
h[3] = (0, -1)
X = 1
gamma = 1.0#DISCOUNT FACTOR

AllDir = 4

CurrDir = 4

P = [[[[0.0 for l in range(CurrDir)] for k in range(AllDir)] for j in range(M)] for i in range(N)]#PROBABILITY MATRIX
S = [[[[(0,0) for l in range(CurrDir)] for k in range(AllDir)] for j in range(M)] for i in range(N)]#
R = [[[[0.0 for l in range(CurrDir)] for k in range(AllDir)] for j in range(M)] for i in range(N)]#REWARD MATRIX

for i in range(N):#ROWS
    for j in range(M):#COLS
        for k in range(AllDir):#ALL DIRECTIOCurrDir
            for l in range(CurrDir):#ALL DIRECTIOCurrDir
                if k==l:#INTENDED DIRECTION
                    P[i][j][k][l] = 0.8
                elif (k+1)%AllDir == l  or (k-1+AllDir)%AllDir==l :#LEFT OR RIGHT TO INTENDED DIRECTION
                    P[i][j][k][l] = 0.1
                else :#OPPOSITE DIRECTION
                    P[i][j][k][l] = 0.0

                r, c = h[l]#DIRECTION WHICH WE ARE HEADING
                nr = i+r#NEW ROW
                nc = j+c#NEW COL

                if nr >= N or nr < 0 or nc >= M or nc < 0 or board[nr][nc] == '-':#BLOCKED
                    S[i][j][k][l] = (i, j)#STAY IN SAME STATE
                else:
                    S[i][j][k][l] = (nr, nc)#NOT BLOCKED NEW STATE

                r, c = S[i][j][k][l]#TO GET REWARD OF NEW STATE
                R[i][j][k][l] = def_reward#####CHECK HERE?
count = 0
change = X

while count < 100:#NO OF ITERATIOCurrDir
    # if(count >= 1 and count <= 5):
    print "Iteration :",count
    print_nice(U)
    UT = copy.deepcopy(U)
    flag = 0
    change = 0
    for i in range(N):
        for j in range(M):
            if board[i][j]=='-' or board[i][j] == 'g' or board[i][j] == 'b':#NO USE UPDATING IF CURRENTLY IN TERMIAllDirL OR WALL STATE
                continue
            max_value = -1000000
            for k in range(AllDir):#ALL DIRECTIOCurrDir
                value = 0
                for l in range(CurrDir):#ALL DIRECTIOCurrDir
                    r, c = S[i][j][k][l]
                    value += P[i][j][k][l] * (UT[r][c] * gamma + R[i][j][k][l])
                max_value = max(max_value, value)#BETTER THAN LAST VALUE ?
            U[i][j] = max_value
    count += 1
    change = 0.00000
    for i in range(N):
        for j in range(M):
            change = max(change, abs(U[i][j] - UT[i][j]))
    if(change < 0.01 * UT[i][j]):
        break
    del UT

print "Iteration :",count
print_nice(U)
