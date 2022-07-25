#include<iostream>
#include<vector>
#include<chrono>
#include<time.h>

using namespace std;


#define hash_size 32  // 32 * 8 = 256(bit)

typedef struct Context {
	unsigned int in_me_HASH[hash_size / 4];
	unsigned char message_block[64];  // 512-bit msg block
}Context;

unsigned char* sm3(unsigned char* message, unsigned int msg_len, unsigned char digest[hash_size]);
unsigned char* sm3_optimized(unsigned char* message, unsigned int msg_len, unsigned char digest[hash_size]);
vector<uint32_t>sm3_hash();
vector<uint32_t>sm3_hash_optimized();

unsigned int t[64];

/*check for Little Endian*/
static const int endian_check = 1;
#define is_little_endian() (*(char *)&endian_check == 1)

/*left shift*/
#define left_rotate(s, bits) ((s) << (bits) | (s) >> (32 - bits))

/*Reverse byte order*/
unsigned int* reserve_s(unsigned int* s)
{
	unsigned char* byte, tmp;
	byte = (unsigned char*)s;
	tmp = byte[0];
	byte[0] = byte[3];
	byte[3] = tmp;

	tmp = byte[1];
	byte[1] = byte[2];
	byte[2] = tmp;
	return s;
}

/*T*/
unsigned int T(int i)
{
	if (i >= 0 && i <= 15)
		return 0x79CC4519;
	else if (i >= 16 && i <= 63)
		return 0x7A879D8A;
	else
		return 0;
}

/*pre_compute T for using*/
void compute_T() {
	for (int i = 0; i < 64; i++) {
		t[i] = left_rotate(T(i), i);
	}
	return;
}

/*FF*/
unsigned int FF(unsigned int X, unsigned int Y, unsigned int Z, int i)
{
	if (i >= 0 && i <= 15)
		return X ^ Y ^ Z;
	else if (i >= 16 && i <= 63)
		return (X & Y) | (X & Z) | (Y & Z);
	else
		return 0;
}

/*GG*/
unsigned int GG(unsigned int X, unsigned int Y, unsigned int Z, int i)
{
	if (i >= 0 && i <= 15)
		return X ^ Y ^ Z;
	else if (i >= 16 && i <= 63)
		return (X & Y) | (~X & Z);
	else
		return 0;
}

/*P0*/
unsigned int P0(unsigned int X)
{
	return X ^ left_rotate(X, 9) ^ left_rotate(X, 17);
}

/*P1*/
unsigned int P1(unsigned int X)
{
	return X ^ left_rotate(X, 15) ^ left_rotate(X, 23);
}

/*init for sm3*/
void sm3_init(Context* context) {
	context->in_me_HASH[0] = 0x7380166F;
	context->in_me_HASH[1] = 0x4914B2B9;
	context->in_me_HASH[2] = 0x172442D7;
	context->in_me_HASH[3] = 0xDA8A0600;
	context->in_me_HASH[4] = 0xA96F30BC;
	context->in_me_HASH[5] = 0x163138AA;
	context->in_me_HASH[6] = 0xE38DEE4D;
	context->in_me_HASH[7] = 0xB0FB0E4E;
}



/*ordinary version*/
void sm3_1_round(int i, unsigned int& A, unsigned int& B, unsigned int& C, unsigned int& D,
	unsigned int& E, unsigned int& F, unsigned int& G, unsigned int& H, unsigned int W[68], unsigned int W1[64], Context* context)
{
	for (int i = 0; i < 64; i++) {
		t[i] = left_rotate(T(i), i);
	}
	unsigned int SS1 = 0, SS2 = 0, TT1 = 0, TT2 = 0;
	SS1 = left_rotate(left_rotate(A, 12) ^ E ^ left_rotate(t[i], i), 7);
	SS2 = SS1 ^ left_rotate(A, 12);
	TT1 = FF(A, B, C, i) ^ D ^ SS2 ^ W1[i];
	TT2 = GG(E, F, G, i) ^ H ^ SS1 ^ W[i];
	D = C;
	C = left_rotate(B, 9);
	B = A;
	A = TT1;
	H = G;
	G = left_rotate(F, 19);
	F = E;
	E = P0(TT2);
}


/*sm3 compress function*/
void sm3_cf(Context* context)
{
	int i;
	unsigned int W[68];
	unsigned int W1[64];
	//A, ..., H: 8 registers
	unsigned int A, B, C, D, E, F, G, H;

	/*expenssion*/
	for (i = 0; i < 16; i++)
	{
		W[i] = *(unsigned int*)(context->message_block + i * 4);
		if (is_little_endian())
			reserve_s(W + i);
	}
	for (i; i < 68; i++)
	{
		W[i] = P1(W[i - 16] ^ W[i - 9] ^ left_rotate(W[i - 3], 15)) ^ left_rotate(W[i - 13], 17) ^ W[i - 6];
		if (is_little_endian())
			reserve_s(W + i);
	}
	for (i = 0; i < 64; i++)
	{
		W1[i] = W[i] ^ W[i + 4];
		if (is_little_endian())
			reserve_s(W + i);
	}
	/*conpress*/
	A = context->in_me_HASH[0];
	B = context->in_me_HASH[1];
	C = context->in_me_HASH[2];
	D = context->in_me_HASH[3];
	E = context->in_me_HASH[4];
	F = context->in_me_HASH[5];
	G = context->in_me_HASH[6];
	H = context->in_me_HASH[7];
	for (i = 0; i <= 64; i++)
	{
		sm3_1_round(i, A, B, C, D, E, F, G, H, W, W1, context);
	}
	context->in_me_HASH[0] ^= A;
	context->in_me_HASH[1] ^= B;
	context->in_me_HASH[2] ^= C;
	context->in_me_HASH[3] ^= D;
	context->in_me_HASH[4] ^= E;
	context->in_me_HASH[5] ^= F;
	context->in_me_HASH[6] ^= G;
	context->in_me_HASH[7] ^= H;
}

unsigned char* sm3(unsigned char* message, unsigned int msg_len, unsigned char digest[hash_size])
{
	Context context;
	unsigned int i, remainder, bit_len;

	/*init context*/
	sm3_init(&context);
	remainder = msg_len % 64;

	for (i = 0; i < msg_len / 64; i++)
	{
		memcpy(context.message_block, message + i * 64, 64);
		sm3_cf(&context);
	}

	/*filling*/
	bit_len = msg_len * 8;
	if (is_little_endian())
		reserve_s(&bit_len);
	memcpy(context.message_block, message + i * 64, remainder);
	context.message_block[remainder] = 0x80;  // add 0x80
	if (remainder <= 55)
	{
		memset(context.message_block + remainder + 1, 0, 64 - remainder - 1 - 8 + 4);
		memcpy(context.message_block + 64 - 4, &bit_len, 4);
		sm3_cf(&context);
	}
	else
	{
		memset(context.message_block + remainder + 1, 0, 64 - remainder - 1);
		sm3_cf(&context);
		memset(context.message_block, 0, 64 - 4);
		memcpy(context.message_block + 64 - 4, &bit_len, 4);
		sm3_cf(&context);
	}

	/*return digest*/
	if (is_little_endian())
		for (i = 0; i < 8; i++)
			reserve_s(context.in_me_HASH + i);
	memcpy(digest, context.in_me_HASH, hash_size);

	return digest;
}

vector<uint32_t>sm3_hash()
{
	vector<uint32_t> hash_result(32, 0);  // (0, 0, ..., 0), 32 zeros
	unsigned char buffer[4] = { 0x01,0x03,0x4a,0x95 };  // assign input
	unsigned char hash_output[32];
	sm3(buffer, 4, hash_output);
	hash_result.assign(&hash_output[0], &hash_output[32]);
	return hash_result;
}


/*optimized version*/

void sm3_1_round_optimized(int i, unsigned int& A, unsigned int& B, unsigned int& C, unsigned int& D,
	unsigned int& E, unsigned int& F, unsigned int& G, unsigned int& H, unsigned int W[68], Context* context)
{
	unsigned int SS1 = 0, SS2 = 0, TT1 = 0, TT2 = 0;
	if (i < 12) {
		W[i + 4] = *(unsigned int*)(context->message_block + (i + 4) * 4);
		if (is_little_endian())
			reserve_s(W + i + 4);
	}
	else {
		W[i + 4] = P1(W[i - 12] ^ W[i - 5] ^ left_rotate(W[i + 1], 15)) ^ left_rotate(W[i - 9], 17) ^ W[i - 2];
	}
	TT2 = left_rotate(A, 12);
	TT1 = TT2 + E + t[i];
	TT1 = left_rotate(TT1, 7);
	TT2 = TT2 ^ TT1;
	D = D + FF(A, B, C, i) + TT2 + (W[i] ^ W[i + 4]);//W'[i]=W[i] ^ W[i + 4]
	H = H + GG(E, F, G, i) + TT1 + W[i];
	B = left_rotate(B, 9);
	F = left_rotate(F, 19);
	H = P0(H);
}

/*optimized compress function*/
void sm3_cf_optimized(Context* context)
{
	int i;
	unsigned int W[68];
	unsigned int A, B, C, D, E, F, G, H;

	/*expension*/
	for (i = 0; i < 4; i++)
	{
		W[i] = *(unsigned int*)(context->message_block + i * 4);
		if (is_little_endian())
			reserve_s(W + i);
	}

	/*compress*/
	A = context->in_me_HASH[0];
	B = context->in_me_HASH[1];
	C = context->in_me_HASH[2];
	D = context->in_me_HASH[3];
	E = context->in_me_HASH[4];
	F = context->in_me_HASH[5];
	G = context->in_me_HASH[6];
	H = context->in_me_HASH[7];
	for (i = 0; i <= 60; i += 4)
	{
		sm3_1_round_optimized(i, A, B, C, D, E, F, G, H, W, context);
		sm3_1_round_optimized(i + 1, D, A, B, C, H, E, F, G, W, context);
		sm3_1_round_optimized(i + 2, C, D, A, B, G, H, E, F, W, context);
		sm3_1_round_optimized(i + 3, B, C, D, A, F, G, H, E, W, context);
	}
	context->in_me_HASH[0] ^= A;
	context->in_me_HASH[1] ^= B;
	context->in_me_HASH[2] ^= C;
	context->in_me_HASH[3] ^= D;
	context->in_me_HASH[4] ^= E;
	context->in_me_HASH[5] ^= F;
	context->in_me_HASH[6] ^= G;
	context->in_me_HASH[7] ^= H;
}

unsigned char* sm3_optimized(unsigned char* message, unsigned int msg_len, unsigned char digest[hash_size])
{
	Context context;
	unsigned int i, remainder, bit_len;

	/*init context*/
	sm3_init(&context);
	remainder = msg_len % 64;
	for (i = 0; i < msg_len / 64; i++)
	{
		memcpy(context.message_block, message + i * 64, 64);
		sm3_cf_optimized(&context);
	}
	/*filling*/
	bit_len = msg_len * 8;
	if (is_little_endian())
		reserve_s(&bit_len);
	memcpy(context.message_block, message + i * 64, remainder);
	context.message_block[remainder] = 0x80;  // add 0x80
	if (remainder <= 55)
	{
		memset(context.message_block + remainder + 1, 0, 64 - remainder - 1 - 8 + 4);
		memcpy(context.message_block + 64 - 4, &bit_len, 4);
		sm3_cf_optimized(&context);
	}
	else
	{
		memset(context.message_block + remainder + 1, 0, 64 - remainder - 1);
		sm3_cf_optimized(&context);
		memset(context.message_block, 0, 64 - 4);
		memcpy(context.message_block + 64 - 4, &bit_len, 4);
		sm3_cf_optimized(&context);
	}

	/*return digest*/
	if (is_little_endian())
		for (i = 0; i < 8; i++)
			reserve_s(context.in_me_HASH + i);
	memcpy(digest, context.in_me_HASH, hash_size);

	return digest;
}

vector<uint32_t>sm3_hash_optimized()
{
	compute_T();  // pre_compute T
	vector<uint32_t> hash_result(32, 0);  // (0, 0, ..., 0), 32 zeros
	unsigned char buffer[4] = { 0x01,0x03,0x4a,0x95 };  // input is same with ordinary version
	unsigned char hash_output[32];
	sm3_optimized(buffer, 4, hash_output);
	hash_result.assign(&hash_output[0], &hash_output[32]);
	return hash_result;
}

int main() {
	int counter = 100; // 
	vector<uint32_t> ordinary_hash;  // result of ordinary version
	vector<uint32_t> optimized_hash;  // result of optimized version
	auto start1 = std::chrono::high_resolution_clock::now();//¼ÇÂ¼Ê±¼ä
	for (int i = 0; i < counter; i++)
	{
		ordinary_hash = sm3_hash();
	}
	auto end1 = std::chrono::high_resolution_clock::now();
	std::cout << "\nordinary version cost ";
	std::chrono::duration<double, std::ratio<1, 1000>> diff1 = (end1 - start1) / 100;
	std::cout << diff1.count() << " ms\n";
	auto start2 = std::chrono::high_resolution_clock::now();
	for (int i = 0; i < counter; i++)
	{
		optimized_hash = sm3_hash_optimized();
	}
	auto end2 = std::chrono::high_resolution_clock::now();
	std::cout << "\noptimized version cost ";
	std::chrono::duration<double, std::ratio<1, 1000>> diff2 = (end2 - start2) / 100;
	std::cout << diff2.count() << " ms\n";
	double rate = diff1.count() / diff2.count();
	cout << "\nthe speed_up ratio is " << rate << endl;
	return 0;
}