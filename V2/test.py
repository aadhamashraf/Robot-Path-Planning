matrix = [
    [ 1 , 2 , 3] ,
    [4 , 5 , 6],

]

result = []
for i in range(len(matrix)):
    temp_row = []
    for j in range(len(matrix[0])):
        if i == j :
            temp_row.append(matrix[i][j])
        else:
            temp_row.append(matrix[j][i])
    result.append(temp_row)

for i in range(len(result)):
    for j in range(len(result[0])) :
        print(result[i][j] ,end="")
    print(" ")