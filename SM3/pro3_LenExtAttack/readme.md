# Project 3: implement length extension attack for SM3, SHA256, etc

## 202000460124 蔡欣悦

### 代码说明

利用md结构长度扩展攻击的原理编写py代码，实现对初始消息a，追加附加消息b的长度扩展攻击。

- SM3_length_attack.py中，***前半部分对SM3的实现复制自网络***，用于SM3算法实现；

- 后半部分，实现对SM3的长度扩展攻击。

### 运行指导

- 随意设置初始消息a与附加消息b：

![image](https://user-images.githubusercontent.com/105582476/180796514-20c9bf7c-a709-4da1-88f4-1669610cb1b6.png)

- 得到伪造哈希与伪造消息：

![image](https://user-images.githubusercontent.com/105582476/180796582-6111532b-9dcc-45d8-976e-86e167381f1c.png)

- 对伪造消息运行sm3算法，得到的输出与伪造哈希进行比较，若相等，则说明攻击成功：

![image](https://user-images.githubusercontent.com/105582476/180796618-a9aea2ac-9235-4f65-a3ff-bad612666bca.png)


### 运行结果

![image](https://user-images.githubusercontent.com/105582476/180796717-555623fb-ea82-4d74-8681-c6816f7b8e03.png)


### 具体贡献

完成对SM3的长度扩展攻击。
