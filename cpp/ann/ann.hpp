#ifndef MYBITS_ANN_HPP
#define MYBITS_ANN_HPP

#include "image.hpp"

namespace mybits
{

    struct Perceptron
    {
        Perceptron() = default;

        void stimulate(int) noexcept;

    private:
        int _M_val;
    };

} // namespace mybits

#endif // MYBITS_ANN_HPP
