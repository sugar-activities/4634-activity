//Looping Example

#include<stdio.h>

// main function which is the first function to be executed in the complete execution 
int main()
{
	//invocation to function with 'for' loop
	forLoopFunction();
	//invocation to function with 'while' loop
	whileLoopFunction();
	//invocation to function with 'do-while' loop
	doWhileLoopFunction();
}

// function with 'for' loop
void forLoopFunction()
{
	printf("\nInside for loop function");
	int i=1;
	for(i=1;i<=10;i++)
	{
		printf("\ni=%d",i);
	}
}

//function with 'while' loop
void whileLoopFunction()
{
	printf("\nInside while loop function");
	int i=0;
	while(i<=10)
	{
		printf("\ni=%d",i);
		i++;
	}
}

//function with 'do-while' loop
void doWhileLoopFunction()
{
	printf("\nInside do-while loop function");
	int i=0;
	do
	{
		printf("\ni=%d",i);
		i++;
	}while(i<=10);
}

