"""
NHP Phase 3 — Per-Company Deep Dive Data
Expanded manufacturer profiles with technical, operational, and strategic data.
"""
from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class DeviceModel:
    """Individual phone model data."""
    name: str
    year: int
    gpu_name: str
    tops: float
    ram_gb: int
    units_sold_millions: float


@dataclass
class AIService:
    """Manufacturer's existing AI service."""
    name: str
    description: str
    description_ar: str
    daily_requests_estimate: int
    current_cloud_provider: str
    estimated_annual_cloud_cost: float


@dataclass
class SecurityFramework:
    """Manufacturer's security infrastructure."""
    tee_name: str
    tee_description: str
    tee_maturity: str  # Mature / Developing / Unknown
    certifications: List[str]
    api_openness: str  # Open / Restricted / Closed


@dataclass
class CompanyProfile:
    """Full company deep-dive profile."""
    name: str
    name_ar: str
    ticker: str
    hq_country: str
    hq_country_ar: str
    founded: int
    ceo: str
    market_cap_billions: float
    annual_revenue_billions: float
    smartphone_market_share_pct: float
    total_active_devices_millions: int
    annual_phone_sales_millions: int

    # Technical
    primary_chipset: str
    secondary_chipset: str
    os_name: str
    security: SecurityFramework
    flagship_models: List[DeviceModel] = field(default_factory=list)
    midrange_models: List[DeviceModel] = field(default_factory=list)

    # AI
    ai_services: List[AIService] = field(default_factory=list)
    ai_strategy: str = ""
    ai_strategy_ar: str = ""

    # Business
    primary_markets: List[str] = field(default_factory=list)
    primary_markets_ar: List[str] = field(default_factory=list)
    partnership_likelihood: str = ""  # High / Medium / Low
    partnership_reason: str = ""
    partnership_reason_ar: str = ""
    competitive_advantage: str = ""
    competitive_advantage_ar: str = ""

    # Integration
    integration_difficulty: str = ""  # Easy / Moderate / Hard
    integration_notes: str = ""
    integration_notes_ar: str = ""
    estimated_integration_months: int = 0
    estimated_integration_cost_millions: float = 0


# ═══════════════════════════════════════════════════════════════════════════
# COMPANY PROFILES
# ═══════════════════════════════════════════════════════════════════════════

COMPANY_PROFILES: Dict[str, CompanyProfile] = {

    # ──────────────────────────── SAMSUNG ────────────────────────────
    "samsung": CompanyProfile(
        name="Samsung Electronics", name_ar="سامسونج إلكترونيكس",
        ticker="005930.KS", hq_country="South Korea", hq_country_ar="كوريا الجنوبية",
        founded=1969, ceo="Jong-Hee Han",
        market_cap_billions=350, annual_revenue_billions=210,
        smartphone_market_share_pct=19.4,
        total_active_devices_millions=300,
        annual_phone_sales_millions=225,
        primary_chipset="Exynos 2400 / Snapdragon 8 Gen 3",
        secondary_chipset="Exynos 1480 / Snapdragon 6 Gen 1",
        os_name="One UI (Android)",
        security=SecurityFramework(
            tee_name="Samsung Knox",
            tee_description="Military-grade hardware-backed security platform. Approved by 60+ governments and defense agencies worldwide. Hardware root of trust from chip fabrication.",
            tee_maturity="Mature",
            certifications=["CC EAL4+", "FIPS 140-2", "DISA STIG", "CSfC"],
            api_openness="Restricted",
        ),
        flagship_models=[
            DeviceModel("Galaxy S24 Ultra", 2024, "Snapdragon 8 Gen 3", 34.0, 12, 10),
            DeviceModel("Galaxy S24+", 2024, "Exynos 2400", 34.0, 12, 8),
            DeviceModel("Galaxy S24", 2024, "Exynos 2400", 34.0, 8, 15),
            DeviceModel("Galaxy S23 Ultra", 2023, "Snapdragon 8 Gen 2", 26.0, 12, 12),
            DeviceModel("Galaxy Z Fold5", 2023, "Snapdragon 8 Gen 2", 26.0, 12, 5),
        ],
        midrange_models=[
            DeviceModel("Galaxy A55", 2024, "Exynos 1480", 12.0, 8, 30),
            DeviceModel("Galaxy A35", 2024, "Exynos 1380", 10.0, 6, 25),
            DeviceModel("Galaxy A15", 2024, "Helio G99", 5.0, 4, 40),
        ],
        ai_services=[
            AIService("Galaxy AI", "On-device and cloud AI for photo editing, translation, summarization, call transcription",
                     "ذكاء اصطناعي على الجهاز والسحابة لتحرير الصور والترجمة والتلخيص",
                     500_000_000, "Google Cloud", 500_000_000),
            AIService("Bixby", "Voice assistant and device control",
                     "مساعد صوتي وتحكم بالجهاز",
                     100_000_000, "Samsung Cloud / AWS", 100_000_000),
        ],
        ai_strategy="Samsung's Galaxy AI is central to their 2024-2026 strategy. They're investing heavily in on-device AI via Exynos NPUs and cloud AI via Google partnership. NHP could reduce their Google Cloud dependency.",
        ai_strategy_ar="Galaxy AI هو محور استراتيجية سامسونج 2024-2026. يستثمرون بكثافة في AI على الجهاز عبر Exynos NPU وفي السحابة عبر شراكة Google. NHP يمكن أن يقلل اعتمادهم على Google Cloud.",
        primary_markets=["South Korea", "USA", "EU", "India", "Brazil", "Southeast Asia"],
        primary_markets_ar=["كوريا الجنوبية", "الولايات المتحدة", "أوروبا", "الهند", "البرازيل", "جنوب شرق آسيا"],
        partnership_likelihood="High",
        partnership_reason="Samsung already has Knox TEE infrastructure, manufactures their own chips (Exynos), and is actively seeking AI cost reduction. They also have a history of adopting innovative features to compete with Apple.",
        partnership_reason_ar="سامسونج تملك بنية Knox التحتية، تصنّع شرائحها (Exynos)، وتبحث فعلاً عن تقليل تكاليف AI. لديها تاريخ في تبني ميزات مبتكرة للتنافس مع Apple.",
        competitive_advantage="'Your Galaxy earns money while you sleep' — a marketing message no competitor can match. Reduces Google Cloud costs. Positions Samsung as leader in distributed AI.",
        competitive_advantage_ar="'جالاكسيك يكسب المال وأنت نايم' — رسالة تسويقية لا يستطيع أي منافس مجاراتها. يقلل تكاليف Google Cloud. يضع سامسونج كرائد في AI الموزع.",
        integration_difficulty="Moderate",
        integration_notes="Knox already provides TEE. Key challenge: opening Knox Vault API for NHP without compromising security guarantees. Samsung has internal SDK teams that can facilitate. Exynos NPU SDK exists but is not public.",
        integration_notes_ar="Knox يوفر TEE جاهزة. التحدي: فتح Knox Vault API لـ NHP دون المساس بالأمان. سامسونج لديها فرق SDK داخلية يمكنها المساعدة. Exynos NPU SDK موجود لكن غير عام.",
        estimated_integration_months=12,
        estimated_integration_cost_millions=30,
    ),

    # ──────────────────────────── APPLE ──────────────────────────────
    "apple": CompanyProfile(
        name="Apple Inc.", name_ar="أبل",
        ticker="AAPL", hq_country="USA", hq_country_ar="الولايات المتحدة",
        founded=1976, ceo="Tim Cook",
        market_cap_billions=3400, annual_revenue_billions=383,
        smartphone_market_share_pct=20.1,
        total_active_devices_millions=1500,
        annual_phone_sales_millions=230,
        primary_chipset="Apple A17 Pro / A18 Pro",
        secondary_chipset="Apple A16 / A15",
        os_name="iOS",
        security=SecurityFramework(
            tee_name="Secure Enclave",
            tee_description="Hardware-isolated coprocessor with encrypted memory, dedicated AES engine, and hardware random number generator. Each Secure Enclave has unique ID not known to Apple.",
            tee_maturity="Mature",
            certifications=["FIPS 140-3", "ISO 27001", "SOC 2 Type II"],
            api_openness="Closed",
        ),
        flagship_models=[
            DeviceModel("iPhone 15 Pro Max", 2023, "A17 Pro", 35.0, 8, 25),
            DeviceModel("iPhone 15 Pro", 2023, "A17 Pro", 35.0, 8, 30),
            DeviceModel("iPhone 15", 2023, "A16", 17.0, 6, 45),
            DeviceModel("iPhone 14 Pro", 2022, "A16", 17.0, 6, 20),
        ],
        midrange_models=[
            DeviceModel("iPhone SE (2022)", 2022, "A15", 15.0, 4, 20),
            DeviceModel("iPhone 14", 2022, "A15", 15.0, 6, 35),
            DeviceModel("iPhone 13", 2021, "A15", 15.0, 4, 30),
        ],
        ai_services=[
            AIService("Apple Intelligence", "System-wide AI: writing tools, image generation, smart summaries, Siri upgrade",
                     "ذكاء اصطناعي شامل: أدوات كتابة، توليد صور، تلخيصات ذكية، ترقية Siri",
                     800_000_000, "Apple Cloud (Private Cloud Compute)", 2_000_000_000),
            AIService("Siri", "Voice assistant with on-device and cloud components",
                     "مساعد صوتي بمكونات على الجهاز وسحابية",
                     300_000_000, "Apple Cloud", 500_000_000),
        ],
        ai_strategy="Apple Intelligence launched in 2024 using Private Cloud Compute — custom Apple Silicon servers. Apple prioritizes privacy above all. NHP aligns with their privacy-first philosophy but Apple rarely opens its ecosystem to third parties.",
        ai_strategy_ar="Apple Intelligence أُطلق في 2024 باستخدام Private Cloud Compute. Apple تعطي الأولوية للخصوصية. NHP يتوافق مع فلسفتهم لكن Apple نادراً ما تفتح نظامها لأطراف خارجية.",
        primary_markets=["USA", "EU", "Japan", "China", "South Korea"],
        primary_markets_ar=["الولايات المتحدة", "أوروبا", "اليابان", "الصين", "كوريا الجنوبية"],
        partnership_likelihood="Low",
        partnership_reason="Apple has the strongest TEE (Secure Enclave) and largest fleet, but their closed ecosystem makes third-party integration very unlikely. They prefer building everything in-house. However, they could build their own NHP-like system.",
        partnership_reason_ar="Apple تملك أقوى TEE وأكبر أسطول، لكن نظامها المغلق يجعل التكامل مع أطراف خارجية صعباً. يفضلون بناء كل شيء داخلياً. لكن يمكنهم بناء نظام شبيه بـ NHP بأنفسهم.",
        competitive_advantage="Massive installed base of 1.5B devices with powerful Apple Silicon. Privacy-first brand alignment. Premium user demo willing to participate for rewards.",
        competitive_advantage_ar="قاعدة ضخمة 1.5 مليار جهاز مع Apple Silicon قوي. توافق مع علامة تجارية تركز على الخصوصية.",
        integration_difficulty="Hard",
        integration_notes="Secure Enclave API is extremely restricted. App Store review would block direct GPU access. Would require deep OS-level integration that Apple controls entirely. Realistically, Apple would build this internally, not partner.",
        integration_notes_ar="Secure Enclave API مقيد جداً. مراجعة App Store ستمنع الوصول المباشر لـ GPU. يتطلب تكاملاً عميقاً على مستوى نظام التشغيل. واقعياً، Apple ستبني هذا داخلياً.",
        estimated_integration_months=24,
        estimated_integration_cost_millions=50,
    ),

    # ──────────────────────────── XIAOMI ─────────────────────────────
    "xiaomi": CompanyProfile(
        name="Xiaomi Corporation", name_ar="شاومي",
        ticker="1810.HK", hq_country="China", hq_country_ar="الصين",
        founded=2010, ceo="Lei Jun",
        market_cap_billions=110, annual_revenue_billions=37,
        smartphone_market_share_pct=12.5,
        total_active_devices_millions=600,
        annual_phone_sales_millions=150,
        primary_chipset="Snapdragon 8 Gen 3",
        secondary_chipset="Dimensity 7200 / Snapdragon 6 Gen 1",
        os_name="HyperOS (Android)",
        security=SecurityFramework(
            tee_name="Qualcomm TEE / Xiaomi Security",
            tee_description="Relies on Qualcomm's QTEE for Snapdragon devices and MediaTek TEE for Dimensity. Xiaomi adds its own security layer via HyperOS.",
            tee_maturity="Developing",
            certifications=["CC EAL2", "China CCRA"],
            api_openness="Open",
        ),
        flagship_models=[
            DeviceModel("Xiaomi 14 Ultra", 2024, "Snapdragon 8 Gen 3", 34.0, 16, 3),
            DeviceModel("Xiaomi 14 Pro", 2024, "Snapdragon 8 Gen 3", 34.0, 12, 5),
            DeviceModel("Xiaomi 14", 2024, "Snapdragon 8 Gen 3", 34.0, 12, 10),
        ],
        midrange_models=[
            DeviceModel("Redmi Note 13 Pro+", 2024, "Dimensity 7200", 10.0, 8, 30),
            DeviceModel("Redmi Note 13", 2024, "Snapdragon 685", 5.0, 6, 50),
            DeviceModel("POCO X6 Pro", 2024, "Dimensity 8300", 12.0, 8, 15),
        ],
        ai_services=[
            AIService("HyperOS AI", "Smart home integration, camera AI, on-device assistant",
                     "تكامل المنزل الذكي، AI الكاميرا، مساعد على الجهاز",
                     300_000_000, "Alibaba Cloud / Tencent Cloud", 200_000_000),
        ],
        ai_strategy="Xiaomi is aggressively expanding AI across HyperOS and its IoT ecosystem. They have 600M+ connected devices. Their open-source philosophy and hunger for differentiation make them an ideal NHP partner.",
        ai_strategy_ar="شاومي توسع AI بقوة عبر HyperOS ونظام IoT الخاص بها. لديها 600M+ جهاز متصل. فلسفتها المفتوحة وشغفها بالتمايز يجعلانها شريكاً مثالياً لـ NHP.",
        primary_markets=["China", "India", "Southeast Asia", "EU", "Latin America"],
        primary_markets_ar=["الصين", "الهند", "جنوب شرق آسيا", "أوروبا", "أمريكا اللاتينية"],
        partnership_likelihood="High",
        partnership_reason="Xiaomi has the most open ecosystem among major manufacturers. They actively seek innovative features to compete with Samsung/Apple. Their massive presence in emerging markets (India, SEA) where $42/month passive income is life-changing makes NHP extremely attractive.",
        partnership_reason_ar="شاومي لديها النظام الأكثر انفتاحاً. تبحث بنشاط عن ميزات مبتكرة للتنافس. تواجدها الضخم في الأسواق الناشئة حيث $42/شهر يغير حياة المستخدم يجعل NHP جذاباً للغاية.",
        competitive_advantage="Massive emerging market presence where passive income matters most. Open ecosystem enables faster integration. 600M+ IoT devices could extend NHP beyond phones.",
        competitive_advantage_ar="تواجد ضخم في الأسواق الناشئة حيث الدخل السلبي أكثر أهمية. النظام المفتوح يسرع التكامل. 600M+ جهاز IoT يمكن أن يوسع NHP.",
        integration_difficulty="Easy",
        integration_notes="Qualcomm TEE is well-documented. HyperOS is Android-based with more developer freedom than Samsung/Apple. Xiaomi's developer community is active and supportive. Could integrate in 6-8 months.",
        integration_notes_ar="Qualcomm TEE موثق جيداً. HyperOS مبني على Android مع حرية أكبر للمطورين. مجتمع مطوري شاومي نشط وداعم. يمكن التكامل في 6-8 أشهر.",
        estimated_integration_months=8,
        estimated_integration_cost_millions=15,
    ),

    # ──────────────────────────── GOOGLE ─────────────────────────────
    "google": CompanyProfile(
        name="Google (Pixel)", name_ar="جوجل (بيكسل)",
        ticker="GOOGL", hq_country="USA", hq_country_ar="الولايات المتحدة",
        founded=1998, ceo="Sundar Pichai",
        market_cap_billions=2100, annual_revenue_billions=307,
        smartphone_market_share_pct=2.0,
        total_active_devices_millions=40,
        annual_phone_sales_millions=10,
        primary_chipset="Google Tensor G3",
        secondary_chipset="Google Tensor G2",
        os_name="Android (Stock)",
        security=SecurityFramework(
            tee_name="Titan M2 + Android TEE",
            tee_description="Custom Titan M2 security chip with Arm TrustZone-based TEE. Google controls the full stack from silicon to OS.",
            tee_maturity="Mature",
            certifications=["FIPS 140-2", "Common Criteria"],
            api_openness="Restricted",
        ),
        flagship_models=[
            DeviceModel("Pixel 8 Pro", 2023, "Tensor G3", 29.0, 12, 4),
            DeviceModel("Pixel 8", 2023, "Tensor G3", 29.0, 8, 5),
            DeviceModel("Pixel 7 Pro", 2022, "Tensor G2", 20.0, 12, 3),
        ],
        midrange_models=[
            DeviceModel("Pixel 7a", 2023, "Tensor G2", 20.0, 8, 5),
            DeviceModel("Pixel 6a", 2022, "Tensor G1", 15.0, 6, 4),
        ],
        ai_services=[
            AIService("Gemini Nano", "On-device LLM for smart replies, summarization, and contextual awareness",
                     "نموذج لغوي على الجهاز للردود الذكية والتلخيص",
                     100_000_000, "Google Cloud", 1_000_000_000),
        ],
        ai_strategy="Google leads AI globally but has a small phone market share. Tensor chips are designed specifically for on-device AI. Unlikely to partner for NHP since they own the largest cloud (GCP) — NHP would cannibalize their revenue.",
        ai_strategy_ar="جوجل تقود AI عالمياً لكن حصتها بالهواتف صغيرة. شرائح Tensor مصممة خصيصاً لـ AI. من غير المرجح الشراكة لأنهم يملكون أكبر سحابة (GCP) — NHP يأكل من إيراداتهم.",
        primary_markets=["USA", "EU", "Japan"],
        primary_markets_ar=["الولايات المتحدة", "أوروبا", "اليابان"],
        partnership_likelihood="Low",
        partnership_reason="Google profits from cloud computing. NHP directly threatens GCP revenue. Small phone fleet reduces impact. However, Google could adopt a similar federated approach for Android ecosystem broadly.",
        partnership_reason_ar="جوجل تربح من الحوسبة السحابية. NHP يهدد إيرادات GCP مباشرة. أسطول الهواتف صغير. لكن يمكنهم تبني نهج مشابه لنظام Android عموماً.",
        competitive_advantage="Full-stack control (silicon + OS + cloud). Leading AI research. But small fleet limits NHP value.",
        competitive_advantage_ar="تحكم كامل (شريحة + نظام + سحابة). بحث AI رائد. لكن الأسطول الصغير يحد من قيمة NHP.",
        integration_difficulty="Moderate",
        integration_notes="Tensor has documented NPU API. Android TEE is standard. But Google has no incentive — they ARE the cloud provider that NHP replaces.",
        integration_notes_ar="Tensor لديها NPU API موثق. Android TEE معياري. لكن جوجل ليس لديها حافز — هم مزود السحابة الذي يستبدله NHP.",
        estimated_integration_months=12,
        estimated_integration_cost_millions=20,
    ),

    # ──────────────────────────── HUAWEI ─────────────────────────────
    "huawei": CompanyProfile(
        name="Huawei Technologies", name_ar="هواوي",
        ticker="Private", hq_country="China", hq_country_ar="الصين",
        founded=1987, ceo="Ren Zhengfei (Founder)",
        market_cap_billions=0, annual_revenue_billions=99,
        smartphone_market_share_pct=5.0,
        total_active_devices_millions=250,
        annual_phone_sales_millions=60,
        primary_chipset="Kirin 9000s",
        secondary_chipset="Kirin 820 / Kirin 710",
        os_name="HarmonyOS",
        security=SecurityFramework(
            tee_name="iTrustee / Huawei TEE",
            tee_description="Huawei's proprietary TEE built into Kirin chipsets. Operates independently from Android ecosystem due to US sanctions.",
            tee_maturity="Mature",
            certifications=["CC EAL3+", "China CCRA", "CMMI Level 5"],
            api_openness="Restricted",
        ),
        flagship_models=[
            DeviceModel("Mate 60 Pro", 2023, "Kirin 9000s", 30.0, 12, 15),
            DeviceModel("P60 Pro", 2023, "Snapdragon 8+ Gen 1", 28.0, 8, 10),
        ],
        midrange_models=[
            DeviceModel("Nova 12", 2024, "Kirin 830", 10.0, 8, 15),
            DeviceModel("Enjoy 70", 2024, "Kirin 710A", 5.0, 4, 20),
        ],
        ai_services=[
            AIService("Celia AI / Pangu Model", "Huawei's own LLM and voice assistant for HarmonyOS",
                     "نموذج Pangu ومساعد Celia لنظام HarmonyOS",
                     200_000_000, "Huawei Cloud", 300_000_000),
        ],
        ai_strategy="Huawei is building a fully independent tech stack post-US sanctions: own chips (Kirin), own OS (HarmonyOS), own cloud. NHP fits perfectly as they need cost-efficient AI alternatives and can't rely on Google/AWS.",
        ai_strategy_ar="هواوي تبني حزمة تقنية مستقلة تماماً بعد العقوبات: شرائحها (Kirin)، نظامها (HarmonyOS)، سحابتها. NHP يناسبها لأنها تحتاج بدائل AI اقتصادية ولا تستطيع الاعتماد على Google/AWS.",
        primary_markets=["China", "Middle East", "Africa", "Southeast Asia"],
        primary_markets_ar=["الصين", "الشرق الأوسط", "أفريقيا", "جنوب شرق آسيا"],
        partnership_likelihood="High",
        partnership_reason="Post-sanctions, Huawei needs alternative computing sources. They have a captive market in China (600M+ HarmonyOS users target). They own the full stack (chips + OS + cloud) making integration possible. US sanctions make Western cloud options unavailable.",
        partnership_reason_ar="بعد العقوبات، هواوي تحتاج مصادر حوسبة بديلة. لديها سوق أسير في الصين. تملك كل الطبقات (شرائح + نظام + سحابة). العقوبات تمنعها من استخدام AWS/GCP.",
        competitive_advantage="Only major manufacturer completely independent from US tech stack. Massive presence in markets underserved by Western cloud providers. HarmonyOS gives full OS-level control.",
        competitive_advantage_ar="المصنّع الوحيد المستقل تماماً عن التقنيات الأمريكية. تواجد ضخم في أسواق لا تخدمها السحابات الغربية. HarmonyOS يعطي تحكم كامل.",
        integration_difficulty="Moderate",
        integration_notes="Full stack control enables deep integration. Kirin NPU SDK available internally. Challenge: US sanctions may complicate NHP's ability to partner if NHP has Western ties. Must structure partnership carefully.",
        integration_notes_ar="التحكم الكامل يتيح تكاملاً عميقاً. Kirin NPU SDK متاح داخلياً. التحدي: العقوبات قد تعقد الشراكة إذا كان لـ NHP روابط غربية.",
        estimated_integration_months=10,
        estimated_integration_cost_millions=20,
    ),

    # ──────────────────────────── OPPO ───────────────────────────────
    "oppo": CompanyProfile(
        name="OPPO (incl. OnePlus)", name_ar="أوبو (ومنها ون بلس)",
        ticker="Private (BBK)", hq_country="China", hq_country_ar="الصين",
        founded=2004, ceo="Tony Chen",
        market_cap_billions=0, annual_revenue_billions=15,
        smartphone_market_share_pct=8.5,
        total_active_devices_millions=300,
        annual_phone_sales_millions=100,
        primary_chipset="Snapdragon 8 Gen 3 / Dimensity 9300",
        secondary_chipset="Dimensity 8200 / Snapdragon 6 Gen 1",
        os_name="ColorOS (Android)",
        security=SecurityFramework(
            tee_name="Qualcomm QTEE / MediaTek TEE",
            tee_description="Uses standard Qualcomm and MediaTek TEE implementations. OPPO adds its own security layer via ColorOS.",
            tee_maturity="Developing",
            certifications=["CC EAL2"],
            api_openness="Open",
        ),
        flagship_models=[
            DeviceModel("Find X7 Ultra", 2024, "Dimensity 9300", 35.0, 16, 2),
            DeviceModel("OnePlus 12", 2024, "Snapdragon 8 Gen 3", 34.0, 12, 5),
        ],
        midrange_models=[
            DeviceModel("OPPO A79", 2024, "Dimensity 6020", 8.0, 8, 20),
            DeviceModel("OnePlus Nord CE 4", 2024, "Snapdragon 695", 6.0, 8, 10),
            DeviceModel("OPPO A18", 2024, "Helio G85", 4.0, 4, 30),
        ],
        ai_services=[
            AIService("ColorOS AI", "Camera AI, smart assistant, translation",
                     "AI الكاميرا، مساعد ذكي، ترجمة",
                     150_000_000, "Alibaba Cloud", 100_000_000),
        ],
        ai_strategy="OPPO is part of BBK Electronics (also Vivo, Realme). Combined fleet of 800M+. They focus on camera AI and emerging market features. Partnership with OPPO could cascade to the entire BBK group.",
        ai_strategy_ar="أوبو جزء من BBK Electronics (أيضاً Vivo, Realme). الأسطول المشترك 800M+. يركزون على AI الكاميرا. الشراكة مع أوبو قد تمتد لمجموعة BBK بالكامل.",
        primary_markets=["China", "India", "Southeast Asia", "Middle East"],
        primary_markets_ar=["الصين", "الهند", "جنوب شرق آسيا", "الشرق الأوسط"],
        partnership_likelihood="Medium",
        partnership_reason="Part of BBK group — one deal could unlock OPPO + Vivo + Realme (800M+ devices). Open Android-based OS. Strong emerging market presence. Less brand recognition means they need differentiators like NHP.",
        partnership_reason_ar="جزء من مجموعة BBK — صفقة واحدة تفتح أوبو + فيفو + ريلمي (800M+ جهاز). نظام مفتوح. تواجد قوي بالأسواق الناشئة.",
        competitive_advantage="Gateway to BBK group (800M+ devices). Strong in India and SEA where passive income is most impactful.",
        competitive_advantage_ar="بوابة لمجموعة BBK (800M+ جهاز). قوية في الهند وجنوب شرق آسيا حيث الدخل السلبي أكثر تأثيراً.",
        integration_difficulty="Easy",
        integration_notes="Standard Qualcomm/MediaTek TEE. Android-based ColorOS is open to deep integration. Active developer relations team. BBK backstop provides resources.",
        integration_notes_ar="TEE معياري من Qualcomm/MediaTek. ColorOS مبني على Android ومفتوح للتكامل العميق. فريق علاقات مطورين نشط.",
        estimated_integration_months=8,
        estimated_integration_cost_millions=12,
    ),

    # ──────────────────────────── VIVO ───────────────────────────────
    "vivo": CompanyProfile(
        name="Vivo (incl. iQOO)", name_ar="فيفو (ومنها iQOO)",
        ticker="Private (BBK)", hq_country="China", hq_country_ar="الصين",
        founded=2009, ceo="Shen Wei",
        market_cap_billions=0, annual_revenue_billions=13,
        smartphone_market_share_pct=7.5,
        total_active_devices_millions=250,
        annual_phone_sales_millions=90,
        primary_chipset="Snapdragon 8 Gen 3 / Dimensity 9200+",
        secondary_chipset="Dimensity 7200 / Snapdragon 6 Gen 1",
        os_name="OriginOS / Funtouch OS (Android)",
        security=SecurityFramework(
            tee_name="Qualcomm QTEE / MediaTek TEE",
            tee_description="Standard chipset TEE with Vivo's OriginOS security additions.",
            tee_maturity="Developing",
            certifications=["CC EAL2"],
            api_openness="Open",
        ),
        flagship_models=[
            DeviceModel("Vivo X100 Pro", 2024, "Dimensity 9300", 35.0, 16, 3),
            DeviceModel("iQOO 12", 2024, "Snapdragon 8 Gen 3", 34.0, 12, 4),
        ],
        midrange_models=[
            DeviceModel("Vivo Y200", 2024, "Snapdragon 4 Gen 2", 6.0, 8, 20),
            DeviceModel("Vivo T3", 2024, "Dimensity 7200", 10.0, 8, 15),
        ],
        ai_services=[
            AIService("OriginOS AI", "Camera AI, system optimization, smart features",
                     "AI الكاميرا، تحسين النظام، ميزات ذكية",
                     120_000_000, "Tencent Cloud / Huawei Cloud", 80_000_000),
        ],
        ai_strategy="Vivo focuses on camera excellence and mid-range domination in India. Part of BBK group. An NHP partnership with Vivo opens the door to the Indian sub-continent's massive smartphone base.",
        ai_strategy_ar="فيفو تركز على تفوق الكاميرا والهيمنة على الفئة المتوسطة في الهند. جزء من مجموعة BBK. شراكة مع فيفو تفتح سوق الهند الضخم.",
        primary_markets=["China", "India", "Southeast Asia", "Middle East"],
        primary_markets_ar=["الصين", "الهند", "جنوب شرق آسيا", "الشرق الأوسط"],
        partnership_likelihood="Medium",
        partnership_reason="Same BBK group as OPPO. Strong India presence. Needs differentiation in a crowded market. NHP passive income feature is powerful in price-sensitive markets.",
        partnership_reason_ar="نفس مجموعة BBK مع أوبو. تواجد قوي بالهند. تحتاج تمايز في سوق مزدحم. ميزة الدخل السلبي قوية في الأسواق الحساسة للسعر.",
        competitive_advantage="BBK group access. #1 in India by volume some quarters. Price-sensitive markets where passive income matters most.",
        competitive_advantage_ar="وصول لمجموعة BBK. الأولى بالهند في بعض الأرباع. أسواق حساسة للسعر حيث الدخل السلبي هو الأهم.",
        integration_difficulty="Easy",
        integration_notes="Identical technical stack to OPPO (same parent company). Integration done for one BBK brand directly transfers to others.",
        integration_notes_ar="حزمة تقنية مطابقة لأوبو (نفس الشركة الأم). التكامل لعلامة BBK واحدة ينتقل مباشرة للبقية.",
        estimated_integration_months=8,
        estimated_integration_cost_millions=12,
    ),
}
