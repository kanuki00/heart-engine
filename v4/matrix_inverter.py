# This code is contributed to geeksforgeeks.org by phasing17

# Python3 program to find adjoint and
# inverse of a matrix


def initialize_matrix(size: int):
    result = []
    for r in range(size):
        row = []
        for c in range(size):
            row.append(None)
        result.append(row)
    return result


N = 4


# Function to get cofactor of
# A[p][q] in temp[][]. n is current
# dimension of A[][]
def cofactor(A, temp, p, q, n):

    i = 0
    j = 0

    # Looping for each element of the matrix
    for row in range(n):

        for col in range(n):

            # Copying into temporary matrix only those element
            # which are not in given row and column
            if row != p and col != q:

                temp[i][j] = A[row][col]
                j += 1

                # Row is filled, so increase row index and
                # reset col index
                if j == n - 1:
                    j = 0
                    i += 1


# Recursive function for finding determinant of matrix.
#  n is current dimension of A[][].
def determinant(in_matrix, n):
    # Initialize result
    det = 0

    # Base case : if matrix contains single element
    if n == 1:
        return in_matrix[0][0]

    # To store cofactors
    temp = initialize_matrix(N)

    # To store sign multiplier
    sign = 1

    # Iterate for each element of first row
    for f in range(n):

        # Getting Cofactor of A[0][f]
        cofactor(in_matrix, temp, 0, f, n)
        det += sign * in_matrix[0][f] * determinant(temp, n - 1)

        # terms are to be added with alternate sign
        sign = -sign

    return det


# Function to get adjoint of A[N][N] in adj[N][N].
def adjoint(in_matrix, adj):

    if N == 1:
        adj[0][0] = 1
        return

    # temp is used to store cofactors of A[][]
    temp = initialize_matrix(N)

    for i in range(N):
        for j in range(N):
            # Get cofactor of A[i][j]
            cofactor(in_matrix, temp, i, j, N)

            # sign of adj[j][i] positive if sum of row
            # and column indexes is even.
            sign = [1, -1][(i + j) % 2]

            # Interchanging rows and columns to get the
            # transpose of the cofactor matrix
            adj[j][i] = (sign)*(determinant(temp, N-1))


# Function to calculate and store inverse, returns false if
# matrix is singular
def inverse(in_matrix, inverse):

    # Find determinant of A[][]
    det = determinant(in_matrix, N)
    if (det == 0):
        print("Singular matrix, can't find its inverse")
        return False

    # Find adjoint
    adj = []
    for i in range(N):
        adj.append([0 for _ in range(N)])
    adjoint(in_matrix, adj)

    # Find Inverse using formula "inverse(A) = adj(A)/det(A)"
    for i in range(N):
        for j in range(N):
            inverse[i][j] = adj[i][j] / det

    return True


# Generic function to display the
# matrix. We use it to display
# both adjoin and inverse. adjoin
# is integer matrix and inverse
# is a float.
def display(in_matrix):
    for i in range(N):
        for j in range(N):
            print(in_matrix[i][j], end=" ")
        print()


def displays(in_matrix):
    for i in range(N):
        for j in range(N):
            print(round(in_matrix[i][j], 6), end=" ")
        print()


# Driver program

my_matrix = [[5, -2, 2, 7],
             [1, 0, 0, 3],
             [-3, 1, 5, 0],
             [3, -1, -9, 4]]
#adj = [None for _ in range(N)]
#inv = [None for _ in range(N)]

#for i in range(N):
#    adj[i] = [None for _ in range(N)]
#    inv[i] = [None for _ in range(N)]
adj = initialize_matrix(N)
inv = initialize_matrix(N)


print("Input matrix is :")
display(my_matrix)

print("\nThe Adjoint is :")
adjoint(my_matrix, adj)
display(adj)

print("\nThe Inverse is :")
if (inverse(my_matrix, inv)):
    displays(inv)
