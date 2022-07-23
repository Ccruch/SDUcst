#pragma once

#define hash_size 32  // 32*8=256-bit
namespace SM3 {
    typedef struct Context {
        unsigned int in_me_HASH[hash_size / 4];
        unsigned char message_block[64];  // 512-bit msg block
    }Context;
}