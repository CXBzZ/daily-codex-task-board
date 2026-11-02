# -*- coding: utf-8 -*-
import json, os
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
started = datetime(2026, 11, 2, 9, 22, 44, tzinfo=CST)
finished = datetime(2026, 11, 2, 10, 5, 0, tzinfo=CST)

details = """1. 行业是什么，为什么小众
一句话定义：帮中小企业/团队做“软件订阅体检”——盘点所有 SaaS 与订阅工具、找出闲置与重复授权、重新谈判续费价格，把年度软件开支砍掉 20%–40%。
为什么小众：需求藏在“老板月底看信用卡账单才发现一堆自动续费”背后；几乎没有老板会主动搜索“SaaS 订阅审计”这个服务名（不像 SEO、建站那样有铺天盖地教程）；它夹在“免费自己翻账单”和“Zylo/Vertice 等年费数万美元的企业级 SaaS 管理平台（只服务大客户）”之间的中端空白；而且技术门槛被高估——本质就是电子表格 + 谈判 + 工具常识，不需要写代码。注意：它与本看板已覆盖的「云成本优化 FinOps」明确区分——FinOps 优化的是 AWS/Azure/GCP 的计算/存储账单（基础设施），本次优化的是按席位付费的业务应用订阅（Slack、Notion、HubSpot、Adobe、各类 AI 工具等）与续费谈判，数据来源、交付物与买家（财务/运营，而非云工程）都不同。

2. 如何运作
典型客户：年营收 $200K–$2M 的小企业、代理机构、独立教育者、电商团队、早期 SaaS 公司——大到已经囤了一堆工具、小到没有专职财务/IT 盯着这块。需求触发：融资尽调、现金流紧张、员工离职后发现账号仍在扣费、续费季账单暴涨、“AI 工具乱买”引发的影子 IT。
核心交付物：(1) 订阅清单（每项的用途/负责人/月费年费/续费日）；(2) 浪费诊断报告（闲置、重复、可降档候选）；(3) 整合替换方案（用 1 个替代 3 个）；(4) 谈判底稿或直接代谈续费折扣；(5) 可选季度复盘 retainer。
完整工作流：获客（LinkedIn、小企业经营社群、冷邮件、播客嘉宾）→ 收 90 天银行卡/信用卡账单或授权只读 SaaS 发现工具 → 用 Spendbase/Torii/Zylo 或直接表格盘点 → 出报告与方案 → 客户确认 → 代谈或指导迁移 → 交付节省证明 → 季度复盘。
关键工具与平台：Spendbase（免费层即可做发现）、Torii/Zylo/Tropic/Vendr（企业级，自由职业者主要借用其免费发现功能或纯表格法）；账单聚合用 Ramp/Mercury/Pilot 导出；谈判基准来自 G2/Capterra 价目与 Vendr 公开基准。

3. 盈利模式
收入来源与定价（据 4minuteworkday 2026 实战框架）：一次性审计 $500–$2,000；审计+整合方案 $2,000–$5,000；全量迁移实施 $10,000–$15,000；季度优化 retainer $1,500–$3,000/月。也可按“省下金额的 20%–30%”分成（前提是客户账单干净、可归因）。
利润空间：工具成本近零（免费层+表格），主要是时间投入；扣除平台费（Upwork 10%–15%、Fiverr 20%）与税费后，审计类毛利极高，retainer 端稳定。
复购与长期合同：天然适合 retainer——订阅会“回潮”（bill creep），季度复盘能持续收钱；客户省了真金白银后转介绍极强，易形成年框。

4. 入门门槛
技能：会看账单、会用电子表格、懂主流 SaaS 定价逻辑（席位/年付折扣/年付 vs 月付/降档）、基本谈判话术；学起来 1–2 周可上手，不需要写代码（高级玩法才接 API）。
工具：起步几乎 0 成本——Google Sheets + 一个免费 SaaS 发现工具（Spendbase 免费层或申请 Torii/Zylo 试用）；后期可选 $0–$50/月。
资金：启动 <$100（主要是时间与免费工具）。
时间：从零到第一单约 2–6 周（先给 1–2 个朋友/小客户免费或 $500 做样板案例）。

5. 为什么适合 OPC / 数字游民
- 异步交付：盘点与报告可完全异步完成，时区不敏感，全球客户都能服务（美国小企业的账单、欧洲代理机构、东南亚电商都行）。
- 零库存零场地：纯分析+咨询，有网+表格即可，数字游民友好，不需要本地执照。
- 边际成本低：一套方法论/模板可复制到多个客户，第一份报告最贵，后续边际时间骤降。
- 可规模化：从一次性审计走向 retainer，再到“外包首席简化官”，客单价随时间提升。
- 现金流正向：审计多为预付或平台托管付款，不像长账期项目那样压资金。
- 全球通用痛点：SaaS 蔓延是所有国家小企业的通病，不依赖特定本地市场。

6. 潜在收益（谨慎，不承诺）
以下为公开行业与第三方数据，不等同于任何个人的实际收入：
- 市场规模：全球 SaaS 管理市场 2025 年 $45.8 亿 → 2030 年 $93.7 亿，CAGR 15.4%（MarketsandMarkets，经 GII 转载）；QYResearch 估“SaaS 运营管理软件”2025 年 $7.16 亿 → 2032 年 $12.9 亿，CAGR 8.9%。
- 浪费规模（需求证据）：Torii 2025 SaaS 基准——企业平均 668 个应用、54% 为影子 IT、61% 的 SaaS 应用闲置却仍在付费；Flexera 2025 State of ITAM——35% 组织 SaaS 浪费同比增加，44% 的 Microsoft 365 授权未充分利用或超配。
- 单客可省案例：Bill Creep 案例 45 人公司年 SaaS $412K，60 天取消 29 个、降档 12 个、重谈 4 个，省 $124K/年（30%）；nex365 多个 SMB 案例省 40%；Spendbase 代谈案例单客户省 45%–50%。
- 服务定价区间（4minuteworkday 2026 实战）：审计 $2K–$5K、迁移 $10K–$15K、retainer $1.5K–$3K/月；成熟者服务 3–5 个客户可在 90–120 天做到 $8K–$15K/月。
新手阶段：前 3 个月靠 1–2 个低价/样板单（$500–$2K），主要攒案例与口碑；成熟阶段：3–5 个 retainer + 偶发项目，公开实战框架中的常见月入目标为 $5K–$15K 区间，但取决于获客与个人能力，绝非保证收入。

7. 主要风险
- 市场风险：2026 年已有“SaaS Subscription Reckoning”叙事，早进场者吃红利，窗口约 8–12 个月；之后 Fiverr/代运营涌入会压价。企业级平台（Zylo/Vertice）也可能下沉抢 SMB 客户。
- 技术风险：依赖客户授权只读数据；银行/账单聚合涉及敏感财务数据，需签 NDA 并加密处理；工具 API 变动会影响盘点口径与发现完整性。
- 合规风险：处理客户财务/银行卡数据须遵守 GDPR/CCPA 与数据最小化原则；跨境收付款涉及税务（如非美居民收美国客户款）；避免触碰“代管客户资金”红线，只做诊断与协调。
- 现金流风险：retainer 稳定但获客初期靠项目，冷启动有空窗；分成模式若归因不清易起纠纷，须事先写清计算口径。

8. 不适合的人群
- 想“挂机被动收入”的人——这是咨询交付，要靠主动盘点与谈判。
- 厌恶看数字/账单、不擅长和人谈价格的人。
- 只想要“卖模板躺赚”的人——模板只是起点，真正价值在诊断与谈判。
- 目标客户群普遍 <10 人、几乎没有订阅积累的市场——省不出可观金额，难收费。

9. 3 个可验证的入门步骤
1. 本周内用 Spendbase 免费层或纯表格，给自己或一位朋友的小生意做一份 90 天订阅盘点，算出“闲置+重复”金额占比——验证你能否在 2 小时内产出让人惊讶的数字（Torii 基准：多数公司闲置率 40%+）。
2. 第 2–3 天，挑 3 个你熟悉的小企业 SaaS（如 Notion/Slack/某 CRM），查 G2/Capterra 与 Vendr 公开基准，写一份“年付 vs 月付 + 降档可省 X%”的样板谈判底稿，发到 1 个小企业经营社群，验证是否有人愿意买单。
3. 第 4–7 天，在 Upwork/Fiverr 或 LinkedIn 发布一个 $500 的“SaaS 订阅急救审计”gig，用第一步的样板作为案例，验证 7 天内是否有询盘——有询盘说明需求真实，无询盘则调整定位（如转向“代理机构工具整合”）。

10. 核验来源
1. Flexera 2025 State of ITAM Report（35% 组织 SaaS 浪费同比增加、44% M365 授权未充分利用）：https://www.flexera.com/about-us/press-center/it-teams-losing-visibility-according-to-flexera-2025-state-of-itam-report
2. GII / MarketsandMarkets：全球 SaaS 管理市场 2025 $45.8 亿 → 2030 $93.7 亿，CAGR 15.4%：https://www.gii.tw/report/mama1883935-saas-management-market-by-platform-deployment-mode.html
3. QYResearch：SaaS 运营管理软件市场 2025 $7.16 亿 → 2032 $12.9 亿：https://www.qyresearch.com.cn/reports/7651444/saas-operations-management-software
4. Bill Creep 真实 SMB 审计案例（45 人公司年省 30%）：https://billcreep.com/case-studies
5. nex365 真实 SMB 瘦身案例（多个 40% 节省）：https://nex365.com/the-ultimate-stack-trim-real-smb-examples-of-cutting-3-tools
6. 4minuteworkday《The SaaS Subscription Reckoning》：审计 $2K–$5K、迁移 $10K–$15K、retainer $1.5K–$3K/月 的实战定价框架：https://4minuteworkday.blog/2026/04/01/emerging-the-saas-subscription-reckoning-what-it-means-why-its-happen
7. Zylo（市场领导者，客户平均发现比自盘多 3 倍的 SaaS 支出、宣称最高省 20%）：https://zylo.com
8. Varisource《7 Best SaaS Spend Management Tools 2026》：工具定价对照（Vertice $30K/年、Tropic $14.5K/年、Vendr $36K/年、Spendbase 免费层）——印证企业级平台留下 SMB 空白：https://www.varisource.com/blog/saas-spend-management-tools"""

data = {
    "taskId": "niche-opc-industry",
    "taskName": "每日小众赚钱行业：SaaS 订阅审计与支出优化（SaaS Spend Audit）",
    "status": "success",
    "startedAt": started.isoformat(),
    "finishedAt": finished.isoformat(),
    "summary": "SaaS 订阅审计与支出优化：帮中小企业盘点闲置/重复的业务软件订阅、重谈续费价格，把年软件开支砍掉 20%–40%。需求隐蔽（藏在自动续费账单里）、无铺天盖地教程、夹在企业级 SaaS 管理平台与免费自盘之间的中端空白，一人可远程异步完成、启动成本不足 $100，全球小企业都是客户，极适合 OPC 与数字游民。",
    "details": details,
    "sourceThread": "workbuddy-daily-niche-research",
    "labels": ["daily", "niche-industry", "opc", "digital-nomad", "saas-audit", "saas-cost-optimization", "subscription-management", "smb-consulting"],
    "nextSteps": [
        "本周内用 Spendbase 免费层或纯表格，给自己或朋友的小生意做 90 天订阅盘点，算出闲置+重复占比（验证能否 2 小时产出惊人数字）。",
        "第 2–3 天写一份 3 个熟悉 SaaS 的“年付 vs 月付+降档可省 X%”样板谈判底稿，发到小企业经营社群验证付费意愿。",
        "第 4–7 天在 Upwork/Fiverr 或 LinkedIn 发布 $500“SaaS 订阅急救审计”gig，用样板作案例，验证 7 天内是否有询盘。"
    ],
    "artifacts": [
        {"label": "Flexera 2025 State of ITAM Report", "path": "https://www.flexera.com/about-us/press-center/it-teams-losing-visibility-according-to-flexera-2025-state-of-itam-report"},
        {"label": "GII SaaS Management Market 2025–2030", "path": "https://www.gii.tw/report/mama1883935-saas-management-market-by-platform-deployment-mode.html"},
        {"label": "QYResearch SaaS Operations Management Software", "path": "https://www.qyresearch.com.cn/reports/7651444/saas-operations-management-software"},
        {"label": "Bill Creep SMB audit case studies", "path": "https://billcreep.com/case-studies"},
        {"label": "nex365 stack trim SMB examples", "path": "https://nex365.com/the-ultimate-stack-trim-real-smb-examples-of-cutting-3-tools"},
        {"label": "4minuteworkday SaaS Subscription Reckoning", "path": "https://4minuteworkday.blog/2026/04/01/emerging-the-saas-subscription-reckoning-what-it-means-why-its-happen"},
        {"label": "Zylo SaaS management leader", "path": "https://zylo.com"},
        {"label": "Varisource SaaS spend management tools pricing", "path": "https://www.varisource.com/blog/saas-spend-management-tools"}
    ]
}

out_dir = os.path.join("runs-workbuddy", "2026-11-02")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "niche-opc-industry.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("WROTE", out_path)
