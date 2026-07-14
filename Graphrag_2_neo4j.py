import pandas as pd
import os
from neo4j import GraphDatabase

out_dir = "./output"
# 连接Neo4j，替换为你的账号密码
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "ymf7435.."))

# 1. 读取实体表，title为实体名称
entities = pd.read_parquet(os.path.join(out_dir, "entities.parquet"))
with driver.session() as sess:
    for _, row in entities.iterrows():
        sess.run("""
        CREATE (e:Entity{
            name:$title,
            desc:$desc,
            freq:$freq,
            degree:$deg
        })
        """,
        title=row["title"],
        desc=row["description"],
        freq=int(row["frequency"]),
        deg=int(row["degree"])
        )

# 2. 读取关系表
rels = pd.read_parquet(os.path.join(out_dir, "relationships.parquet"))
with driver.session() as sess:
    for _, row in rels.iterrows():
        sess.run("""
        MATCH (a:Entity{name:$s}), (b:Entity{name:$t})
        CREATE (a)-[:REL{desc:$rd, weight:$w}]->(b)
        """,
        s=row["source"],
        t=row["target"],
        rd=row["description"],
        w=float(row["weight"])
        )

# 3. 绑定实体所属社区
comm = pd.read_parquet(os.path.join(out_dir, "communities.parquet"))
with driver.session() as sess:
    for _, row in comm.iterrows():
        # entity_ids是数组，循环绑定社区id
        entity_names = row["entity_ids"]
        cid = row["human_readable_id"]
        for name in entity_names:
            sess.run("""
            MATCH (e:Entity{name:$n})
            SET e.community = $cid
            """, n=name, cid=cid)

print("全部导入完成")
driver.close()