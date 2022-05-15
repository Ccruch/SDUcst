#include "sm4.h"
#include <string.h>
#include<iostream>
#include<time.h>
using namespace std;
const int M = 1000;
const int N = 16 * M;
const int len = 128;
unsigned char plain1[N];
unsigned char cipher1[N];
unsigned char plainFromDec1[N];
unsigned char plain2[N];
unsigned char cipher2[N];
unsigned char plainFromDec2[N];
unsigned char plain4[N];
unsigned char cipher4[N];
unsigned char plainFromDec4[N];
unsigned char plain8[N];
unsigned char cipher8[N];
unsigned char plainFromDec8[N];
unsigned char plain16[N];
unsigned char cipher16[N];
unsigned char plainFromDec16[N];
int main()
{
	cout << "循环次数：" << M << endl;
	cout << "=========平凡SM4========\n";
	unsigned char key[16] = { 0x01,0x23,0x45,0x67,0x89,0xab,0xcd,0xef,0xfe,0xdc,0xba,0x98,0x76,0x54,0x32,0x10 };
	unsigned char plain[16] = { 0x01,0x23,0x45,0x67,0x89,0xab,0xcd,0xef,0xfe,0xdc,0xba,0x98,0x76,0x54,0x32,0x10 };
	unsigned char cipher[16];
	unsigned char plainFromDec[16];
	sm4Context ctx;
	sm4Context ctx2;
	clock_t start, end;
	init(plain1, N);
	init(plain2, N);
	init(plain4, N);
	init(plain8, N);
	init(plain16, N);
	/* 1.加密测试 */
	sm4Setkey_Enc(&ctx, key);
	start = clock();
	for (int I = 0; I < M; I++)
	{
		sm4_1_Round(ctx.sk, plain, cipher);
	}
	end = clock();
	cout << "平凡循环的加密 " << (double)(end - start) * 1000 / CLOCKS_PER_SEC << "ms\n";
	//shower(cipher, 16);

	/* 2.解密测试 */
	sm4Setkey_Dec(&ctx, key);
	start = clock();
	for (int I = 0; I < M; I++)
	{
		sm4_1_Round(ctx.sk, cipher, plainFromDec);
	}
	end = clock();
	cout << "平凡循环的解密 " << (double)(end - start) * 1000 / CLOCKS_PER_SEC << "ms\n";
	//shower(plainFromDec, 16);




	/* 3.ecb模式测试 */
	sm4Setkey_Enc(&ctx2, key);
	start = clock();
	sm4_ecb(ctx2.sk, plain1, cipher1, N);
	end = clock();
	cout << "ecb的加密 " << (double)(end - start) * 1000 / CLOCKS_PER_SEC << "ms\n";

	sm4Setkey_Dec(&ctx2, key);
	start = clock();
	sm4_ecb(ctx2.sk, cipher1, plainFromDec1, N);
	end = clock();
	cout << "ecb的解密 " << (double)(end - start) * 1000 / CLOCKS_PER_SEC << "ms\n";
	//shower(cipher2, len);
	//shower(plainFromDec2, len);

	/* 4.unroll2测试 */
	sm4Setkey_Enc(&ctx2, key);
	start = clock();
	sm4_ecb_LoopUnRoll2(ctx2.sk, plain2, cipher2, N);
	end = clock();
	cout << "ecb循环展开2次的加密 " << (double)(end - start) * 1000 / CLOCKS_PER_SEC << "ms\n";

	sm4Setkey_Dec(&ctx2, key);
	start = clock();
	sm4_ecb_LoopUnRoll2(ctx2.sk, cipher2, plainFromDec2, N);
	end = clock();
	cout << "ecb循环展开2次的解密 " << (double)(end - start) * 1000 / CLOCKS_PER_SEC << "ms\n";


	/* 5.unroll4测试 */
	sm4Setkey_Enc(&ctx2, key);
	start = clock();
	sm4_ecb_LoopUnRoll4(ctx2.sk, plain4, cipher4, N);
	end = clock();
	cout << "ecb循环展开4次的加密 " << (double)(end - start) * 1000 / CLOCKS_PER_SEC << "ms\n";

	sm4Setkey_Dec(&ctx2, key);
	start = clock();
	sm4_ecb_LoopUnRoll4(ctx2.sk, cipher4, plainFromDec4, N);
	end = clock();
	cout << "ecb循环展开4次的解密 " << (double)(end - start) * 1000 / CLOCKS_PER_SEC << "ms\n";


	/* 6.unroll8测试 */
	sm4Setkey_Enc(&ctx2, key);
	start = clock();
	sm4_ecb_LoopUnRoll8(ctx2.sk, plain8, cipher8, N);
	end = clock();
	cout << "ecb循环展开8次的加密 " << (double)(end - start) * 1000 / CLOCKS_PER_SEC << "ms\n";

	sm4Setkey_Dec(&ctx2, key);
	start = clock();
	sm4_ecb_LoopUnRoll8(ctx2.sk, cipher8, plainFromDec8, N);
	end = clock();
	cout << "ecb循环展开8次的解密 " << (double)(end - start) * 1000 / CLOCKS_PER_SEC << "ms\n";

	/* 7.unroll16测试 */
	sm4Setkey_Enc(&ctx2, key);
	start = clock();
	sm4_ecb_LoopUnRoll16(ctx2.sk, plain16, cipher16, N);
	end = clock();
	cout << "ecb循环展开16次的加密 " << (double)(end - start) * 1000 / CLOCKS_PER_SEC << "ms\n";

	sm4Setkey_Dec(&ctx2, key);
	start = clock();
	sm4_ecb_LoopUnRoll16(ctx2.sk, cipher16, plainFromDec16, N);
	end = clock();
	cout << "ecb循环展开16次的解密 " << (double)(end - start) * 1000 / CLOCKS_PER_SEC << "ms\n";




	cout << "\n========SIMD========\n";
	/* 8.加密测试 SIMD */
	sm4Setkey_Enc(&ctx, key);
	start = clock();
	for (int I = 0; I < M; I++)
	{
		sm4_1_Round_SIMD(ctx.sk, plain, cipher);
	}
	end = clock();
	cout << "平凡循环的加密 " << (double)(end - start) * 1000 / CLOCKS_PER_SEC << "ms\n";
	//shower(cipher, 16);

	/* 9.解密测试 SIMD */
	sm4Setkey_Dec(&ctx, key);
	start = clock();
	for (int I = 0; I < M; I++)
	{
		sm4_1_Round_SIMD(ctx.sk, cipher, plainFromDec);
	}
	end = clock();
	cout << "平凡循环的解密 " << (double)(end - start) * 1000 / CLOCKS_PER_SEC << "ms\n";
	//shower(plainFromDec, 16);


	/* 10.ecb模式测试 */
	sm4Setkey_Enc_SIMD(&ctx2, key);
	start = clock();
	sm4_ecb_SIMD(ctx2.sk, plain1, cipher1, N);
	end = clock();
	cout << "ecb的加密 " << (double)(end - start) * 1000 / CLOCKS_PER_SEC << "ms\n";

	sm4Setkey_Dec_SIMD(&ctx2, key);
	start = clock();
	sm4_ecb_SIMD(ctx2.sk, cipher1, plainFromDec1, N);
	end = clock();
	cout << "ecb的解密 " << (double)(end - start) * 1000 / CLOCKS_PER_SEC << "ms\n";
	//shower(cipher2, len);
	//shower(plainFromDec2, len);

	return 0;
}
