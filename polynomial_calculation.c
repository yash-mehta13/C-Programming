#include <stdio.h>
#include <math.h>

int main() {
    int degree1, degree2;
    printf("Enter the degree of the polynomial1: ");
    scanf("%d", &degree1);
    printf("Enter the degree of the polynomial2: ");
    scanf("%d", &degree2);
    
    int coefficients1[degree1 + 1];
    printf("Enter the coefficients of the polynomial1 (from highest degree to constant term):\n");
    for(int i = 0; i <= degree1; i++) {
        scanf("%d", &coefficients1[i]);
    }
    int coefficients2[degree2 + 1];
    printf("Enter the coefficients of the polynomial2 (from highest degree to constant term):\n");
    for(int i = 0; i <= degree2; i++) {
        scanf("%d", &coefficients2[i]);
    }
    int x;
    printf("Enter the value of x: ");
    scanf("%d", &x);
    
    int result1 = 0;
    int result2 = 0;
    int result = 0;
    for(int i = 0; i <= degree1; i++) {
        result1 += coefficients1[i] * pow(x, degree1 - i);
    }
    for(int i = 0; i <= degree2; i++) {
        result2 += coefficients2[i] * pow(x, degree2 - i);
    }

    result = result1 + result2;
    
    printf("The value of result at x = %d is: %d\n", x, result);
    
    return 0;
}