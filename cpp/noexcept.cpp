#include <iostream>
#include <exception>

using namespace std;

struct A
{
    virtual void show() const
    {
        _show();
        cout << "show" << endl;
    }

    void _show() const noexcept
    {
        throw std::exception();
    }
};

int
main()
{
    try {
    A().show();
    } catch (...) {}
    return 0;
}
