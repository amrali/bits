/**
 * @section DESCRIPTION
 *
 * Unit tests for template metaprogramming tools.
 */

#define CATCH_CONFIG_MAIN

#include <utility>
#include <unordered_map>

#include "catch.hpp"
#include "meta.hpp"

using namespace mybits;

TEST_CASE("Test tuple applicator")
{
    auto tuple = std::make_tuple(10, 20, 55);

    size_t i;
    std::tuple_element_t<0, decltype(tuple)> a;
    std::tuple_element_t<1, decltype(tuple)> b;
    std::tuple_element_t<2, decltype(tuple)> c;

    apply_at(tuple, 0, [&](auto idx, auto& item) { i = idx; a = item; });
    REQUIRE( a == std::get<0>(tuple) );
    REQUIRE( i == 0 );

    apply_at(tuple, 1, [&](auto idx, auto& item) { i = idx; b = item; });
    REQUIRE( b == std::get<1>(tuple) );
    REQUIRE( i == 1 );

    apply_at(tuple, 2, [&](auto idx, auto& item) { i = idx; c = item; });
    REQUIRE( c == std::get<2>(tuple) );
    REQUIRE( i == 2 );
}

TEST_CASE("Test pair-generic std::hash specialization")
{
    std::unordered_map<std::pair<int, int>, int> k = {
        {{1, 2}, 3}
    };
}
