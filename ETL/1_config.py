# ==============================================================================
# 模块一：导入配置与依赖 (Config & Dependencies)
# ==============================================================================
import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3
import logging
import os
import warnings

# 忽略不必要的警告
warnings.filterwarnings('ignore')

# --- 1. 全局路径配置 ---
# 数据库路径
DB_NAME = "ecommerce_clean.db"

# CSV 源文件配置 (请确保这些文件在同级目录下)
CSV_FILES = {
    'time_dim': 'cleaned_time_dim.csv',
    'regions': 'cleaned_regions.csv',
    'products': 'cleaned_products.csv',
    'customers': 'cleaned_customers.csv',
    'orders': 'cleaned_orders.csv',
    'behavior_logs': 'cleaned_behavior_logs.csv'
}

# --- 2. 日志系统配置 ---
# 定义日志格式和输出文件
LOG_FILE = "etl_pipeline.log"

def setup_logging():
    """初始化日志配置，同时输出到控制台和文件"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    logging.info(">>> 系统日志初始化完成")

# 初始化配置
if __name__ == "__main__":
    setup_logging()
    print("配置模块测试成功：依赖导入正常，路径配置已加载。")
