# Project 3: implement length extension attack for SM3, SHA256, etc

## 202000460124 蔡欣悦

### 代码说明

利用md结构长度扩展攻击的原理编写py代码，实现对初始消息a，追加附加消息b的长度扩展攻击。

SM3_length_attack.py中，***前半部分对SM3的实现复制自网络***，用于SM3算法实现；

后半部分，实现对SM3的长度扩展攻击。

### 运行指导

随意设置初始消息a与附加消息b：
<img width="475" alt="1" src="https://user-images.githubusercontent.com/105582476/180706487-96c533dc-a433-403a-b341-1c158712356f.png">
得到伪造哈希与伪造消息：
![image](https://user-images.githubusercontent.com/105582476/180706582-dd28da7c-9017-49c4-83e8-5e1fa291b815.png)
对伪造消息运行sm3算法，得到的输出与伪造哈希进行比较，若相等，则说明攻击成功：
![image](https://user-images.githubusercontent.com/105582476/180706708-0e2a69a7-6947-4a47-bd45-e34c65a8d36d.png)


### 运行结果
![image](https://user-images.githubusercontent.com/105582476/180706768-61434df1-5758-4040-b709-2070a8b7d23b.png)

### 具体贡献
完成对SM3的长度扩展攻击。
