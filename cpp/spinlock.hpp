#include <atomic>
#include "singleton.hpp"

namespace mybits
{

    class SpinLock : singleton<std::atomic_flag>
    {
    public:

        SpinLock(unsigned int key = 0) :
            _M_key(key)
        {
            auto _ = ATOMIC_FLAG_INIT;
            while (instance<decltype(_)::value_type>(key, ATOMIC_FLAG_INIT)
                    ->test_and_set(std::memory_order_acquire));
        }

        ~SpinLock()
        {
            instance(_M_key)->clear(std::memory_order_release);
        }

        SpinLock(const SpinLock&) = delete;

    private:
        unsigned int _M_key;
    };

} // namespace mybits

