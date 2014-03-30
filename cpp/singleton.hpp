#include <atomic>
#include <memory>
#include <unordered_map>

#define unlikely(x) __builtin_expect(!!(x), 0)

namespace mybits
{

    template <typename Tp, typename Key = unsigned int>
    class singleton
    {
    public:
        typedef std::shared_ptr<Tp> Tp_ptr;

        template <typename... Args>
        inline static Tp_ptr&
        instance(Key key, Args... args)
        {
            while(_S_lock.test_and_set(std::memory_order_acquire));
            auto itr = _Sp_map.find(key);

            if (unlikely(itr == _Sp_map.end())) {
                auto& ptr = _Sp_map[key] = Tp_ptr(new Tp(args...));
                _S_lock.clear(std::memory_order_release);
                return ptr;
            }

            _S_lock.clear(std::memory_order_release);
            return itr->second;
        }

    private:
        static std::atomic_flag _S_lock;
        static std::unordered_map<Key, Tp_ptr> _Sp_map;
    };

    template <typename Tp, typename Key>
    std::atomic_flag singleton<Tp, Key>::_S_lock = ATOMIC_FLAG_INIT;

    template <typename Tp, typename Key>
    std::unordered_map<Key, typename singleton<Tp, Key>::Tp_ptr>
    singleton<Tp, Key>::_Sp_map;

} // namespace mybits

