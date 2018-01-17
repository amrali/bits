#include <utility>
#include <cstdint>
#include <iostream>

using namespace std;

using collatz_t = uint64_t;

template <collatz_t N>
struct collatz
{
    void operator() (collatz_t start = 0) const noexcept
    {
        for (auto i = start; i < N; ++i) {
            auto res = is_collatz(i);
            if (1 != res)
                cout << res << endl;
        }
    }

    static collatz_t is_collatz(collatz_t start)
    {
        while (start != 1 and start != 0)
            start = (start % 2) == 0 ? start >> 1 : 3 * start + 1;

        return start;
    }
};

int main()
{
    collatz<100000>{}();
    return 0;
}
