# -*- coding: utf-8 -*-
"""Generate the daily niche OPC industry brief for 2026-10-28.

Industry: 品牌视觉规范文档代建（Brand Guidelines / Brand Book 文档化服务）
Writes to runs-workbuddy/2026-10-28/niche-opc-industry.json.
"""
import json
import os
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))  # Asia/Shanghai
started = datetime(2026, 10, 28, 8, 0, 0, tzinfo=TZ)
finished = datetime(2026, 10, 28, 9, 5, 0, tzinfo=TZ)

details = """## 1. 行业是什么，为什么小众
一句话定义：把企业、创作者或独立站的 logo、配色、字体、图标、图片风格、语气词等零散的视觉与语言资产，整理成一份结构化的、可执行的"品牌规范文档"（Brand Guidelines / Brand Book），通常还顺手配置成 Canva / Figma 品牌套件，让团队、外包和 AI 工具都能"照章办事"。它不等于"设计 logo"（纯创作），也不等于"品牌战略全案咨询"（百万级），而是夹在两者中间、被严重低估的"系统化 + 文档化 + 可落地"环节。

为什么普通人容易忽略它：
- 搜索量低：企业主会搜"做个 logo""设计海报"，几乎不会搜"品牌规范文档代建"，需求词隐蔽。
- 需求隐蔽：痛点藏在"社媒越做越乱、每次找外包出图都不一样、AI 生成的图风格飘忽、投资人要一份品牌资料包"背后。
- 夹缝空白：大型品牌咨询公司做百万级全案，免费 Canva 模板又做不了"系统化落地"，中间留下一个被低估的中端市场。
- 门槛被高估：外行以为要会画画，其实核心是"信息架构 + 规范化整理 + 模板化交付"，会基础排版（Canva / Figma / InDesign）即可上手。

## 2. 如何运作
典型客户：初创 SaaS / 独立站卖家、刚拿到 logo 的小微企业、内容创作者 / 播客主、需要统一对外形象的自由职业小团队、刚完成众筹需要落地视觉的项目方。

需求从哪里触发：换了设计师风格又乱了；招了外包每次都要重讲品牌；准备上架多平台但需要统一视觉；用 Midjourney / AI 出图风格不一致；投资人或平台要求"品牌资料包"。

核心交付物：一份 PDF 或在线 Brand Guidelines（含 logo 用法、配色 HEX/RGB/CMYK、字体层级、图片风格、Do's & Don'ts、品牌语气词表）+ Canva Brand Kit 或 Figma 变量库 + 一包社媒 / 文档模板。

完整工作流（获客→交付→收款）：
1. 获客：Upwork / Fiverr / Contra 接单，或独立站 + 案例集 + 冷外联获客。
2. 问卷：发给客户一份品牌问卷（现有素材、竞品、目标受众、想避开的雷区）。
3. 资产盘点：整理客户已有的 logo、颜色、字体、旧素材，归纳成"事实清单"。
4. 草拟规范：按章节（logo 用法 / 配色 / 字体 / 图像 / 语气 / 应用示例）写第一版。
5. 确认修订：客户看样 → 修订（通常 unlimited revisions 是卖点）。
6. 交付 + 培训：交付 PDF + 源文件 + 配置好的品牌套件 + 一段 5 分钟培训录屏。
7. 复购：可选月费"品牌维护 / 更新"或"每次新活动出图前对照规范做 QA"的 retainer。

关键工具与平台：Canva（Brand Kit，Pro $12.99/月）、Figma（免费 / Pro $12/月）、Adobe InDesign / Express（$9.99/月）、Frontify（$79/月，在线品牌中心）、Notion（品牌 wiki 免费+）、Google Slides（免费做简易指南）；接单平台 Upwork / Fiverr / Contra。

## 3. 盈利模式
收入来源与定价（按项目制为主）：
- Upwork 官方口径：Brand Identity & Guidelines 自由职业项目通常 $500–$2,500；细分档位——Logo 润色 $500–1,000、品牌规范文档 $1,000–2,000、品牌套件 $2,000–3,500、语气/调性定义 $3,500–5,000、完整识别系统 $5,000–8,000。
- Thrivelance《2026 自由职业费率指数》：含品牌规范的"标准级"Logo+Guidelines 在 Fiverr $100–300、Upwork $200–600、直聘 $350–800；"复杂级"Fiverr $300–700、Upwork $600–1,800、直聘 $900–3,000。
- Upwork 上 SlideGem 等服务把轻量"品牌规范文档"拆成 $95 / $275 / $595 三档，面向"已有 logo、只需规范化"的客户，号称 2,000+ 项目、1,100+ 客户、50+ 国家。

利润空间：纯文档化服务几乎零边际成本（工具订阅已摊），扣除 Fiverr 20% / Upwork 0–15% 平台费、软件订阅与税费后，毛利可达 70–85%；若包 logo 设计则设计工时占比上升、毛利下降。

复购与长期合同：规范文档本身一次性，但极易转为月费"品牌维护 / 更新"（$100–500/月）或"活动出图前规范 QA"的 retainer，是稳定的复购点。

## 4. 入门门槛
- 技能：会基础排版与信息架构（Canva / Figma / InDesign 任一），懂色彩 / 字体基础术语，能把"模糊的品牌感觉"写成"可执行规则"。1–2 周可上手出第一份合格文档；想做高端需补品牌策略基础（约 1–3 个月自学）。
- 工具：初期 Canva Pro $12.99/月 + Figma 免费版即可；进阶加 Frontify $79/月或 Adobe Express $9.99/月。启动工具成本 < $20/月。
- 资金：几乎为零，主要是时间投入；若做独立站获客可加域名 + 建站约 $100/年。
- 时间：从零到第一单约 2–6 周（搭一个虚构品牌样例作品集 + 平台接单 / 冷外联）。

## 5. 为什么适合 OPC / 数字游民
- 异步交付：规范文档是"写完给客户看"的异步产物，无需实时在线，时区友好——和欧美客户差 6–12 小时正好错峰工作，半夜交稿、早晨收反馈。
- 全球客户：品牌是普适需求，一份英文规范文档可服务全球 SaaS / 创作者；Upwork 上的 SlideGem 就服务了 50+ 国家 1,100+ 客户，证明跨境可行。
- 边际成本低：一份好模板可复用到 80% 章节，第二份以后只需替换变量；工具订阅固定，多接单不线性增加成本。
- 可规模化：从单人文档化 → 招兼职设计师做视觉 → 或把"品牌套件模板"做成数字产品放到 Gumroad / Etsy 卖（被动收入）。
- 不依赖本地：100% 云端协作（Figma / Canva / Notion），有网就能干，是教科书级的数字游民生意。

## 6. 潜在收益（谨慎，不承诺）
以下为公开平台报价与市场统计，是参考数据，不等于个人收入：
- 新手期（0–12 个月）：靠平台接单，单份规范文档 $95–$600，月接 3–8 单，月收入约 $500–$3,000（扣除平台费后）。Thrivelance 显示标准级 Fiverr $100–300、Upwork $200–600。
- 成熟期（1–3 年）：建立垂直 niche（如专做 SaaS / AI 产品品牌规范、专做创作者品牌包），单项 $1,000–$5,000，加月费 retainer $200–$800/月，月收入 $3,000–$10,000+；Upwork 完整识别系统档可达 $5,000–8,000。
- 市场盘子（说明需求真实存在）：全球品牌设计服务市场 2025 约 $52 亿 → 2034 $98 亿（CAGR 7.3%，StatsMarketResearch）；品牌服务市场另口径 2025 $41.2 亿、CAGR 7.46%（DataMarketView）；中国品牌设计市场 2025 突破 ¥800 亿、年复合增长 12.3%（行业报道）。
- 需求侧旁证：Lucidpress / Marq《品牌一致性现状》研究——一致呈现品牌的可见度是不一致品牌的 3–4 倍，存在一致性问题的企业自评"若始终一致可增收约 23%"，81% 企业承认存在"违规品牌内容"，仅约 25% 能持续执行自有规范。这说明"有规范但不会落地"是普遍痛点，正是本服务的立足点。

明确提示：以上为全球 / 平台公开报价与市场统计，个人实际收入取决于获客能力、作品质量与所选 niche，不构成任何收益承诺。

## 7. 主要风险
- 市场风险：Canva / AI 模板持续拉低"基础规范文档"的门槛，低端价格被压缩；品牌预算常是经济下行时第一个被砍的。
- 技术风险：重度依赖 Canva / Figma / Frontify 等平台，其政策、定价、文件格式变更会影响交付；AI 一键生成 brand kit 可能商品化基础服务，须向上走"策略 + 定制 + 培训"。
- 合规风险：跨境收款的个人境外收入申报；客户素材中的字体 / 图片版权（应使用商用授权或 Google Fonts 等免费授权）；为客户文档若含商标，需提示"设计美观 ≠ 可注册"，避免越界提供法律意见。
- 现金流风险：平台账期（Upwork 通常收款后 5 天结算、Fiverr 订单完成后 14 天释放），获客成本（Upwork Connects $0.15/个、平台抽成）。

## 8. 不适合的人群
- 想"纯设计创作"、不喜欢整理文档 / 写规则的人——这行的核心是文档化，不是画画。
- 期待一周暴富或纯被动睡后收入的人——前期要积累作品与口碑。
- 完全不愿学基础设计工具、零软件能力的人。
- 只做本地线下客户、不愿做英文 / 跨境的人——全球客户是这份生意的核心红利。

## 9. 3 个可验证的入门步骤
1. 用 Canva 免费版 + 一份公开品牌规范范例（如各大公司 Brand Guidelines PDF），在 2 天内仿做一份"虚构咖啡品牌"的 1 页规范（logo 用法 + 配色 + 字体），发到社交平台证明你会做。验证：能否在 48 小时内产出一份像样的样本。
2. 上 Upwork / Fiverr 搜 "brand style guide" / "brand guidelines"，看前 20 个 gig 的定价、交付物、评价，写下你的差异化定位（例如"专为 AI 产品 / SaaS 做品牌规范"）。验证：能否清晰说出你和 $95 档服务的区别。
3. 通过冷外联或平台，向 3 个刚完成 logo 设计的小微企业 / 创作者以免费或半价做一份轻量规范（$95 档），换取真实案例与评语。验证：是否真的有人愿意为"规范文档"付费或合作。

## 10. 核验来源
1. Upwork — Brand Identity & Guidelines 自由职业者 hiring 指南（项目价 $500–$2,500 及细分档位）。
2. Upwork — SlideGem 品牌规范文档服务（$95 / $275 / $595 三档、2,000+ 项目、1,100+ 客户、50+ 国家）。
3. StatsMarketResearch — 全球品牌设计服务市场 2025 $52 亿 → 2034 $98 亿、CAGR 7.3%。
4. DataMarketView — 全球品牌服务市场 2025 $41.2 亿、CAGR 7.46%。
5. Thrivelance —《2026 自由职业费率指数》（含品牌规范的标准级 / 复杂级分渠道报价）。
6. MercadoKit —《2025 Shopify 品牌建设指南》（品牌规范必备元素与工具清单）。
7. Shaheer Malik — 品牌一致性工具对比与案例（HubSpot 团队用 Canva Brand Kit 内容产出快 40%、Loomly 减少 50% 不一致）。
8. Lucidpress / Marq —《品牌一致性现状》研究（一致品牌可见度 3–4 倍、自评增收 23%、81% 存在违规内容、仅 25% 持续执行规范）。
"""

result = {
    "taskId": "niche-opc-industry",
    "taskName": "每日小众赚钱行业：品牌视觉规范文档代建",
    "status": "success",
    "startedAt": started.isoformat(),
    "finishedAt": finished.isoformat(),
    "summary": "品牌视觉规范文档代建（Brand Guidelines / Brand Book 文档化服务）是把企业零散的 logo、配色、字体、语气整理成可执行规范文档并配置品牌套件的中端服务。它小众被低估——需求藏在'品牌越做越乱、AI 出图风格飘忽'背后、几乎无人主动搜索、夹在免费模板与百万级全案之间；一人可远程异步交付、启动工具成本不到 $20/月、有真实市场（全球品牌设计服务 2025 约 $52 亿、Upwork 项目 $500–$2,500），非常适合 OPC 与数字游民。",
    "details": details,
    "sourceThread": "workbuddy-daily-niche-research",
    "labels": [
        "daily",
        "niche-industry",
        "opc",
        "digital-nomad",
        "brand-guidelines",
        "visual-identity",
        "freelance-design",
        "solopreneur-services",
    ],
    "nextSteps": [
        "用 Canva 免费版 + 公开品牌规范范例，2 天内仿做一份'虚构品牌'的 1 页规范（logo 用法+配色+字体），发社交平台证明能力。",
        "上 Upwork / Fiverr 搜 'brand style guide'，研究前 20 个 gig 的定价与交付物，写下你的差异化定位（如专做 AI 产品/SaaS 品牌规范）。",
        "向 3 个刚完成 logo 的小微企业/创作者免费或半价做轻量规范（$95 档），换真实案例与评语验证需求。",
    ],
    "artifacts": [
        {
            "label": "Upwork — Brand Identity & Guidelines 自由职业者指南（项目价 $500–$2,500）",
            "path": "https://upwork.com/hire/brand-identity-and-guidelines-freelancers",
        },
        {
            "label": "Upwork — SlideGem 品牌规范文档服务（$95/$275/$595，2000+ 项目，50+ 国家）",
            "path": "https://upwork.com/services/product/design-a-professional-brand-style-guide-and-corporate-brand-identity-2084988087010159380",
        },
        {
            "label": "StatsMarketResearch — 全球品牌设计服务市场（2025 $52 亿→2034 $98 亿，CAGR 7.3%）",
            "path": "https://www.statsmarketresearch.com/global-br-design-services-market-8082610",
        },
        {
            "label": "DataMarketView — 全球品牌服务市场（2025 $41.2 亿，CAGR 7.46%）",
            "path": "https://www.datamarketview.com/reports/branding-service-156307",
        },
        {
            "label": "Thrivelance — 2026 自由职业费率指数（含品牌规范分渠道报价）",
            "path": "https://thrivelance.com/research/freelance-rate-index",
        },
        {
            "label": "MercadoKit — 2025 Shopify 品牌建设指南（规范元素与工具清单）",
            "path": "https://mercadokit.com/guides/shopify-brand-building-guide-2025",
        },
        {
            "label": "Shaheer Malik — 品牌一致性工具对比与案例（HubSpot/Loomly）",
            "path": "https://shaheermalik.com/blog/everything-you-need-to-know-about-brand-consistency",
        },
        {
            "label": "Lucidpress / Marq — 品牌一致性现状研究（增收 23%、81% 违规内容、仅 25% 执行）",
            "path": "http://pub.lucidpress.com/multi-location-branding-guide/",
        },
    ],
}

out_dir = os.path.join("runs-workbuddy", "2026-10-28")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "niche-opc-industry.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print("Wrote", out_path)
