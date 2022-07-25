# Project 5: Impl Merkle Tree following RFC6962

## 202000460124 蔡欣悦

### 项目代码说明

* ***复制了picosha.h***：本头文件从网络上复制而来，并用于在Merkle Tree中实现sha256算法；

* origin.cpp：完成Merkle Tree的创建，能够根据输入创建Merkle Tree；因为是树的结果，所以能够使用先序遍历函数打印树，并根据打印结果，确定每个节点的sha256哈希值；给定某叶子节点需要的节点的哈希值，可以判断该叶子节点确实存在于Merkle Tree中。

### 运行指导

- 首先利用append函数添加叶子节点，append函数会自动生成相应Merkle Tree

<img width="251" alt="1" src="https://user-images.githubusercontent.com/105582476/180704528-9bdf6ab5-51d3-4732-81ee-e723675cc722.png">

- 利用先序遍历函数打印先序遍历的结果：

<img width="382" alt="2" src="https://user-images.githubusercontent.com/105582476/180704541-c2b9706c-d66a-4039-b8a1-458883c17153.png">

遍历结果见运行结果中；该结果可还原成树状如下：

![4](https://user-images.githubusercontent.com/105582476/180704564-a0065fc4-3cbb-4141-afed-86904b5be733.png)
判断"555"是否在该Merkle Tree中，需要额外提供蓝色打勾的三个节点的哈希值，判断结果见运行结果中。

<img width="547" alt="7" src="https://user-images.githubusercontent.com/105582476/180704585-8a6ce5d2-708a-4f35-b3ca-d46fb9bf7dd3.png">

### 运行结果

<img width="395" alt="6" src="https://user-images.githubusercontent.com/105582476/180704611-908b4167-a4e4-414d-8f8e-76e1a3fec896.png">

### 具体贡献

完成Merkle Tree实现的cpp代码，并完成对某节点inclusion的证明的cpp代码。
