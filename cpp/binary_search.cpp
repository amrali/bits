#include <iostream>

using namespace std;

template <typename T>
int binary_search(const T* space, const T& key, int imin, int imax)
{
	while (imax >= imin)
	{
		int imid = (imax - imin) >> 1;

		if (space[imid] < key)
			imin = imid + 1;
		else if (space[imid] > key)
			imax = imid - 1;
		else
			return imid;
	}
	return -1;
}

int
main()
{
	int a[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15};
	cout << binary_search(a, 2, 0, 14) << endl;
	return 0;
}

