# 我的实时风控项目架构图

下面是基于 Kafka + Flink + MySQL 的 Docker 容器架构与数据流向图：

```mermaid
graph TD
    %% 定义样式
    classDef container fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef file fill:#fff3e0,stroke:#ff6f00,stroke-width:2px,stroke-dasharray: 5 5;
    classDef logic fill:#f3e5f5,stroke:#7b1fa2,stroke-width:1px;

    subgraph "Docker Host (你的电脑)"
        
        subgraph "数据源层 (Data Source)"
            CSV[(" fraud_dataset.csv")]:::file
            Producer[" Python Producer\n(producer.py)"]:::container
            CSV -->|1. 读取模拟数据| Producer
        end

        subgraph "消息队列层 (Message Queue)"
            ZK[(" Zookeeper")]:::container
            Kafka[(" Kafka Broker\n(Container)")]:::container
            ZK -.->|协调管理| Kafka
            Producer -->|2. 发送 JSON 流数据| Kafka
            
            %% Kafka 内部 Topic
            subgraph "Kafka Topics"
                TopicMain[(" Topic: finance_stream")]
                TopicDLQ[(" Topic: dead_letter_queue")]
            end
            Kafka --- TopicMain
            Kafka --- TopicDLQ
        end

        subgraph "实时计算层 (Real-time Processing)"
            FlinkJM[" Flink JobManager\n(Container)"]:::container
            FlinkTM[" Flink TaskManager\n(Container)"]:::container
            FlinkJM -.->|任务调度| FlinkTM
            
            %% Flink 内部逻辑
            subgraph "Flink SQL Job (flink_to_mysql.py)"
                Source(" Source: Kafka"):::logic
                Filter(" Filter/Split: 脏数据判断"):::logic
                Window(" Window: 5秒滚动窗口聚合"):::logic
                SinkMySQL(" Sink: JDBC to MySQL"):::logic
                SinkDLQ(" Sink: Kafka DLQ"):::logic
            end
            
            TopicMain -->|3. 消费数据| Source
            Source --> Filter
            Filter -->|正常数据| Window
            Filter -->|异常数据 (<0)| SinkDLQ
            SinkDLQ -->|4a. 写回死信队列| TopicDLQ
        end

        subgraph "存储与服务层 (Storage & Serving)"
            Redis[(" Redis\n(Container)")]:::container
            MySQL[(" MySQL\n(Container)")]:::container
            
            Window -.->|5. (可选) 关联维表| Redis
            Window -->|4b. 写入聚合结果| SinkMySQL
            SinkMySQL -->|存储 risk_stats| MySQL
        end

    end

    %% 数据流向连线说明
    linkStyle 2,5,9,10,11,12 stroke:#4caf50,stroke-width:2px;
```
