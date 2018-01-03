/**
 * @section DESCRIPTION
 *
 * A set of TMP tools.
 */

#ifndef META_HPP
#define META_HPP

#include <utility>
#include <type_traits>

namespace std
{

    // A pair-generic std::hash specialization. Hopefully this will either be
    // unnecessary, more flexible, or causes more readable errors for disabled
    // specializations in C++17/C++20.

    template <class T, class U>
    struct hash<pair<T, U>>
    {
        using argument_type = pair<T, U>;
        using result_type = size_t;

        result_type operator() (const argument_type& t) const
        {
            result_type const h1 ( hash<T>{}(t.first) );
            result_type const h2 ( hash<U>{}(t.second) );

            return h1 ^ (h2 << 2);
        }
    };

} // namespace std

namespace mybits
{

    // apply_at(Tuple, Index, Functor) is a function to apply a functor on
    // elements in a tuple at a specific index. In C++17 a much simpler version
    // of this will be possible due to std::apply.

    template <size_t N>
    struct apply_tuple
    {
        template <class Tuple, class Functor>
        static void apply(Tuple&& tuple, size_t n, Functor&& func)
        {
            if (N - 1 != n)
                apply_tuple<N - 1>::apply(
                        std::forward<Tuple>(tuple), n, std::forward<Functor>(func));
            else
                std::forward<Functor>(func)(n,
                        std::get<N - 1>(std::forward<Tuple>(tuple)));
        }

    };

    template <>
    struct apply_tuple<0>
    {
        template <class Tuple, class Functor>
        static void apply(Tuple&, size_t, Functor)
        {
            return;
        }
    };

    template <class Functor, class ...Ts>
    void apply_at(std::tuple<Ts...>& tuple, size_t idx, Functor&& func)
    {
        apply_tuple<sizeof...(Ts)>::apply(
                tuple, idx, std::forward<Functor>(func));
    }

} // namespace mybits

#endif // META_HPP
