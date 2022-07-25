# Project12: implement sm2 2P sign with real network communication

## 202000460124 蔡欣悦

### 代码说明

- 即需要双方参与的SM2签名，这里设置client作为签名发起方、server作为签名辅助方。
- SM2_2P_sign_server.py ：负责接收client的请求，生成并保存子私钥（sub private key）之一的d2，完成一些辅助client签名的计算，并向其发送辅助的数据；需要import： pre_SM2
- SM2_2P_sign_client.py ：生成并保存子私钥（sub private key）之一的d1，请求server完成需要的辅助工作，并针对消息M完成SM2 2P sign；需要import：pre_SM2

### 运行指导
先运行SM2_2P_sign_server.py文件，再运行SM2_2P_sign_client.py文件。

### 运行结果

- <img width="379" alt="image" src="https://user-images.githubusercontent.com/105582476/180717292-c08002e4-4223-4296-aaf3-4fa342795369.png">

   


- <img width="481" alt="image" src="https://user-images.githubusercontent.com/105582476/180717371-216ca9cf-9a3a-4000-8b2d-5c2398db9feb.png">



### 具体贡献

完成传递udp数据包的情况下，sm2 2P sign 的实现。
