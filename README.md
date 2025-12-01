# E-commerce-Database-Setup-and-Operation-Process
本项目模拟一个中型电商平台的完整数据生态系统，构建了一个包含用户画像、交易分析、行为追踪和商品管理的综合性数据仓库

主要解决数据孤岛问题，整合分散的用户、订单、行为数据，提供标准化的模型和查询接口，为业务部门提供数据驱动的决策依据，同时支持用户画像和推荐算法开发

其中包含的数据表：

📊 事实表：

├── orders (订单事实表) - 核心交易数据

📈 维度表：

├── customers (用户维度) - 用户画像数据

├── products (商品维度) - 商品分类信息 

├── time_dim (时间维度) - 时间分析支持

├── regions (地区维度) - 地域分布分析

└── behavior_logs (行为日志) - 用户交互数据

详细表单字段名称请查阅 Introduction to Each Form's Data Fields
