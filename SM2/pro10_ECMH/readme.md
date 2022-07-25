# Project10: Implement the above ECMH scheme

## 202000460124 蔡欣悦

### 代码说明

- 代码包含SM2系统参数，以及椭圆曲线上的一些运算：点加、点减、逆元、点乘等；

- 对于消息，先利用sha256算法进行哈希，并尝试将该hash值映射到椭圆曲线上的某点；我原本尝试以哈希值为横坐标，求解纵坐标，但在循环群上求解开方较困难：我尝试了穷举以及Cipolla算法，都难以得到结果；

- 于是修改映射关系，将得到的hash值模SM2系统参数中点G的阶N，设该结果为k，则消息的哈希映射到椭圆曲线上的点为k倍点G，如此映射关系可以较快得到结果。
### 运行指导

根据需要，随意设置几个消息，并以某种顺序组成消息集合，并验证重复元素代表集合并不相同、集合中消息增加与集合的hash相加有相等结果、集合中消息的移除、结合等，均通过验证。

![image](https://user-images.githubusercontent.com/105582476/180713607-08f58a31-dd26-43b6-8526-19302814140d.png)


### 运行结果

![image](https://user-images.githubusercontent.com/105582476/180713682-24b15a0f-7359-4178-8836-64049b7655fe.png)


### 具体贡献

完成ECMH scheme的实现。