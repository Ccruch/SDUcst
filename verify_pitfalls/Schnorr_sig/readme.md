# Project9: verify the above pitfalls with proof-of-concept code


## 202000460124 蔡欣悦

### 代码说明

EC.py ： 椭圆曲线上某些参数的定义、一些运算：点加、点减、点乘、逆元等；

Schnorr_sv.py ： 完成了基本的ECDSA签名与验证；需要 imporyt：EC

leaking_k.py ：完成了对pitfall1：leaking k leads to leaking of d的验证；需要 import：EC、Schnorr_sv

reusing_k.py ：完成了对pitfall2：reusing k leads to leaking of d的验证；需要 import：pre_SM2、Schnorr_sv

same_dk_withECDSA.py ：完成了对pitfall7：same d and k with ECDSA, leads to leaking of d的验证；需要 import：pre_SM2、Schnorr_sv

#### Schnorr签名中，对不同条件下，私钥d的推导部分见下图：

![IMG_20220725_154522](https://user-images.githubusercontent.com/105582476/180729809-e4ecfd0c-ff85-459d-bbd1-693dededc912.jpg)


### 运行指导

Schnorr_sv.py、leaking_k.py、reusing_k.py、same_dk_withECDSA.py 已经设置好一定的消息，直接运行即可。

### 运行结果

- <img width="340" alt="image" src="https://user-images.githubusercontent.com/105582476/180729317-f7e5b907-9294-4064-9edf-7257dfb0dd59.png">

- <img width="344" alt="image" src="https://user-images.githubusercontent.com/105582476/180729434-ce6e704a-082e-43d2-be32-486464779d3b.png">

- <img width="284" alt="image" src="https://user-images.githubusercontent.com/105582476/180729592-3bd415f0-eecd-46c4-b791-2a390588b892.png">

### 具体贡献

完成了对部分pitfall的证明。
