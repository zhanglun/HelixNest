# HelixNest
Where Molecules Meet Distributed Intelligence

让我们重新设计一个化学化合物智能分析平台项目，结合技术需求，使用以下免费科研API：

## 项目目标

构建支持以下功能的化合物研究系统：

* 自动聚合多源化合物数据（PubChem+PDB）
* 异步批量处理化学结构数据
* 毒性/生物活性预测模型
* 化合物交互关系可视化

### 技术选型

```
[Web界面] Flask + Plotly Dash
    ↑↓ RabbitMQ
[Celery Worker] 化学计算任务队列
    ↑↓ 
[数据分析] Pandas + RDKit
    ↑↓ 
[NoSQL数据库] MongoDB（存储分子结构+实验数据）
    ↑↓ 
[数据源] PubChem REST API、PDB API
```

**免费化学API推荐**

1. PubChem REST API (NIH提供)
  * 端点示例：https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/JSON
  * 可获取：分子式、3D结构、生物活性等
2. RCSB PDB API
  * 端点示例：https://data.rcsb.org/rest/v1/core/entry/1tqn
  * 可获取：蛋白质晶体结构数据
3. ChEMBL API
  * 端点示例：https://www.ebi.ac.uk/chembl/api/data/molecule/CHEMBL25
   * 提供药物活性数据
