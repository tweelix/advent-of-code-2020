#include <fstream>
#include <iostream>
#include <vector>
#include <string_view>
#include <unordered_set>
#include <algorithm>
#include <constexpr_map.h>

enum class OpCodes
{
    acc,
    jmp,
    nop
};

using namespace std::literals::string_view_literals;
static constexpr std::array<std::pair<std::string_view, OpCodes>, 3> opcode_values{
    {{"acc"sv, OpCodes::acc},
     {"jmp"sv, OpCodes::jmp},
     {"nop"sv, OpCodes::nop}}};

static constexpr auto code_lookup = Map<std::string_view, OpCodes, opcode_values.size()>{{opcode_values}};

struct Instruction
{
    OpCodes op_code;
    int value;
};
typedef std::vector<Instruction> Program;
struct LoopTestResults
{
    bool has_loop;
    int acc;
};

LoopTestResults has_infinite_loop(Program const &program)
{
    unsigned program_counter{};
    int acc{};
    std::unordered_set<unsigned> visited;
    while (program_counter < program.size())
    {
        if (visited.contains(program_counter))
        {
            return {true, acc};
        }
        visited.insert(program_counter);

        switch (program[program_counter].op_code)
        {
        case OpCodes::nop:
            break;
        case OpCodes::jmp:
            program_counter += program[program_counter].value;
            continue;
        case OpCodes::acc:
            acc += program[program_counter].value;
        }
        program_counter++;
    }
    return {false, acc};
}

int bruteforce_program_until_it_works(Program program)
{
    LoopTestResults result;
    for (auto &instruction : program)
    {
        switch (instruction.op_code)
        {
        case OpCodes::nop:
            instruction.op_code = OpCodes::jmp;
            result = has_infinite_loop(program);
            if (!result.has_loop)
            {
                return result.acc;
            }
            instruction.op_code = OpCodes::nop;
            break;
        case OpCodes::jmp:
            instruction.op_code = OpCodes::nop;
            result = has_infinite_loop(program);
            if (!result.has_loop)
            {
                return result.acc;
            }
            instruction.op_code = OpCodes::jmp;
            break;
        case OpCodes::acc:
            break;
        }
    }
    return -1;
}

int main()
{
    std::ifstream infile("input");
    Program program;
    std::string op_code;
    int a;
    while (infile >> op_code >> a)
    {
        program.emplace_back(Instruction{code_lookup.at(op_code), a});
    }
    std::cout << "Task 1: " << has_infinite_loop(program).acc << std::endl;
    std::cout << "Task 2: " << bruteforce_program_until_it_works(program) << std::endl;
}