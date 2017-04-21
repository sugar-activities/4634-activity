// Recursive Factorial Example

#include<stdio.h>

// main function which is the first function to be executed in the complete execution 
int main()
{
	int a=factorial(5);
	printf("\n%d!=%d",5,a);
}

// Recursive Factorial function with input parameter 'n' of integer type.
int factorial(int n)
{
	if(n==0)
	return 1;
	else
	return n*factorial(n-1);
}