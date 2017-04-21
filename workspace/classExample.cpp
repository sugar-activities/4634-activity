// class Example

#include<iostream>
#include<string.h>

using namespace std;

//defining 'student' class to hold roll number and name
class student
{
	// private members only accessible through member functions
	private:
		int rno;
		char name[500];

	//public members accessible through methods
	public:
		//Zero argument constructor
		student()
		{
			cout<<"\nZero argument constructor called for student";
		}
		//two argument constructor
		student(int rnoValue,char* nameValue)
		{
			cout<<"\nTwo argument constuctor called for student";
			this->rno=rnoValue;
			strcpy(this->name,nameValue);
		}
		//method to show the details of student
		void show()
		{
			cout<<"\nRoll Number: "<<this->rno;
			cout<<" Name: "<<this->name;
		}
};

//main function
int main()
{
	cout<<"\nClass Example";
	student s1(1,"ganesha");
	s1.show();
}
