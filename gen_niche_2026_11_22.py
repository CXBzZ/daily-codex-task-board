#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 2026-11-22 每日小众赚钱行业调研结果：企业分类法与元数据体系设计（Taxonomy & Metadata Design）。"""

import json
import os
from datetime import datetime, timezone, timedelta

SH_TZ = timezone(timedelta(hours=8))
now = datetime.now(SH_TZ)
started = now - timedelta(minutes=11)
finished = now

details = """1. 行业是什么，为什么小众
一句话定义：为电商目录、网站/App 导航、企业知识库、CMS/DAM 与 AI 检索系统设计「分类法 + 受控词表 + 元数据模型 + 标签治理规则」——让内容、产品和文档能被用户找到、被系统复用、在不同平台里说的是同一种话。业内常叫 taxonomy design、controlled vocabulary、metadata architecture，或信息架构（IA）里最偏数据和治理的那一半。
为什么被忽略：（1）成果是隐形的，用户只看到导航栏、筛选项和搜索结果，不会想到背后有一套有偿设计的规则；（2）需求触发很隐蔽——出现在网站改版、CMS 迁移、搜索零结果、电商属性筛选错乱、标签越打越乱、AI 客服/RAG 答非所问的时候，客户搜的是“search relevance”“faceted navigation”“tag cleanup”，几乎没人搜“分类法顾问”；（3）它夹在 UX、SEO、内容运营、数据治理、图书馆情报学几个大行业之间，各方都觉得“那是别人的事”，中间这条专业服务带长期存在却没人命名；（4）门槛认知两极：外行以为就是“排个目录”，内行知道要做卡片分类、树测试、层级与分面的取舍、同义词/上位词/弃用词、跨系统映射和治理流程，于是低价标签整理很多、能交付治理体系的人很少；（5）没有响亮工种名，供给分散在 LIS（图书馆与信息科学）和内容策略圈，大众教程自然少。不属于持证上岗线下工种，也不需要库存或店面。

2. 如何运作
典型客户：SKU 数千到数万、筛选维度混乱的中型电商与 DTC 品牌；文档站/B2B SaaS；媒体、协会、出版社的内容团队；企业内部知识库、Intranet、DAM/PIM 管理员；正要上 AI 客服或企业搜索、却发现“文档 tagging 一团糟”的团队；合并重组后术语不统一的组织。需求触发点高度一致：网站改版、系统迁移、搜索转化差、内容找不到、AI 检索答非所问。
核心交付物：一张可扩展的分类树/分面模型（含层级、facet、命名规则）；受控词表与同义词表（首选词、弃用词、See/See also、定义、上下位关系）；元数据模型（字段、类型、是否必填、取值来源、schema.org/SKOS 映射）；内容审计与迁移映射表；治理手册（谁有权新增词、审批流、变更日志、季度清理节奏）；验证报告（卡片分类聚类和树测试成功率）；可导入的 CSV/JSON/SKOS 文件。
完整工作流：1）30–60 分钟需求诊断电话或问卷 → 2）付费小审计：抽样 100–300 条产品/文档，统计重复标签、缺失属性、零结果搜索词 → 3）出 SOW、报价、NDA → 4）内容盘点 + 竞品与用户语言调研（用户怎么叫这个东西，而不是内部行话）→ 5）开放式卡片分类（Open Card Sorting，让用户自己归类）→ 6）设计分类树、词表、元数据模型 → 7）树测试验证（Treejack；业界常用参考是 50 名参与者、任务成功率 80%+ 才算健康）→ 8）与内容/IT/市场方 1–2 轮评审 → 9）交付导入文件 + 治理手册 + 一次培训 → 10）按月 retainer 做新增词审批与季度清理。
关键工具和平台：Google Sheets / Excel / Airtable（词表和映射表，免费起）；Miro / FigJam（工作坊和树图，免费–$15/月）；Optimal Workshop 的 Card Sorting + Tree Testing（Starter 方案 $199/月、按年付、每年 5 个研究，适合把测试成本计入项目报价）；OpenRefine（免费，术语归一化去重）；W3C SKOS、Dublin Core、schema.org（免费标准，用来做跨系统映射）；客户侧常见 PoolParty / TopBraid / Smartlogic / Collibra（企业软件，由客户买单，自由职业者不必自购）；理解 Elasticsearch / Solr 的分面检索文档有助于让方案落地。

3. 盈利模式
收入来源与计价：按项目为主。公开市场中，Rubicon CX 列出独立内容策略顾问常见 $50–300/小时或 $5,000–25,000/项目；企业级“内容模型 + taxonomy”项目报价 $40,000–80,000、周期 8–16 周；其 fractional content lead 为 $6,000–20,000/月。对一人公司更现实的产品阶梯是：付费健康检查 $300–2,000；SMB 分类法 + 词表 + 元数据模型 $3,000–12,000；月度治理维护 $500–3,000；半天工作坊 $1,000–3,000；模板/课程产品化再叠一层长尾收入。
利润空间：主要成本是时间和工具（Optimal $199/月按年付，被试招募按人计费），没有库存、物流或场地。扣掉工具、支付/平台费和自雇税后，项目毛利率通常仍高（大致 70%–90%），但前期访谈、评审和范围蔓延会吃掉大量非计费小时，真实有效时薪要自己记时核算。
复购/长期合同：天然有续费属性——新品类上线、并购整合、CMS/DAM 迁移、多语言扩张、AI 检索上线都要重新对齐分类体系；一旦词表嵌入客户系统，替换成本高，年度维护 retainer 比一次性项目更稳。

4. 入门门槛
技能：核心是信息组织基本功（层级 vs 分面、受控词表、同义词/上下位/弃用词、命名一致性）、用户调研（卡片分类、树测试、写不诱导的任务）、基础数据分析（Excel 透视表/去重）、能读懂电商后台和 CMS 字段、能把治理规则写成客户可执行的文档。不需要 MLS 学位或法定执照；图书馆、内容策略、UX、电商运营背景是加分项而非硬门槛。系统学习 4–8 周可上手：读 W3C SKOS  primer/参考与 Optimal 的卡片分类、树测试文档，跟做 2 个公开案例，再用免费层跑一次真实小测试。
工具：起步 $0–60/月（Sheets/Airtable、Miro 免费层、OpenRefine 免费）；需要做正式验证时再买 Optimal Starter $199/月（按年付），并把成本写进项目报价；PoolParty 等企业语义工具由客户侧提供，不要求你自己买。
资金：$0–500（域名/作品集、少量被试招募、偶尔的测试额度），不需要设备、库存或场地。
时间：2–4 周能做出 2 个可展示案例并挂出服务；从零到第一单常见 1–3 个月，关键变量是能否找到正处在改版/迁移/搜索优化节点的客户。

5. 为什么适合 OPC / 数字游民
全异步远程：只需要客户导出的 CSV/JSON、录屏访谈和评审会议，不需要到现场，也不需要本地执照或实体场所；白天开客户会、夜里搭词表非常契合游民时区。
客户与市场全球化：英语市场为主，电商、SaaS、出版、协会团队分散在欧美澳；一套英文作品集可同时卖给多个国家客户，不受本地经济圈限制。
边际成本低、可模板化：词表结构、治理手册、健康检查清单都可以做成模板复用；AI 擅长做初筛聚类和同义词候选，人负责判断、取舍和担责，一个人能覆盖过去需要小团队的工作量。
高价值、不被按人头计价：客户买的是“搜索可用性、筛选转化、AI 检索准确性”的决策质量，不是工时数量；一次几百美元的小审计往往能带出上万美元的体系项目。
延迟不敏感、时区友好：卡片分类和树测试是无人值守的，被试可以在任何时区完成；交付物是结构化文件而非实时服务。
边界清晰：不碰库存、物流、线下施工，也不像纯写作/设计那样陷入按篇按张的低价竞争，适合喜欢结构化思考、能坐得住细节的人长期经营。

6. 潜在收益（谨慎，不承诺）
公开参考数据：Rubicon CX 公开报价显示独立顾问 $50–300/小时或 $5,000–25,000/项目、企业内容模型与 taxonomy 项目 $40,000–80,000/8–16 周、fractional 岗位 $6,000–20,000/月；Grand View Research 估算全球企业搜索市场 2023 年 48.672 亿美元、2030 年 88.517 亿美元，CAGR 8.9%，说明“找得到”这件事有持续预算；PoolParty 官网称其语义套件被 180+ 企业与机构使用，并列出 Microsoft、Wolters Kluwer、HealthDirect Australia 等案例；Lettria 与 Leroy Merlin 母公司 Adeo 的公开案例显示，分类师+AI 辅助为产品本体新增 10,000+ 类、60%+ 建议被采纳、节省 100+ 小时。上述都是市场规模、企业报价或大企业团队成果，不是个人收入承诺。
分阶段、条件化推算：新手阶段（有 2–3 个作品、1 个小审计和一个 SMB 项目）：单项目 $1,000–5,000，月收入 $1,000–4,000、有效时薪约 $30–80 更现实，前 3 个月为 $0 也很常见；成熟阶段（3–5 个回头客户或 1–2 个 retainer、有英文案例和垂直口碑）：月 $5,000–15,000 可期，接到企业内容模型项目会更高，但那要求企业级沟通和系统落地经验。这些是参考数据，不等于个人收入；实际受语言能力、作品集质量、客户所在市场、获客渠道和宏观预算周期影响极大。

7. 主要风险
市场风险：需求常被推迟到改版/迁移才发生，销售周期长；AI 搜索与 RAG 热潮让部分客户误以为“大模型自动打标就够了”，低估治理价值；低端“标签整理”外包会压价。
技术风险：客户系统碎片化（CMS、DAM、PIM、电商各自一套字段），设计得漂亮却落不了地；Optimal/PoolParty 等工具涨价或政策变化；SKOS、schema.org 等标准持续演进，需要跟着学。
合规风险：会接触企业内部文档、产品数据和用户搜索词，NDA、GDPR、数据跨境与客户数据保密条款必须落实；医疗、金融、政府内容有更严格限制；交付物的术语所有权与复用权要写进合同。
现金流风险：项目制加 Net-30/60 账期，访谈和评审若不计入交付会吞噬利润；测试工具年付、被试招募是前置成本；“顺便帮我们清一下标签”这类范围蔓延必须用 SOW 和变更单控制。

8. 不适合的人群
讨厌访谈、评审和反复沟通，只想闷头产出图或代码的人；对“一个标签到底叫 color 还是 colour”没有耐心、不愿逐条核对上百行词表的人；期待两周内出单、又不愿先做低价审计积累案例的人；英文读写与结构化表达吃力却主攻欧美客户的人；把“AI 一键生成分类”当完整交付、不愿为判断质量担责的人；需要稳定月薪、无法承受项目空窗的现金流敏感型选手。

9. 3 个可验证的入门步骤
第一步（1 天）：读 W3C SKOS 主页与 Optimal Workshop 的卡片分类/树测试文档，为一个你熟悉的小站点或公开电商类目，用 Excel 写出 30 个概念的首选词、同义词、上位词、弃用词各一列，并写 3 条治理规则。验证标准：2 小时内完成，且自己说不清的条目少于 5 个。
第二步（2–3 天）：找 1 个真实小样本（朋友的 Shopify 店、Notion 知识库或文档站），导出 100–200 条标题/标签，用 OpenRefine 或 Sheets 找出重复标签和缺失属性，输出一页“分类健康检查”PDF，并当面讲清 3 个最值钱的修复点。验证标准：对方愿意给一句推荐，或愿意付 $100–300 做完整版。
第三步（1–3 天）：用 Notion/Carrd 搭一个极简作品集页，在 Upwork、LinkedIn 和相关社群发布“$299 Taxonomy Health Check（限 5 名）”服务，或向 Taxonomy Boot Camp / ASIS&T 圈子里 3 个潜在客户约 20 分钟诊断电话。验证标准：两周内拿到至少 1 个付费小单或 1 个明确的改版/迁移项目线索；若零反馈，就收窄到垂直场景（如“Shopify 产品属性与筛选治理”）重来。

10. 核验来源
W3C SKOS 官方标准（分类法/词表/受控词汇的语义网标准）：https://www.w3.org/2004/02/skos/
Taxonomy Boot Camp 2026（第 21 届分类法与元数据专业会议，证明成熟职业社群）：https://www.taxonomybootcamp.com/
PoolParty Semantic Suite 官网（180+ 企业客户、Microsoft/Wolters Kluwer/HealthDirect 案例）：https://www.poolparty.biz/
Lettria × Adeo / Leroy Merlin 案例（10,000+ 新类、60%+ 采纳、100+ 小时节省）：https://www.lettria.com/case-study/leroy-merlin-knowledge-graph-product-recommendations
Rubicon CX 公开报价（自由顾问 $50–300/小时、$5k–25k/项目；企业 taxonomy $40k–80k）：https://rubicon.cx/fractional-services/costs/
Optimal Workshop 卡片分类/树测试产品页与定价（Starter $199/月、50 人与 80% 成功率的测试建议）：https://www.optimalworkshop.com/treejack
Grand View Research 全球企业搜索市场（2023 $48.672 亿 → 2030 $88.517 亿，CAGR 8.9%）：https://www.grandviewresearch.com/horizon/outlook/enterprise-search-market/global/scopes
ASIS&T 官网（信息科学与信息组织专业协会、职业资源）：https://www.asist.org/
"""

payload = {
    "taskId": "niche-opc-industry",
    "taskName": "每日小众赚钱行业：企业分类法与元数据体系设计（Taxonomy & Metadata Design）",
    "status": "success",
    "startedAt": started.isoformat(),
    "finishedAt": finished.isoformat(),
    "summary": "企业分类法与元数据体系设计是为电商目录、知识库、CMS/DAM 与 AI 检索系统设计受控词表、标签规则和信息架构的小众服务，需求藏在“搜索不准、筛选混乱、AI 答非所问”背后，极少被当成一项可外包的专业活。它 100% 远程异步、客户遍布英语市场、起步工具成本近乎为零，一次设计还能自然续接年度维护，特别适合擅长结构化思考与跨团队沟通的一人公司和数字游民。",
    "details": details,
    "sourceThread": "workbuddy-daily-niche-research",
    "labels": [
        "daily",
        "niche-industry",
        "opc",
        "digital-nomad",
        "information-architecture",
        "taxonomy",
        "metadata",
        "remote-consulting",
    ],
    "nextSteps": [
        "第一步（1 天）：读 W3C SKOS 主页与 Optimal Workshop 的卡片分类/树测试文档，为一个你熟悉的小站点或公开电商类目，用 Excel 写出 30 个概念的首选词、同义词、上位词、弃用词各一列，并写 3 条治理规则。验证标准：2 小时内完成，且自己说不清的条目少于 5 个。",
        "第二步（2–3 天）：找 1 个真实小样本（朋友的 Shopify 店、Notion 知识库或文档站），导出 100–200 条标题/标签，用 OpenRefine 或 Sheets 找出重复标签和缺失属性，输出一页“分类健康检查”PDF，并当面讲清 3 个最值钱的修复点。验证标准：对方愿意给一句推荐，或愿意付 $100–300 做完整版。",
        "第三步（1–3 天）：用 Notion/Carrd 搭一个极简作品集页，在 Upwork、LinkedIn 和相关社群发布“$299 Taxonomy Health Check（限 5 名）”服务，或向 Taxonomy Boot Camp / ASIS&T 圈子里 3 个潜在客户约 20 分钟诊断电话。验证标准：两周内拿到至少 1 个付费小单或 1 个明确的改版/迁移项目线索；若零反馈，就收窄到垂直场景（如“Shopify 产品属性与筛选治理”）重来。",
    ],
    "artifacts": [
        {
            "label": "W3C SKOS 官方标准（分类法/受控词汇的语义网标准）",
            "path": "https://www.w3.org/2004/02/skos/",
        },
        {
            "label": "Taxonomy Boot Camp 2026（第 21 届分类法与元数据专业会议）",
            "path": "https://www.taxonomybootcamp.com/",
        },
        {
            "label": "PoolParty Semantic Suite 官网（180+ 企业客户与 Microsoft 等案例）",
            "path": "https://www.poolparty.biz/",
        },
        {
            "label": "Lettria × Adeo / Leroy Merlin 分类法与知识图谱案例",
            "path": "https://www.lettria.com/case-study/leroy-merlin-knowledge-graph-product-recommendations",
        },
        {
            "label": "Rubicon CX 内容策略与 taxonomy 公开报价",
            "path": "https://rubicon.cx/fractional-services/costs/",
        },
        {
            "label": "Optimal Workshop 树测试产品页（卡片分类/树测试与验证方法）",
            "path": "https://www.optimalworkshop.com/treejack",
        },
        {
            "label": "Grand View Research 全球企业搜索市场 2023–2030 数据",
            "path": "https://www.grandviewresearch.com/horizon/outlook/enterprise-search-market/global/scopes",
        },
        {
            "label": "ASIS&T 信息科学与技术协会官网（职业资源与社群）",
            "path": "https://www.asist.org/",
        },
    ],
}

out_dir = "/Users/pupu/Documents/每日任务/runs-workbuddy/2026-11-22"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "niche-opc-industry.json")
with open(out_path, "w", encoding="utf-8") as fh:
    json.dump(payload, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print(out_path)
