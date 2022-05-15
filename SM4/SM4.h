#pragma once


#define SM4_ENCRYPT 1//加密标志
#define SM4_DECRYPT 0//解密标志

struct sm4Context
{
	int mode;//选择加密/解密mode
	unsigned long sk[32];//subkey:32个轮密钥
};



/* 加密的context设置：mode确定是加密enc，轮密钥调用密钥扩展算法生成
*\param  ctx <sm4Context*>             一次sm4的上下文
*        key <unsigned char[16]>       这次的主密钥
*/
void sm4Setkey_Enc(sm4Context* ctx, unsigned char key[16]);



/* 解密的context设置：mode确定是解密dec，轮密钥调用密钥扩展算法生成
*\param  ctx <sm4Context*>            一次sm4的上下文
*        key <unsigned char[16]>      这次的主密钥
*/
void sm4Setkey_Dec(sm4Context* ctx, unsigned char key[16]);



/* 一轮sm4
*\param  SK                           32个轮密钥
*        plain                        明文
*        cipher                       密文
*/
void sm4_1_Round(unsigned long SK[32], unsigned char plain[16], unsigned char cipher[16]);


/* ecb模式
 *\param  SK      32个轮密钥
 *        input   输入
 *        output  输出
 *        length  长度
 */
void sm4_ecb(unsigned long SK[32], unsigned char* input, unsigned char* output, unsigned long length);


/* 循环展开 内部2次 的ecb */
void sm4_ecb_LoopUnRoll2(unsigned long SK[32], unsigned char* input, unsigned char* output, unsigned long length);

/* 循环展开 内部4次 的ecb */
void sm4_ecb_LoopUnRoll4(unsigned long SK[32], unsigned char* input, unsigned char* output, unsigned long length);

/* 循环展开 内部8次 的ecb */
void sm4_ecb_LoopUnRoll8(unsigned long SK[32], unsigned char* input, unsigned char* output, unsigned long length);

/* 循环展开 内部16次 的ecb */
void sm4_ecb_LoopUnRoll16(unsigned long SK[32], unsigned char* input, unsigned char* output, unsigned long length);


/* 展示的函数 */
void shower(unsigned char* show, unsigned long len);


/* 初始化数组 */
void init(unsigned char* arr, int len);


/* 加密的context设置：mode确定是加密enc，轮密钥调用密钥扩展算法生成  simd
*\param  ctx <sm4Context*>       一次sm4的上下文
*        key <unsigned char[16]> 这次的主密钥
*/
void sm4Setkey_Enc_SIMD(sm4Context* ctx, unsigned char key[16]);


/* 解密的context设置：mode确定是解密dec，轮密钥调用密钥扩展算法生成  simd
*\param  ctx <sm4Context*>       一次sm4的上下文
*        key <unsigned char[16]> 这次的主密钥
*/
void sm4Setkey_Dec_SIMD(sm4Context* ctx, unsigned char key[16]);

/* 一轮sm4 simd
*\param  SK   32个轮密钥
*        plain 明文
*        cipher 密文
*/
void sm4_1_Round_SIMD(unsigned long SK[32], unsigned char plain[16], unsigned char cipher[16]);

/* ecb模式   simd
 *\param  SK      32个轮密钥
 *        input   输入
 *        output  输出
 *        length  长度
 */
void sm4_ecb_SIMD(unsigned long SK[32], unsigned char* input, unsigned char* output, unsigned long length);