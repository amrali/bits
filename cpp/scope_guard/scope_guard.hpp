/**
 * @section DESCRIPTION
 *
 * A scope guard implementation to help with situations where RAII
 * is not a viable solution.
 */

#ifndef SCOPE_GUARD_HPP
#define SCOPE_GUARD_HPP

#include <utility>
#include <exception>
#include <type_traits>

#include "meta.hpp"

namespace mybits
{

    // scope_guard

    template <class Scope, class Cleaner>
    struct scope_guard
    {

        using scope_return_type = typename std::result_of<Scope()>::type;
        static_assert(not std::is_void<scope_return_type>{},
                "Scope: return type cannot be void");

        scope_guard(Scope&& scope, Cleaner&& cleaner, bool run = false) :
            _M_scope(std::forward<Scope>(scope)),
            _M_cleaner(std::forward<Cleaner>(cleaner))
        {
            if (run)
                execute();
        }

        virtual ~scope_guard() noexcept
        {
            if (std::uncaught_exception())
                rollback();
        }

        void execute()
        {
            _M_scope_retval = _M_scope();
        }

        void rollback() noexcept
        {
            _M_cleaner(_M_scope_retval);
        }

    private:
        typename std::remove_reference<Scope>::type _M_scope;
        typename std::remove_reference<Cleaner>::type _M_cleaner;
        typename std::remove_reference<scope_return_type>::type _M_scope_retval;
    };

    // Syntactic sugar, class template argument type inference from constructors
    // is supported in C++17.
    template <class Scope, class Cleaner>
    scope_guard<Scope, Cleaner> make_scope_guard(
            Scope&& scope, Cleaner&& cleaner, bool run = false)
    {
        return scope_guard<Scope, Cleaner>(
                std::forward<Scope>(scope), std::forward<Cleaner>(cleaner), run);
    }

    // scope_chain

    struct scope_chain
    {

        bool error_occurred = false;

        template <class ...Guards>
        void operator() (Guards&& ...guards)
        {
            std::tuple<Guards...> t_guards{std::forward<Guards>(guards)...};
            const auto t_size = std::tuple_size<decltype(t_guards)>{};

            for (size_t i = 0; i < t_size; ++i)
            {
                try {
                    apply_at(t_guards, i,
                            [] (auto, auto& guard) { guard.execute(); });
                } catch (...) {
                    // Rollback all previously executed guards if one fails
                    for (size_t r = 0; r < i; ++r)
                        apply_at(t_guards, r,
                                [] (auto, auto& guard) { guard.rollback(); });

                    // Stop executing more guards
                    error_occurred = true;
                    break;
                }
            }
        }

    };

} // namespace mybits

#endif // SCOPE_GUARD_HPP
