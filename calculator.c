#include <stdio.h>
#include <math.h>

int main(){
    int a, b;
    printf("Enter a & b : ");
    scanf("%d %d", &a, &b);

    int c;
    printf("Enter the operation no. = ");
    scanf("%d", &c);

    int sum = a + b;
    int minus = a - b;
    double Multiply = a * b;
    double divide = a / b;
    double exponential = pow(a,b);
    double square_root = sqrt(b);
    double sine = sin(a);
    double cos_cos = cos(b);
    double logarithemic = log(a);

    switch(c){
        case 1:
        printf("Sum = %d\n", sum);
        break;

        case 2:
        printf("minus = %d\n", minus);
        break;

        case 3:
        printf("Multiply = %lf\n", Multiply);
        break;

        case 4:
        printf("Division = %lf\n", divide);
        break;

        case 5:
        printf("exponential = %lf\n", exponential);
        break;

        case 6:
        printf("square root = %lf\n", square_root);
        break;

        case 7:
        printf("Sine = %lf\n", sine);
        break;

        case 8:
        printf("Cos = %lf\n", cos);
        break;

        case 9:
        printf("Log = %lf\n", logarithemic);
        break;

        default:
        printf("Invalid operation\n");
        break;
    }

}