#include <iostream>
#include <cstdint>

constexpr int32_t divisor = 20201227;

int32_t find_loop_size(const int32_t pk)
{
    constexpr int32_t subject_number = 7;
    int32_t start = 1;
    int32_t loop_counter = 0;
    while(start != pk)
    {
        start *= subject_number;
        start %= divisor;
        loop_counter++;
    }
    return loop_counter;
}

int64_t transform_subject_number(const int32_t subject_number, const int32_t loop_size)
{
    int64_t start = 1;
    for (int32_t i = 0; i < loop_size; i++){
        start *= subject_number;
        start %= divisor;
    }
    return start;
}

int32_t find_encryption_key(const int32_t pk_1, const int32_t pk_2)
{
    int32_t lc_1 = find_loop_size(pk_1);
    return transform_subject_number(pk_2, lc_1);
}


int32_t main() 
{
    constexpr int32_t pk_1 = 1327981;
    constexpr int32_t pk_2 = 2822615;
    std::cout << find_encryption_key(pk_1, pk_2) << std::endl;
    return 0;    
}