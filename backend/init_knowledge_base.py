#!/usr/bin/env python3
"""
初始化知识库脚本

功能：
1. 检查 Milvus 健康状态
2. 创建 Collection（如不存在）
3. 向量化知识库文档并入库
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def init_knowledge_base():
    """初始化知识库"""
    print("开始初始化知识库...")
    
    try:
        # 检查 Milvus 连接
        print("1. 检查 Milvus 连接...")
        try:
            from pymilvus import connections
            connections.connect(
                alias="default",
                host=os.getenv("MILVUS_HOST", "milvus-standalone"),
                port=os.getenv("MILVUS_PORT", "19530")
            )
            print("   ✓ Milvus 连接成功")
        except Exception as e:
            print(f"   ✗ Milvus 连接失败: {e}")
            print("   提示：如果没有配置 Milvus，可以跳过此步骤，使用规则推理模式。")
            return
        
        # 加载知识库文档
        print("2. 加载知识库文档...")
        # TODO: 实现文档加载和向量化
        print("   提示：知识库向量化功能待实现（Stage 4）")
        
        print("\n✓ 知识库初始化完成！")
        
    except Exception as e:
        print(f"\n✗ 初始化失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_knowledge_base()
