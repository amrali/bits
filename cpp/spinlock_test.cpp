#include <iostream>
#include <thread>
#include <vector>

#include "spinlock.hpp"

using namespace std;

void f(int n)
{
    mybits::SpinLock sl;
    cout << "Output from thread " << n << endl;
}

int
main()
{
    // GCC 4.8.1 bug: use -Wl,--no-as-needed with -pthread to enable threading
    vector<std::thread> v;

    for (int n = 0; n < 20; ++n)
        v.emplace_back(f, n);

    for (auto& t : v)
        t.join();

    return 0;
}
