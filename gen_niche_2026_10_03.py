#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the daily niche OPC industry brief for 2026-10-03.

Industry: 专业族谱研究 / 家史编撰服务（含血统公民身份文件整理与 DNA 寻亲）
Writes runs-workbuddy/2026-10-03/niche-opc-industry.json
"""
import json
import os

OUT_DIR = os.path.join(os.path.dirname(__file__), "runs-workbuddy", "2026-10-03")
OUT_PATH = os.path.join(OUT_DIR, "niche-opc-industry.json")

details = """1. 行业是什么，为什么小众
专业族谱研究 / 家史编撰服务（Professional Genealogy Research & Family History），指帮个人客户追溯祖先、梳理家族脉络、考证血缘关系，并交付一份带原始档案引用的家谱/家族报告、系谱图（GEDCOM 文件）甚至精装家史书。它还包括两个高价值细分：一是「血统公民身份文件整理」（为想申请爱尔兰、意大利、波兰等血统入籍的人，考证并获取完整证明链文件），二是「DNA 寻亲/被收养者寻根」（用基因检测结果 + 谱系三角定位，帮人找到生物学亲人）。

为什么小众、容易被忽略：
- 搜索量极低：客户不会搜「族谱研究服务」，他们搜的是「我爷爷是哪来的」「怎么证明意大利血统」「找亲生父母」。需求极其隐蔽，独立从业者很难被算法发现，反而被 Ancestry/MyHeritage 这类自助平台截流表面流量。
- 夹缝生存：大众以为「查家谱」要么自己用 Ancestry 免费捣鼓，要么花几千美元找 Legacy Tree 这种大机构；中间价位、个人化、可远程交付的「一人研究者」档位长期缺位。
- 认知偏差：外人以为这需要历史学位或能读古拉丁文，实际核心是方法论 + 耐心 + 用对数据库，普通人在 1-2 个月就能上手基础交付。
- 数字游民视角下被低估：它 100% 可远程、全球客户、低边际成本，却很少出现在「一人公司赚钱方向」清单里，因为不性感、不科技。

2. 如何运作
典型客户与需求触发：
- 好奇家族史的普通消费者（做家谱书当礼物、给子孙留记录）。
- 想申请血统公民身份的人（爱尔兰/意大利/波兰/德国等，需一整条无断点的出生/结婚/死亡证明链）。
- 被收养者、NPE（基因检测结果意外发现非亲生父母）、捐精受孕者，想找生物学亲人。
- 继承/遗嘱纠纷中需要证明亲属关系的人；想要进宗族协会（lineage society）的人。

核心交付物：
- 带原始档案引用的系谱报告（PDF）+ 可导入 Ancestry/MyHeritage 的 GEDCOM 文件；
- 系谱图、家族时间线、移民路线可视化；
- 血统入籍用的「文件清单 + 已获取并认证的证明链」；
- DNA 寻亲的「匹配三角分析报告 + 亲属身份推断」。
（不提供法律意见——涉及入籍/法庭时转介持证律师，这是红线。）

完整工作流：
- 获客：Upwork / Fiverr / Contra 发服务；在 APG（专业家谱师协会）目录挂名建立可信度；Facebook/Reddit 寻根社群、血统入籍论坛、领英内容引流；熟人/移民律师/公证处转介。
- 沟通报价：先让客户填已知信息（姓名/日期/地点），做免费可行性初查确认「有没有足够记录」，再出方案与报价。常见按小时（$30–$200）或按项目（starter $50–$300，深度项目 $500–$5,000+）。
- 研究执行：在 FamilySearch（免费、40 亿+记录）、Ancestry、MyHeritage、Findmypast、各国国家档案馆数字库里检索户籍/教堂/ census/移民/军事/报纸档案；DNA 案用 GEDmatch、DNAPainter 做三角定位。
- 交付收款：产出带引用的 PDF 报告 + GEDCOM，走平台托管或 Stripe/平台收款；可转为月度 retainer（持续研究）或升级到家史书精装版。

关键工具/平台：
- 记录库：FamilySearch（免费）、Ancestry、MyHeritage、Findmypast、Geneanet、BillionGraves（墓碑）。
- DNA：AncestryDNA、23andMe、FamilyTreeDNA、GEDmatch（免费上传）、DNAPainter。
- 软件：Gramps（免费开源）、RootsMagic、Legacy Family Tree、Family Tree Maker；标准格式 GEDCOM。
- 证书/可信度：APG 会员目录、BCG（Board for Certification of Genealogists）认证。
- 交付美化：Canva / Adobe InDesign 做家史书，静态站做家族网站。

3. 盈利模式
收入来源与定价：
- 按项目（最常见）：Fiverr 上入门档 $10–$60，标准 3 代 $30–$250，深度 5 代 $250+；Upwork「Family & Genealogy」类目有 180+ 在售项目，起价 $25，意大利血统资格预检 $25、深度研究 $50–$300。
- 按小时：APG 公布区间 $30–$200+/小时（经验、地区、专业度决定）；个体研究者约 $65/小时，自由职业者 $40–$60，机构 $75–$95。
- 高端项目：Legacy Tree 套餐 BASIC 25 小时 $3,200（$128/时）、STANDARD 50 小时 $6,000、PREMIUM 100 小时 $11,500；Ancestry ProGenealogists 起价 $3,700（20 小时）。
- 血统入籍专项：专门研究者按 $50–$200/时，整案 $500–$5,000（LegalClarity）；CitizenX 估计专业家谱服务 $2,000–$10,000，整项入籍总成本 $5,000–$15,000。
- DNA 寻亲：专业基因家谱师 $500–$3,000，完整寻亲 $1,500–$5,000+；DNAngels 付费档 Bronze $1,250 / Silver $2,500 / Gold $5,000。
- 产品化：低价「资格预检」「starter 系谱报告」「DNA 匹配解读咨询」可批量获客；家史书精装升级包。

利润空间：工具成本极低——FamilySearch 免费，Ancestry 订阅约 $25–$50/月，软件多为一次性或免费；主要成本就是你的时间。扣除平台费（Upwork 约 10%、Fiverr 20%）后，单人项目毛利常在 70%–90%。一份 $1,500 的 3 代报告，成本主要是订阅与研究时间。

复购/长期：家史是持续工程，客户常追加支线、升级家史书、转月度 retainer；血统入籍客户还会带来亲友转介（一个家族多人申请）。

4. 入门门槛
技能：会检索与交叉验证档案、懂基础史料来源评级（一手/二手）、能写清晰引用；DNA 方向需懂基本遗传规律与三角定位（可学）；耐心与细心比学位重要。历史/外语（意、西、德、波、中地方志）是加分项而非必需。
学起来多快：每天 1–2 小时，4–8 周可独立交付「3 代 sourced 报告」。FamilySearch、NGS（国家家谱学会）有免费入门课。

工具/费用：起步几乎为零——FamilySearch 免费 + 一个 Ancestry 月付试用（$25–$50）；免费 Gramps 软件；DNA 案需让客户自行购买试剂盒（约 $100–$120，客户出）。初期月成本可控在 $50–$100。

资金：启动资金可接近 0（用免费库 + Fiverr/Upwork 零入驻费），最多几百元订阅费。

时间：从零到第一单通常 2–6 周（先打磨 1 份样稿 + 上架服务），比多数技能型服务快，因为门槛低、平台已有现成需求池。

5. 为什么适合 OPC / 数字游民
- 100% 远程 + 异步：记录几乎全在线上（户籍数字化浪潮，FamilySearch 2025 年 5 月单月新增 1.18 亿条来自 37 国的记录），沟通靠邮件/Zoom，研究本身是可深夜异步推进的深度活。
- 全球客户： diaspora（移民后裔）、想拿欧盟护照的人、跨国被收养者遍布全球，你住巴厘岛也能服务美国/欧洲/拉美客户，天然地理套利——用美元定价、低成本生活。
- 低边际成本、高时薪：一份报告卖 $150–$1,500，复制成本为零，且越是「稀缺专业」（如意大利血统、犹太谱系、亚洲离散族群）越能溢价。
- 可规模化：把流程拆成低价「资格预检/DNA 解读」引流产品 + 高价「完整研究/家史书」利润产品；做模板、SOP、甚至轻量课程。
- 时区友好：核心交付是书面报告，不要求实时在线；少量客户电话可约在重叠时段。
- 护城河来自专精：选一个细分（如「意大利 jure sanguinis 文件链」「爱尔兰 Foreign Births Register」「华裔寻根」）积累案例与口碑，比泛做更难被低价竞争者取代。

6. 潜在收益（谨慎，不承诺）
以下为公开数据区间，仅作参考，不等于个人收入：
- 新手阶段（前 3–6 月）：在 Fiverr/Upwork 接 starter 单，单价 $30–$250，月接 5–15 单，毛收入约 $300–$2,000/月；多数时间用于建口碑与案例。
- 成熟阶段（6–18 月后）：建立专精 + 直接客户 + retainer，时薪 $65–$150，深度项目 $1,500–$5,000/单，月 2–4 单可到 $3,000–$10,000/月；血统入籍专项客单价更高。
- 市场大盘：全球族谱产品与服务市场 2024 年约 $66 亿，预计 2032 年达 $166 亿（Kings Research，CAGR 12.06%）；另一报告给出 2025 年 $58.5 亿 → 2032 年 $115.5 亿（CAGR 10.21%）。北美占约 34% 份额，亚太增速最快（13%+）。Ancestry 拥有 1,200 万+ 家谱树，FamilySearch 免费库 40 亿+ 记录，说明底层需求池巨大。
- 机构对标：Legacy Tree / Ancestry ProGenealogists 单客收费数千美元，证明「有人愿意为靠谱研究付高价」。
提示：这是研究服务，结果不保证（记录可能损毁），收入随经济与个人口碑波动，切勿理解为稳定被动收入。

7. 主要风险
- 市场风险：家谱属「可延迟消费」，经济差时需求先被砍；血统入籍需求受政策直接冲击——意大利 2025 年 3 月颁布的政令（后转为 2025 年第 74 号法律）大幅收紧资格（限父母/祖父母为纯意大利籍且未入籍他国），直接导致部分从业者需求缩水。
- 技术风险：平台政策变化（Ancestry/MyHeritage 访问限制、DNA 数据隐私监管 GDPR 收紧）；各国档案数字化不均，部分记录根本未上线；AI 自动化会吃掉最浅层的「查一下」活（MyHeritage 称 AI 匹配减少 60% 人工）。
- 合规风险：DNA 与家谱含高度敏感个人数据，须遵守 GDPR/各地隐私法，跨境传输要谨慎；血统入籍涉及法律程序，超出研究范围必须转介持证移民律师，不能给法律意见；全球客户可能触发增值税/所得税与常设机构问题。
- 现金流风险：深度项目周期长（4–6 月常见），建议收预付款/分阶段里程碑收款；获客初期依赖平台抽成高、排名难。

8. 不适合的人群
- 想要「今天做明天收钱」即时收入的人：研究常需数周。
- 追求确定性与「保证找到」的人：记录可能灭失，专业做法是诚实报告「无解」而非忽悠。
- 讨厌琐碎案头与老文件/手写体的人。
- 想要纯被动收入、不愿持续与人沟通交付的人。
- 没有耐心学外语或跨档案推理的人；以及想借「入籍服务」打法律擦边球的人（红线）。

9. 3 个可验证的入门步骤
- 7 天内：注册 FamilySearch（免费）并开一个 Ancestry 试用，给自己或朋友做一份 3 代谱系树，学会来源引用与 GEDCOM 导出；验证你能否在线上档案里真正推进。成本约 $0–$50。
- 14 天内：选定一个专精方向（如意大利/爱尔兰血统资格预检，或美国「brick wall」研究），在 Upwork/Fiverr/Contra 上读 10 个真实在售 gig，记录真实报价与需求，并草拟你自己的服务页/报价单；可顺手看一节免费家谱入门课。
- 21 天内：以 $50–$150 低价在 Fiverr/Upwork 或熟人圈推出「starter 系谱报告」（1 条线、2–3 代、带引用 PDF + GEDCOM），真实完成 1–2 单走完「沟通→研究→交付→收款」全流程，验证客户付费意愿与自身研究能力。成本主要是一点心力和 $50–100/月订阅。

10. 核验来源
（详见文末 artifacts 链接，均为真实可访问页面）
- APG（专业家谱师协会）「如何聘请家谱师」与费率说明：$30–$200+/小时。
- Legacy Tree 官方价目：BASIC $3,200 / STANDARD $6,000 / PREMIUM $11,500。
- Upwork「Family & Genealogy」类目：180+ 在售项目，起价 $25，含意大利血统资格预检 $25、深度研究 $50–$300。
- Fiverr 实际 gig：入门 $10–$60、标准 3 代 $30–$250、深度 5 代 $250+。
- FamilySearch 免费档案库（40 亿+ 记录，2025 年 5 月单月新增 1.18 亿条）。
- Kings Research 族谱市场报告：2024 $66 亿 → 2032 $166 亿（CAGR 12.06%）。
- PMarketResearch 族谱市场报告：2025 $58.5 亿 → 2032 $115.5 亿（CAGR 10.21%）。
- CitizenX 血统入籍词条：专业家谱服务 $2,000–$10,000，整项入籍 $5,000–$15,000。
- DNAngels 付费服务：Bronze $1,250 / Silver $2,500 / Gold $5,000（DNA 寻亲对标）。"""

data = {
    "taskId": "niche-opc-industry",
    "taskName": "每日小众赚钱行业：专业族谱研究 / 家史编撰服务",
    "status": "success",
    "startedAt": "2026-10-03T09:07:00+08:00",
    "finishedAt": "2026-10-03T09:58:00+08:00",
    "summary": "专业族谱研究 / 家史编撰服务：帮个人追溯祖先、考证血缘并交付带档案引用的家谱报告与 GEDCOM 文件，还覆盖高价值的血统公民身份文件整理与 DNA 寻亲。它 100% 可远程、全球客户、启动成本近乎为零、单人即可闭环，且底层需求池巨大（全球市场 2024 年约 $66 亿、年增 12%），是非常契合一人公司/数字游民却被严重低估的方向。",
    "details": details,
    "sourceThread": "workbuddy-daily-niche-research",
    "labels": [
        "daily",
        "niche-industry",
        "opc",
        "digital-nomad",
        "genealogy",
        "family-history",
        "research-service",
        "citizenship-by-descent",
    ],
    "nextSteps": [
        "7 天内注册 FamilySearch（免费）并开 Ancestry 试用，给自己或朋友做一份 3 代谱系树并学会来源引用与 GEDCOM 导出，验证能否在线上档案里真正推进研究。",
        "14 天内选定一个专精方向（如意大利/爱尔兰血统资格预检或美国 brick-wall 研究），在 Upwork/Fiverr/Contra 读 10 个真实在售 gig 记录报价与需求，草拟自己的服务页与报价单。",
        "21 天内以 $50–$150 低价推出「starter 系谱报告」（1 条线、2–3 代、带引用 PDF + GEDCOM），真实完成 1–2 单走完沟通→研究→交付→收款全流程，验证客户付费意愿与自身研究能力。",
    ],
    "artifacts": [
        {
            "label": "APG 专业家谱师协会 — 如何聘请与费率说明（$30–$200+/小时）",
            "path": "https://www.apgen.org/cpages/how-to-hire-a-professional-genealogist",
        },
        {
            "label": "Legacy Tree Genealogists 官方价目（BASIC $3,200 / STANDARD $6,000 / PREMIUM $11,500）",
            "path": "https://www.legacytree.com/order/?product_id=11673",
        },
        {
            "label": "Upwork Family & Genealogy 类目（180+ 在售项目，起价 $25）",
            "path": "https://www.upwork.com/services/family-genealogy",
        },
        {
            "label": "FamilySearch 免费档案库（40 亿+ 记录）",
            "path": "https://www.familysearch.org/",
        },
        {
            "label": "Kings Research — 族谱产品与服务市场（2024 $66 亿 → 2032 $166 亿，CAGR 12.06%）",
            "path": "https://www.kingsresearch.com/genealogy-products-and-services-market-29",
        },
        {
            "label": "PMarketResearch — 族谱研究产品与服务市场（2025 $58.5 亿 → 2032 $115.5 亿）",
            "path": "https://pmarketresearch.com/?p=2303893",
        },
        {
            "label": "CitizenX — 血统入籍词条（专业家谱服务 $2,000–$10,000）",
            "path": "https://citizenx.com/glossary/citizenship-by-descent",
        },
        {
            "label": "DNAngels 付费 DNA 寻亲服务（Bronze $1,250 / Silver $2,500 / Gold $5,000）",
            "path": "https://dnangels.org/paid-services",
        },
    ],
}

os.makedirs(OUT_DIR, exist_ok=True)
with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("wrote", OUT_PATH)
