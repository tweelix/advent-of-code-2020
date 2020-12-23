#include <algorithm>
#include <iostream>
#include <list>
#include <numeric>
#include <vector>

std::list<int> simulate_game(std::list<int> initial_game_state,
                             unsigned steps)
{
    int max_value =
        *std::max_element(initial_game_state.cbegin(), initial_game_state.cend());
    std::vector<std::list<int>::iterator> positions;
    positions.resize(initial_game_state.size());
    for (auto it = initial_game_state.begin(); it != initial_game_state.end();
         it++)
    {
        positions[*it - 1] = it;
    }
    std::list<int> hand;
    for (unsigned i = 0; i < steps; i++)
    {
        int target_cup = (*initial_game_state.begin()) - 1;
        target_cup = target_cup == 0 ? max_value : target_cup;
        auto hand_range_start = std::next(initial_game_state.cbegin());
        auto hand_range_end = std::next(hand_range_start, 3);

        hand.splice(hand.cbegin(), initial_game_state, hand_range_start,
                    hand_range_end);
        while (std::find(hand.cbegin(), hand.cend(), target_cup) != hand.cend())
            target_cup = target_cup == 1 ? max_value : target_cup - 1;

        auto target_cup_it = positions[target_cup - 1];
        initial_game_state.splice(std::next(target_cup_it), hand);
        for (int j = 1; j <= 3; j++)
        {
            positions[*std::next(target_cup_it, j) - 1] = std::next(target_cup_it, j);

        }

        initial_game_state.splice(initial_game_state.end(), initial_game_state, initial_game_state.begin());
        positions[initial_game_state.back() - 1] = std::prev(initial_game_state.end());
    }
    return initial_game_state;
}

int main()
{
    constexpr std::array<int, 9> game_state = {9, 5, 2, 4, 3, 8, 7, 1, 6};

    std::list<int> game_state_list = {};
    for (const auto e : game_state)
    {
        game_state_list.push_back(e);
    }
    auto result_array = simulate_game(game_state_list, 100);
    std::rotate(result_array.begin(),
                std::find(result_array.begin(), result_array.end(), 1),
                result_array.end());
    std::cout << "Task 1: ";
    for (auto i = std::next(result_array.cbegin()); i != result_array.cend();
         i++)
    {
        std::cout << *i;
    }
    std::cout << std::endl;

    for (int i = *std::max_element(game_state.cbegin(), game_state.cend()) + 1;
         i <= 1000000; i++)
    {
        game_state_list.push_back(i);
    }
    auto return_list = simulate_game(game_state_list, 10000000);

    auto it_1 = std::find(return_list.cbegin(), return_list.cend(), 1);
    auto lo1_1 =
        it_1 == return_list.cend() ? return_list.cbegin() : std::next(it_1);
    auto lo1_2 =
        lo1_1 == return_list.cend() ? return_list.cbegin() : std::next(lo1_1);
    long val1 = *lo1_1;
    long val2 = *lo1_2;
    std::cout << "Task 2: " << val1 * val2 << std::endl;
}