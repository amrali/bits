#include <iostream>
#include <algorithm>

using namespace std;

template <typename T>
void
selection_sort(T* array, int length)
{
	for (int j = 0; j < length - 1; ++j)
	{
		int imin = j;

		for (int i = j + 1; i < length; ++i)
		{
			if (array[i] < array[imin])
				imin = i;
		}

		if (imin != j)
			swap(array[j], array[imin]);
	}
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
	int a[] = {5,2,7,4,8,90,4,1,5,6,8};
	print_res(a, 11);
	selection_sort(a, 11);
	print_res(a, 11);
	return 0;
}

