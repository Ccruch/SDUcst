# Project7: report on the application of this deduce technique in Ethereum with ECDSA

# 202000460124 蔡欣悦

## 以太坊中签名前缀与公钥恢复的report

### 原理

- 根据ECDSA签名算法中s的计算公式，利用适当的等式变形可以推导出公钥P的表达式：

$$
s = k^{-1} (e +dr)
$$

$$
skG = eG + drG
$$

$$
sR = eG + rP
$$

$$
P = r^{-1}(sR-eG)......①
$$

- 那么问题则从公钥表达式转移至还原R：
  
  在ECDSA签名算法中，r等于点R的横坐标；已知r，且点R在椭圆曲线：
  
  $$
  y^2=x^3+Ax+B
  $$
  
  上，我们可以通过横坐标r计算点R的纵坐标y，即求解二次剩余；
  
  利用Tonelli Shanks算法，我们能够得到两个y值，即可计算点R与点R'， 且R与R'关于x轴对称。
  
  显然，R与R'中，只有一个点与ECDSA签名时使用的R点相同。

- 那么问题从还原R转移至选择R点：
  
  若得到签名(r, s)的同时得到签名前缀v，且v对于选择哪个R点有明确的指向性，那么就可以轻松地恢复R，并带入①式即可还原公钥P；
  
  参考的资料中，对于签名前缀v没有具体的介绍，但如果签名前缀的作用仅是对恢复点R有明确指向性，那设计签名前缀v的算法是容易的：
  
  - 首先，当Tonelli Shanks算法的输入一定时，它的输出即是固定的；
  
  - 那么我们在ECDSA签名算法中，可以将r值代入Tonelli Shanks算法，判断一下关系式：
    
    $$
    tonellishanks(r, P)==R_y
    $$
    
     并设置一定的v值，使v与关系式是否成立有明确的联系；
  
  - 恢复公钥时，一样是利用Tonelli Shanks算法计算纵坐标，并联系v值，选择：
    
    1.Tonelli Shanks算法的输出y所计算的点R:(x, y)；
    
    2.选择另一个点R':(x, P - y)。

### 参考资料

[第七章 交易 - 签名前缀值（v）和公钥恢复 - 《精通以太坊 （中文版）》 - 书栈网 · BookStack](https://www.bookstack.cn/read/ethereum_book-zh/spilt.9.ee4988229e1934ea.md)









## 项目说明

### 代码说明

deduce_PK_ECDSA.py：根据恢复密钥的原理，对ECDSA签名算法适当增加计算签名前缀v的部分，并编写恢复公钥的函数。

### 运行指导

直接运行deduce_PK_ECDSA.py即可。

### 运行结果
![image](https://user-images.githubusercontent.com/105582476/181795079-fb662aa7-9f7a-4830-adb5-eaacdf25c305.png)

### 具体贡献

完成以太坊中ECDSA如何恢复公钥的report，并完成相应的代码实现。


