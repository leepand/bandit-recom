# bandit-recom
通过AI驱动的推荐，提高客户满意度和消费。适用于您的主页、产品详情、电子邮件营销活动等。帮助企业快速搭建推荐系统，为用户提供千人千面的个性化体验，解决信息过载与用户注意力有限之间的矛盾，将每一次曝光价值最大化


具体来说，这个系统包含：

- Python服务的模型服务代码
- AI助力实时机器学习
- 卓越的可扩展性，大数据基础设施
- 通过高度通用和可扩展的解决方案实现内容的个性化
- 实时分析和无缝配置
- 开放的算法实验平台,可实现A/B测试
- 快速、简单的集成即可融入您的环境


## 支持的模型、策略及特征类型

当前支持的模型列表:

- Contextual Bandits (small datasets)
  - [x] Linear bandit w/ ε-greedy exploration
  - [x] Random forest bandit w/ ε-greedy exploration
  - [x] Gradient boosted decision tree bandit w/ ε-greedy exploration
- Contextual Bandits (medium datasets)
  - [x] Neural bandit with ε-greedy exploration
  - [x] Neural bandit with UCB-based exploration [(via. dropout exploration)](https://arxiv.org/abs/1506.02142)
  - [x] Neural bandit with UCB-based exploration [(via. mixture density networks)](https://publications.aston.ac.uk/id/eprint/373/1/NCRG_94_004.pdf)
- Reinforcement Learning (large datasets)
  - [ ] [Deep Q-learning with ε-greedy exploration](https://www.cs.toronto.edu/~vmnih/docs/dqn.pdf)
  - [ ] [Quantile regression DQN with UCB-based exploration](https://arxiv.org/abs/1710.10044)
  - [ ] [Soft Actor-Critic](https://arxiv.org/abs/1801.01290)

<b>4</b> 支持的特征类型:
* <b>Numeric:</b> standard floating point features
  * e.g. `{totalCartValue: 39.99}`
* <b>Categorical:</b> low-cardinality discrete features
  * e.g. `{currentlyViewingCategory: "men's jeans"}`
* <b>ID list:</b> high-cardinality discrete features
  * e.g. `{productsInCart: ["productId022", "productId109"...]}`
  * Handled via. learned embedding tables
* <b>"Dense" ID list:</b> high-cardinality discrete features, manually mapped to dense feature vectors
  * e.g `{productId022: [0.5, 1.3, ...], productId109: [1.9, 0.1, ...], ...}`

## 技术架构

bandit-recom技术架构遵循经典的工业级深度学习推荐系统架构，包括了离线数据处理、模型训练、近线的流处理、线上模型服务、前端推荐结果显示等多个模块：
![alt text](sources/recom-serving.jpg)