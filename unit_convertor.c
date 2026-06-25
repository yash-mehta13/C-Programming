#include <stdio.h>

int main(){
    printf("===== UNIT CONVERSION =====\n");
    printf("1. Length Conversion\n 2. Weight Conversion\n 3. Temperature Conversion\n 4. Speed Conversion\n 5. Time Conversion\n 6. Exit\n");

    int m, n;
    double value, result;
    printf("Enter your choice = ");
    scanf("%d", &m);

    switch(m){
        case 1:
        printf("=== Length Conversion ===\n");
        printf("1. Meter to Kilometer\n 2. Kilometer to Meter\n 3. Centimeter to Meter\n 4. Meter to Centimeter\n 5. Inch to Centimeter\n 6. Feet to Meter");
        printf("Enter your choice - conversion = ");
        scanf("%d\n", &n);
        switch(n){
            case 1:
                printf("Enter value in Meter: ");
                scanf("%lf", &value);
                result = value / 1000;
                printf("%.2lf Meter = %.2lf Kilometer\n", value, result);
                break;

            case 2:
                printf("Enter value in Kilometer: ");
                scanf("%lf", &value);
                result = value * 1000;
                printf("%.2lf Kilometer = %.2lf Meter\n", value, result);
                break;

            case 3:
                printf("Enter value in Centimeter: ");
                scanf("%lf", &value);
                result = value / 100;
                printf("%.2lf Centimeter = %.2lf Meter\n", value, result);
                break;

            case 4:
                printf("Enter value in Meter: ");
                scanf("%lf", &value);
                result = value * 100;
                printf("%.2lf Meter = %.2lf Centimeter\n", value, result);
                break;

            case 5:
                printf("Enter value in Inch: ");
                scanf("%lf", &value);
                result = value * 2.54;
                printf("%.2lf Inch = %.2lf Centimeter\n", value, result);
                break;

            case 6:
                printf("Enter value in Feet: ");
                scanf("%lf", &value);
                result = value * 0.3048;
                printf("%.2lf Feet = %.2lf Meter\n", value, result);
                break;

            default:
                printf("Invalid length conversion choice.\n");
                break;
        }
        break;

        case 2:
        printf("=== Weight Conversion ===\n");
        printf("1. Kilogram to Gram\n 2. Gram to Kilogram\n 3. Kilogram to Pound\n 4. Pound to Kilogram\n");
        printf("Enter your choice - conversion = ");
        scanf("%d", &n);

        //double value, result;

        switch(n){
            case 1:
                printf("Enter value in Kilogram: ");
                scanf("%lf", &value);
                result = value * 1000;
                printf("%.2lf Kilogram = %.2lf Gram\n", value, result);
                break;

            case 2:
                printf("Enter value in Gram: ");
                scanf("%lf", &value);
                result = value / 1000;
                printf("%.2lf Gram = %.2lf Kilogram\n", value, result);
                break;

            case 3:
                printf("Enter value in Kilogram: ");
                scanf("%lf", &value);
                result = value * 2.20462;
                printf("%.2lf Kilogram = %.2lf Pound\n", value, result);
                break;

            case 4:
                printf("Enter value in Pound: ");
                scanf("%lf", &value);
                result = value / 2.20462;
                printf("%.2lf Pound = %.2lf Kilogram\n", value, result);
                break;

            default:
                printf("Invalid weight conversion choice.\n");
                break;
        }
        break;

        case 3:
        printf("=== Temperature Conversion ===\n");
        printf("1. Celsius to Fahrenheit\n 2. Fahrenheit to Celsius\n 3. Celsius to Kelvin\n 4. Kelvin to Celsius\n");
        printf("Enter your choice - conversion = ");
        scanf("%d", &n);

        //double value, result;

        switch(n){
            case 1:
                printf("Enter value in Celsius: ");
                scanf("%lf", &value);
                result = (value * 9 / 5) + 32;
                printf("%.2lf Celsius = %.2lf Fahrenheit\n", value, result);
                break;

            case 2:
                printf("Enter value in Fahrenheit: ");
                scanf("%lf", &value);
                result = (value - 32) * 5 / 9;
                printf("%.2lf Fahrenheit = %.2lf Celsius\n", value, result);
                break;

            case 3:
                printf("Enter value in Celsius: ");
                scanf("%lf", &value);
                result = value + 273.15;
                printf("%.2lf Celsius = %.2lf Kelvin\n", value, result);
                break;

            case 4:
                printf("Enter value in Kelvin: ");
                scanf("%lf", &value);
                result = value - 273.15;
                printf("%.2lf Kelvin = %.2lf Celsius\n", value, result);
                break;

            default:
                printf("Invalid temperature conversion choice.\n");
                break;
        }
        break;

        case 4:
        printf("=== Speed Conversion ===\n");
        printf("1. Kilometer/hour to Meter/second\n 2. Meter/second to Kilometer/hour\n 3. Miles/hour to Kilometer/hour\n");
        printf("Enter your choice - conversion = ");
        scanf("%d", &n);

        //double value, result;

        switch(n){
            case 1:
                printf("Enter value in Kilometer/hour: ");
                scanf("%lf", &value);
                result = value * 5 / 18;
                printf("%.2lf Kilometer/hour = %.2lf Meter/second\n", value, result);
                break;

            case 2:
                printf("Enter value in Meter/second: ");
                scanf("%lf", &value);
                result = value * 18 / 5;
                printf("%.2lf Meter/second = %.2lf Kilometer/hour\n", value, result);
                break;

            case 3:
                printf("Enter value in Miles/hour: ");
                scanf("%lf", &value);
                result = value * 1.60934;
                printf("%.2lf Miles/hour = %.2lf Kilometer/hour\n", value, result);
                break;

            default:
                printf("Invalid speed conversion choice.\n");
                break;
        }
        break;

        case 5:
        printf("=== Time Conversion ===\n");
        printf("1. Seconds to Minutes\n 2. Minutes to Seconds\n 3. Minutes to Hours\n 4. Hours to Minutes\n");
        printf("Enter your choice - conversion = ");
        scanf("%d", &n);

        //double value, result;

        switch(n){
            case 1:
                printf("Enter value in Seconds: ");
                scanf("%lf", &value);
                result = value / 60;
                printf("%.2lf Seconds = %.2lf Minutes\n", value, result);
                break;

            case 2:
                printf("Enter value in Minutes: ");
                scanf("%lf", &value);
                result = value * 60;
                printf("%.2lf Minutes = %.2lf Seconds\n", value, result);
                break;

            case 3:
                printf("Enter value in Minutes: ");
                scanf("%lf", &value);
                result = value / 60;
                printf("%.2lf Minutes = %.2lf Hours\n", value, result);
                break;

            case 4:
                printf("Enter value in Hours: ");
                scanf("%lf", &value);
                result = value * 60;
                printf("%.2lf Hours = %.2lf Minutes\n", value, result);
                break;

            default:
                printf("Invalid time conversion choice.\n");
                break;
        }
        break;

        case 6:
        printf("Exiting the Unit Converter Program.\n");
        break;

        default:
        printf("Invalid main menu choice.\n");
        break;
    }

    return 0;
}