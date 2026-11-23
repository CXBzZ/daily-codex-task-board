import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path('/Users/pupu/Documents/每日任务')
DATE = '2026-11-23'
TZ = timezone(timedelta(hours=8))

details = '''一、行业是什么，为什么小众
一句话定义：以独立顾问或小型服务商身份，凭客户书面授权拿到 UPS/FedEx 等承运商的账单 CSV 与发货记录，逐票比对合同费率、附加费、燃油附加费表、计费重量和服务时效，找出多收与可退款项目，在承运商窗口期内代为提交争议或服务失败退款申请，最后按追回金额分成或收固定审计费。
为什么被低估：需求藏在“运费每个月都在涨，但没人说得清为什么”里面，客户不会主动搜索“货运账单审计”；它夹在物流运营、财务应付、电商运营三个岗位之间，谁都觉得该由别人管；费率卡、zone、accessorial、dimensional weight、GSR 等黑话让门槛看起来很高，实际是规则比对活；大型自动化平台只盯中高票量客户，月运费两万美元上下的长尾商家没人服务；而且供应商不会公开“帮客户追回了多少钱”，案例极难被搜到。

二、如何运作
典型客户：月运费约 2 万至 10 万美元的 DTC 品牌、Shopify 商家、Amazon FBM 卖家、小型 3PL/代运营、跨境独立站。触发点通常是季度运费突然上升、毛利率被物流吃掉、年度承运商续约、或财务发现附加费异常。
交付物：异常明细表（追踪号、费用代码、争议依据、金额、证据截图）、代提交的服务失败/账单争议申请、追回到账核对表、费率卡对照表、合同基准与谈判建议报告。
完整工作流：签授权与 NDA（明确只读访问账单账户、代提交权限、分成口径）→ 从 UPS Billing Center / FedEx Billing Online 导出原始发票 CSV，而不是 PDF 摘要 → 从 Shopify/OMS 导出发货记录，以追踪号为主键对齐 → 规则扫描：重复计费、体积重误算、住宅/偏远附加费误用、地址更正费、服务降级仍按高价计费、燃油费率月份错配、折扣未生效 → 时效扫描：对比承诺送达与实际送达，剔除天气、节假日、地址错误、危险品、海关延误等免责情形 → 在窗口内提交申请（UPS/FedEx 服务失败退款通常以 15 天为关键窗口，部分附加费争议窗口更长，须以当期官方条款为准）→ 逐周核对抵扣是否真进账户（FedEx 多抵原发票，UPS 多抵下周发票）→ 出月度报告与续约建议 → 按已到账金额开票收款。
关键工具：承运商官方账单中心、Google Sheets / Excel / Airtable、Python + pandas 或 DuckDB（票量大时）、Shopify/OMS 导出、邮件或 Slack 异步汇报。不需要车辆、仓库或任何本地牌照。

三、盈利模式
收入来源与定价：①追回分成，这是行业主流：Refund Retriever 按年运费分档收 50%/45%/40%，无设置费、无月费、无取消费；71lbs 对年运费 30 万美元以下客户收追回额的 40%，企业版定制。②固定审计费：历史账单一次性复盘 500–2,000 美元，或按月 300–1,000 美元的持续监控保留服务。③合同优化与费率谈判：按项目 1,000–5,000 美元，或按未来节支分成。
利润空间：主要成本是时间和少量工具（表格免费至 20 美元/月，脚本免费，BI 0–30 美元/月），没有库存与场地。若按追回额 30%–40% 收费，一笔 5,000 美元追回对应 1,500–2,000 美元收入，扣除支付通道与税后大致保留七到八成；但被拒争议不产生收入，账期由承运商抵扣节奏决定。
复购：月度审计天然续费，续约谈判形成年度节点；把累积的费率基准整理成同行对标报告，可二次售卖给同类商家。

四、入门门槛
技能：表格透视与 XLOOKUP、读懂费率卡与附加费代码、理解承运商退款条款与免责清单、能写清楚的英文争议邮件。2–4 周可上手，先用脱敏账单练手再接单。
工具： Sheets/Airtable 免费或每月 10–20 美元；Python 免费；可选 BI 每月 0–30 美元；合同与 NDA 模板可用免费模板起步。
资金：0–300 美元（域名、邮箱、合同模板），无库存与重型设备。
时间：从零到第一单常见 3–8 周——2 周练手与建模板，1–2 周内容输出或定向外联，1–2 周试点成交；已有电商物流人脉会更快。

五、为什么适合 OPC / 数字游民
第一，100% 异步：输入和输出都是文件，客户无需实时会议；你睡觉时美国客户在白天提交或确认争议，时区差反而是优势。第二，客户全球分布：UPS/FedEx 的服务条款是公开文本，研究一次可服务多国英文客户，不依赖本地关系。第三，边际成本低：规则表、脚本和报告模板一次搭好，新客户主要增加核对时间而不是重建交付。第四，价值可量化：追回多少美元就是客户看得见的 ROI，容易写案例、容易提价、续费理由天然成立。第五，体量友好：月运费 2 万至 10 万美元的品牌对大平台是长尾，正是单人顾问的空间。第六，可阶梯化：分成试点 → 固定月费 → 合同谈判 → 同行基准报告，一个人也能逐步抬高客单而不必招人。

六、潜在收益（谨慎，不承诺）
公开市场数据：Global Info Research 统计 2024 年全球货运审计与支付服务收入约 10.4 亿美元，预计 2031 年 25.86 亿美元，2025–2031 年 CAGR 13.7%；WiseGuy Reports 口径更宽，2025 年货运审计服务 59.2 亿美元、2035 年 105 亿美元，CAGR 5.9%；QYResearch 口径为 2025 年 11.64 亿美元、2032 年 28.8 亿美元，CAGR 14%。不同报告口径差异很大，不能相加，只用来说明这是有真实支出的成熟市场。
错误率与可追回空间：据 Sifted 2026 年 5 月数据（经大数跨境转述），每周 500–5,000 包裹的中型 DTC 发货方，承运商发票错误率占运费 2.1%–4.8%；年运费 200 万美元对应 4.2 万至 9.6 万美元的可追回超额费用。注意这是错误总额，不是你的收入。Refund Retriever 自述平均可让账单降低 5%–10%，这是服务提供商的营销口径，应打折看待。
条件化区间：新手期（0–3 个月）若拿到 2–4 家、合计月运费 5 万至 20 万美元的客户，按追回额 30%–40% 计，实际追回 1,000–4,000 美元/月时对应收入 300–1,600 美元/月；常见情况是前 1–2 个月为零。成熟期（6–12 个月以上、5–10 家稳定客户、合计月运费 50 万美元以上），追回 5,000–20,000 美元/月时，分成收入 1,500–8,000 美元/月，叠加固定审计费和谈判项目可能到 3,000–12,000 美元/月。以上均为假设条件下的推算，这些是参考数据，不等于个人收入，也不构成任何收益承诺。

七、主要风险
市场风险：承运商可随时调整或暂停服务保证——FedEx 加拿大页面显示 2026 年 2 月 12 日起仅对部分 Express 服务、且仅对加拿大付款人恢复退款保证，其余服务继续暂停，可追回池会随政策收缩；自动化平台下沉（Shipware 已并入 SIB，71lbs 推出面向大客户的产品）持续压低纯追收单价；客户学会自己claim 后需求消失。
技术风险：账单字段与导出格式改版会让规则脚本失效；平台内置审计先把明显错误吃掉；漏判或误判会直接损害客户信任；过度依赖单一错误类型。
合规风险：必须先取得书面授权才能访问账单账户与代提争议；FedEx 美国条款明确写明第三方（非付款人）提出请求时可能不予受理，因此必须以账户持有人名义提交；账单含收件人地址与电话，受 GDPR/CCPA 约束；跨境收款、税务申报需自行处理；只做“研究 + 代提交 + 报告”，不对外声称法律或税务意见。
现金流风险：分成模式要等抵扣到账才收费，周期可能 30–90 天；争议被拒比例不低（Refund Retriever 自述约 50% 逾期件因免责条款不符合而无资格）；获客与学习期没有收入，需要准备 2–3 个月生活缓冲。

八、不适合的人群
想赚快钱、不愿长期做枯燥逐票核对的人；不懂也不愿学表格与数据分析、无法对金额准确性负责的人；不愿写英文邮件、对承运商条款没有耐心的人；无法承受前 1–3 个月零收入、把分成当被动收入的人；打算用“保证追回多少钱”话术成交、或未经授权登录/抓取客户账户的人；已有丰富物流资源但不愿做执行细节的人，更适合直接做高阶费率谈判咨询而不是从审计做起。

九、3 个可验证的入门步骤
步骤 1（1–2 天，成本 0）：拿一份脱敏的 UPS/FedEx 月度账单 CSV 与对应发货记录（朋友企业样例或公开教程数据均可），在 Sheets 里以追踪号对齐后抽查 100 票，统计重复计费、体积重、附加费误用、服务降级四类异常率。若异常率低于 1%，换样本或换客户群；高于 2% 进入下一步。
步骤 2（2–3 天，成本 0）：挑 1–2 笔确认逾期且无免责情形的包裹，通过官方账单中心的 Dispute 入口或客服渠道，在 15 天窗口内自行提交退款申请，记录从提交、批准到抵扣到账的天数与被拒原因。跑不通整条链路就停止投入。
步骤 3（3 天，成本 50 美元以内）：在跨境电商与物流社区发一篇“前 5 家免费首月异常扫描”的服务贴，并定向联系 10 家月运费 2 万至 10 万美元的 DTC 品牌；以 Refund Retriever 的 40%–50% 分成为锚，报 30%–40% 分成或 500 美元起的固定审计费。拿到 1 家愿意签授权并提供账单样本的意向客户，即视为值得继续。

十、核验来源
1. FedEx 官方 Money-Back Guarantee Policy（加拿大，2026 年 2 月 12 日更新，15 天申请窗口与服务暂停说明）：https://fedex.com/en-ca/service-guide/money-back-guarantee.html
2. UPS 官方 Money-Back Guarantee（15 天书面/电话申请、Billing Center Dispute、免责条件）：https://www.ups.com/fi/en/help-center/shipping-support/service-guarantee.page
3. Refund Retriever 定价页（50%/45%/40% 分档、无月费、平均降账单 5%–10%）：https://www.refundretriever.com/pricing/
4. 71lbs 定价页（年运费 30 万美元以下收追回额 40%、无前期费用）：https://71lbs.com/pricing/
5. Global Info Research 货运审计和支付服务市场报告（2024 年 10.4 亿美元→2031 年 25.86 亿美元）：https://www.globalinforesearch.com.cn/reports/2053199/freight-audit-and-payment-service
6. WiseGuy Reports 全球货运审计服务市场（2025 年 59.2 亿美元→2035 年 105 亿美元）：https://www.wiseguyreports.com/cn/reports/freight-audit-service-market
7. 大数跨境：货运审计与支付流程、索赔窗口与四类可追回费用：https://applet.10100.com/article/152573894
8. 物流前沿：包裹账单审计 ROI 公式与月运费分档建议：https://www.logifrontier.com/zh/article/parcel-invoice-audit-worth-it-guide
补充参考：ANKPOST 运费审计与付款词条（2%–6% 差异、第三方审计 3%–8% 或固定费）：https://www.ankpost.com/cn/wiki/freight-audit-payment-cn'''

summary = (
    '快递/货运账单审计（Parcel & Freight Invoice Audit）是凭客户授权核对 UPS/FedEx 账单与发货记录，'
    '找出重复计费、附加费误用和逾期送达可退款项，代客在窗口期提交争议并按追回额分成的小众服务。'
    '它夹在物流、财务与电商运营之间，需求真实但几乎无人主动搜索；输入全是文件、可异步交付、'
    '规则模板边际成本极低，且月运费 2 万至 10 万美元的长尾商家被自动化平台忽视，'
    '因此特别适合一人公司和数字游民远程切入。'
)

next_steps = [
    '1–2 天、零成本：用脱敏账单 CSV 与发货记录在 Sheets 按追踪号对齐，抽查 100 票统计四类异常率；异常率低于 1% 就换样本，高于 2% 继续。',
    '2–3 天、零成本：挑 1–2 笔无免责的逾期件，走官方账单中心 Dispute 或客服渠道在 15 天窗口内提交退款，记录提交到抵扣到账的天数与拒因；跑不通就停。',
    '3 天、50 美元以内：发“前 5 家免费首月异常扫描”服务贴并定向联系 10 家月运费 2 万至 10 万美元的 DTC 品牌，以 40%–50% 分成为锚报 30%–40% 或 500 美元起固定费，拿到 1 家签授权并提供账单样本的客户即验证通过。',
]

artifacts = [
    {'label': 'FedEx 官方 Money-Back Guarantee 政策（2026 更新、15 天窗口、服务暂停）', 'path': 'https://fedex.com/en-ca/service-guide/money-back-guarantee.html'},
    {'label': 'UPS 官方 Money-Back Guarantee（申请条件、Dispute 流程、免责条款）', 'path': 'https://www.ups.com/fi/en/help-center/shipping-support/service-guarantee.page'},
    {'label': 'Refund Retriever 定价（50%/45%/40% 分成、无月费、平均降本 5%–10%）', 'path': 'https://www.refundretriever.com/pricing/'},
    {'label': '71lbs 定价（年运费 30 万美元以下按追回额 40% 收费）', 'path': 'https://71lbs.com/pricing/'},
    {'label': 'Global Info Research 货运审计与支付服务市场规模报告', 'path': 'https://www.globalinforesearch.com.cn/reports/2053199/freight-audit-and-payment-service'},
    {'label': 'WiseGuy Reports 全球货运审计服务市场（2025–2035）', 'path': 'https://www.wiseguyreports.com/cn/reports/freight-audit-service-market'},
    {'label': '大数跨境：货运审计流程、索赔窗口与可追回费用类型', 'path': 'https://applet.10100.com/article/152573894'},
    {'label': '物流前沿：包裹账单审计 ROI 公式与客户体量分档', 'path': 'https://www.logifrontier.com/zh/article/parcel-invoice-audit-worth-it-guide'},
]

now = datetime.now(TZ).replace(microsecond=0)
started = now.replace(hour=9, minute=14, second=44)
record = {
    'taskId': 'niche-opc-industry',
    'taskName': '每日小众赚钱行业：快递/货运账单审计与退款追收（Parcel Invoice Audit）',
    'status': 'success',
    'startedAt': started.isoformat(),
    'finishedAt': now.isoformat(),
    'summary': summary,
    'details': details,
    'sourceThread': 'workbuddy-daily-niche-research',
    'labels': [
        'daily', 'niche-industry', 'opc', 'digital-nomad',
        'parcel-audit', 'freight-invoice-audit', 'cross-border-ecommerce', 'logistics-cost',
    ],
    'nextSteps': next_steps,
    'artifacts': artifacts,
}

out = ROOT / 'runs-workbuddy' / DATE / 'niche-opc-industry.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'wrote {out} ({out.stat().st_size} bytes)')
