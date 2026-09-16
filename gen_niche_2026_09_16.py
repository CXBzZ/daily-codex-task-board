# -*- coding: utf-8 -*-
import json
import os

try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("Asia/Shanghai")
    from datetime import datetime
    finished_at = datetime.now(TZ).strftime("%Y-%m-%dT%H:%M:%S+08:00")
except Exception:
    finished_at = "2026-09-16T09:50:00+08:00"

started_at = "2026-09-16T09:10:55+08:00"

details = """# 每日小众赚钱行业调研：企业 SOP / 流程文档代建（SOP & Process Documentation）

## 1. 行业是什么，为什么小众
一句话定义：帮中小企业把"只存在于某个老员工脑子里的操作流程"整理成标准化、可复用、可交接的 SOP（标准作业程序）与流程文档，并以 Word / Google Docs / Notion / PDF 形式交付。
为什么容易被忽略：① 搜索量低，"SOP writing service" 这类词在大众和自由职业者里竞争很小；② 需求隐蔽——企业主通常不到"新人总出错、自己一请假就乱、想扩张却复制不出第二家"的痛点时刻，根本不会想到"我需要有人来写 SOP"；③ 它夹在"管理咨询""虚拟助理""Notion 搭建"几个大行业之间，既不是纯咨询也不只是打字，导致供给端也很少人把它当一门独立生意来做。

## 2. 如何运作
- 典型客户：5-50 人的服务型小团队（数字营销代理、房产运营、理疗/诊所、coaching/课程团队、本地连锁门店、电商卖家）；痛点是"关键流程只在一个人脑子里"，想扩张、招人或休假却卡住。需求触发场景：招了新人却长时间带不动、创始人想抽身、准备卖公司、要接受认证/audits。
- 核心交付物：按流程拆分的 SOP 文档库（每个流程含步骤、责任人、决策点、异常分支、截图/录屏）、一份主索引（master index）、可选的 Loom 录屏与更新协议。
- 完整工作流：
  1. 获客：在 Upwork / Contra / Fiverr 上架服务、LinkedIn 定向触达代理/教练群体、在 IndieHackers 等社区分享"如何用 SOP 给自己放假"、与 SOP SaaS（SweetProcess / Trainual）做联盟合作引流。
  2. 诊断：让客户填一份"流程清单"，挑出最痛的 3-5 个流程。
  3. 访谈+观察：与客户团队做 1-3 次录音访谈，或让其用 Loom 录屏演示真实操作；也可从其 Slack / 邮件里提炼。
  4. 撰写：把口述流程结构化，写清步骤、决策点、例外、负责人，配截图/简图。
  5. 交付+修订：出 Google Docs / Notion / PDF 初稿，1-2 轮修订，交付带版本号和更新协议的 SOP 库。
  6. 收款：按项目一次性收费，或加"季度更新"retainer（例：$298/月）持续维护。
- 关键工具/平台：文档（Google Docs、Notion、Confluence）、录屏（Loom、Scribe 自动生成步骤）、流程图（Whimsical、draw.io）、接单平台（Upwork、Contra、Fiverr）、SaaS 联盟（SweetProcess / Trainual / Process Street 的 affiliate）。

## 3. 盈利模式
- 收入来源：① 按项目一次性收费（最常见）；② 月度/季度维护 retainer（持续更新 SOP 库）；③ 加购录屏 / Loom、流程图、培训视频等增值项；④ 工具联盟佣金（推荐客户用 SweetProcess / Trainual 可拿 affiliate 收入）。
- 定价参考（均为真实公开报价）：
  - dailypro.us：Essential $1,200 / Standard $1,700 / Premium $2,200 / Enterprise 起 $2,800。
  - BOOJEE Estate：Solo $497（≤10 SOP）/ Growing $997（≤25）/ Enterprise $1,997；加购每 5 个 SOP $158；季度维护 $298/月。
  - 自由职业者（zinnhub）：Basic $99（2 流程）/ Standard $275（5）/ Premium $400（7）。
  - 咨询 / SOP 机构（SOPX 2026 成本指南）：小企业在 $5,000–$25,000 区间，综合运营手册可超 $50,000；fractional COO $5k–15k/月。
- 利润空间：纯写作+文档工具，边际成本极低。以 BOOJEE 的 $497 套餐（≤10 SOP，2 次访谈）为例，工具成本近乎为 0（Loom 免费档 + Scribe 免费档足够），毛利可达 90%+；扣除平台费（Upwork 抽成 0-15%）、税费后净利仍很高。retainer 模式（如 $298/月）几乎零边际成本，是利润核心。
- 复购/长期合同：强。SOP 库需要随业务迭代更新，可签季度/年度维护合同；客户扩张时还会加购新流程文档，LTV 可观。

## 4. 入门门槛
- 技能：会"把混乱的流程听明白并写清楚"——结构化写作、提问（访谈 SME）、基本的流程图表达。不需要编程。会用 AI（让 ChatGPT / Claude 辅助整理访谈纪要）能明显提速。学习曲线：有写作/运营基础者 1-2 周即可接第一单标准项目。
- 工具：初期几乎零成本——Google Docs（免费）、Loom（免费档）、Scribe（免费档自动出步骤）、draw.io（免费）。可选付费：Notion（个人免费）、SOP SaaS 演示账号。首月工具花费可压到 $0–$30。
- 资金：启动资金近乎为 0（一台电脑+网络）。如需建简单作品集站，可用 Carrd / Notion 免费页。
- 时间：从零到第一单，认真经营平台档案+发 10-20 个精准提案，通常 1-4 周；先用低价/案例换 1-2 个好评，再逐步涨价。

## 5. 为什么适合 OPC / 数字游民
- 异步交付：本质是"写作+访谈"，全程可异步进行，不要求实时在线，时区友好——和欧美客户差 8-12 小时反而方便"白天访谈、夜间写稿"。
- 全球客户：SOP 是企业通用痛点，英语客户遍布美/英/澳/加，无需本地执照或实体场所。
- 边际成本极低：文档复制、模板复用、AI 辅助整理，使第 10 个 SOP 的成本远低于第 1 个，可规模化而不增人头。
- 可产品化：把常见流程（如"客户 onboarding SOP 模板""电商退货 SOP 模板"）做成可售模板/小课程，一次制作多次售卖，进一步去人力化。
- 联盟叠加：远程向客户推荐 SOP SaaS 还能赚 affiliate，纯被动增量收入。
- 与既有方向的区隔：相对"帮助中心知识库搭建"（面向客服支持）和"Notion 系统搭建"（面向工具本身），本方向聚焦"企业内部操作流程的知识资产化"，交付物是内容而非系统，更轻、更纯写作、更适合个人远程。

## 6. 潜在收益（谨慎，不承诺）
以下为公开行业/平台数据的参考区间，"这些是参考数据，不等于个人收入"：
- 新手阶段（0-6 月，靠平台接单）：单项目报价 $99–$1,200，月接 2-4 单，月收入约 $500–$3,000；Upwork 上写作类时薪参考 $15–$40，SOP 写作因更专业可更高。
- 成熟阶段（有作品集+直接客户+retainer）：单项目 $1,200–$5,000，维护 retainer $298–$1,000/月/客户，若维护 5-10 个客户，月经常性收入可达 $1,500–$10,000+；头部 SOP 咨询/机构可达 $25,000+ 项目费。
- 市场大盘：SOP 管理软件市场 2025 年约 $12.5 亿，预计 2032 年达 $26.95 亿（CAGR 11.6%）；业务流程文档工具市场 2025 年 $21.6 亿→2030 年 $34.5 亿（CAGR 9.5%）——说明"企业愿意为流程文档化持续付费"是真实且增长的趋势，而非昙花一现。
- 需求侧证据：Staudt Solutions 汇总数据，已文档化 SOP 的企业运营错误率平均降 32%（制造 41%、服务 23%），新人上手时间缩短 15-30%（OneModel 对 8,000+ 小企业：上手周期 6.8→5.0 周，知识留存 +34%）。客户"省下的返工成本"远超付给你的文档费，这是你能持续收费的根本。

## 7. 主要风险
- 市场风险：经济下行时"写文档"易被视作可削减的开支；若只做一次性项目而无 retainer，收入波动大。
- 技术风险：过度依赖某家 SOP SaaS（如 API/定价变动）会影响你的交付/联盟收入；AI 自动生成 SOP 工具（Scribe、SweetAI）会压低"纯转录"类低价单，需往"访谈+行业判断+落地"高价值端走。
- 合规风险：跨境收款涉及税务（如美国客户付款可能触发 W-8BEN/流水申报）；若接触客户敏感流程数据，需注意数据隐私（签 NDA、用加密共享）；某些受监管行业（医疗、食品）的 SOP 有合规格式要求，需明确"你提供的是文档服务，非合规认证"。
- 现金流风险：平台账期（Upwork 固定价项目客户有 14 天确认 + 5 天安全期）；获客初期需持续投入提案时间；避免只绑定 1-2 个大客户。

## 8. 不适合的人群
- 想要"完全不用和人沟通"的纯异步宅家型：本行核心是与客户团队做访谈、追问细节，社恐或抗拒开会者会很痛苦。
- 追求"今天做明天暴富"的人：需先积累 1-2 个案例和好评，前期收入不稳定。
- 不愿写、怕长文的人：本质是高密度写作，讨厌文档者做不久。
- 想做重交付/雇团队扩张的人：这恰恰是 OPC 生意，重资产化会丧失其优势。

## 9. 3 个可验证的入门步骤
1. （1 天）做 1 份"虚拟案例"练手：挑你熟悉的任一小生意（如独立咖啡馆 / 自媒体团队），写 2 个 SOP（如"新客户 onboarding""周更内容排期"），用 Google Docs + Loom 录屏，存成作品集。验证：能否在 3 小时内产出一份结构清晰、外人能照做的 SOP。
2. （2-3 天）上 Upwork / Contra，建"SOP & Process Documentation"档案，发 10 个精准提案给"正在招人/扩张"的小团队，报价从 $99–$150 起换首单+好评。验证：一周内是否收到 ≥1 个回复或咨询。
3. （持续）跑通第一单后，把流程模板化，并注册 SweetProcess / Trainual 的 affiliate，向客户推荐时叠加被动收入；同时把首单成果（脱敏）写成一篇 LinkedIn / IndieHackers 帖子引流。验证：首单是否按时交付并拿到五星评价，能否自然带来 1 个转介绍。

## 10. 核验来源
（见文末 artifacts 列表，均为可公开访问的真实链接）"""

task = {
    "taskId": "niche-opc-industry",
    "taskName": "每日小众赚钱行业：企业SOP/流程文档代建（SOP & Process Documentation）",
    "status": "success",
    "startedAt": started_at,
    "finishedAt": finished_at,
    "summary": "企业 SOP / 流程文档代建：把小团队'只在一个人脑子里的操作流程'整理成可复用、可交接的标准化文档。需求隐蔽但真实（SOP 软件市场 2025 年约 $12.5 亿、年增 11.6%），纯写作+异步交付、零库存零执照、启动成本近乎为零，是典型的一人公司/数字游民生意。",
    "details": details,
    "sourceThread": "workbuddy-daily-niche-research",
    "labels": [
        "daily",
        "niche-industry",
        "opc",
        "digital-nomad",
        "process-documentation",
        "sop",
        "remote-service",
        "knowledge-management"
    ],
    "nextSteps": [
        "做 1 份虚拟案例练手：挑熟悉的小生意写 2 个 SOP（onboarding / 内容排期），用 Google Docs + Loom 存成作品集，验证 3 小时内能否产出外人能照做的文档。",
        "上 Upwork / Contra 建'SOP & Process Documentation'档案，发 10 个精准提案给正在招人/扩张的小团队，报价 $99–$150 起换首单+好评，验证一周内是否有回复。",
        "跑通首单后把流程模板化，注册 SweetProcess / Trainual 的 affiliate 叠加被动收入，并把脱敏成果写成 LinkedIn / IndieHackers 帖子引流，验证能否带来转介绍。"
    ],
    "artifacts": [
        {
            "label": "SOP 管理软件市场 2026（规模 $12.5 亿→$26.95 亿，CAGR 11.6%）",
            "path": "https://pmarketresearch.com/?p=2450868/"
        },
        {
            "label": "业务流程文档工具市场报告 2026（Research and Markets，$21.6 亿→$34.5 亿）",
            "path": "https://www.researchandmarkets.com/reports/5983775/global-business-process-documentation-tools"
        },
        {
            "label": "数字 SOP 市场 2025（规模 $14.5 亿→$30.97 亿）",
            "path": "https://pmarketresearch.com/it/digital-standard-operating-procedure-market/"
        },
        {
            "label": "dailypro.us SOP 代写真实报价（$1,200–$2,800+）",
            "path": "https://dailypro.us/sop-creation"
        },
        {
            "label": "BOOJEE Estate SOP Builder 真实报价（Solo $497 / Growing $997 / 季度维护 $298）",
            "path": "https://www.boojee.estate/sop-builder"
        },
        {
            "label": "zinnhub 自由职业者 SOP 服务（Basic $99 / Standard $275 / Premium $400）",
            "path": "https://zinnhub.com/fr/zinns/je-documenterai-vos-processus-metier-en-procedures-operationnelles-claires-et-professionnelles-que-votre-equipe-utilisera-reellement"
        },
        {
            "label": "SweetProcess 定价页（SOP SaaS 需求验证，$99/月）",
            "path": "https://www.sweetprocess.com?p=14436/"
        },
        {
            "label": "Vidocu：2026 年 8 款 SOP 软件定价对比（市场透明度参考）",
            "path": "https://vidocu.ai/blog/8-best-sop-software-tools-in-2026-compared-with-pricing"
        },
        {
            "label": "SOPX 2026 SOP 顾问成本指南（小企业 $5k–$25k 区间）",
            "path": "https://sopx.io/insights/sop-consultant-cost"
        }
    ]
}

out_dir = os.path.join("runs-workbuddy", "2026-09-16")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "niche-opc-industry.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(task, f, ensure_ascii=False, indent=2)

print("WROTE", out_path)
print("bytes:", os.path.getsize(out_path))
