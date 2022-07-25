# Project1: implement the naïve birthday attack of reduced SM3

## 202000460124 蔡欣悦

### 代码说明

SM3_BirthdayAttack.py ：利用生日攻击原理，寻找高n比特碰撞时，随机选取2^(n/2)个输入将以较大概率找到一对碰撞。

### 运行指导

可在代码开头设置希望碰撞的比特数与希望重复运行的次数，随后运行代码即可。

![image](https://user-images.githubusercontent.com/105582476/180795742-fbc7b50f-2d2e-489b-b609-0c60a22bc5eb.png)


### 运行结果

![image](https://user-images.githubusercontent.com/105582476/180795190-1bf496e7-d727-4de3-bbfa-2bd7cd7c4e96.png)

### 具体贡献

完成对SM3算法高8/16比特的生日攻击。
