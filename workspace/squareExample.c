// square Example
#include<stdio.h>

int main()
{
	//declaring a variable
	int n;
	printf("Enter a number for squaring: ");

	//reading the value and setting in variable using scanf
	scanf("%d",&n);
	int result;

	//calling square function
	result=square(n);

	printf("\nSquare of %d is %d",n,result);
	
}

//function taking parameter of 'int' type and return its square as 'int' type
int square(int number)
{
	return number*number;
}