#include <iostream>

using namespace std;

struct param_t
{
    unsigned char mox2 : 4, we : 4;
};

int main()
{
    unsigned int val = 0xf1;
    param_t a = *reinterpret_cast<param_t*>(&val);
    cout << val << endl;
    cout << (unsigned int)a.mox2 << endl;
    cout << (unsigned int)a.we << endl;
    cout << (unsigned int)*reinterpret_cast<unsigned char*>(&a) << endl;
    return 0;
}
