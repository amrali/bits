#include <iostream>
#include <string>
#include <cstring>
#include <cstdint>
#include <utility>
using namespace std;

int main() {
    static char k = '\x00';
    const char* a = new char[32];

    memcpy(const_cast<char*>(a), "ece73f1dd0285dcf13d240f75205c406P&\373\031", 36);

    swap(k, const_cast<char&>(a[16]));
    uint64_t hi = stoull(a, nullptr, 16);
    cout << hi << endl;

    swap(k, const_cast<char&>(a[16]));
    swap(k, const_cast<char&>(a[32]));
    uint64_t lo = stoull(&a[16], nullptr, 16);
    cout << lo << endl;
    return 0;
}
