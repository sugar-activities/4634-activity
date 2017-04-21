//switch-case Example

#include<stdio.h>

int main()
{
	//defining a variable
	int a=2;
	
	//using switch statement to control the decision flow
	switch  (a)
	{
		// if value of expression given with switch evaluates to 1
		case 1:
		printf("a is 1"); 
		break;
	
		// if value of expression given with switch evaluates to 2
		case 2:
		printf("a is 2");
		break;
		
		// if value of expression given with switch evaluates to 3
		case 3:
		printf("a is 3");
		break;

		// if value of expression given with switch evaluates to something else other than 1,2 and 3
		default:
		printf("I don't know what is the value of a");
	}
}