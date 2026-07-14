import pandas as pd
import os

out = "./output"
# 读取关系表
rels = pd.read_parquet(os.path.join(out, "relationships.parquet"))
print("===== 全部实体关联关系 =====")
# 核心字段：source(起点实体)、target(终点实体)、description(关系描述)、weight(关联强度)
print(rels[["source", "target", "description", "weight"]].to_string())

# 顺便打印实体对照表（title是实体名称）
entities = pd.read_parquet(os.path.join(out, "entities.parquet"))
print("\n===== 实体清单 =====")
print(entities[["title", "description", "frequency"]].to_string())