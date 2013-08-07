#include <iostream>
#include <algorithm>

using namespace std;

template <typename T>
void
bubble_sort(T* array, int length)
{
	bool swapped = false;

	for (int i = 0; i < length; ++i)
	{
		if (i + 1 == length)
			break;

		if (array[i] > array[i + 1])
		{
			swapped = true;
			swap(array[i], array[i + 1]);
		}
	}

	if (swapped == true)
		bubble_sort(array, length);
}

template <typename T>
void
print_res(const T* array, int length)
{
	for (int i = 0; i < length; ++i)
	{
		cout << array[i];
		cout << " ";
	}
	cout << endl;
}

int
main()
{
	int a[] = {5,2,7,4,8,90,4,1,5,7,8};
	print_res(a, 11);
	bubble_sort(a, 11);
	print_res(a, 11);
	return 0;
}

