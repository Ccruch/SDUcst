# Project13: implement sm2 2P decrypt with real network communication

## 202000460124 蔡欣悦

### 代码说明

- 即需要双方参与的SM2解密，这里设置client作为解密发起方、server作为解密辅助方。
- SM2_2P_decrypt_server.py ：负责接收client的请求，生成并保存子私钥（sub private key）之一的d2，计算并公布双方子私钥对应的公钥，完成一些辅助client解密的计算，并向其发送辅助的数据；需要import： pre_SM2
- SM2_2P_decrypt_client.py ：生成并保存子私钥（sub private key）之一的d1，请求server完成需要的辅助工作，并针对使用server公布的公钥加密的密文完成SM2 2P decrypt；需要import：pre_SM2、mySM2

### 运行指导
先运行SM2_2P_decrypt_server.py文件，再运行SM2_2P_decrypt_client.py文件。

### 运行结果

- <img width="396" alt="image" src="https://user-images.githubusercontent.com/105582476/180720703-9d648ed0-69ac-4b4a-a8a0-84ebe9b31c97.png">


- <img width="388" alt="image" src="https://user-images.githubusercontent.com/105582476/180720747-acc99144-8a79-46e3-b106-0ee01756a7e1.png">



### 具体贡献

完成传递udp数据包的情况下，sm2 2P decrypt 的实现。
