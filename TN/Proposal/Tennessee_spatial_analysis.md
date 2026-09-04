# Tennessee Data Center空间分布分析：TN-first研究流程

## 研究定位

> 研究区域：Tennessee  
> 主要数据源：dcmap.us  
> 当前任务：建立可复现的州级空间分布与基础设施关联分析  
> 当前不做：全国数据整合、全国模型训练、未来选址预测  
> 长期方向：只有TN流程通过数据与统计检验后，才考虑以同一规范扩展到其他州

本研究不把Tennessee简单视为全国分析的缩小版，而把它作为一个完整的州级研究对象。当前核心问题是：

\[
\boxed{
\text{在控制可开发土地与城市化背景后，Tennessee运营数据中心是否仍集中于特定基础设施环境？}
}
\]

研究逻辑为：

\[
\text{Canonical Sites}
\rightarrow
\text{Observed Spatial Pattern}
\rightarrow
\text{Conditional Infrastructure Association}
\rightarrow
\text{Residual Clustering}
\rightarrow
\text{Exploratory Infrastructure Regimes}
\]

所有结论首先限定为Tennessee州内的观察性空间关联。除非有独立时间证据或政策证据，否则不使用因果性的“机制证明”表述。

---

# 1. 当前研究边界

## 1.1 研究对象

主要研究总体为：

\[
S_{op}=\{\text{dcmap.us中Tennessee内去重后的operational site/campus}\}
\]

Under Construction和Planned / Approved项目单独保存，但不与Operational混合构成主要点模式。

状态分层为：

| 状态 | 当前用途 | 是否进入主要点模式 |
|---|---|---:|
| Operational | 已投入服务的设施 | 是 |
| Under Construction | 正在建设的设施 | 否，单独描述 |
| Planned / Approved | 已宣布或获批但尚未建成的设施 | 否，单独描述 |
| Paused | 已公开停滞但尚未放弃的项目 | 否 |
| Cancelled | 已公开放弃、但由dcmap.us保留在建设记录中的项目 | 否 |

## 1.2 当前不回答的问题

本阶段不回答：

- Tennessee哪里最适合建设未来数据中心；
- 某地是否一定会建设数据中心；
- Tennessee结果是否能够直接代表美国；
- 某项基础设施是否因果性导致数据中心落地。

## 1.3 未来扩展边界

未来可能从TN扩展到其他州，但当前只保留以下可移植要求：

- 使用稳定的site与facility定义；
- 使用统一的字段名称、单位和时间口径；
- 保留数据来源、版本和处理记录；
- 使用可替换的州边界与候选空间；
- 不在TN阶段下载或分析全国数据。

---

# 2. 研究问题与预设假设

主假设应在查看最终显著性结果前固定。PCA、HDBSCAN和UMAP结果不得反向修改主假设。

## H1：电力基础设施关联

> 在控制可开发土地、城市化和市场位置后，运营数据中心仍比可用空间更接近变电站或高压输电环境。

可能支持H1的观察：

- 条件化背景下，站点到变电站距离显著更短；
- 电力变量在点过程模型中具有稳定方向；
- 不同空间划分下结论方向一致。

可能否定或削弱H1的观察：

- 控制城市化后效应消失；
- 结果只由Nashville或Memphis少数站点驱动；
- 换用不同可开发土地定义后方向改变。

## H2：网络基础设施关联

> 运营数据中心在商业高速光纤覆盖或高网络可达环境中出现得更频繁。

需要避免的解释：

- 光纤供应商数量可能只是城市化代理；
- 当前光纤覆盖不能自动解释历史站点；
- 发布记录数量不能直接等同于独立供应商数量。

## H3：市场与基础设施的独立作用

> 数据中心的电力或网络关联不能完全由距离城市市场更近来解释。

如果加入市场和人口变量后，电力与网络变量失去稳定性，应报告：

> 当前数据未显示其具有超出城市化背景的独立关联。

## H4：容量尺度差异

> 以site count和以MW capacity加权时，Tennessee的数据中心空间结构不同。

这是count geography与capacity geography的对比，不假定哪一种更正确。

---

# 3. 第一阶段：建立dcmap.us Tennessee Canonical Dataset

任何空间统计之前，先完成数据对象定义。这个阶段是研究的质量门，不是普通清洗步骤。

## 3.1 两种分析单位

### Site/Campus Level

用于：

- 点模式分析；
- KDE地图；
- Ripley’s K/L；
- 基础设施关联。

### Facility/Building Level

用于：

- 建筑数量；
- 容量汇总；
- 园区扩张；
- 建设强度。

原则：

\[
\boxed{\text{一个物理园区在主要空间分析中只贡献一个site point}}
\]

## 3.2 建议保留的核心字段

| 字段 | 含义 | 主要用途 |
|---|---|---|
| site_id | 去重后的独立物理站点ID | 主要分析主键 |
| facility_id | dcmap.us设施记录ID | 来源追踪 |
| parent_site_id | facility所属site/campus | 父子关系 |
| site_name | 规范化站点名称 | 人工复核 |
| operator | 设施公开关联的运营品牌 | 去重辅助与描述 |
| owner / developer / anchor_tenant | 所有者、开发商与主要租户（如公开） | 角色区分与描述 |
| latitude / longitude | 站点坐标 | 空间连接 |
| coordinate_precision | 坐标精度等级 | 不确定性分析 |
| county / market | 行政区与市场 | 分层和匹配 |
| status | Operational等状态 | 样本分层 |
| facility_type | 统一类型 | 异质性分析 |
| capacity_mw | 已报告或估算的铭牌/规划容量，不等于当前负荷 | 容量加权 |
| capacity_estimated | 容量为reported或estimated | 容量不确定性分析 |
| opening_year / milestone_date | 首次运营年份或公开项目里程碑日期 | 时间分析 |
| source_snapshot_date | 数据快照日期 | 可复现性 |
| source_url | 来源页面 | 审核 |
| review_flag | 是否需要人工判断 | 质量控制 |

## 3.3 Site去重判断顺序

1. 使用dcmap.us记录的campus structure或multi-building关系。
2. 检查相同规范化名称、运营商和地址。
3. 检查坐标距离与共同园区证据。
4. 多栋building属于同一campus时，保留全部facility成员，但只生成一个site。
5. 相邻但运营商、地址或园区证据不同的设施不能仅凭距离自动合并。
6. 无法确认时保留为独立site并标记review_flag，而不是强制合并。

至少生成两张表：

| 表 | 内容 |
|---|---|
| canonical_sites | 每个独立site一行 |
| site_facility_crosswalk | 每条facility如何映射到site及其依据 |

## 3.4 数据源审查

在分析前记录：

- dcmap.us数据获得方式与快照日期；
- dcmap.us使用条款、记录级数据访问授权与再分发限制；
- Tennessee记录总数；
- Campus、Facility、Building结构；
- 状态字段定义；
- 坐标精度；
- capacity、capacity_estimated和时间字段缺失率；
- 不同facility type的覆盖情况；
- 基于公开记录编制可能产生的收录偏差。

dcmap.us不能在未验证前被称为Tennessee完整普查。研究表述应为：

> dcmap.us中可识别的Tennessee data-center sites。

dcmap.us公开Agent API只提供聚合结果，且使用条款不允许批量抓取或复制底层数据集。因此，本proposal中的记录级空间分析必须基于dcmap.us明确授权的数据导出或其他经许可的记录级访问方式；公开州级汇总页面只能用于核对总量，不能替代分析数据表。

---

# 4. 第二阶段：定义Tennessee可用空间背景

本研究不标注随机地点为“失败项目”，但必须定义数据中心可能被考虑的availability domain。

## 4.1 三层空间背景

### D0：Tennessee Land Baseline

全州陆地区域，仅作为最宽松描述性基线。

### D1：Developable-Land Baseline

排除明显不可建设区域，例如：

- 大型水体；
- 保护地；
- 明显不可接受的坡度；
- 机场跑道安全范围；
- 军事限制区；
- 其他确定性不可建设地类。

D1是主要推断背景。

### D2：Urban/Industrial Matched Baseline

在相同metro、工业或已开发土地环境内生成匹配背景，用于检验电力、网络和水资源变量是否只是城市化代理。

## 4.2 防止循环控制

当检验某个变量时，不能用该变量先定义背景。

例如：

- 检验变电站距离时，不用“距离变电站2 km内”定义D1；
- 检验供水距离时，不先删除全部远离供水区的位置；
- 检验光纤距离时，不用光纤覆盖定义候选域。

否则结论会被研究设计预先固定。

## 4.3 空间尺度

主要空间单元建议使用一个固定的equal-area grid或H3分辨率。County和Census tract只用于描述或敏感性分析。

至少比较：

- 主尺度；
- 一个更细尺度；
- 一个更粗尺度。

如果结论随尺度发生方向变化，应报告为尺度不稳定，而不是只保留最显著结果。

---

# 5. 第三阶段：描述性空间分布

这一步只描述“在哪里”，不作机制或显著性结论。

## 5.1 基础地图

分别绘制：

- Operational sites；
- Under Construction sites；
- Planned / Approved sites；
- facility type；
- site count；
- capacity-weighted symbols；
- coordinate precision或缺失状态。

Operational、Under Construction和Planned / Approved不得合成一个“现有站点”图层。

## 5.2 两套空间表述

### Site-count geography

\[
\lambda_{count}(s)
\]

每个独立site权重为1。

### Capacity geography

\[
\lambda_{MW}(s)
\]

site按可核实MW加权。

容量缺失站点不能自动填为0。容量图需要同时报告：

- 有容量记录的site比例；
- 容量已知样本的空间覆盖；
- 缺失是否集中于某类facility。

## 5.3 KDE的角色

KDE用于：

- 展示Nashville、Memphis、Knoxville、Chattanooga等局部密度；
- 对比count与capacity热点；
- 比较不同bandwidth下地图稳定性。

KDE不单独作为显著性证据。至少比较5、10、20和30 km，或依据最近邻距离设置数据驱动带宽并做敏感性分析。

---

# 6. 第四阶段：主要统计检验

## 6.1 首选方法：条件化空间点过程

主要模型采用inhomogeneous Poisson point process，或其等价的case-availability近似：

\[
\lambda(s)
=
\exp
\left[
\beta_0+
f_{power}(s)+
f_{fiber}(s)+
f_{water}(s)+
f_{market}(s)+
f_{land}(s)
\right]
\]

背景点是对availability domain进行数值积分或抽样，不代表真实失败项目。

## 6.2 第一版核心变量

| 因素 | 第一版变量 | 判断边界 |
|---|---|---|
| 电力 | 变电站距离、输电线距离、电压等级 | 距离不等于剩余容量 |
| 网络 | 商业高速光纤覆盖、供应商数或记录数 | 记录数与独立供应商数分开 |
| 水 | 公共供水服务区距离 | 供水覆盖不等于可提供项目需水量 |
| 市场 | metro距离、人口或就业密度 | 用于控制城市化 |
| 土地 | 可开发土地、坡度、土地价值代理 | 历史与当前年份要区分 |
| 交通/风险 | 仅保留定义稳定且可解释的少量变量 | 不堆积低质量字段 |

existing DC density不能进入regime或关联模型的解释变量，因为目标本身就是DC位置。

## 6.3 变量时间边界

主要横截面分析可以使用统一当前快照，但只能解释：

> 当前站点与当前基础设施环境的空间对应关系。

只有获得接近opening year的历史基础设施数据后，才能解释历史选址条件。当前基础设施不能直接作为早期站点的决策时点变量。

## 6.4 验证方式

不使用普通随机train/test split。采用：

- 按metro或空间块划分的spatial cross-validation；
- leave-one-metro-out敏感性分析；
- Nashville、Memphis等单一区域影响诊断；
- spatial block bootstrap置信区间；
- 变量定义和背景域敏感性分析。

## 6.5 主要结果

报告：

- 变量效应方向；
- 效应量与置信区间；
- 空间外验证性能；
- 不同背景域下的稳定性；
- 是否由单一metro驱动；
- 不支持假设的结果。

显著性不能替代效应量和空间稳定性。

---

# 7. 第五阶段：剩余空间聚集

在主要协变量模型之后，使用inhomogeneous Ripley’s K/L检验：

> 控制可开发土地、市场、电力、网络和水资源环境后，数据中心是否仍存在未解释聚集？

分析要求：

- 使用Tennessee边界的edge correction；
- 使用与主要模型一致的availability domain；
- 通过Monte Carlo envelope比较；
- 预先固定距离范围；
- 避免对每个距离分别进行未经校正的显著性解释。

距离尺度可从1、5、10、20、50和100 km开始，但最终范围应结合TN站点数量和空间尺度确定。

普通nearest-neighbor analysis仅作为直观补充，不作为主要推断证据。

---

# 8. 第六阶段：Infrastructure Regimes探索

这一阶段是探索性分析，不参与主要假设的显著性结论。

## 8.1 分析对象

在D1或D2背景中的所有空间cell上构造基础设施向量：

\[
X_i=[
Power_i,
Fiber_i,
Water_i,
Land_i,
Market_i,
Hazard_i
]
\]

先对偏态距离和成本变量变换，再标准化。

## 8.2 推荐流程

\[
X
\rightarrow
PCA
\rightarrow
HDBSCAN
\rightarrow
Infrastructure\ Regimes
\rightarrow
DC\ Enrichment
\]

- PCA用于解释主要基础设施维度；
- HDBSCAN用于发现稳定环境类型；
- UMAP只作为辅助可视化；
- 不解释UMAP坐标轴；
- 不把cluster直接命名为高、中、低适宜性。

## 8.3 Regime enrichment

\[
ER_k=
\frac{P(Regime=k\mid DC)}
{P(Regime=k\mid Availability)}
\]

分母使用D1或D2 availability，不使用全州面积作为唯一基准。

报告：

- enrichment ratio；
- log enrichment；
- spatial block bootstrap置信区间；
- 不同空间尺度和cluster参数下的稳定性；
- HDBSCAN noise比例。

如果Regime A只对应“城市”，应直接命名为urban infrastructure regime，而不是创造过度抽象的机制名称。

---

# 9. Facility Type、Capacity和Time的启动条件

## 9.1 Facility-type分析

dcmap.us定义的Hyperscale、Colocation、Enterprise和Neocloud可以分层，但只有满足以下条件才进行独立推断：

- 类型定义能够稳定映射；
- 每类具有足够独立sites；
- 结果不由一个campus主导；
- 坐标和关键特征覆盖率可接受。

样本不足时只报告描述统计，或合并为少数有物理意义的大类。

## 9.2 Capacity分析

容量加权分析只有在以下条件下进入主要结果：

- capacity统一按dcmap.us定义解释为铭牌或规划容量，而不是当前运营负荷；
- reported与estimated容量分开报告并进行敏感性分析；
- 缺失模式得到报告；
- 极端大站点的影响进行leave-one-site-out检验。

## 9.3 Temporal分析

时间演化是后续可选模块。只有同时满足以下条件才启动：

- opening year覆盖充分；
- 各时期有足够独立sites；
- 状态和年份定义一致；
- 关键基础设施具有历史版本；
- 当前数据库的收录时间偏差能够评估。

否则只能描述不同opening cohort的当前空间分布，不能写成历史选址机制变化。

---

# 10. 方法分级与取舍

## 10.1 主要方法

- Campus/site canonicalization；
- developable-land availability domain；
- conditional point-process model；
- spatial cross-validation。

## 10.2 次级诊断

- KDE；
- count与capacity地图；
- inhomogeneous Ripley’s K/L；
- leave-one-metro-out；
- matched Monte Carlo。

## 10.3 探索性方法

- PCA；
- HDBSCAN；
- regime enrichment；
- UMAP visualization；
- facility-type和temporal stratification。

## 10.4 当前不作为核心的方法

- 对原始count同时运行Moran’s I、LISA和Getis-Ord全部检验；
- 使用DBSCAN给少量DC点强制定义市场；
- 在全州uniform random结果上作主要结论；
- 用existing DC density解释DC分布；
- 根据TN结果反向修改预设假设或分析阈值；
- 把无监督cluster称为suitability grade。

---

# 11. Multiple Testing与结果解释

主假设数量应保持有限。建议H1–H4为预先声明问题，其余均标记为探索性。

如果对多个基础设施变量、距离阈值或facility type重复检验，应：

- 报告检验总数；
- 使用FDR或其他适当校正；
- 报告效应量与置信区间；
- 保存不显著结果；
- 不根据显著性选择bandwidth、空间尺度或背景域。

核心表述分为：

- **观察证据：**数据中直接计算出的结果；
- **模型推断：**在模型假设下得到的关联；
- **候选解释：**可能的基础设施或市场原因；
- **不能确认：**数据无法区分的替代解释。

---

# 12. Adversarial Review：哪些结果会使研究结论变弱？

以下情况必须被视为实质性反证或限制：

1. 控制urban/industrial背景后，电力和网络效应消失。
2. 结论只在statewide uniform背景下显著。
3. Nashville或Memphis任一区域删除后效应方向改变。
4. Site去重规则稍作改变，聚集结论明显变化。
5. dcmap.us坐标或状态存在系统性错误。
6. Capacity结果完全由一个超大型campus驱动。
7. PCA/HDBSCAN regimes随空间尺度或参数剧烈改变。
8. 当前基础设施变量无法代表站点建设年份。
9. dcmap.us基于公开记录的编制方式对小型、私有或早期设施存在明显漏报。

这些结果不能被隐藏在平均指标中，应进入主文限制或敏感性分析。

---

# 13. TN阶段交付物

## 13.1 数据产物

- dcmap.us Tennessee授权数据快照说明；
- canonical_sites；
- site_facility_crosswalk；
- status与facility type映射表；
- capacity和opening year缺失报告；
- Tennessee availability domain；
- site-to-infrastructure feature table；
- 每个特征的来源、年份、单位和空间处理说明。

## 13.2 图表

1. Tennessee operational、under-construction和planned/approved分层地图；
2. Site count KDE；
3. Capacity-weighted KDE；
4. D0、D1和D2背景地图；
5. 主要基础设施距离分布；
6. 空间点过程效应图；
7. Residual Ripley’s L envelope；
8. PCA loading与regime地图；
9. Regime enrichment及置信区间；
10. 数据缺失和坐标精度图。

## 13.3 结果表

- Canonicalization汇总；
- 主假设与统计结果；
- 不同availability domain敏感性；
- leave-one-metro-out结果；
- count与capacity差异；
- 探索性regime稳定性；
- 未通过的数据质量门。

---

# 14. 阶段质量门

## Gate A：数据对象可用

必须满足：

- parent-child关系得到处理；
- site去重规则可复现；
- 状态定义明确；
- 坐标错误和重复记录有复核结果。

未满足则停止空间统计。

## Gate B：主要空间变量可用

必须满足：

- 基础设施图层覆盖Tennessee；
- 单位和投影统一；
- 图层年份已记录；
- 距离和重叠计算通过抽样检查。

未满足则只发布描述性地图。

## Gate C：统计推断可用

必须满足：

- Operational独立site数量足以支持所选模型；
- spatial folds不会产生空测试区域；
- 结果不完全由一个metro驱动；
- sensitivity analysis能够运行。

未满足则不报告强推断。

## Gate D：扩展模块可用

Facility type、capacity和temporal分析分别通过自身的数据量、定义和时间条件后才启动。它们不是主流程的必需条件。

---

# 15. 优化后的TN工作流

    dcmap.us Tennessee Authorized Snapshot
                │
                ▼
    Source and License Audit
                │
                ▼
    Campus / Site Canonicalization
                │
                ├── canonical_sites
                └── site_facility_crosswalk
                │
                ▼
    Status and Type Stratification
                │
                ▼
    Tennessee Availability Domains
                │
                ├── D0 State Land
                ├── D1 Developable Land
                └── D2 Urban/Industrial Matched
                │
                ▼
    Descriptive Mapping
                │
                ├── Operational / Under Construction / Planned or Approved
                ├── Site Count
                └── Capacity Weighted
                │
                ▼
    Conditional Point-Process Analysis
                │
                ├── Power
                ├── Fiber
                ├── Water
                ├── Market
                └── Land
                │
                ▼
    Spatial Validation and Residual K/L
                │
                ▼
    Exploratory Infrastructure Regimes
                │
                ├── PCA
                ├── HDBSCAN
                └── Enrichment
                │
                ▼
    Optional Type / Capacity / Temporal Modules
                │
                ▼
    Tennessee Findings and Limitations

---

# 16. 当前最重要的下一步

当前不应首先计算KDE、PCA或训练模型。第一项任务是完成：

\[
\boxed{\text{dcmap.us Tennessee Canonical Site Table}}
\]

具体顺序：

1. 获得并冻结经dcmap.us许可的Tennessee记录级数据快照；
2. 列出原始字段、状态值和facility type；
3. 建立Campus与child facility关系；
4. 形成site-level去重结果；
5. 人工复核模糊合并；
6. 统计Operational独立site数量；
7. 报告capacity、opening year和坐标精度；
8. 根据实际样本量决定哪些分析模块能够启动。

完成这一步后，再决定主要空间单元、availability domain和第一版基础设施变量。全国扩展不属于当前阶段，也不应影响TN数据对象和主要假设的判断。
