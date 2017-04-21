// structure Example

#include<stdio.h>
#include<string.h>

// Defining a structure-collection of dissimilar datatypes
struct Student 
{
	char name[500];
	int rollNumber;
};

int main()
{
	printf("\nStructure Example\n");

	//declaring a structure variable of student type
	struct Student s1;

	// Getting the values for member variables of structure through scanf
	printf("Enter a roll number:");
	scanf("%d",&s1.rollNumber);

	// Getting the values for member variables of structure through scanf
	printf("Enter a name:");
	scanf("%s",&s1.name);
	
	printf("\n You entered student roll number: %d and Name: %s",s1.rollNumber,s1.name);
}