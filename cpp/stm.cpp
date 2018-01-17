#include <iostream>
#include <vector>
#include <unordered_map>

#define __purify(name, args...) \
    __attribute__((transaction_pure)) void __throw_##name(args) __attribute__((__noreturn__));

namespace std __attribute__((__visibility__("default")))
{
//    __purify(bad_exception, void);
//    __purify(bad_alloc, void);
//    __purify(bad_cast, void);
//    __purify(bad_typeid, void);
//    __purify(logic_error, const char*);
//    __purify(domain_error, const char*);
//    __purify(invalid_argument, const char*);
//    __purify(length_error, const char*);
//    __purify(out_of_range, const char*);
//    __purify(out_of_range_fmt, const char*, ...);
//    __purify(runtime_error, const char*);
//    __purify(range_error, const char*);
//    __purify(overflow_error, const char*);
//    __purify(underflow_error, const char*);
//    __purify(ios_failure, const char*);
//    __purify(system_error, int);
//    __purify(future_error, int);
//    __purify(bad_function_call)

//    template<class _Key, class _Tp,
//        class _Hash,
//        class _Pred,
//        class _Alloc> class __attribute__((transaction_safe)) unordered_map;

//    template<typename _Key, typename _Value,
//        typename _Alloc,
//        typename _ExtractKey,
//        typename _Equal,
//        typename _H1,
//        typename _H2,
//        typename _Hash,
//        typename _RehashPolicy,
//        typename _Traits> class __attribute__((transaction_safe)) _Hashtable;

namespace __detail
{

//    auto ____need_rehash_backup = &_Prime_rehash_policy::_M_need_rehash;
//
//    __attribute__((transaction_unsafe))
//    pair<bool, size_t> _Prime_rehash_policy::_M_need_rehash(size_t __n_bkt, size_t __n_elt, size_t __n_ins) const
//    { return (this->*____need_rehash_backup)(__n_bkt, __n_elt, __n_ins); }

} // namespace __detail

} // namespace std

using namespace std;

int main()
{
    vector<int> list(5);
    unordered_map<int, int> uno_map;

    auto list_insert = [&]() __attribute__((transaction_safe)) { list.push_back(1); };

    __transaction_atomic {
        //uno_map[5] = 3;
        //insert_new(uno_map);
        //uno_map.insert(make_pair(5,3));
        //list.push_back(1);
        list[0] = 1;
        //__transaction_cancel;
    }

    cout << "list size: " << list.size() << endl;
    for (auto i = list.begin(); i != list.end(); ++i)
        cout << "list: " << *i;
    cout << endl;

    cout << "map[5]: " << uno_map[5] << endl;

    return 0;
}
