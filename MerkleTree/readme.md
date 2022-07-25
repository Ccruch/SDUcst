# Project 5: Impl Merkle Tree following RFC6962

## 202000460124 蔡欣悦

### 项目代码说明

* ***复制了picosha.h***：本头文件从网络上复制而来，并用于在Merkle Tree中实现sha256算法；

* origin.cpp：完成Merkle Tree的创建，能够根据输入创建Merkle Tree；因为是树的结果，所以能够使用先序遍历函数打印树，并根据打印结果，确定每个节点的sha256哈希值；给定某叶子节点需要的节点的哈希值，可以判断该叶子节点确实存在于Merkle Tree中。

### 运行指导

- 首先利用append函数添加叶子节点，append函数会自动生成相应Merkle Tree

![](C:\Users\Crush\Desktop\1.png)

- 利用先序遍历函数打印先序遍历的结果：

![](C:\Users\Crush\Desktop\2.png)

遍历结果见运行结果中；该结果可还原成树状如下：

![](C:\Users\Crush\Desktop\4.png)

判断"555"是否在该Merkle Tree中，需要额外提供蓝色打勾的三个节点的哈希值，判断结果见运行结果中。

![](C:\Users\Crush\Desktop\7.png)

### 运行结果

![](C:\Users\Crush\Desktop\6.png)

### 具体贡献

完成Merkle Tree实现的cpp代码，并完成对某节点inclusion的证明的cpp代码。
