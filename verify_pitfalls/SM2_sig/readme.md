# Project9: verify the above pitfalls with proof-of-concept code


## 202000460124 蔡欣悦

### 代码说明

pre_SM2.py ： 椭圆曲线上某些参数的定义、一些运算：点加、点减、点乘、逆元等；

SM2_sv.py ： 完成了基本的ECDSA签名与验证；需要 imporyt：pre_SM2

leaking_k.py ：完成了对pitfall1：leaking k leads to leaking of d的验证；需要 import：pre_SM2、SM2_sv

reusing_k.py ：完成了对pitfall2：reusing k leads to leaking of d的验证；需要 import：pre_SM2、SM2_sv

same_dk_withECDSA.py ：完成了对pitfall7：same d and k with ECDSA, leads to leaking of d的验证；需要 import：pre_SM2、SM2_sv
#### SM2签名中，对不同条件下，私钥d的推导情况见下图（标注ppt部分是课件ppt中已经显示了相关证明）：
![IMG_20220725_154454](https://user-images.githubusercontent.com/105582476/180731174-e8375946-8676-4ebe-8170-c14ae25fc603.jpg)


### 运行指导

ECDSA_sv.py、leaking_k.py、reusing_k.py、same_dk_withECDSA.py 已经设置好一定的消息，直接运行即可。

### 运行结果

- <img width="332" alt="image" src="https://user-images.githubusercontent.com/105582476/180728462-eecb2548-59b9-4c36-9d19-98aa17f60fee.png">

- <img width="331" alt="image" src="https://user-images.githubusercontent.com/105582476/180728827-9c00bbea-4392-4390-8954-baabbccbb246.png">

- <img width="299" alt="image" src="https://user-images.githubusercontent.com/105582476/180728630-80bad78e-c059-4622-906d-de5f653027d5.png">


### 具体贡献

完成了对部分pitfall的证明。
