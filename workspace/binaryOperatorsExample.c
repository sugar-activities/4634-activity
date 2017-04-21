// binary operators Example
#include<stdio.h>

int main()
{
	int a=1;

	// '<<' operator is used to shifting the bits to the left
	// bits of binary representation of a are shifted to two places to left side and assigned the value to b
	int b=a<<2;
	printf("\n Integer value of b=%d",b);
	printf("\n Binary value of b=");
	
	//invoking showbits function
	showbits(b);
}

// showbits function to print the binary representation of a number
void showbits(int n)
{
	int i,andmask,k;
	for(i=15;i>=0;i--)
	{
		andmask=1<<i;
		k=n&andmask;
		k==0?printf("0"):printf("1");
	}
}