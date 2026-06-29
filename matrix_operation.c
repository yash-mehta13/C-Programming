#include <stdio.h>

int main(){
    int n,m;
    printf("Enter the number of rows and columns: ");
    scanf("%d %d", &n, &m);
    int A[n][m];
    int B[n][m];
    int C[n][m];

    printf("Enter the elements of the first matrix:\n");
    for(int i=0; i<n; i++){
        for(int j=0; j<m; j++){
            scanf("%d", &A[i][j]);
        }
    }

    printf("Enter the elements of the second matrix:\n");
    for(int i=0; i<n; i++){
        for(int j=0; j<m; j++){
            scanf("%d", &B[i][j]);
        }
    }

    printf("The 1st matrix is:\n");
    for(int i=0; i<n; i++){
        for(int j=0; j<m; j++){
            printf("%d ", A[i][j]);
        }
        printf("\n");
    }

    printf("The 2nd matrix is:\n");
    for(int i=0; i<n; i++){
        for(int j=0; j<m; j++){
            printf("%d ", B[i][j]);
        }
        printf("\n");
    }
    
    int operation;
    printf("Enter the operation number (1 for addition, 2 for subtraction, 3 for multiplication, 4 for transpose, 5 for determinant): ");
    scanf("%d", &operation);
    switch(operation){
        case 1:
            // Perform matrix addition
            for(int i=0; i<n; i++){
                for(int j=0; j<m; j++){
                    C[i][j] = A[i][j] + B[i][j];
                }
            }
            printf("The result of matrix addition is:\n");
            for(int i=0; i<n; i++){
                for(int j=0; j<m; j++){
                    printf("%d ", C[i][j]);
                }
                printf("\n");
            }
            break;
        case 2:
            // Perform matrix subtraction
            for(int i=0; i<n; i++){
                for(int j=0; j<m; j++){
                    C[i][j] = A[i][j] - B[i][j];
                }
            }
            printf("The result of matrix subtraction is:\n");
            for(int i=0; i<n; i++){
                for(int j=0; j<m; j++){
                    printf("%d ", C[i][j]);
                }
                printf("\n");
            }
            break;
        case 3:
            // Perform matrix multiplication
            for(int i=0; i<n; i++){
                for(int j=0; j<m; j++){
                    C[i][j] = 0;
                    for(int k=0; k<m; k++){
                        C[i][j] += A[i][k] * B[k][j];
                    }
                }
            }
            printf("The result of matrix multiplication is:\n");
            for(int i=0; i<n; i++){
                for(int j=0; j<m; j++){
                    printf("%d ", C[i][j]);
                }
                printf("\n");
            }
            break;
        case 4:
            // Perform matrix transpose of the first matrix
            printf("The transpose of the first matrix is:\n");
            for(int i=0; i<m; i++){
                for(int j=0; j<n; j++){
                    printf("%d ", A[j][i]);
                }
                printf("\n");
            }
            printf("The transpose of the second matrix is:\n");
            for(int i=0; i<m; i++){
                for(int j=0; j<n; j++){
                    printf("%d ", B[j][i]);
                }
                printf("\n");
            }
            break;
        case 5:
            if(n == 2 && m == 2){
                // Perform matrix determinant of the first matrix
                int determinant = A[0][0] * A[1][1] - A[0][1] * A[1][0];
                printf("The determinant of the first matrix is: %d\n", determinant);
                int determinant2 = B[0][0] * B[1][1] - B[0][1] * B[1][0];
                printf("The determinant of the second matrix is: %d\n", determinant2);
            } 
            else if(n == 3 && m == 3){
                // Perform matrix determinant of the first matrix
                int determinant = A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1]) - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0]) + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]);
                printf("The determinant of the first matrix is: %d\n", determinant);
                int determinant2 = B[0][0] * (B[1][1] * B[2][2] - B[1][2] * B[2][1]) - B[0][1] * (B[1][0] * B[2][2] - B[1][2] * B[2][0]) + B[0][2] * (B[1][0] * B[2][1] - B[1][1] * B[2][0]);
                printf("The determinant of the second matrix is: %d\n", determinant2);
            }
            else {
                printf("Determinant can only be calculated for 2x2 & 3x3 matrices.\n");
            }
            break;
        default:
            printf("Invalid operation number.\n");
    }
    printf("Thank you for using the matrix calculator!\n");
    
    return 0;
}