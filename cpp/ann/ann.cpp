#include "ann.hpp"

namespace mybits
{

    void
    Perceptron::stimulate(int value) noexcept
    {
        _M_val = value;
    }

} // namespace mybits
