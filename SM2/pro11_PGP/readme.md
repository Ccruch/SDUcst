# Project11: Implement a PGP scheme with SM2

## 202000460124 蔡欣悦

### 代码说明
- 以下图为原理，消息发送方随机生成对称加密的会话密钥sessionkey，并用接收方的SM2公钥加密sessionkey，用sessionkey加密消息，同时发送给接收方；

- 接收方收到两个密文，先用自己的SM2私钥解得会话密钥sessionkey，再利用sessionkey解对称密码得消息明文。

<img width="477" alt="image" src="https://user-images.githubusercontent.com/105582476/180714773-0315769f-d0cf-41a9-9500-e55aeb2788e2.png">

- 需要import： mySM2

- 选择对称加密算法为：SM4算法，***SM4算法部分均复制自网络。***

### 运行指导

假设A向B发送消息：

![image](https://user-images.githubusercontent.com/105582476/180715523-896bd884-b51b-4d89-8768-2c5ab9961091.png)


### 运行结果

![image](https://user-images.githubusercontent.com/105582476/180715592-d41b3b0c-dad4-4849-947a-955f1cf488dc.png)


### 具体贡献

完成对SM2 PGP scheme的实现。
