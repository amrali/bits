/**
 * @section DESCRIPTION
 *
 * Unit tests for scope guard and scope guard chaining implementation.
 */

#define CATCH_CONFIG_MAIN

#include <vector>
#include <string>

#include "catch.hpp"
#include "scope_guard.hpp"

using namespace mybits;

TEST_CASE("Test Scope guard and scope chaining")
{
    int test_value = 0;

    auto a = make_scope_guard(
            [&] { test_value += 50; return 50; },
            [&] (auto  in) { test_value -= in; });

    scope_chain chain1; chain1(a);
    REQUIRE( test_value == 50 ); // value: 50
    REQUIRE( chain1.error_occurred == false );

    auto b = make_scope_guard(
            [&] { test_value += 200; return 200; },
            [&] (auto in) { test_value -= in; });

    scope_chain chain2; chain2(a, b);
    REQUIRE( test_value == 300 ); // value: 50 + a(50) + b(200)
    REQUIRE( chain2.error_occurred == false );

    auto c = make_scope_guard(
            [&]() -> int { throw 1; },
            [&] (auto) {});

    scope_chain chain3; chain3(a, b, c);
    REQUIRE( test_value == 300 ); // all changes were rolled back
    REQUIRE( chain3.error_occurred == true );

    auto d = make_scope_guard(
            [&] { test_value += 300; return 300; },
            [&] (auto in) { test_value -= in; });

    scope_chain chain4; chain4(a, b, c, d);
    REQUIRE( test_value == 300 ); // all changes were rolled back and `d` never ran
    REQUIRE( chain4.error_occurred == true );
}

TEST_CASE("Test practical example")
{
    using namespace std::string_literals;

    using NameManaPair = std::pair<std::string, int>;
    using NameLangPair = std::pair<std::string, std::string>;

    std::vector<NameManaPair> wizards_info;
    std::vector<NameLangPair> wizards_langs;

    // Reserve enough capacity to avoid invalidating iterators if reallocation
    // happens on insertion.
    wizards_info.reserve(5);
    wizards_langs.reserve(5);

    // Create two guards for two insertions into two vectors and return them.
    auto lazy_insert_wizard = [&] (auto name, auto mana, auto lang) {
        auto wiz_info = make_scope_guard(
                [&] { return wizards_info.emplace(std::begin(wizards_info), name, mana); },
                [&] (auto itr) { wizards_info.erase(itr); });

        auto wiz_lang = make_scope_guard(
                [&] { return wizards_langs.emplace(std::begin(wizards_langs), name, lang); },
                [&] (auto itr) { wizards_langs.erase(itr); });

        return std::make_pair(wiz_info, wiz_lang);
    };

    auto bob_guards = lazy_insert_wizard("bob"s, 42, "js"s);
    auto alice_guards = lazy_insert_wizard("alice"s, 420, "rust"s);

    scope_chain chain;

    // Chaining guards here will make sure that we either atomically
    // insert to all vectors or to none at all.
    chain(
            std::get<0>(bob_guards), std::get<1>(bob_guards),
            std::get<0>(alice_guards), std::get<1>(alice_guards));

    REQUIRE( wizards_info.size() == 2 );
    REQUIRE( wizards_langs.size() == 2 );

    // alice must come first since we emplace wizards at std::begin()
    REQUIRE( std::get<0>(wizards_info.at(0)) == "alice"s );
    REQUIRE( std::get<0>(wizards_info.at(1)) == "bob"s );
    REQUIRE( std::get<0>(wizards_langs.at(0)) == "alice"s );
    REQUIRE( std::get<0>(wizards_langs.at(1)) == "bob"s );
}
