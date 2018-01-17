#include <iostream>
#include <functional>
#include <utility>
#include <unordered_map>

// this works with c++14 only.

template <class Tp, class ...Params>
struct TupleKeyHash
{
    size_t operator() (const Tp& value) const
    {
        std::index_sequence_for<Params...> index;
        size_t result = 0;

        for (auto& i : index()) {
            auto& val = std::get<i>(value);
            result += std::hash<decltype<val>>()(val);
        }

        return result;
    }
};

template <class ReturnType, class ...Args>
std::function<ReturnType (Args...)> memoize(std::function<ReturnType (Args...)> func)
{
    return [=](Args... args) mutable {
        static std::unordered_map<std::tuple<Args...>, ReturnType,
            TupleKeyHash<std::tuple<Args...>, Args...> > cache;
        std::tuple<Args...> t(args...);

        auto cache_itr = cache.find(t);

        if (cache_itr == cache.end()) {
            auto result = func(args...);
            cache[t] = result;

            return result;
        }

        return cache_itr->second;
    };
}

int adder(int a, int b)
{
    std::cout << a << " + " << b << " = " << a + b << std::endl;
    return a + b;
}

int main() {
    auto add = memoize(std::function<decltype(adder)>(adder));
    std::cout << add(1, 2) << std::endl;
    std::cout << add(3, 4) << std::endl;
    std::cout << add(1, 2) << std::endl;
    // your code goes here
    return 0;
}
