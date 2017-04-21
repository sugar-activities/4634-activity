// tertiary operators Example
#include<stdio.h>

int main()
{
	int a;
	
	//asking you to enter a number
	printf("\nEnter a number: ");
	//setting the value of a using scanf
	scanf("%d",&a);

	// (expression1)?(statement1):(statement2)
	// if expression before '?' evaluates to true then statement1 is executed else statement2 is executed
	a>=5?printf("\n a is greater than or equal to 5"):printf("\n a is less than 5");

	
}

