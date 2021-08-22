#include <iostream>

template <typename T>
class PooClass
{
	T* ptr;

	void add()
	{
		*ptr += 3;
	}
};

int main(char* argsv[], int argsc)
{
	int ints[30] = { 1, 2, 3 };

	for (int i = 0; i < 30; ++i)
		ints[i] = 30 - ints[i] * 2;

	char* str = "Test string\n";

	char* raw = R"(
	THIS
	IS A
	RAW STRING)";

	struct poop
	{
		int a, b;
	};

	return 0;
}