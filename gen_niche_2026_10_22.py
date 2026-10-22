#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the daily niche OPC industry brief for 2026-10-22 (Asia/Shanghai)."""
import json
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

SHANGHAI = ZoneInfo("Asia/Shanghai")
NOW = datetime.now(SHANGHAI)
STARTED = NOW - timedelta(minutes=10)
FINISHED = NOW

DATE = "2026-10-22"
OUT_DIR = os.path.join("runs-workbuddy", DATE)
OUT_PATH = os.path.join(OUT_DIR, "niche-opc-industry.json")

summary = (
    "B2B 投标书/RFP 应答代写（Bid & Proposal Writing as a Service）帮 SaaS、IT 服务、咨询与工程承包商，"
    "把客户或政府发布的几百条招标问题、合规清单与技术规格组织成合规、有说服力、能中标的标书。"
    "它搜索量极低、需求隐蔽、夹在免费自写与昂贵机构之间，是典型被低估的中端空白；"
    "单人即可异步远程交付，启动成本近乎为零，且有 Loopio/Responsive/APMP 等公开数据与自由职业平台订单可验证。"
)

details_lines = [
    "【1. 行业是什么，为什么小众】",
    "一句话定义：帮企业（尤其是 B2B SaaS、IT 服务、管理咨询、建筑工程分包、医疗/政府承包商）撰写和应答客户或政府发布的 RFP（Request for Proposal，招标/询价文件），把对方几百条问题、合规清单、技术规格、资质证明，组织成一份合规、有说服力、能中标的标书。",
    "",
    "为什么容易被忽略（四个隐蔽来源）：",
    "① 搜索量极低——企业主不会搜“RFP writing service”，他们搜的是“怎么中标”“标书怎么写”，行业因此“隐形”；",
    "② 需求隐蔽且紧急——触发点是“客户在采购门户发了一个 200 页 RFP，周五前必须交”，非日常、非主动搜索；",
    "③ 看起来技术门槛高——涉及 FAR（联邦采购条例）、Section L/M 指令、合规矩阵，外行误以为要持证上岗；",
    "④ 夹在“免费自己写（但写不好就丢标）”和“大型提案机构（收费 2.5 万–10 万美元）”之间的中端空白，单人自由职业者恰好填补。",
    "",
    "【2. 如何运作】",
    "典型客户：投标频率中等的 B2B 公司——SaaS、IT 服务、管理咨询、建筑工程分包商、政府/医疗承包商；内部没有专职 proposal manager，或旺季需要 overflow 产能。",
    "需求触发：客户在 SAM.gov、BidNet 或私域采购门户发布 RFP；或代理商把标书写作环节外包。",
    "核心交付物：合规矩阵（compliance matrix，逐条对照 Section L/M 指令）、技术/管理叙事、过往业绩（past performance）文案、定价叙事、资质证明包，以及最终排版 PDF。",
    "完整工作流：① 接单并评估标书（看截止日、复杂度、是否值得投）→ ② 建合规矩阵与 storyboard → ③ 起草各 section（客户既有内容库 + AI 草稿）→ ④ 内部评审（Pink/Red/Gold color team）→ ⑤ 排版与终稿 → ⑥ 协助在采购门户提交 → ⑦ 收款（里程碑或项目制）。",
    "关键工具和平台：Loopio / Responsive（前 RFPIO）做内容库与协作；PandaDoc / Proposify 排版；GovWin / SAM.gov 找标；Notion 或 Excel 做合规矩阵；Grammarly；以及客户提供的 SME 访谈记录。",
    "",
    "【3. 盈利模式】",
    "收入来源与定价（多口径）：",
    "① 按小时：政府标书偏高，初级 $50–$85、中级 $85–$135、资深 $135–$200、涉密/垂直专家 $175–$300+；",
    "② 按项目固定费：简单州/地方 RFP（<30 页）$2,500–$6,000，中型联邦任务单 $6,000–$12,000，完整联邦提案 $12,000–$25,000+，复杂基建标 >$50,000；",
    "③ 按月 retained：$3,000–$8,000/月（管道分诊 + 模板维护 + 固定数量应答）；",
    "④ 机构收费：$150–$350/时，或 $25,000–$100,000+/大单。",
    "利润空间：单人 freelancer 工具成本极低（AI 软件 $5K–$30K/年可摊，但初期可用 Notion+GPT+Excel 替代，约 $0–$50/月）。扣掉平台费（Upwork 抽成约 10%，自建获客则 0）、税费后，按项目毛利常 >70%。一个中等标书 25–40 小时交付、收 $5,000–$10,000，等效时薪 $125–$400。",
    "复购/长期合同：retainer 模式天然复购；建筑/咨询客户旺季常年有标，易转月度留存。",
    "",
    "【4. 入门门槛】",
    "技能：强商业/说服性写作、把复杂信息结构化、读懂 RFP 指令（Section L/M）、基础合规意识。1–3 个月可接简单单；可考 APMP Foundation（约 $300）背书。",
    "工具：前期几乎零成本——Notion 或 Excel（合规矩阵）、Grammarly、ChatGPT/Claude（草稿）、Google Docs/Word（排版）；可选订阅 Loopio/Responsive（贵，初期不必）。总成本 $0–$100/月。",
    "资金：启动 <$500（主要是时间 + 一个作品集样例 + 可能的 APMP 考试费）。",
    "时间：从零到第一单约 2–6 周（建 1 个虚构/公开标书样稿 → 在 Upwork/Fiverr/Contra 或 LinkedIn 接小单）。",
    "",
    "【5. 为什么适合 OPC / 数字游民】",
    "异步交付：标书写作是纯文档工作，靠书面沟通，几乎不需要实时会议；客户在欧美时区发 RFP，你在任何时区写，靠截止日而非时钟协作——完美适配时区差。",
    "全球客户：英文 RFP 是全球 B2B 通用语言，可服务美/英/澳/加客户，不限本地执照、不需实体场所。",
    "边际成本低：一旦建好可复用内容库（公司概述、安全合规、案例），后续标书大量复用，单位时间产出随经验指数上升。",
    "可规模化：从单人接单 → retainer 多客户 → 招兼职写手转包，或做成 AI+模板产品化，无需库存/场地。",
    "时区友好：紧急标书常出现在客户工作日下午，你的“夜间”正好是他们的白天，反而成接急单优势。",
    "",
    "【6. 潜在收益（谨慎，不承诺）】",
    "以下为公开区间参考数据，不等于个人收入：",
    "① Upwork 提案/投标写作中位时薪 $32.5–$42.5（Business Proposal $42.5），属最高付费写作类之一（UpAlerts 2026，基于 1.2 万岗位）；",
    "② 政府 RFP 自由职业者 $75–$200/时 或 $3,000–$15,000/提案，复杂联邦 >$20,000（Wonit/APMP 口径）；",
    "③ 独立提案顾问 $100–$200/时、$10K–$50K/提案、retainer $5K–$15K/月（GovCon Giants 2026）；",
    "④ 全职 proposal manager $80K–$130K/年 + 福利，资深 $115K–$200K（govcongiants）。",
    "新手阶段：前 3–6 个月靠平台接小单，月收入约 $1,000–$4,000（按 $30–$75/时 × 每周 15–25 小时），靠作品集爬坡。",
    "成熟阶段：建立 retainer + 高客单价项目后，月收入约 $5,000–$15,000+（每年 20–40 个标书 × $3K–$12K，或 2–4 个 retainer × $5K），等效年 $60K–$180K。这些是行业区间参考，不等于个人能保证的收入，受获客、专业度、中标率影响。",
    "",
    "【7. 主要风险】",
    "市场风险：① AI 工具（Loopio/Responsive/AutoRFP.ai）把基础标书草稿商品化，压低初级写手单价；② 经济下行时政府/企业削减外包预算；③ 竞争加剧，低价外包以 $15–$30/时抢单。",
    "技术风险：① 过度依赖单一 AI 平台——Market Intelo 指出 18–25% 企业需对 AI 生成内容大幅返工，须保留人工 review；② 客户内容库过时导致错答（“幻觉”合规声明会直接丢标）；③ 平台政策（Upwork 抽成、SAM.gov 规则）变动。",
    "合规风险：① 政府标书涉及 FAR/Section L/M，错读指令 = 直接废标；② 数据隐私——处理客户敏感资质/财务须符合 GDPR/SOC 2，美国 DOJ Bulk Data Rule（2025）收紧；③ 跨境收款与税务（数字游民须处理本国 + 客户国税务）；④ 不得越界提供“法律意见”（UPL 边界，定位为写作与组织，非法律意见）。",
    "现金流风险：① 标书项目账期 15–45 天，retainer 可缓解；② 获客成本（平台抽成或自建漏斗）；③ 紧急单加价但也可能因客户临时撤标而白干（须在合同里约定“启动费不退”）。",
    "",
    "【8. 不适合的人群】",
    "· 讨厌写长文档、扛 deadline 高压、或英语非母语且无意愿提升写作的人；",
    "· 想要“被动收入/躺赚”、不愿做客户沟通与 SME 访谈的人；",
    "· 只接政府标却不愿学 FAR/合规的人（容易废标吃差评）；",
    "· 完全不懂某个垂直行业、又不愿做功课的人（标书靠 domain insight 取胜，不是套模板）。",
    "",
    "【9. 3 个可验证的入门步骤】",
    "步骤 1（1 天，成本 0 元）：建一个“样稿标书”——下载一份公开 RFP（如 SAM.gov 或市县政府公开采购），用 Notion/Excel 做一份合规矩阵 + 2 个 section 草稿（公司概述、过往业绩），本地完成。验证：能否在 24 小时内产出一份像样的 5 页样稿——能，说明具备基础交付力。",
    "步骤 2（2 小时，成本 0 元）：验证市场与定价——在 Upwork 搜 “RFP response” / “proposal writing”，数在招项目数与报价区间；读 Loopio 2023 RFP Benchmark Report（免费）确认行业体量。验证：确认你所在细分（如 SaaS/IT）每月有 ≥10 个在招且报价 ≥$30/时——有，则值得继续。",
    "步骤 3（3 天，成本 ≤$50）：接第一单小标——在 Contra/Fiverr/Upwork 发一个 “$300 帮写 RFP 应答 1 个 section 或合规矩阵” 的 gig，或主动 LinkedIn 触达 10 家刚发 RFP 的小公司。验证：2 周内拿到 ≥1 个付费咨询/小单（哪怕 $150）——拿到，说明获客闭环成立。",
    "",
    "【10. 核验来源】",
    "① Loopio 官网与 RFP Benchmark Report（loopio.com / Loopio 2023 RFP Benchmark Report 与 APMP 联合，1,500+ 响应团队：平均 25 小时/标、年提交 166 次）；",
    "② Responsive 官网（前 RFPIO，responsive.io，RFP 响应自动化 AI 市场约 18–20% 份额）；",
    "③ APMP 国际提案管理专业人士协会（apmp.org，行业认证与薪酬基准来源）；",
    "④ RFP Response Management Software Market：2025 $435M → 2032 $992.11M，CAGR 12.5%（PMarketResearch）；",
    "⑤ RFP Response Automation AI Market：2025 $2.4B → 2034 $8.9B，CAGR 14.8%（Market Intelo）；",
    "⑥ 联邦合同统计 2026：小承包商单标 40+ 小时、$8,000 全载成本、带 capture 中标率 15–25%（winacontract.com）；",
    "⑦ AI 标书写作：Loopio/APMP 25 小时、APMP 会员 41 小时、澳洲标准标书 $2,750–$8,000（tenderbuilt.com.au）；",
    "⑧ Upwork 提案/投标写作中位时薪 $32.5–$42.5（UpAlerts 2026，基于 Upwork 1.2 万岗位分析，upalerts.app）。",
]

details = "\n".join(details_lines)

next_steps = [
    "步骤1：用一份公开 RFP（SAM.gov/市县政府采购）做 5 页样稿+合规矩阵，24 小时内验证基础交付力（成本 0）。",
    "步骤2：在 Upwork 搜 RFP response/proposal writing 数在招项目与报价，读 Loopio Benchmark Report 确认体量（2 小时）。",
    "步骤3：在 Contra/Fiverr/Upwork 发 $300 小单或 LinkedIn 触达 10 家刚发 RFP 的小公司，2 周内拿下首个付费小单（≤$50）。",
]

artifacts = [
    {"label": "Loopio 官网与 RFP Benchmark Report", "path": "https://loopio.com"},
    {"label": "Responsive（前 RFPIO）官网", "path": "https://responsive.io"},
    {"label": "APMP 国际提案管理专业人士协会", "path": "https://apmp.org"},
    {"label": "RFP Response Management Software Market 2025–2032", "path": "https://pmarketresearch.com/it/rfp-response-management-software-market/"},
    {"label": "RFP Response Automation AI Market 2025–2034", "path": "https://marketintelo.com/report/rfp-response-automation-ai-market"},
    {"label": "联邦合同统计 2026（成本/时间/中标率）", "path": "https://winacontract.com/federal-contracting-statistics-2026"},
    {"label": "AI 标书写作：Loopio/APMP 工时与澳洲定价", "path": "https://tenderbuilt.com.au/ai-tender-writing-australia"},
    {"label": "Upwork 提案/投标写作时薪中位数", "path": "https://upalerts.app/blog/high-paying-writing-skills-upwork"},
]

result = {
    "taskId": "niche-opc-industry",
    "taskName": "每日小众赚钱行业：B2B 投标书/RFP 应答代写服务",
    "status": "success",
    "startedAt": STARTED.isoformat(),
    "finishedAt": FINISHED.isoformat(),
    "summary": summary,
    "details": details,
    "sourceThread": "workbuddy-daily-niche-research",
    "labels": ["daily", "niche-industry", "opc", "digital-nomad", "rfp", "proposal-writing", "bid-writing", "b2b-services"],
    "nextSteps": next_steps,
    "artifacts": artifacts,
}

os.makedirs(OUT_DIR, exist_ok=True)
with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Wrote", OUT_PATH)
print("Bytes:", os.path.getsize(OUT_PATH))
print("Labels:", result["labels"])
print("Artifacts:", len(artifacts))
