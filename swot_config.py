SWOT_CATEGORIES = {
    "Company Overview": {
        "Overview": {
            "questions": [
                "What is the exact name of the registrant as specified in its charter (i.e., the full legal name of the company)?",
                "Where is the company's global headquarters located",
                "what is its primary industry/business classification ",
                "What are the customer segments it serves?",
                "What are the  the geographic markets in which it  operates in?",
                "What are the key services offered by the company",
                "What are the key products offered by the company",
                "How many business segments is the company operating in as per the latest annual report?",
                "Name the business segments of the company",
                "What is the one main strength for the company",
                "What is the one major threat for the company"
            ],
            "summary_instruction": "This section is the company's overview in its swot report. Summarize all the information above into one paragraph. Include the company’s full legal name, primary industry, and global headquarters location. Summarize main customer segments, geographic markets, key products, proprietary technologies, and business segments (number and names). Any numbers such as percentages, years, values and key stats should not be included in the overview. Competitor's names, strategy and other details should not be included"
        }
    },
    "Strengths": {
        "R&D Focus": {
            "questions": [
                "What is the company's strategy towards R&D?",
                "How much did the company spend on R&D in the latest FY?",
                "What is the year-on-year growth in R&D spend and percentage of revenue? ",
                "WHow many patents are being filed?",
                "Where are the company's key research facilities located, and are there any new ones added recently?",
                "What technological innovations support the company's products and services?",
                "A recent example of innovation, launch, expansion, research investment, or approval that supports R&D strength."
            ],
            "summary_instruction": "Generate a single paragraph summarizing the company’s approach to research and development (R&D) based on the answers to the listed questions. Include details about the company’s R&D strategy and how it aligns with long-term goals. Mention the latest fiscal year’s R&D expenditure, the year-on-year change, and the percentage of revenue spent on R&D. Describe trends in patent filings and their relevance to competitiveness. List the locations of key research facilities and highlight any recent expansions. Include technological innovations applied to the company’s products or services, and provide a recent example that demonstrates innovation strength, such as a new launch or approval."
        },
        "Financial Strengths": {
            "questions": [
                "What is the year-on-year revenue growth for the company in its latest fiscal year, and what were the key contributing business segments?",
                "What does the YoY change in the company's financial metrics suggest about its long-term growth?",
                "What are the main reasons and factors for the revenue growth of the company in the current fiscal year?",
                "How has the company's operating income and margin changed compared to the previous fiscal year, and what does this indicate about its operational performance?",
                "How has the company's net income and net margin evolved year-over-year, and what might this imply for long-term profitability?",
                "What are the earnings per share (EPS) for the company in the most recent year, and how has it changed from the previous year?",
                "How might the operational improvements in revenue, margin, and income metrics impact investor sentiment towards the company?",
                "(If non-US company) What is the company's revenue for the latest fiscal year in its local reporting currency, and what is it equivalent in USD?"
            ],
            "summary_instruction": "Combine all financial performance details into one comprehensive paragraph. Include year-on-year revenue growth for the latest fiscal year and the main business segments contributing to it. Highlight key internal or external factors driving revenue, and discuss how operating income and margin have changed year-over-year. Mention the evolution of net income and net margin, and what that suggests about long-term profitability. Include earnings per share (EPS) for the latest year and compare with the previous year. Discuss how operational improvements in revenue and profitability might influence investor sentiment. Also mention the company’s latest annual revenue in local currency and its equivalent in USD (if applicable). Do not include strategy or industry benchmarking data."
        },
        "Credit Ratings": {
            "questions": [
                "What are the company's long-term and short-term credit ratings from major rating agencies, how have they changed, and what outlook is assigned?",
                "How do the company's credit ratings and how do they impact its ability to raise capital, attract investors, and support financial resilience?",
                "How does capital adequacy support the company's strong credit ratings and overall group-wide financial health?"
            ],
            "summary_instruction": "Summarize the company’s current credit profile in a single paragraph. Include both short-term and long-term credit ratings from major rating agencies, any recent changes, and the outlook assigned by each agency. Explain how these ratings impact the company’s access to capital, investor confidence, and financial flexibility. Include capital adequacy indicators, such as debt-to-equity or coverage ratios, and explain how these support creditworthiness. Avoid comparisons with competitors or future strategic recommendations."
        },
        "Brand Value": {
            "questions": [
                "How does the company's brand portfolio contribute to its overall brand equity and market recognition?",
                "What are the key consumer and industrial brands under the company's portfolio, and how do they support diverse market segments?",
                "What product categories does the company serve through its major brands, and how do these appeal to a broad customer base?",
                "How has the company expanded or diversified its brand offerings in recent years?",
                "Under which banners or brand names does the company operate its stores in domestic and international markets?",
                "What industry-specific brands does the company offer across verticals such as healthcare, manufacturing, or automotive?",
                "What recognitions, accolades, or rankings (e.g., Fortune, Forbes, Interbrand) has the company received that highlight its brand strength, corporate reputation, or market perception?",
                "How does a diverse brand portfolio help the company attract customers from different industries and geographies?"
            ],
            "summary_instruction": "Craft a paragraph that outlines the company’s brand strength. Mention the key consumer and industrial brands under the company’s portfolio and explain how they support diverse customer segments. Include recent efforts to diversify or expand brand offerings, and the types of products or services each brand caters to. Highlight any accolades, awards, or global rankings that reflect brand strength and corporate reputation. Conclude with how the brand portfolio helps the company achieve broad market recognition and sustainable long-term growth."
        },
        "Product/service spread": {
            "questions": [
                "What are the key products in the company's portfolio, and how are they distributed across areas or product categories?",
                "In what ways does the company tailor its product offerings to different geographic markets?",
                "What are the key segments or products offered by the company, and what market share do they have in the recent fiscal year?",
                "How does the company support its products with value-added services such as installation, repair, or consultation?",
                "How does product and service diversity help the company maintain consistent revenue growth and offset risks from downturns?",
                "How does a wide portfolio contribute to the company's competitive positioning?"
            ],
            "summary_instruction": "Develop a single paragraph summarizing the company’s product portfolio and global competitiveness. List key products and the categories or areas they serve. Explain how the company adapts its offerings to different geographic markets and customer needs. Highlight value-added services that support these products. Emphasize how portfolio diversity helps mitigate business risk, maintain revenue stability, and enhance global positioning. Do not include unrelated data such as employee numbers or brand rankings."
        },
        "Market share & market position": {
            "questions": [
                "How does a diversified product lineup help the company manage business risks and stabilize revenue streams?",
                "How could the company's presence across multiple industries and segments enhance its overall market position, and what are the leading products and services, or segments?",
                "Which brands or products have a strong market share across the globe?",
                "How has the company performed in global brand rankings, and how does this reflect its market reputation?"
            ],
            "summary_instruction": "Write a paragraph that focuses on the company’s market positioning. Explain how its diversified product lineup stabilizes revenue and reduces business risks. Identify its leading products, services, or segments and their contribution to its market strength. Highlight any brands or products that hold a strong market share globally. Mention performance in recent global brand rankings as evidence of its market reputation. Avoid future projections, R&D content, and competitor names."
        },
        "Geographic reach & channels": {
            "questions": [
                "How many physical locations, offices, or facilities does the company operate globally, and how are they distributed by region?",
                "In which countries or territories does the company have a physical presence, and how does this support its operational scale?",
                "How does the company leverage its international infrastructure to support customer access and business continuity?",
                "How many service points, branches, or outlets does the company operate, and how do these enhance customer engagement?",
                "What are the key geographic regions contributing to the company's global footprint and market expansion?",
                "How has the company expanded its reach in the past year, and what physical assets supported this growth?",
                "What types of stores (e.g., flagship, outlet, mobile, specialty) are included in the company's operational network?",
                "How does the company's real estate and logistics infrastructure contribute to operational efficiency and brand visibility?",
                "How does a wide geographic footprint help the company mitigate regional risks and drive sustainable growth?",
                "How does the physical store network contribute to the company's market coverage and revenue generation?",
                "How has the company expanded or optimized its retail presence in recent fiscal years?",
                "How does the company balance between the owned versus the leased locations in its store network?",
                "How does the company manage supply chain efficiency through its facility network?",
                "In how many countries or regions does the company operate?",
                "How is the company's revenue distributed across major global regions?",
                "How many distribution centres does the company operate, and what is the total area covered by these centres?",
                "How does the company utilize its logistics infrastructure to support omnichannel operations and customer fulfilment?",
                "What portion of the company's operational infrastructure is leased versus owned, and how does this affect flexibility?"
            ],
            "summary_instruction": "Generate a detailed paragraph about the company’s global presence. Include how many physical locations, service points, or outlets the company operates worldwide and how these are distributed by region. Mention countries or territories with a strong physical presence and how that supports scale and customer access. Include how logistics and real estate infrastructure (owned vs leased) support operational efficiency. Also discuss how geographic diversity aids in mitigating regional risks and driving sustainable growth. Mention revenue distribution by major global regions and physical asset expansions in the recent year."
        },
        "Customer base and digital strength": {
            "questions": [
                "How many active customers or users does the company serve, and how does this reflect its market dominance?",
                "What is the scale and functionality of the company's digital platforms (e.g., mobile apps, web platforms)?",
                "How many users access the company's digital services, and how is digital adoption contributing to overall performance?",
                "How does the company support retail, commercial, or small business clients through digital and physical channels?",
                "What unique features or scale of the company's online platforms distinguish it in the market?",
                "Through which digital domains or websites does the company offer its products or services?",
                "How does the company integrate online platforms with its physical store network to enhance customer convenience?",
                "How does the company's omnichannel approach (retail + digital) contribute to attracting a wider customer base?",
                "What channels (retail, wholesale, direct-to-consumer, digital) are used to deliver the company's products?"
            ],
            "summary_instruction": "Summarize the company’s customer base and digital capabilities in one paragraph. Include the number or scale of active users/customers and what that suggests about market penetration. Mention the company’s digital assets, such as websites, mobile apps, or platforms, and how they support customer engagement, sales, or retention. Highlight omnichannel integration—how physical and digital channels work together to serve customers. Mention unique features of the company’s digital presence, and the main channels (retail, direct, digital) used to deliver products or services. Avoid using outdated or unrelated metrics."
        },
        "Orderbook health": {
            "questions": [
                "Analyze the current size and year-on-year growth of the company’s orderbook.",
                "Assess revenue conversion potential of the orderbook for the upcoming fiscal year.",
                "Break down orderbook contributions by business segments (e.g., consulting, managed services).",
                "Evaluate the role of orderbook in ensuring long-term financial stability.",
                "Track new bookings and backlog accumulation trends.",
                "Measure managed services bookings growth and segment performance.",
                "Benchmark conversion rates against industry norms and best practices.",
                "Examine how macroeconomic factors influence orderbook health and resilience.",
                "Assess the orderbook's role in supporting visibility during economic slowdowns."
            ],
            "summary_instruction": "Write a detailed paragraph summarizing the company’s orderbook and future revenue visibility. Include the current size of the orderbook, year-on-year growth, and its breakdown by business segments. Assess how this backlog supports financial stability and visibility into future revenues. Highlight trends in new bookings, backlog accumulation, and managed services growth. Discuss how macroeconomic factors affect orderbook health and how it provides resilience during downturns. Do not include competitor data, strategic targets, or financial metrics not tied to actual order intake."
        },
        "CET values and performances": {
            "questions": [
                "What is the company's Common Equity Tier 1 (CET1) capital ratio, and how does it compare to regulatory minimums?",
                "What are the company's Tier 1 and total capital ratios as per the latest fiscal year?",
                "How does the company's leverage ratio compare to the minimum threshold set by regulators?",
                "How does the company define and report its capital adequacy under Basel III standards?",
                "How much buffer does the company maintain above regulatory capital thresholds?",
                "Which regulatory frameworks (e.g., APRA, etc.) apply to the company's capital adequacy?"
            ],
            "summary_instruction": "Write a paragraph analyzing the company’s capital adequacy and its alignment with regulatory standards. Include the latest reported Common Equity Tier 1 (CET1), Tier 1, and Total Capital Ratios, and compare these against the minimum requirements set by Basel III or relevant regulatory authorities (e.g., APRA, ECB). Mention the company’s leverage ratio and assess whether it exceeds the regulatory threshold. Highlight any capital buffers the company maintains above the mandated minimums. Explain how the company defines, calculates, and discloses its capital adequacy, and benchmark its capital strength against peers or industry norms. Exclude unrelated information such as leadership appointments or management profiles."
        }
    },
    "Weaknesses": {
        "Legal issues": {
            "questions": [
                "Has the company made false or misleading claims about its products/services (including advertising or labelling)?",
                "Has the company failed to comply with industry regulations, safety standards, or government guidelines?",
                "Are there known violations or citations from regulatory authorities (e.g., FDA, FTC, OSHA)?",
                "Is the company selling products not approved or properly disclosed under local laws?",
                "What are the details and reasons for any lawsuit filings (parties involved, court, location, and nature of the suit)?",
                "What specific laws, regulations, or compliance requirements did the company violate, and was the violation intentional, negligent, or systemic?",
                "What fines, legal costs, settlements, or liabilities has the company incurred, and could these trigger further legal or regulatory actions?",
                "How do legal or regulatory issues affect the company's ability to operate in regulated markets?"
            ],
            "summary_instruction": "Summarize all the legal issues the company is facing into a single paragraph. Include the nature of the lawsuits, the parties involved, the courts where they were filed, and the locations and reasons for these legal actions. Mention if the company made false claims, violated regulations, or sold unauthorized products. Highlight known violations or citations from regulatory bodies and whether these were intentional, negligent, or systemic. Summarize the legal liabilities—such as fines, settlements, or ongoing legal costs—and assess the risk of future regulatory or legal actions. Conclude by stating how these legal issues are affecting the company’s operations in regulated markets."
        },
        "Product/service issues": {
            "questions": [
                "What product recalls has the company faced, and what are the details (reason, affected units/regions, regulatory involvement)?",
                "Are there known product defects, malfunctions, or safety risks (including links to injuries, fatalities, or illnesses)?",
                "Have internal quality control processes or regulatory bodies flagged any safety concerns or issued warnings?",
                "Can the recall or defect be corrected, or must the product/service be withdrawn completely?"
            ],
            "summary_instruction": "Write a detailed paragraph summarizing product recalls and safety concerns affecting the company. Include the reasons for each recall, the types of products affected, the scale (units or regions), and whether regulatory authorities were involved. Describe any known product defects, safety risks, or links to injuries, fatalities, or illnesses. State whether internal audits or external regulatory bodies flagged the issues. Assess whether the product defect was correctable or if a full market withdrawal was required. Avoid including unrelated data or competitor mentions."
        },
        "Incidents & accidents": {
            "questions": [
                "Were there any significant workplace accidents or incidents in recent past?",
                "If yes, when, where, what was the sequence of events, and who all were involved?",
                "Did this result in any injuries or damages, and was there a delay in reporting?",
                " Are there known safety hazards, defective equipment, or unsafe conditions?",
                "Has the company received past warnings or citations for safety violations?",
                "Was the incident caused by human error, mechanical failure, environmental conditions, or a combination?",
                "What legal or financial impact resulted from these incidents?"
            ],
            "summary_instruction": "Generate a paragraph summarizing any workplace accidents or operational incidents. Include when and where the incidents occurred, the sequence of events, and who was involved. Describe any resulting injuries, damages, or reporting delays. Highlight known causes such as human error, mechanical failure, or environmental factors. Include whether defective equipment or unsafe working conditions contributed, and whether the company received any prior warnings or citations. Discuss the legal or financial impacts stemming from these incidents, if any."
        },
        "Operational issues": {
            "questions": [
                "What factors contributed to a decline in total revenue, operating income, or net income compared to the previous year?",
                "Were there major product lines, regions, or customer segments that underperformed, and what were the reasons?",
                "Were there significant increases in operating expenses or declines in operating/net margins or EPS?",
                "Are declines in EPS proportionate to net income decline, or are other factors at play?"
            ],
            "summary_instruction": "Summarize the company’s annual revenue and income performance decline in one paragraph. Include key factors behind the fall in total revenue, operating income, and net income compared to the prior year. Identify underperforming product lines, regions, or customer segments and explain the reasons for their poor performance. Mention any increases in operating expenses or decreases in operating and net margins or EPS. Assess whether the EPS decline aligns with net income or is due to other influencing factors. Do not include quarterly-only data or mix in unrelated strengths or R&D content."
        },
        "Financial issues": {
            "questions": [
                "How much did total cash and cash equivalents decline over the reporting period, and what were the main causes?",
                "Did the cash decline impact the company's ability to meet short-term obligations or affect credit ratings/investor confidence?",
                "Has net cash from operating activities decreased due to lower net income, increased working capital needs, or other factors?",
                "Did the company make large capital expenditures, investments, or debt repayments that reduced cash reserves?",
                "Is the decline in working capital due to faster growth in current liabilities than in current assets, or due to asset write-downs?",
                "Are short-term borrowings, trade payables, or accrued expenses rising significantly?",
                " Are current liabilities increasing due to upcoming debt maturities or legal obligations?",
                "How is declining working capital affecting the company's ability to fund operations or meet short-term obligations?"
            ],
            "summary_instruction": "Craft a paragraph analyzing the decline in the company’s total cash and cash equivalents during the most recent reporting period. Quantify the decrease and outline the primary causes, such as reduced operating cash flow, increased working capital needs, large capital expenditures, investments, or debt repayments. Discuss whether the company’s ability to meet short-term obligations has been impacted, including effects on investor confidence or credit ratings. Include any rise in short-term liabilities like borrowings, trade payables, or accrued expenses, and explain how working capital changes may affect ongoing operations or liquidity."
        }
    },
    "Opportunities": {
        "Product/Service Launch & Market Expansion": {
            "questions": [
                "What external market trends or forecasts indicate significant growth potential for the company's offerings?",
                "How do recent product innovations or launches demonstrate the company's ability to meet evolving consumer needs?",
                "How do new products or services align with the company's long-term goals and differentiation strategy?",
                "What strategic advantages could be gained by entering or expanding within fast-growing sectors?",
                "How might new initiatives, launches, or expansions enhance the company's business portfolio and revenue potential?",
                "What recent regulatory approvals or designations strengthen the company's market position?",
                "How do new offerings position the company as a leader in niche or rapidly evolving segments?",
                "How does expansion into high-growth or underserved markets enhance competitive advantage?",
                "How could enhancements in service delivery, accessibility, or personalization support customer retention and acquisition?",
                "How do the company's moves reflect a broader strategy of innovation and differentiation?",
                "What is the expected impact of scaling operations across geographies or digital channels?",
                "How can the company use tech-enabled strategies or marketplace models to unlock new revenue streams?",
                "What are the potential benefits of integrating third-party platforms or launching a marketplace?",
                "How does enabling global, multi-currency operations contribute to international growth?",
                "Has the company launched a new product, service, or platform recently? What problem does it solve, and what are the expected outcomes?",
                "How do recent initiatives position the company in terms of innovation, leadership, or competitiveness?",
                "What is the point of opportunity with recent launches, approvals, expansions, or acquisitions?"
            ],
            "summary_instruction": "Summarize the company's recent product launches, services, and market expansion efforts in a single paragraph. Focus on how these moves align with broader market trends and the company’s long-term strategy. Highlight how the company’s new offerings support differentiation and innovation, meet evolving consumer needs, and tap into high-growth or underserved sectors. Include the expected impact on revenue, market positioning, and competitive edge. Incorporate any recent regulatory approvals, geographic or digital expansion efforts, marketplace integration, or tech-driven enhancements, and assess how these contribute to overall growth potential. Avoid internal metrics like R&D spending, net sales, or job creation."
        },
        "Industry Opportunity": {
            "questions": [
                "What is the estimated size and projected growth (CAGR) of the company's industry?",
                "What are the drivers behind this industry's growth, and what is the forecast period?",
                "What initiatives has the company taken to tap into this growing market, and how do they align with trends?",
                "How could the combination of market growth and company action benefit the company (e.g., portfolio expansion, revenue, innovation)?"
            ],
            "summary_instruction": "Generate a paragraph analyzing the overall industry size and growth potential relevant to the company. Include the latest estimated market size, projected CAGR, and key drivers of growth. Discuss how long the forecast period extends and evaluate the reliability of the projections. Highlight how the company is positioned to benefit from this growth through existing or planned initiatives, and how such industry momentum can drive innovation, product portfolio expansion, and revenue growth. Avoid outdated base year data, unrelated regional market share, or competitive challenges."
        },
        "Partnerships & Collaborations": {
            "questions": [
                "Has the company entered into any recent partnerships or collaborations? Who are the partners, and what is their expertise?",
                "What are the objectives and expected outcomes of these partnerships (e.g., customer experience, cross-border operations, marketplace expansion)?",
                "What technologies or platforms are being integrated, and how will they improve operational efficiency or service delivery?",
                "What new business avenues, customer segments, or markets do these partnerships open?",
                "How do these collaborations support technological innovation, product scalability, or industry-specific challenges?",
                "What product lines or solutions will be delivered under new agreements?",
                "How will partnerships enable penetration or strengthening in next-gen infrastructure or strategic industries?",
                "What consortiums, alliances, or coalitions has the company joined to support tech initiatives?",
                "How do these partnerships help boost revenue, expand the client base, or unlock new market opportunities?"
            ],
            "summary_instruction": "Create a paragraph summarizing the company’s recent partnerships and collaborations. Include the names and expertise of the partners, and describe the strategic goals of these alliances—such as customer experience improvement, operational efficiency, or expansion into new markets. Explain what technologies, platforms, or product lines are being co-developed or integrated. Assess the value these partnerships add in terms of innovation, scalability, revenue generation, or customer acquisition. Mention any consortiums or industry alliances the company has joined and how these support growth in strategic industries or next-gen infrastructure."
        },
        "Acquisitions or Regulatory Milestones of Products": {
            "questions": [
                "Has the company received any recent regulatory approvals? Which authority granted it, and for what product/service?",
                "What evidence or trials supported the approval, and does it address a niche or underserved population?",
                "What geographic markets are opened or strengthened through this milestone?",
                "How does this strengthen the company's portfolio, leadership, or regional presence, and what is the opportunity?"
            ],
            "summary_instruction": "Summarize any recent regulatory approvals received by the company, including which authority granted them and for which product or service. Explain the evidence or clinical trials that supported the approval and assess whether it targets a niche, underserved, or new geographic population. Highlight the strategic impact of the approval on the company’s portfolio, regional footprint, and market competitiveness. Focus on how this milestone represents an opportunity for expansion, leadership positioning, or service diversification. Do not include unrelated leadership announcements or old approvals."
        },
        "Digital Transformation & Infrastructure Expansion": {
            "questions": [
                "Has the company launched or expanded digital or physical infrastructure? In what regions and for what purpose?",
                "How are new services or locations improving customer access, personalization, or inclusion?",
                "How does the company integrate digital and physical touchpoints for a seamless experience?",
                "What long-term benefits (e.g., deeper relationships, operational scalability, financial inclusion) are expected from these efforts?"
            ],
            "summary_instruction": "Generate a paragraph detailing the company’s recent developments in digital or physical infrastructure. Describe what was launched or expanded, the regions involved, and the strategic purpose behind these efforts. Highlight how these developments improve customer access, enhance personalization or inclusion, and contribute to better service delivery. Explain how digital and physical channels are being integrated to create a seamless experience. Assess the long-term benefits, such as operational scalability, financial inclusion, or deeper customer engagement. Avoid citing data from sustainability reports or outdated initiatives."
        }
    },
    "Threats": {
        "Stringent regulations": {
            "questions": [
                "What are the new or existing regulations are considered particularly stringent or burdensome?",
                "Which specific aspects of the company's operations, products, or services are directly affected?",
                "Does compliance require significant system upgrades, audits, certifications, or trainings?",
                "Are the regulatory requirements vague, frequently changing, or difficult to interpret?",
                "Has the regulation forced changes to production, sourcing, or any processes of the company?",
                "Does the regulation limit the company's growth, innovation, or competitive agility?",
                "Have the regulators increased audits, inspections, or penalties in the company's business?"
            ],
            "summary_instruction": "Generate a paragraph explaining how stringent or changing regulations are impacting the company’s operations. Identify any specific laws or policies that are considered burdensome and the exact parts of the company (e.g., products, processes, sourcing, systems) that are affected. Mention if compliance demands major system upgrades, training, certifications, or audits. Assess whether vague, shifting, or complex rules are disrupting innovation, slowing growth, or requiring production changes. Include any increase in inspections, penalties, or regulatory scrutiny. Avoid unrelated operational strengths or internal initiatives."
        },
        "Intense competition": {
            "questions": [
                "Which competitors are gaining market share or outperforming the company?",
                "List out the direct major competitors of the company?",
                "Has a competitor initiated any launches / contracts / partnerships / acquisitions / expansions / agreements / innovations that threatens the company's market share and would be able to strengthen their position?",
                "Are pricing wars, customers acquisition costs, or marketing intensity increased?"
            ],
            "summary_instruction": "Write a paragraph analyzing the current competitive threats to the company. Identify major direct competitors and any recent actions—such as product launches, acquisitions, partnerships, or pricing strategies—that may negatively impact the company’s market position. Highlight if competitors are gaining market share or outperforming the company in key areas. Include details on pricing wars, customer acquisition cost increases, or intensified marketing efforts. Avoid internal investment or expansion narratives—focus solely on external threats from the competition."
        },
        "Volatile raw material prices": {
            "questions": [
                "Which raw materials (e.g. crude oil, jet fuel, natural gas, petrochemicals, and metals) are experiencing price volatility?",
                "Are fluctuations driven by global demand supply imbalances, geopolitical events, or market demand?",
                "Have OPEC policies, trade decisions, or sanctions contributed to recent price shifts?",
                "How does change in raw material prices could affect the company's production or operational costs?",
                "Are there disruptions in sourcing or delivery of raw materials due to price volatility?"
            ],
            "summary_instruction": "Create a paragraph describing how raw material price fluctuations are affecting the company. Specify which raw materials are volatile (e.g., crude oil, metals, chemicals) and what is driving these changes—such as global supply-demand imbalances, geopolitical tensions, OPEC policies, or sanctions. Explain the consequences of these price shifts on production costs, sourcing challenges, or delivery disruptions. Avoid competitor comparisons or contradictory opportunity points; focus solely on cost and supply-related threats."
        },
        "Cybersecurity issues & data breaches": {
            "questions": [
                "What products and services of the company were vulnerable to data breaches?",
                "When did the data breaches occurred (date, month, year) and how long did it go unnoticed?",
                "What happened in the data breaches and who discovered the breach (internal teams, third party, external whistleblowers)?",
                "Was there a delay in reporting or disclosing the breach to stakeholders or regulators?",
                "Did the breach violate data protection law (GDPR, CCPA, HIPAA)?",
                "What are the notification obligations to affected parties and regulators?",
                "What type of data was compromised (personal, customer, employee, financial, health, etc)?",
                "How many individual's records or data compromised?",
                "Was the breach limited to a specific system or widespread across the multiple platforms?"
            ],
            "summary_instruction": "Write a paragraph analyzing any cybersecurity vulnerabilities or data breaches the company has faced. Identify the affected systems or services, the date and duration of any breach, and how it was discovered. Explain the nature and scope of compromised data (e.g., personal, financial, customer) and whether the incident violated data protection regulations (e.g., GDPR, HIPAA). Include disclosure timelines, legal obligations, and any reputational or customer trust impacts. Exclude resolved breaches, outdated settlements, or unrelated industry data."
        },
        "Wages": {
            "questions": [
                "Have there been recent changes to federal, state and local minimum wage laws affecting the company?",
                "Is the company complying with living wage initiatives?",
                "What is the minimum industry specific wage set by the government?",
                "Are wages aligned with inflation, cost of living, and market benchmark?",
                "Which states are having how much amount of minimum wage?How might credit rating downgrades affect their access to capital?"
            ],
            "summary_instruction": "Generate a paragraph detailing how wage inflation or new wage laws are affecting the company. Mention any changes in federal, state, or regional minimum wage laws that apply to the company and whether it aligns with living wage standards. Assess how wages compare to inflation and cost-of-living benchmarks, and if wage-related cost pressures are impacting operations or profitability. Avoid contradictory narratives about industry growth; focus purely on wage-related threats."
        },
        "Natural calamities": {
            "questions": [
                "Has the company’s supply chain, manufacturing, or logistics been impacted by recent natural disasters (e.g., floods, wildfires, earthquakes)?",
                "What are the company’s products and services that are vulnerable to natural hazards?",
                "Did the company report any operational disruptions or facility closures due to a natural calamity?",
                "Are the company’s key operations or data centres located in high-risk zones for natural disasters?",
                "Is the company facing higher insurance costs or claims related to recent catastrophes?"
            ],
            "summary_instruction": "Write a paragraph evaluating the company’s exposure to natural disasters and the resulting risks. Specify if recent events like floods, earthquakes, or wildfires have caused supply chain disruptions, facility closures, or product delays. Identify any operations located in high-risk zones and discuss insurance cost implications. Exclude any information that indicates strong disaster preparedness or resilience, and do not cite infrastructure drills or mitigation efforts that would reduce the threat."
        },
        "Dependence on third-party supplier": {
            "questions": [
                "Has the company reported any delays or disruptions in its supply chain due to third-party vendor issues?",
                "Are there any quality control concerns linked to the company's third-party suppliers?",
                "Has the company experienced increased costs due to supplier pricing changes or contract renegotiations?",
                "Is the company overly dependent on a single or limited number of suppliers?",
                "Is the company exposed to geopolitical risks due to supplier locations (e.g., China, Ukraine, etc.)?"
            ],
            "summary_instruction": "Create a paragraph describing how dependence on third-party suppliers exposes the company to risk. Identify if there have been delays, quality control issues, or pricing changes due to supplier problems. Note if the company relies heavily on a single supplier or on suppliers based in geopolitically sensitive regions (e.g., China, Russia, Ukraine). Assess the potential cost, operational, or reputational consequences of such dependencies. Avoid contradictory industry growth commentary and exclude legal cases unless they directly tie into supplier reliability."
        }
    },
    "General": {
        "General": {
            "questions": [
                "What are the company’s top differentiators and core competencies?",
                "Identify best-performing products/services by growth, margin, and satisfaction.",
                "Evaluate the performance of current products or services to identify those with declining sales, relevance, or market demand.",
                "Examine financial records to identify weaknesses such as poor cost control, declining margins, or limited cash flow.",
                "Identify top 5 emerging trends with highest growth potential.",
                "Identify underserved customer segments with detailed demographics.",
                "Analyze competitive pressures and new entrant risks.",
                "Evaluate impact of changing regulations and tax policies."
            ],
            "summary_instruction": "Write a comprehensive paragraph analyzing the company’s strategic position, product and financial performance, market opportunities, and external threats. Begin by identifying the company’s core differentiators and key competitive strengths that set it apart in the market. Highlight the best-performing products or services based on growth, margins, and customer satisfaction metrics. Contrast this by evaluating any underperforming offerings that show signs of declining sales or relevance. Examine financial data to uncover operational weaknesses, including cost inefficiencies, shrinking margins, or limited cash flow. Then, identify five emerging trends with the highest projected growth potential and assess how the company is positioned to capitalize on them. Explore underserved customer segments with clear demographic insights and quantify their market potential. Analyze current competitive pressures, including risks posed by new entrants or disruptive rivals. Finally, evaluate the impact of changing regulations or tax policies on the company’s operations and profitability. The analysis should weave together insights from each question, avoid bullet-pointed responses, and maintain a cohesive narrative structure."
        }
    }
}
