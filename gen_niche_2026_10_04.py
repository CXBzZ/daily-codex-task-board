# -*- coding: utf-8 -*-
"""Generate the daily niche OPC industry brief for 2026-10-04."""
import json
import os

started = "2026-10-04T09:05:00+08:00"
finished = "2026-10-04T09:14:00+08:00"

details = """1. 行业是什么，为什么小众
一句话定义：独立字体设计（Independent Typeface Design）是指个人设计师独立创作一套完整的字体（字库），通过字体市场或自有渠道授权给品牌、设计师和内容创作者使用，赚取一次性授权费或长期被动版税。它夹在"平面设计"和"软件开发"两个大行业之间——外人以为它是设计，其实更接近"一次设计、无限次授权"的数字产品生意；又因为字体无处不在却又"隐形"，普通人从不会主动想到"我也能做字体卖钱"。

为什么被低估：①搜索量低、教程少——市面上的设计副业教程几乎都在讲 logo、插画、PPT，几乎没人教"如何靠卖字体赚钱"；②需求隐蔽——每个 App、网站、品牌都在用字体，但没人会觉得"买字体"是需要专门去找人的服务；③看起来技术门槛高——人们误以为做字体需要专业科班背景，实际上 Latin / Display 字体靠审美 + 工具即可入门；④夹缝行业——它既不是纯艺术也不是纯代码，被主流自由职业分类忽略。

2. 如何运作
典型客户：①全球独立设计师 / 品牌工作室（在 Creative Market、MyFonts 上买 display 字体做项目）；②中小企业 / 创业公司（需要品牌专属定制字体）；③内容创作者（YouTuber、播客、独立开发者需要独特视觉识别）；④大型品牌的定制字体外包（通过代理或直接洽谈）。

需求从哪里触发：品牌升级、新品发布、节日营销、App 改版、独立创作者的视觉差异化需求。触发渠道：设计社区（Behance、Dribbble、Instagram、Pinterest 展示作品）、字体市场自然搜索、直接外联品牌 / 代理商。

核心交付物：①零售字体（在 MyFonts / Creative Market 上架，按 license 销售，一次制作长期售卖）；②定制字体（为某品牌独家设计一套字库，按项目收费）；③字体相关附加数字产品（字体包 + 样机 mockup、alternates 字母变体包）。

完整工作流：
1. 选题与调研：找趋势缺口（如复古衬线、手写体、可变字体），确定风格方向（1–3 天）。
2. 草图与数字化：在 Illustrator / Procreate 画核心字母，导入 Glyphs 数字化（1–2 周）。
3. 扩展字符集：大写、小写、数字、标点、常用多语言字符（1–2 周）。
4. 间距与字偶距（spacing & kerning）：最耗时也最决定专业度的一步（1–2 周）。
5. 测试与导出：在真实设计场景中测试可读性，导出 OTF / TTF / WOFF2（数天）。
6. 上架与定价：在 MyFonts / Creative Market / Fontspring 建立店铺，写描述、做预览图、设分档 license。
7. 推广：Instagram / Pinterest / Behance 展示真实用例，提供免费字体引流。
8. 收款：平台按月结算（通常 30–60 天账期），自有站通过 Gumroad / Stripe 即时收款。

关键工具与平台：
- 设计工具：Glyphs 4（行业标准，一次性 $319；Glyphs Mini $53/月；学生半价 $159）、FontForge（免费开源）、FontLab（订阅起 $9/月）、BirdFont（免费）。
- 矢量草图：Adobe Illustrator、Procreate。
- 市场：MyFonts（最大零售）、Creative Market（独立友好）、Fontspring（透明授权）、Envato / GraphicRiver、YouWorkForThem、Etsy、Gumroad（自有直销，低抽成）。

3. 盈利模式
收入来源与定价：
- 零售授权（被动收入主力）：基础 display 字体 $10–$30，专业字族 $50–$200+，完整字体系统 $300–$500+。分档 license：个人 $29–49、商用 $79–199、扩展（App / 电子书嵌入）$299–999、企业 $1,000+。
- 定制字体（项目制）：小型单字重 $1,000–$3,000，中型多字重 $3,000–$7,000，品牌全套 / 大型 $10,000+（按 40–200 小时、$50–150/时计；中国定制 Logo 字体 3,000–30,000 元，全套字库 10 万–100 万+ 元）。
- 自有站直销：通过 Gumroad 抽成更低，保留更多利润。

利润空间（扣工具 / 平台 / 税后）：
- 平台零售抽成：MyFonts ~50%、Creative Market ~40%、Fontspring ~30%；自有站抽成最低（Gumroad 约 10% 以内 + 支付费）。
- 据 gigmoneytips 测算，熟练设计师有效时薪：MyFonts $55–180、Creative Market $50–140、YouWorkForThem $60–160。
- 扣 30% 税 + 平台费后，一个能稳定销售的字族首年可产生 $1,000–$10,000+/月（designflea 数据；earnifyhub 案例 Sarah Chen 6 个月净收入 ~$7,910，月均 ~$1,318）。

复购 / 长期合同：零售是"一次制作、多年授权"的被动收入；定制项目可转化为品牌年度字体维护 / 扩展合同；自有站回头客复购率高。

4. 入门门槛
技能：需要审美（字形结构、节奏、对比）、耐心（spacing / kerning 极耗时间）、基础矢量软件操作。不需要美术科班——很多成功独立字体师是自学。从画核心字母 → 数字化 → spacing，熟练周期约 1–3 个月可产出第一个可售字体。

工具：初期 Glyphs Mini（$53/月）或免费 FontForge 即可起步；进阶再买 Glyphs 4（$319 一次性）。无需服务器 / 库存。

资金：启动成本极低——软件 $0–$319，预览图用免费工具，平台开店免费。总计可控制在 $0–$500 内起步（不含时间成本）。

时间：从零到第一单（零售第一笔 license 或第一个定制客户）通常 2–6 个月：1–2 个月做出第一个字体，再 1–4 个月推广等待首单。定制路线若有现成作品集接单更快。

5. 为什么适合 OPC / 数字游民
- 异步交付：字体文件（OTF / TTF）是数字交付，无需实时会议，时区完全无关，适合全球客户 + 睡觉时也能成交。
- 全球客户：Latin / Display 字体面向英语国家市场（MyFonts、Creative Market 以欧美买家为主），一个中国设计师可直接服务全球，无地域限制。
- 边际成本极低 / 可规模化：字体是"一次设计、无限授权"的数字产品，第 1001 次销售的边际成本≈0，天然适合一人放大。
- 被动收入属性：上架后字体可卖数年甚至数十年，minimal maintenance，契合数字游民"不在场也能赚钱"的目标。
- 无需团队：从设计、上架到推广、客服，一个人闭环；客服主要是 license 咨询，可模板化。
- 轻资产：无库存、无场地、无重型设备，一台 Mac + 软件即可全球运营。

6. 潜在收益（谨慎，不承诺）
参考区间（公开数据，不等于个人收入）：
- 新手阶段（前 6–12 个月，1–5 款字体）：零售月收入 $50–$500；主要靠持续出新品 + 推广（copyfontsonline、designflea 数据）。
- 中间阶段（组合 10–30 款 + 初步口碑）：$500–$2,000/月（copyfontsonline 中间档）。
- 成熟阶段（强组合 + 自有站 + 少量定制）：$2,000–$10,000+/月（designflea 高级档；gigmoneytips 有效时薪测算年化可达数万美元）。
- 定制路线：单项目 $1,000–$10,000+，品牌年度维护合同可更高。

市场背景（谨慎引用）：全球字体与字库市场 2024 约 $1.197B、2025 $1.242B、2031 $1.584B（CAGR 4.1%，QY Research）；更宽泛口径（含订阅与服务）2025 约 $8.11B（Verified Market Research）。内容创作者占应用端约 60%（QY Research），需求结构持续向独立创作者倾斜。

明确提示：这些是平台与行业参考数据，不等于任何个人的实际收入。字体销售高度依赖质量、风格趋势与推广，收入波动大，前几个月可能只有个位数销售。

7. 主要风险
- 市场风险：趋势衰减快（display 字体易过时）、平台折扣文化压低客单价、竞争极激烈（Creative Market 已有 30 万+ 字体）。
- 技术 / 平台风险：①平台政策与抽成变动（MyFonts 被 Monotype 收购后条款变化）；②AI 字体生成器 2026 年走向主流，将冲击中端"够用型"功能字体市场（freefontzone 行业预测）；③字体文件被盗版 / 免费分享，维权成本高。
- 合规风险：①版权——必须确保字体为原创，避免抄袭商业字库；②AI 训练数据合法性争议（多起 foundry 诉讼）；③跨境收款税务（自由职业者需自行申报）。
- 现金流风险：平台账期 30–60 天；获客依赖平台自然流量时被动；前期数月可能零收入，需预备生活费。

8. 不适合的人群
- 期待"快速变现 / 月入过万"的人——字体需要审美积累与数月打磨，前几个月收益微薄。
- 没有耐心做 spacing / kerning 的人——这是专业与否的分水岭，跳过则卖不动。
- 完全不懂设计审美、只想"批量产字体"的人——AI 会先淘汰这类低质产出。
- 不愿做推广 / 社媒的人——"上传即等卖"在 30 万+ 字体里几乎不可能。
- 想做中文字库全字库的人——几千字工作量巨大，不适合一人轻启动（建议从 Latin / Display 或单一品牌定制起步）。

9. 3 个可验证的入门步骤
1. 【第 1–3 天，成本 $0】用免费 FontForge 或 Glyphs 30 天试用，照教程做出一个最小字符集（A–Z、a–z、0–9、常用标点）的单字重 display 字体，导出 OTF。验证：能否走完"画字 → 数字化 → 导出可用字体"全流程。
2. 【第 1 周内，成本 $0】在 Instagram / Pinterest / Behance 发布这个字体的 3 张真实用例 mockup（logo、海报、网页标题），观察互动与询问。验证：是否有人对你的风格表达兴趣（点赞 / 私信 / 收藏），判断风格方向是否值得继续。
3. 【第 2–4 周，成本 $0 起】把字体上架 Creative Market 或 MyFonts（免费开店），定低价（$10–$19）观察自然搜索带来的首单；同时外联 3–5 个小品牌 / 独立开发者提供低价定制报价。验证：能否在 30 天内产生第一笔真实收入（哪怕 $10），确认市场愿意为你的字体付费。

10. 核验来源
（1）QY Research《全球 Font and Typeface 市场报告 2025》：2024 $1.197B → 2031 $1.584B，CAGR 4.1%。
（2）Verified Market Research《Font and Typeface Market》：2025 $8.11B → 2033 $12.5B（宽泛口径）。
（3）Glyphs 官方：行业主流字体编辑器，Glyphs 4 $319 一次性 / Mini $53 月付 / 学生半价。
（4）Creative Market 字体市场：独立设计师友好，抽成约 40%，已上架 30 万+ 字体。
（5）MyFonts：全球最大字体零售市场，分销抽成约 50%。
（6）Fontspring：透明授权、低抽成约 30%。
（7）designflea《Sell Fonts》：独立字库月收入 $1,000–$10,000+、价格带与平台对比。
（8）WhatFontIs 分析：2026 设计师抵制 AI 字体、手工字体更值钱——风险与机会并存。"""

data = {
    "taskId": "niche-opc-industry",
    "taskName": "每日小众赚钱行业：独立字体设计与字库授权（Typeface Design & Font Licensing）",
    "status": "success",
    "startedAt": started,
    "finishedAt": finished,
    "summary": "独立字体设计是个人设计师创作完整字库并通过市场授权赚取被动版税的隐形赛道，夹在设计与软件之间、需求真实却极少人主动入局。它一次设计、无限授权、全球异步交付、零库存低启动，非常契合一人公司与数字游民；但需审美积累与数月打磨，且中端市场正受 AI 生成字体冲击。",
    "details": details,
    "sourceThread": "workbuddy-daily-niche-research",
    "labels": ["daily", "niche-industry", "opc", "digital-nomad", "font-design", "typeface", "creative-economy", "passive-income"],
    "nextSteps": [
        "用免费 FontForge 或 Glyphs 试用，3 天内做出最小字符集（A–Z/a–z/0–9/标点）的单字重 display 字体并导出 OTF，验证全流程能否走通。",
        "在 Instagram / Pinterest / Behance 发布 3 张真实用例 mockup，观察互动与私信询问，判断风格方向是否值得继续。",
        "第 2–4 周把字体上架 Creative Market 或 MyFonts（免费开店）定低价，并外联 3–5 个小品牌提供低价定制，验证 30 天内能否产生第一笔真实收入。"
    ],
    "artifacts": [
        {"label": "QY Research：全球 Font and Typeface 市场报告 2025（规模与 CAGR）", "path": "https://www.qyresearch.com/reports/3422828/font-and-typeface"},
        {"label": "Verified Market Research：Font and Typeface Market（宽泛口径 $8.11B）", "path": "https://www.verifiedmarketresearch.com/product/font-and-typeface-market/"},
        {"label": "Glyphs 官方（主流字体编辑器）", "path": "https://glyphsapp.com/"},
        {"label": "Glyphs 定价页（Glyphs 4 $319 / Mini $53 月付 / 学生半价）", "path": "https://glyphsapp.com/buy"},
        {"label": "Creative Market 字体市场（独立设计师友好，抽成约 40%）", "path": "https://creativemarket.com/fonts"},
        {"label": "MyFonts（全球最大字体零售市场，分销抽成约 50%）", "path": "https://www.myfonts.com/"},
        {"label": "Fontspring（透明授权、低抽成约 30%）", "path": "https://www.fontspring.com/"},
        {"label": "WhatFontIs：2026 设计师抵制 AI 字体，手工字体更值钱（风险与机会）", "path": "https://www.whatfontis.com/blog/designers-are-punishing-ai-fonts-in-2026-and-its-making-type-more-human/"}
    ],
}

out_dir = os.path.join("runs-workbuddy", "2026-10-04")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "niche-opc-industry.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("WROTE", out_path)
