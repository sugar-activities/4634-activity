// fibbonaci series Example

#include<stdio.h>

int main()
{
	int num;

	// asking for length of fibbonaci series you want to display
	printf("Enter the number of numbers you want to see from Fibbonaci Series: ");
	scanf("%d",&num);

	//invoking the fibbonaci function
	fibbonaci(num);
}

// fibbonaci function that prints the fibbonaci series
void fibbonaci(int n)
{
	int a=1;
	int b=1;
	int c,j;
	for(j=1;j<=n;j++)
	{
		printf("\n%d",a);
		c=a+b;
		a=b;
		b=c;
	}
}