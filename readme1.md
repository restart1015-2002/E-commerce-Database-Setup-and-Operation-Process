graph TD
    %% 样式定义
    classDef container fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef file fill:#fff3e0,stroke:#ff6f00,stroke-width:2px,stroke-dasharray: 5 5;
    classDef logic fill:#f3e5f5,stroke:#7b1fa2,stroke-width:1px;

    subgraph Docker_Host_PC ["Docker Host (Your PC)"]
        
        subgraph Data_Source ["Data Source Layer"]
            CSV[("fraud_dataset.csv")]:::file
            Producer["Python Producer"]:::container
            CSV -->|1. Read Data| Producer
        end

        subgraph Message_Queue ["Message Queue Layer"]
            ZK[("Zookeeper")]:::container
            Kafka[("Kafka Broker")]:::container
            ZK -.->|Coordination| Kafka
            Producer -->|2. Send JSON| Kafka
            
            subgraph Topics
                TopicMain[("Topic: finance_stream")]
                TopicDLQ[("Topic: dead_letter_queue")]
            end
            Kafka --- TopicMain
            Kafka --- TopicDLQ
        end

        subgraph Processing ["Real-time Processing Layer"]
            FlinkJM["Flink JobManager"]:::container
            FlinkTM["Flink TaskManager"]:::container
            FlinkJM -.->|Schedule| FlinkTM
            
            subgraph Flink_Job ["Flink SQL Job"]
                Source("Source: Kafka"):::logic
                Filter("Filter: Check Amount"):::logic
                Window("Window: 5s Aggregation"):::logic
                SinkMySQL("Sink: JDBC to MySQL"):::logic
                SinkDLQ("Sink: Kafka DLQ"):::logic
            end
            
            TopicMain -->|3. Consume| Source
            Source --> Filter
            Filter -->|Valid Data| Window
            Filter -->|Invalid < 0| SinkDLQ
            SinkDLQ -->|4a. Write to DLQ| TopicDLQ
        end

        subgraph Storage ["Storage Layer"]
            Redis[("Redis Cache")]:::container
            MySQL[("MySQL DB")]:::container
            
            Window -.->|5. Optional Join| Redis
            Window -->|4b. Write Result| SinkMySQL
            SinkMySQL -->|Risk Stats| MySQL
        end

    end

    %% 连线样式
    linkStyle 2,5,9,10,11,12 stroke:#4caf50,stroke-width:2px;
