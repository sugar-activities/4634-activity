#include<iostream>
#include<string.h>

using namespace std;

//Defining a clas vehicle; This class is acting as base class for 'car' derived class
class vehicle
{
	// private members only accessible through member functions
	private:
		int id;
		char name[500];

	//public members accessible through methods
	public:
		// Zero argument constructor
		vehicle()
		{}
		//two argument constructor
		vehicle(int idValue,char* nameValue)
		{
			this->id=idValue;
			strcpy(this->name,nameValue);
		}
		//method to display values in member variables
		void show()
		{
			cout<<"\nId: "<<this->id;
			cout<<" Name: "<<this->name;
		}
};

//class 'car' is derived from 'vehicle' base class; vehicle class is publicly inherited
class car:public vehicle
{
	// private members only accessible through member functions
	private:
		char type[300];

	//public members accessible through methods
	public:
		// Zero argument constructor
		car()
		{}
		//three argument constructor. This constructor calls constructor of base class as well by passing parameters to it.
		car(int idValue,char* name,char* typeValue):vehicle(idValue,name)
		{
			strcpy(this->type,typeValue);
		}
		//method to display car details
		void showCar()
		{
			this->show();
			cout<<" Type:"<<this->type;
		}
};

//main function
int main()
{
	cout<<"\nInheritance Example";

	//creating instance of car class
	car c1(1,"Ferrari","Sports");
	c1.showCar();
	
}
