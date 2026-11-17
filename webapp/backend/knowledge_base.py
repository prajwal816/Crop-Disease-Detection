"""
Advisory knowledge base for the Main19 crop disease classifier.
Derived from notebook 11: rag_multilingual_advisory.ipynb

Coverage: 19 classes × 3 languages (en, hi, te) × 5 sections.
Languages: en = English, hi = Hindi, te = Telugu
Sections: symptoms, monitoring, immediate_actions, prevention, escalation
"""

ADVISORY_KB: dict[str, dict[str, dict[str, str]]] = {

    "bell_pepper__bacterial_spot": {
        "en": {
            "symptoms": "Small water-soaked or dark spots may develop on leaves. Spots can enlarge, become angular, and may lead to yellowing or leaf drop under wet conditions.",
            "monitoring": "Check new leaves and nearby plants for spreading spots. Record whether symptoms increase after rain, overhead irrigation, or handling plants while foliage is wet.",
            "immediate_actions": "Avoid working in the crop when foliage is wet. Remove severely affected plant material when practical. Improve airflow and reduce prolonged leaf wetness.",
            "prevention": "Use clean planting material, sanitize tools, rotate away from susceptible hosts where feasible, and avoid overhead irrigation when alternatives are available.",
            "escalation": "Seek local extension or plant-health advice if symptoms spread rapidly, occur in seedlings, or affect a large proportion of plants.",
        },
        "hi": {
            "symptoms": "पत्तियों पर छोटे पानी-भिगे या काले धब्बे दिख सकते हैं। नमी की स्थिति में धब्बे बढ़कर कोणीय हो सकते हैं और पत्तियाँ पीली होकर गिर सकती हैं।",
            "monitoring": "नई पत्तियों और आसपास के पौधों पर फैलते धब्बों की जाँच करें। बारिश या सिंचाई के बाद लक्षणों की स्थिति दर्ज करें।",
            "immediate_actions": "जब पत्तियाँ गीली हों तब फसल में काम न करें। गंभीर रूप से प्रभावित पौधे सामग्री हटाएँ। वायु प्रवाह सुधारें और लंबे समय तक पत्तियों की नमी कम करें।",
            "prevention": "स्वच्छ रोपण सामग्री का उपयोग करें, उपकरण स्वच्छ रखें, फसल चक्र अपनाएँ, और ऊपर से सिंचाई से बचें।",
            "escalation": "यदि लक्षण तेजी से फैलें, पौधशाला में हों, या बड़ी संख्या में पौधे प्रभावित हों तो स्थानीय कृषि विशेषज्ञ से सलाह लें।",
        },
        "te": {
            "symptoms": "ఆకులపై చిన్న నీటిలో తడిసిన లేదా చీకటి మచ్చలు కనిపించవచ్చు. తేమ పరిస్థితుల్లో మచ్చలు పెద్దవై కోణీయంగా మారవచ్చు.",
            "monitoring": "కొత్త ఆకులు మరియు సమీపంలోని మొక్కలపై వ్యాపిస్తున్న మచ్చలను తనిఖీ చేయండి. వర్షం లేదా నీటి తడి తర్వాత లక్షణాలు పెరుగుతున్నాయో లేదో గమనించండి.",
            "immediate_actions": "ఆకులు తడిగా ఉన్నప్పుడు పంటలో పని చేయకండి. తీవ్రంగా ప్రభావితమైన మొక్కల భాగాలను తొలగించండి. గాలి ప్రసరణ మెరుగుపరచండి.",
            "prevention": "శుభ్రమైన నాటు సామగ్రిని ఉపయోగించండి, పరికరాలను శుభ్రంగా ఉంచండి, పంట మార్పిడి చేయండి, పై నుండి నీటిపారుదల మానండి.",
            "escalation": "లక్షణాలు వేగంగా వ్యాపిస్తే, మొలకలలో కనిపిస్తే లేదా అనేక మొక్కలు ప్రభావితమైతే స్థానిక వ్యవసాయ నిపుణుల సహాయం తీసుకోండి.",
        },
    },

    "bell_pepper__healthy": {
        "en": {
            "symptoms": "No disease signs detected. Leaves appear uniformly green with no spots, lesions, or discolouration. A single image cannot rule out very early disease.",
            "monitoring": "Inspect both upper and lower leaf surfaces and observe several plants across the field or garden weekly.",
            "immediate_actions": "Continue regular monitoring and maintain good field hygiene.",
            "prevention": "Use clean tools, avoid unnecessary handling of wet plants, and maintain appropriate irrigation, spacing, nutrition, and weed management.",
            "escalation": "Request expert support if new spots, yellowing, wilting, or rapid decline appear.",
        },
        "hi": {
            "symptoms": "कोई रोग संकेत नहीं मिला। पत्तियाँ समान रूप से हरी दिख रही हैं। एक ही तस्वीर से बहुत प्रारंभिक रोग को नकारा नहीं जा सकता।",
            "monitoring": "प्रत्येक सप्ताह पत्ती की ऊपरी और निचली सतह की जाँच करें और कई पौधों का निरीक्षण करें।",
            "immediate_actions": "नियमित निगरानी जारी रखें और खेत की स्वच्छता बनाए रखें।",
            "prevention": "स्वच्छ उपकरणों का उपयोग करें, उचित सिंचाई, पोषण और खरपतवार प्रबंधन बनाए रखें।",
            "escalation": "यदि नए धब्बे, पीलापन, मुरझाना, या तेजी से गिरावट आए तो विशेषज्ञ सहायता लें।",
        },
        "te": {
            "symptoms": "వ్యాధి లక్షణాలు కనుగొనబడలేదు. ఆకులు సమానంగా ఆకుపచ్చగా కనిపిస్తున్నాయి. ఒకే చిత్రం ద్వారా చాలా ప్రారంభ వ్యాధిని తోసిపుచ్చలేము.",
            "monitoring": "వారంవారీ ఆకు యొక్క పై మరియు కింది భాగాలను తనిఖీ చేయండి.",
            "immediate_actions": "నిర్బంధ పర్యవేక్షణ కొనసాగించండి మరియు మంచి పొలం పరిశుభ్రత నిర్వహించండి.",
            "prevention": "శుభ్రమైన పరికరాలను ఉపయోగించండి, సరైన నీటిపారుదల, పోషణ మరియు కలుపు నిర్వహణ నిర్వహించండి.",
            "escalation": "కొత్త మచ్చలు, పసుపు రంగు, వాడిపోవడం లేదా వేగంగా క్షీణత కనిపిస్తే నిపుణుల సహాయం తీసుకోండి.",
        },
    },

    "corn__cercospora_leaf_spot_gray_leaf_spot": {
        "en": {
            "symptoms": "Lesions are often rectangular or elongated and may appear gray to tan, expanding along leaf veins and reducing green leaf area.",
            "monitoring": "Inspect lower and middle leaves first, then assess whether lesions are spreading upward. Note recent humidity, rainfall, residue, and crop history.",
            "immediate_actions": "Mark affected areas and monitor disease progression. Avoid moving potentially contaminated crop residue or tools between fields.",
            "prevention": "Use locally suitable resistant hybrids where available, rotate crops, and manage infected residue according to local agronomic guidance.",
            "escalation": "Consult local extension personnel if lesions are widespread before key growth stages or if disease pressure is increasing quickly.",
        },
        "hi": {
            "symptoms": "घाव अक्सर आयताकार या लंबे होते हैं और धूसर से तन रंग के दिख सकते हैं, पत्ती की शिराओं के साथ फैलते हैं।",
            "monitoring": "पहले निचली और मध्य पत्तियों का निरीक्षण करें। हाल की नमी, वर्षा और फसल इतिहास नोट करें।",
            "immediate_actions": "प्रभावित क्षेत्रों को चिह्नित करें और रोग की प्रगति पर नजर रखें। दूषित फसल अवशेष या उपकरणों को खेतों के बीच न ले जाएँ।",
            "prevention": "स्थानीय रूप से उपयुक्त प्रतिरोधी संकर किस्मों का उपयोग करें, फसल चक्र अपनाएँ।",
            "escalation": "यदि मुख्य विकास चरणों से पहले घाव व्यापक हों या रोग का दबाव तेजी से बढ़ रहा हो तो स्थानीय विशेषज्ञ से परामर्श लें।",
        },
        "te": {
            "symptoms": "గాయాలు తరచుగా దీర్ఘచతురస్రాకారంగా లేదా పొడవుగా ఉంటాయి మరియు బూడిద నుండి టాన్ రంగులో కనిపిస్తాయి.",
            "monitoring": "మొదట దిగువ మరియు మధ్యస్థ ఆకులను తనిఖీ చేయండి. గాయాలు పైకి వ్యాపిస్తున్నాయో లేదో అంచనా వేయండి.",
            "immediate_actions": "ప్రభావిత ప్రాంతాలను గుర్తించండి మరియు వ్యాధి అభివృద్ధిని పర్యవేక్షించండి.",
            "prevention": "స్థానికంగా అనుకూలమైన నిరోధక సంకరజాతులను ఉపయోగించండి, పంట మార్పిడి చేయండి.",
            "escalation": "లక్షణాలు విస్తృతంగా ఉంటే స్థానిక వ్యవసాయ నిపుణులను సంప్రదించండి.",
        },
    },

    "corn__common_rust": {
        "en": {
            "symptoms": "Small reddish-brown or orange pustules may occur on either leaf surface. Severe infections can cause extensive leaf yellowing or drying.",
            "monitoring": "Check multiple plants and both leaf surfaces. Track whether pustules are increasing and whether symptoms are concentrated in humid areas.",
            "immediate_actions": "Monitor spread and maintain field records. Avoid unnecessary movement through wet foliage.",
            "prevention": "Use resistant hybrids when locally available and maintain balanced crop nutrition and good field management.",
            "escalation": "Ask a local crop adviser for confirmation when rust is widespread or appears early in a susceptible crop.",
        },
        "hi": {
            "symptoms": "पत्तियों की दोनों सतहों पर छोटे लाल-भूरे या नारंगी उभार हो सकते हैं। गंभीर संक्रमण में पत्तियाँ पीली हो सकती हैं।",
            "monitoring": "कई पौधों और दोनों पत्ती सतहों की जाँच करें। नम क्षेत्रों में उभारों की स्थिति ट्रैक करें।",
            "immediate_actions": "प्रसार की निगरानी करें और रिकॉर्ड बनाए रखें। गीले पत्तों में अनावश्यक आवागमन से बचें।",
            "prevention": "स्थानीय रूप से उपलब्ध प्रतिरोधी संकर किस्मों का उपयोग करें और संतुलित पोषण बनाए रखें।",
            "escalation": "जब रतुआ व्यापक हो या संवेदनशील फसल में जल्दी दिखे तो स्थानीय सलाहकार से पुष्टि करें।",
        },
        "te": {
            "symptoms": "ఆకుల రెండు వైపులా చిన్న ఎర్రటి-గోధుమ రంగు లేదా నారింజ రంగు పస్టుల్స్ కనిపించవచ్చు.",
            "monitoring": "అనేక మొక్కలు మరియు రెండు ఆకు ఉపరితలాలను తనిఖీ చేయండి. తేమ ప్రాంతాలలో పస్టుల్స్ పెరుగుతున్నాయో లేదో గమనించండి.",
            "immediate_actions": "వ్యాప్తిని పర్యవేక్షించండి మరియు రికార్డులు నిర్వహించండి.",
            "prevention": "నిరోధక సంకరజాతులను ఉపయోగించండి మరియు సమతుల్య పంట పోషణ నిర్వహించండి.",
            "escalation": "తుప్పు విస్తృతంగా ఉంటే లేదా అతిగ్రాహ్య పంటలో ముందుగా కనిపిస్తే స్థానిక సలహాదారుని సంప్రదించండి.",
        },
    },

    "corn__healthy": {
        "en": {
            "symptoms": "No disease signs detected. The image is consistent with a healthy corn leaf, but image-based screening cannot exclude early infection or non-disease stress.",
            "monitoring": "Continue routine scouting across several locations in the field.",
            "immediate_actions": "Maintain normal crop monitoring and record any emerging symptoms.",
            "prevention": "Use clean seed, suitable hybrids, crop rotation, field sanitation, and locally recommended agronomic practices.",
            "escalation": "Seek advice if symptoms appear suddenly, spread quickly, or affect multiple plants.",
        },
        "hi": {
            "symptoms": "कोई रोग संकेत नहीं मिला। छवि स्वस्थ मकई की पत्ती के अनुरूप है।",
            "monitoring": "खेत में कई स्थानों पर नियमित सर्वेक्षण जारी रखें।",
            "immediate_actions": "सामान्य फसल निगरानी बनाए रखें और उभरते लक्षणों को दर्ज करें।",
            "prevention": "स्वच्छ बीज, उपयुक्त संकर, फसल चक्र और स्थानीय अनुशंसित कृषि पद्धतियों का उपयोग करें।",
            "escalation": "यदि लक्षण अचानक प्रकट हों, तेजी से फैलें, या कई पौधे प्रभावित हों तो सलाह लें।",
        },
        "te": {
            "symptoms": "వ్యాధి లక్షణాలు కనుగొనబడలేదు. చిత్రం ఆరోగ్యకరమైన మొక్కజొన్న ఆకుతో అనుకూలంగా ఉంది.",
            "monitoring": "పొలంలో అనేక స్థలాలలో నిర్బంధ సర్వే కొనసాగించండి.",
            "immediate_actions": "సాధారణ పంట పర్యవేక్షణ నిర్వహించండి మరియు ఉద్భవిస్తున్న లక్షణాలను నమోదు చేయండి.",
            "prevention": "శుభ్రమైన విత్తనం, తగిన సంకరజాతులు, పంట మార్పిడి మరియు స్థానికంగా సిఫార్సు చేయబడిన పద్ధతులను ఉపయోగించండి.",
            "escalation": "లక్షణాలు అకస్మాత్తుగా కనిపిస్తే, వేగంగా వ్యాపిస్తే లేదా అనేక మొక్కలు ప్రభావితమైతే సలహా కోరండి.",
        },
    },

    "corn__northern_leaf_blight": {
        "en": {
            "symptoms": "Long, cigar-shaped gray-green to tan lesions may appear on leaves. Lesions can enlarge and merge under favourable conditions.",
            "monitoring": "Inspect lower leaves and assess whether long lesions are increasing toward upper canopy leaves.",
            "immediate_actions": "Monitor disease progression and avoid spreading residue or wet foliage between fields.",
            "prevention": "Use resistant hybrids where appropriate, rotate crops, and manage crop residue according to locally suitable practices.",
            "escalation": "Contact a local adviser if symptoms occur early, spread rapidly, or threaten a large area of the crop.",
        },
        "hi": {
            "symptoms": "पत्तियों पर लंबे, सिगार के आकार के धूसर-हरे से तन रंग के घाव दिख सकते हैं।",
            "monitoring": "निचली पत्तियों की जाँच करें और देखें कि लंबे घाव ऊपरी छत्र पत्तियों की ओर बढ़ रहे हैं या नहीं।",
            "immediate_actions": "रोग की प्रगति की निगरानी करें और खेतों के बीच अवशेष या गीले पत्ते फैलने से बचाएँ।",
            "prevention": "उचित प्रतिरोधी संकर किस्मों का उपयोग करें, फसल चक्र अपनाएँ।",
            "escalation": "यदि लक्षण जल्दी प्रकट हों, तेजी से फैलें, या बड़े क्षेत्र को खतरा हो तो स्थानीय सलाहकार से संपर्क करें।",
        },
        "te": {
            "symptoms": "ఆకులపై పొడవైన, సిగారు ఆకారపు బూడిద-ఆకుపచ్చ నుండి టాన్ రంగు గాయాలు కనిపించవచ్చు.",
            "monitoring": "దిగువ ఆకులను తనిఖీ చేయండి మరియు పొడవైన గాయాలు పై వాతావరణ ఆకుల వైపు పెరుగుతున్నాయో లేదో అంచనా వేయండి.",
            "immediate_actions": "వ్యాధి అభివృద్ధిని పర్యవేక్షించండి మరియు పొలాల మధ్య అవశేషాలు వ్యాపించకుండా నిరోధించండి.",
            "prevention": "నిరోధక సంకరజాతులను ఉపయోగించండి, పంట మార్పిడి చేయండి.",
            "escalation": "లక్షణాలు ముందుగా కనిపిస్తే, వేగంగా వ్యాపిస్తే లేదా పెద్ద ప్రాంతానికి ముప్పు ఏర్పడితే స్థానిక సలహాదారుని సంప్రదించండి.",
        },
    },

    "potato__early_blight": {
        "en": {
            "symptoms": "Older leaves may develop brown spots with concentric ring patterns, often surrounded by yellowing.",
            "monitoring": "Check older leaves first and estimate how many plants show expanding spots.",
            "immediate_actions": "Remove heavily affected leaves only if practical and hygienic. Reduce prolonged leaf wetness and avoid unnecessary handling of wet plants.",
            "prevention": "Use clean seed tubers, rotate crops, manage volunteer plants and debris, and maintain balanced crop nutrition.",
            "escalation": "Seek local advice if symptoms spread quickly, move to younger leaves, or threaten a substantial portion of the canopy.",
        },
        "hi": {
            "symptoms": "पुरानी पत्तियों पर भूरे धब्बे और केंद्रित वलय पैटर्न दिख सकते हैं, अक्सर पीलेपन से घिरे हुए।",
            "monitoring": "पहले पुरानी पत्तियों की जाँच करें और अनुमान लगाएँ कि कितने पौधों में धब्बे बढ़ रहे हैं।",
            "immediate_actions": "भारी रूप से प्रभावित पत्तियाँ व्यावहारिक हो तो हटाएँ। लंबे समय तक पत्तियों की नमी कम करें।",
            "prevention": "स्वच्छ बीज कंद उपयोग करें, फसल चक्र अपनाएँ, स्वयंसेवी पौधे और मलबा हटाएँ।",
            "escalation": "यदि लक्षण जल्दी फैलें, युवा पत्तियों पर आएँ, या छत्र के बड़े हिस्से को खतरा हो तो स्थानीय सलाह लें।",
        },
        "te": {
            "symptoms": "పాత ఆకులపై కేంద్రీకృత వలయ నమూనాలతో గోధుమ రంగు మచ్చలు కనిపించవచ్చు, తరచుగా పసుపు రంగులో చుట్టుముట్టబడి.",
            "monitoring": "మొదట పాత ఆకులను తనిఖీ చేయండి మరియు ఎన్ని మొక్కలలో మచ్చలు పెరుగుతున్నాయో అంచనా వేయండి.",
            "immediate_actions": "తీవ్రంగా ప్రభావితమైన ఆకులను తొలగించండి. ఆకుల తేమ తగ్గించండి.",
            "prevention": "శుభ్రమైన బీజ దుంపలు ఉపయోగించండి, పంట మార్పిడి చేయండి, స్వచ్ఛంద మొక్కలు తొలగించండి.",
            "escalation": "లక్షణాలు వేగంగా వ్యాపిస్తే లేదా యువ ఆకులకు చేరుకుంటే స్థానిక సలహా తీసుకోండి.",
        },
    },

    "potato__healthy": {
        "en": {
            "symptoms": "No disease signs detected. The image is consistent with a healthy potato leaf, but continued field scouting is still necessary.",
            "monitoring": "Inspect lower and upper canopy leaves on multiple plants.",
            "immediate_actions": "Continue routine scouting and keep irrigation and field hygiene practices consistent.",
            "prevention": "Use healthy seed tubers, crop rotation, sanitation, and locally recommended soil, nutrition, and irrigation management.",
            "escalation": "Consult an adviser if dark spots, blight-like lesions, wilting, or rapid foliage decline develops.",
        },
        "hi": {
            "symptoms": "कोई रोग संकेत नहीं मिला। छवि स्वस्थ आलू की पत्ती के अनुरूप है।",
            "monitoring": "कई पौधों पर निचली और ऊपरी छत्र पत्तियों का निरीक्षण करें।",
            "immediate_actions": "नियमित सर्वेक्षण जारी रखें और सिंचाई एवं स्वच्छता पद्धतियाँ बनाए रखें।",
            "prevention": "स्वस्थ बीज कंद, फसल चक्र, स्वच्छता और स्थानीय अनुशंसित प्रबंधन का उपयोग करें।",
            "escalation": "यदि काले धब्बे, झुलसन जैसे घाव, मुरझाना, या तेजी से पत्ते खराब हों तो सलाहकार से परामर्श लें।",
        },
        "te": {
            "symptoms": "వ్యాధి లక్షణాలు కనుగొనబడలేదు. చిత్రం ఆరోగ్యకరమైన బంగాళాదుంప ఆకుతో అనుకూలంగా ఉంది.",
            "monitoring": "అనేక మొక్కలపై దిగువ మరియు పై వాతావరణ ఆకులను తనిఖీ చేయండి.",
            "immediate_actions": "నిర్బంధ సర్వే కొనసాగించండి మరియు నీటిపారుదల మరియు పొలం పరిశుభ్రత పద్ధతులు నిర్వహించండి.",
            "prevention": "ఆరోగ్యకరమైన బీజ దుంపలు, పంట మార్పిడి, పరిశుభ్రత మరియు స్థానికంగా సిఫార్సు చేయబడిన నిర్వహణ ఉపయోగించండి.",
            "escalation": "చీకటి మచ్చలు, తెగులు లాంటి గాయాలు, వాడిపోవడం లేదా వేగంగా ఆకుల క్షీణత కనిపిస్తే సలహాదారుని సంప్రదించండి.",
        },
    },

    "potato__late_blight": {
        "en": {
            "symptoms": "Leaves may show irregular water-soaked, dark green to brown lesions. Under humid conditions, pale growth may be visible around lesion edges.",
            "monitoring": "Inspect frequently during cool, wet, or humid weather. Check whether lesions expand rapidly or appear on multiple plants.",
            "immediate_actions": "Treat rapidly spreading blight-like symptoms as urgent: mark affected areas, minimize movement through wet foliage, and obtain local diagnostic advice.",
            "prevention": "Use healthy seed, remove volunteer plants, improve airflow where possible, and follow local late-blight monitoring and management programmes.",
            "escalation": "Contact a local agricultural extension officer or plant-health professional promptly if late blight is suspected, especially during favourable weather.",
        },
        "hi": {
            "symptoms": "पत्तियों पर अनियमित पानी-भिगे, गहरे हरे से भूरे घाव दिख सकते हैं। नमी की स्थिति में घाव के किनारों पर हल्की वृद्धि दिख सकती है।",
            "monitoring": "ठंडे, गीले या नमी वाले मौसम में बार-बार निरीक्षण करें। देखें कि घाव तेजी से बढ़ रहे हैं या नहीं।",
            "immediate_actions": "तेजी से फैलने वाले झुलसन जैसे लक्षणों को तुरंत महत्व दें। प्रभावित क्षेत्रों को चिह्नित करें और स्थानीय निदान सलाह लें।",
            "prevention": "स्वस्थ बीज का उपयोग करें, स्वयंसेवी पौधे हटाएँ और स्थानीय पछेती झुलसन प्रबंधन कार्यक्रम का पालन करें।",
            "escalation": "यदि पछेती झुलसन का संदेह हो तो तुरंत स्थानीय कृषि विस्तार अधिकारी से संपर्क करें।",
        },
        "te": {
            "symptoms": "ఆకులపై అనియమిత నీటిలో నానిన, ముదురు ఆకుపచ్చ నుండి గోధుమ రంగు గాయాలు కనిపించవచ్చు.",
            "monitoring": "చల్లని, తడి లేదా తేమ వాతావరణంలో తరచుగా తనిఖీ చేయండి.",
            "immediate_actions": "వేగంగా వ్యాపిస్తున్న తెగులు లాంటి లక్షణాలను అత్యవసరంగా పరిగణించండి. ప్రభావిత ప్రాంతాలను గుర్తించి స్థానిక నిపుణుల సహాయం తీసుకోండి.",
            "prevention": "ఆరోగ్యకరమైన విత్తనం ఉపయోగించండి, స్వచ్ఛంద మొక్కలు తొలగించండి, గాలి ప్రసరణ మెరుగుపరచండి.",
            "escalation": "ఆలస్య తెగులు అనుమానం ఉంటే వెంటనే స్థానిక వ్యవసాయ విస్తరణ అధికారిని సంప్రదించండి.",
        },
    },

    "tomato__bacterial_spot": {
        "en": {
            "symptoms": "Small dark, sometimes water-soaked spots may occur on leaves. Severe symptoms can cause yellowing and defoliation.",
            "monitoring": "Check new growth, nearby plants, and whether symptoms increase after wet weather.",
            "immediate_actions": "Avoid handling wet plants, sanitize tools, reduce leaf wetness, and avoid moving affected plant material between growing areas.",
            "prevention": "Use clean seed or transplants, practice crop rotation, maintain sanitation, and improve airflow and drainage.",
            "escalation": "Ask local extension staff for confirmation if symptoms are spreading or occur widely in young plants.",
        },
        "hi": {
            "symptoms": "पत्तियों पर छोटे काले, कभी-कभी पानी-भिगे धब्बे हो सकते हैं। गंभीर लक्षणों में पीलापन और पत्तियाँ गिरना हो सकता है।",
            "monitoring": "नई वृद्धि, आसपास के पौधों की जाँच करें और देखें कि गीले मौसम के बाद लक्षण बढ़ते हैं या नहीं।",
            "immediate_actions": "गीले पौधों को न छुएँ, उपकरण साफ करें, पत्तियों की नमी कम करें।",
            "prevention": "स्वच्छ बीज या पौधे उपयोग करें, फसल चक्र अपनाएँ, स्वच्छता बनाए रखें।",
            "escalation": "यदि लक्षण फैल रहे हों या युवा पौधों में व्यापक हों तो स्थानीय कृषि कर्मचारियों से पुष्टि लें।",
        },
        "te": {
            "symptoms": "ఆకులపై చిన్న చీకటి, కొన్నిసార్లు నీటిలో నానిన మచ్చలు కనిపించవచ్చు. తీవ్రమైన లక్షణాలు పసుపు రంగు మరియు ఆకు రాలుటకు దారితీయవచ్చు.",
            "monitoring": "కొత్త పెరుగుదల, సమీపంలోని మొక్కలను తనిఖీ చేయండి.",
            "immediate_actions": "తడి మొక్కలను తాకకండి, పరికరాలను శుభ్రంగా ఉంచండి, ఆకుల తేమ తగ్గించండి.",
            "prevention": "శుభ్రమైన విత్తనం లేదా నాటు మొక్కలు ఉపయోగించండి, పంట మార్పిడి చేయండి.",
            "escalation": "లక్షణాలు వ్యాపిస్తే లేదా యువ మొక్కలలో విస్తృతంగా కనిపిస్తే స్థానిక నిపుణుల సహాయం తీసుకోండి.",
        },
    },

    "tomato__early_blight": {
        "en": {
            "symptoms": "Brown lesions with concentric ring patterns may develop first on older leaves, often with yellowing around the lesion.",
            "monitoring": "Inspect lower, older foliage and check whether spots increase after warm, wet conditions.",
            "immediate_actions": "Remove severely affected foliage only when safe and practical, reduce leaf wetness, and avoid working when foliage is wet.",
            "prevention": "Use crop rotation, clean stakes and tools, mulching where appropriate, suitable spacing, and balanced nutrition.",
            "escalation": "Seek local advice if symptoms expand rapidly or affect a substantial portion of the canopy.",
        },
        "hi": {
            "symptoms": "केंद्रित वलय पैटर्न वाले भूरे घाव पहले पुरानी पत्तियों पर दिख सकते हैं, अक्सर घाव के चारों ओर पीलापन होता है।",
            "monitoring": "निचली, पुरानी पत्तियों का निरीक्षण करें और गर्म, गीली परिस्थितियों के बाद धब्बों की स्थिति जाँचें।",
            "immediate_actions": "गंभीर रूप से प्रभावित पत्तियाँ व्यावहारिक हो तो हटाएँ, पत्तियों की नमी कम करें।",
            "prevention": "फसल चक्र, स्वच्छ डंडे और उपकरण, उचित दूरी और संतुलित पोषण का उपयोग करें।",
            "escalation": "यदि लक्षण तेजी से फैलें या छत्र के बड़े हिस्से को प्रभावित करें तो स्थानीय सलाह लें।",
        },
        "te": {
            "symptoms": "కేంద్రీకృత వలయ నమూనాలతో గోధుమ రంగు గాయాలు మొదట పాత ఆకులపై కనిపించవచ్చు.",
            "monitoring": "దిగువ, పాత ఆకులను తనిఖీ చేయండి మరియు వెచ్చని, తడి పరిస్థితుల తర్వాత మచ్చలు పెరుగుతున్నాయో లేదో తనిఖీ చేయండి.",
            "immediate_actions": "తీవ్రంగా ప్రభావితమైన ఆకులను తొలగించండి, ఆకుల తేమ తగ్గించండి.",
            "prevention": "పంట మార్పిడి, శుభ్రమైన కర్రలు మరియు పరికరాలు, తగిన అంతరం మరియు సమతుల్య పోషణ ఉపయోగించండి.",
            "escalation": "లక్షణాలు వేగంగా విస్తరిస్తే స్థానిక సలహా తీసుకోండి.",
        },
    },

    "tomato__healthy": {
        "en": {
            "symptoms": "No disease signs detected. The image is consistent with a healthy tomato leaf, but it is not a confirmed diagnosis.",
            "monitoring": "Inspect multiple plants, including lower leaf surfaces, stems, and new growth.",
            "immediate_actions": "Continue regular scouting and maintain hygiene, irrigation, and nutrition practices.",
            "prevention": "Use clean planting material, sanitize tools, maintain spacing and airflow, and manage weeds and crop debris.",
            "escalation": "Seek support if spots, wilting, yellowing, or rapid symptom spread occurs.",
        },
        "hi": {
            "symptoms": "कोई रोग संकेत नहीं मिला। छवि स्वस्थ टमाटर की पत्ती के अनुरूप है।",
            "monitoring": "निचली पत्ती सतहों, तनों और नई वृद्धि सहित कई पौधों का निरीक्षण करें।",
            "immediate_actions": "नियमित सर्वेक्षण जारी रखें और स्वच्छता, सिंचाई और पोषण पद्धतियाँ बनाए रखें।",
            "prevention": "स्वच्छ रोपण सामग्री, उपकरण स्वच्छता, उचित दूरी और खरपतवार प्रबंधन बनाए रखें।",
            "escalation": "यदि धब्बे, मुरझाना, पीलापन, या तेज लक्षण फैलाव हो तो सहायता लें।",
        },
        "te": {
            "symptoms": "వ్యాధి లక్షణాలు కనుగొనబడలేదు. చిత్రం ఆరోగ్యకరమైన టొమాటో ఆకుతో అనుకూలంగా ఉంది.",
            "monitoring": "దిగువ ఆకు ఉపరితలాలు, కాండాలు మరియు కొత్త పెరుగుదలతో సహా అనేక మొక్కలను తనిఖీ చేయండి.",
            "immediate_actions": "నిర్బంధ సర్వే కొనసాగించండి మరియు పరిశుభ్రత, నీటిపారుదల మరియు పోషణ పద్ధతులు నిర్వహించండి.",
            "prevention": "శుభ్రమైన నాటు సామగ్రి, పరికరాల పరిశుభ్రత, తగిన అంతరం మరియు కలుపు నిర్వహణ నిర్వహించండి.",
            "escalation": "మచ్చలు, వాడిపోవడం, పసుపు రంగు లేదా వేగంగా లక్షణాలు వ్యాపిస్తే సహాయం తీసుకోండి.",
        },
    },

    "tomato__late_blight": {
        "en": {
            "symptoms": "Irregular dark, water-soaked-looking leaf lesions can expand rapidly, especially during cool and humid weather.",
            "monitoring": "Check frequently during wet or humid periods and inspect neighbouring tomato and potato plants.",
            "immediate_actions": "Rapidly expanding blight-like symptoms require prompt local assessment. Avoid moving through wet foliage and avoid transporting affected material.",
            "prevention": "Use healthy transplants, improve airflow, remove volunteer hosts, practice sanitation, and follow local disease alerts where available.",
            "escalation": "Contact local extension or plant-health services promptly if late blight is suspected.",
        },
        "hi": {
            "symptoms": "अनियमित काले, पानी-भिगे जैसे पत्ती के घाव तेजी से फैल सकते हैं, खासकर ठंडे और नमी वाले मौसम में।",
            "monitoring": "गीले या नमी के दौरान बार-बार जाँच करें और आसपास के टमाटर और आलू के पौधों का निरीक्षण करें।",
            "immediate_actions": "तेजी से फैलने वाले झुलसन जैसे लक्षणों के लिए तुरंत स्थानीय मूल्यांकन आवश्यक है।",
            "prevention": "स्वस्थ पौधे उपयोग करें, वायु प्रवाह सुधारें, स्वयंसेवी पौधे हटाएँ, स्वच्छता बनाए रखें।",
            "escalation": "यदि पछेती झुलसन का संदेह हो तो तुरंत स्थानीय कृषि सेवाओं से संपर्क करें।",
        },
        "te": {
            "symptoms": "అనియమిత చీకటి, నీటిలో నానిన లాంటి ఆకు గాయాలు వేగంగా విస్తరించవచ్చు.",
            "monitoring": "తడి లేదా తేమ కాలాలలో తరచుగా తనిఖీ చేయండి మరియు పొరుగు టొమాటో మరియు బంగాళాదుంప మొక్కలను తనిఖీ చేయండి.",
            "immediate_actions": "వేగంగా విస్తరిస్తున్న తెగులు లాంటి లక్షణాలకు వెంటనే స్థానిక అంచనా అవసరం.",
            "prevention": "ఆరోగ్యకరమైన నాటు మొక్కలు ఉపయోగించండి, గాలి ప్రసరణ మెరుగుపరచండి, పరిశుభ్రత పాటించండి.",
            "escalation": "ఆలస్య తెగులు అనుమానం ఉంటే వెంటనే స్థానిక వ్యవసాయ సేవలను సంప్రదించండి.",
        },
    },

    "tomato__leaf_mold": {
        "en": {
            "symptoms": "Yellowish areas may form on upper leaf surfaces, while olive-green to brown mold-like growth can occur on lower leaf surfaces in humid conditions.",
            "monitoring": "Inspect lower leaf surfaces and note whether symptoms are concentrated in humid, dense canopy areas.",
            "immediate_actions": "Improve airflow, reduce humidity where possible, and avoid prolonged leaf wetness.",
            "prevention": "Use appropriate plant spacing, ventilation in protected cultivation, sanitation, and locally suitable resistant varieties where available.",
            "escalation": "Seek confirmation if symptoms persist, spread in protected cultivation, or affect many plants.",
        },
        "hi": {
            "symptoms": "ऊपरी पत्ती सतह पर पीले क्षेत्र और निचली पत्ती सतह पर जैतूनी-हरे से भूरे फफूंद जैसी वृद्धि हो सकती है।",
            "monitoring": "निचली पत्ती सतहों की जाँच करें और देखें कि लक्षण नमी वाले, घने छत्र क्षेत्रों में केंद्रित हैं या नहीं।",
            "immediate_actions": "वायु प्रवाह सुधारें, जहाँ संभव हो नमी कम करें और लंबे समय तक पत्तियों की नमी से बचें।",
            "prevention": "उचित पौधे दूरी, संरक्षित खेती में वेंटिलेशन, स्वच्छता और स्थानीय प्रतिरोधी किस्मों का उपयोग करें।",
            "escalation": "यदि लक्षण बने रहें, संरक्षित खेती में फैलें, या कई पौधे प्रभावित हों तो पुष्टि करें।",
        },
        "te": {
            "symptoms": "ఆకు ఉపరితలంపై పసుపు రంగు ప్రాంతాలు మరియు దిగువ ఆకు ఉపరితలంపై ఆలివ్-ఆకుపచ్చ నుండి గోధుమ రంగు అచ్చు లాంటి పెరుగుదల కనిపించవచ్చు.",
            "monitoring": "దిగువ ఆకు ఉపరితలాలను తనిఖీ చేయండి మరియు లక్షణాలు తేమ, దట్టమైన వాతావరణ ప్రాంతాలలో కేంద్రీకృతమయ్యాయో లేదో గమనించండి.",
            "immediate_actions": "గాలి ప్రసరణ మెరుగుపరచండి, తేమ తగ్గించండి, ఆకుల దీర్ఘకాల తేమ నివారించండి.",
            "prevention": "తగిన మొక్కల అంతరం, రక్షిత సాగులో వెంటిలేషన్, పరిశుభ్రత మరియు నిరోధక జాతులు ఉపయోగించండి.",
            "escalation": "లక్షణాలు కొనసాగితే లేదా అనేక మొక్కలు ప్రభావితమైతే నిర్ధారణ కోరండి.",
        },
    },

    "tomato__septoria_leaf_spot": {
        "en": {
            "symptoms": "Numerous small circular spots with pale or gray centres and darker margins may develop, often first on lower leaves.",
            "monitoring": "Inspect lower leaves and monitor whether the number of spots is increasing after rainfall or overhead irrigation.",
            "immediate_actions": "Remove heavily affected lower leaves only if practical, improve spacing and airflow, and reduce leaf wetness.",
            "prevention": "Practice crop rotation, remove crop debris, control volunteer tomatoes and related weeds, and sanitize tools.",
            "escalation": "Seek local support when symptoms spread quickly or lower-canopy defoliation becomes substantial.",
        },
        "hi": {
            "symptoms": "हल्के या धूसर केंद्र और गहरे किनारों वाले कई छोटे गोलाकार धब्बे दिख सकते हैं, अक्सर पहले निचली पत्तियों पर।",
            "monitoring": "निचली पत्तियों की जाँच करें और बारिश या सिंचाई के बाद धब्बों की संख्या बढ़ रही है या नहीं देखें।",
            "immediate_actions": "भारी प्रभावित निचली पत्तियाँ व्यावहारिक हो तो हटाएँ, दूरी और वायु प्रवाह सुधारें।",
            "prevention": "फसल चक्र, फसल मलबा हटाना, स्वयंसेवी टमाटर नियंत्रण और उपकरण स्वच्छता अपनाएँ।",
            "escalation": "जब लक्षण तेजी से फैलें या निचले छत्र का पत्ते झड़ना महत्वपूर्ण हो तो स्थानीय सहायता लें।",
        },
        "te": {
            "symptoms": "లేత లేదా బూడిద కేంద్రాలు మరియు ముదురు అంచులతో అనేక చిన్న వృత్తాకార మచ్చలు కనిపించవచ్చు.",
            "monitoring": "దిగువ ఆకులను తనిఖీ చేయండి మరియు వర్షం లేదా నీటిపారుదల తర్వాత మచ్చల సంఖ్య పెరుగుతున్నదో లేదో పర్యవేక్షించండి.",
            "immediate_actions": "తీవ్రంగా ప్రభావితమైన దిగువ ఆకులను తొలగించండి, అంతరం మరియు గాలి ప్రసరణ మెరుగుపరచండి.",
            "prevention": "పంట మార్పిడి, పంట అవశేషాలు తొలగించడం, స్వచ్ఛంద టొమాటో నియంత్రణ మరియు పరికరాల పరిశుభ్రత పాటించండి.",
            "escalation": "లక్షణాలు వేగంగా వ్యాపిస్తే లేదా దిగువ వాతావరణం ఆకు రాలుట గణనీయంగా ఉంటే స్థానిక సహాయం తీసుకోండి.",
        },
    },

    "tomato__spider_mites_two_spotted_spider_mite": {
        "en": {
            "symptoms": "Fine stippling, yellowing, bronzing, and sometimes webbing may occur, especially in hot, dry conditions.",
            "monitoring": "Inspect leaf undersides with a hand lens if available and look for mites, eggs, and fine webbing.",
            "immediate_actions": "Monitor affected areas closely, reduce plant stress, and avoid actions that disrupt beneficial insects.",
            "prevention": "Maintain plant health, monitor hot and dry areas, manage dust where feasible, and use integrated pest management practices.",
            "escalation": "Consult local advisers if mite populations increase rapidly or webbing and bronzing become widespread.",
        },
        "hi": {
            "symptoms": "सूक्ष्म बिंदु, पीलापन, कांस्य रंग, और कभी-कभी जाल दिख सकते हैं, खासकर गर्म, शुष्क परिस्थितियों में।",
            "monitoring": "यदि उपलब्ध हो तो हैंड लेंस से पत्ती की निचली सतह की जाँच करें। माइट्स, अंडे और जाल देखें।",
            "immediate_actions": "प्रभावित क्षेत्रों की निगरानी करें, पौधे का तनाव कम करें, और लाभकारी कीटों को बाधित करने वाली कार्रवाई से बचें।",
            "prevention": "पौधे का स्वास्थ्य बनाए रखें, गर्म और शुष्क क्षेत्रों की निगरानी करें, एकीकृत कीट प्रबंधन पद्धतियाँ उपयोग करें।",
            "escalation": "यदि माइट आबादी तेजी से बढ़े या जाल और कांस्य रंग व्यापक हो तो स्थानीय सलाहकारों से परामर्श लें।",
        },
        "te": {
            "symptoms": "సూక్ష్మమైన బిందువులు, పసుపు రంగు, కాంస్య రంగు మరియు కొన్నిసార్లు వలలు కనిపించవచ్చు.",
            "monitoring": "హ్యాండ్ లెన్స్‌తో ఆకు దిగువ ఉపరితలాన్ని తనిఖీ చేయండి. పురుగులు, గుడ్లు మరియు వలలు చూడండి.",
            "immediate_actions": "ప్రభావిత ప్రాంతాలను నిశితంగా పర్యవేక్షించండి, మొక్కల ఒత్తిడి తగ్గించండి.",
            "prevention": "మొక్కల ఆరోగ్యం నిర్వహించండి, వేడి మరియు పొడి ప్రాంతాలను పర్యవేక్షించండి, సమగ్ర పీడ నిర్వహణ పద్ధతులు ఉపయోగించండి.",
            "escalation": "పురుగుల జనాభా వేగంగా పెరిగితే లేదా వలలు మరియు కాంస్య రంగు విస్తృతంగా మారితే స్థానిక సలహాదారులను సంప్రదించండి.",
        },
    },

    "tomato__target_spot": {
        "en": {
            "symptoms": "Brown lesions with concentric or target-like patterns may occur on leaves. Symptoms can overlap visually with other tomato foliar diseases.",
            "monitoring": "Check whether lesions are increasing, merging, or causing leaf yellowing and drop.",
            "immediate_actions": "Reduce prolonged leaf wetness, improve airflow, and avoid spreading plant debris or wet foliage.",
            "prevention": "Use sanitation, crop rotation, balanced nutrition, and locally appropriate spacing and irrigation practices.",
            "escalation": "Request local confirmation because target spot can resemble early blight and other foliar diseases.",
        },
        "hi": {
            "symptoms": "पत्तियों पर केंद्रित या लक्ष्य जैसे पैटर्न वाले भूरे घाव हो सकते हैं। लक्षण अन्य टमाटर पत्ती रोगों जैसे दिख सकते हैं।",
            "monitoring": "जाँचें कि घाव बढ़ रहे हैं, विलीन हो रहे हैं, या पत्तियाँ पीली होकर गिर रही हैं।",
            "immediate_actions": "लंबे समय तक पत्तियों की नमी कम करें, वायु प्रवाह सुधारें।",
            "prevention": "स्वच्छता, फसल चक्र, संतुलित पोषण और उचित दूरी व सिंचाई पद्धतियाँ उपयोग करें।",
            "escalation": "लक्ष्य धब्बा पहली झुलसन और अन्य पत्ती रोगों जैसा दिख सकता है, इसलिए स्थानीय पुष्टि लें।",
        },
        "te": {
            "symptoms": "ఆకులపై కేంద్రీకృత లేదా లక్ష్య లాంటి నమూనాలతో గోధుమ రంగు గాయాలు కనిపించవచ్చు.",
            "monitoring": "గాయాలు పెరుగుతున్నాయో, విలీనమవుతున్నాయో లేదా ఆకు పసుపు రంగు మరియు రాలుటకు కారణమవుతున్నాయో తనిఖీ చేయండి.",
            "immediate_actions": "ఆకుల దీర్ఘకాల తేమ తగ్గించండి, గాలి ప్రసరణ మెరుగుపరచండి.",
            "prevention": "పరిశుభ్రత, పంట మార్పిడి, సమతుల్య పోషణ మరియు తగిన అంతరం మరియు నీటిపారుదల పద్ధతులు ఉపయోగించండి.",
            "escalation": "లక్ష్య మచ్చ ముందస్తు తెగులు మరియు ఇతర ఆకు వ్యాధులను పోలి ఉంటుంది కాబట్టి స్థానిక నిర్ధారణ కోరండి.",
        },
    },

    "tomato__tomato_mosaic_virus": {
        "en": {
            "symptoms": "Leaves may show mosaic-like light and dark green patterning, distortion, or reduced vigour. Symptoms can resemble nutritional or other viral problems.",
            "monitoring": "Inspect several plants for a repeated mosaic pattern, leaf distortion, and symptom distribution within the crop.",
            "immediate_actions": "Avoid handling plants unnecessarily, wash hands, sanitize tools, and separate suspect plants while seeking confirmation.",
            "prevention": "Use clean seed or transplants, sanitize tools and hands, control volunteer plants, and use resistant varieties where locally suitable.",
            "escalation": "Seek expert confirmation because virus-like symptoms can be confused with other stresses and management depends on accurate diagnosis.",
        },
        "hi": {
            "symptoms": "पत्तियों पर मोजेक जैसे हल्के और गहरे हरे पैटर्न, विकृति, या कम जीवन शक्ति दिख सकती है।",
            "monitoring": "बार-बार मोजेक पैटर्न, पत्ती विकृति और फसल में लक्षण वितरण के लिए कई पौधों का निरीक्षण करें।",
            "immediate_actions": "पौधों को अनावश्यक रूप से न छुएँ, हाथ धोएँ, उपकरण साफ करें और संदिग्ध पौधों को अलग करें।",
            "prevention": "स्वच्छ बीज या पौधे उपयोग करें, उपकरण और हाथ स्वच्छ रखें, स्वयंसेवी पौधे नियंत्रित करें।",
            "escalation": "वायरस जैसे लक्षण अन्य तनावों से भ्रमित हो सकते हैं, इसलिए विशेषज्ञ पुष्टि लें।",
        },
        "te": {
            "symptoms": "ఆకులు మొజాయిక్ లాంటి లేత మరియు ముదురు ఆకుపచ్చ నమూనా, వికారం లేదా తక్కువ శక్తిని చూపించవచ్చు.",
            "monitoring": "పదే పదే మొజాయిక్ నమూనా, ఆకు వికారం మరియు పంటలో లక్షణ పంపిణీ కోసం అనేక మొక్కలను తనిఖీ చేయండి.",
            "immediate_actions": "మొక్కలను అనవసరంగా తాకకండి, చేతులు కడుక్కోండి, పరికరాలు శుభ్రంగా ఉంచండి.",
            "prevention": "శుభ్రమైన విత్తనం లేదా నాటు మొక్కలు ఉపయోగించండి, పరికరాలు మరియు చేతులు శుభ్రంగా ఉంచండి.",
            "escalation": "వైరస్ లాంటి లక్షణాలు ఇతర ఒత్తిళ్లతో గందరగోళ పడవచ్చు, కాబట్టి నిపుణుల నిర్ధారణ కోరండి.",
        },
    },

    "tomato__tomato_yellow_leaf_curl_virus": {
        "en": {
            "symptoms": "Young leaves may curl upward, become smaller, and show yellowing. Plants may become stunted.",
            "monitoring": "Inspect new growth and monitor for whitefly activity, especially around crop edges and nearby hosts.",
            "immediate_actions": "Isolate suspect plants where practical, manage weeds and volunteer hosts, and seek local confirmation.",
            "prevention": "Use clean transplants, resistant varieties where available, physical exclusion in protected systems, and integrated whitefly monitoring and management.",
            "escalation": "Contact local extension staff if virus-like symptoms or whitefly activity are increasing.",
        },
        "hi": {
            "symptoms": "युवा पत्तियाँ ऊपर की ओर मुड़ सकती हैं, छोटी हो सकती हैं और पीलापन दिखा सकती हैं। पौधे बौने हो सकते हैं।",
            "monitoring": "नई वृद्धि का निरीक्षण करें और सफेद मक्खी गतिविधि की निगरानी करें, खासकर फसल के किनारों और आसपास के पौधों के पास।",
            "immediate_actions": "जहाँ व्यावहारिक हो संदिग्ध पौधों को अलग करें, खरपतवार और स्वयंसेवी पौधे हटाएँ।",
            "prevention": "स्वच्छ पौधे, उपलब्ध होने पर प्रतिरोधी किस्में, संरक्षित प्रणालियों में भौतिक बहिष्करण और सफेद मक्खी प्रबंधन का उपयोग करें।",
            "escalation": "यदि वायरस जैसे लक्षण या सफेद मक्खी गतिविधि बढ़ रही हो तो स्थानीय कृषि कर्मचारियों से संपर्क करें।",
        },
        "te": {
            "symptoms": "యువ ఆకులు పైకి వంగవచ్చు, చిన్నవి అవుతాయి మరియు పసుపు రంగు చూపించవచ్చు. మొక్కలు వికసించకపోవచ్చు.",
            "monitoring": "కొత్త పెరుగుదలను తనిఖీ చేయండి మరియు తెల్ల ఈగ కార్యకలాపాలను పర్యవేక్షించండి.",
            "immediate_actions": "సాధ్యమైన చోట అనుమానిత మొక్కలను వేరుచేయండి, కలుపు మరియు స్వచ్ఛంద ఆతిథేయిలను నిర్వహించండి.",
            "prevention": "శుభ్రమైన నాటు మొక్కలు, నిరోధక జాతులు, రక్షిత వ్యవస్థల్లో భౌతిక మినహాయింపు మరియు తెల్ల ఈగ నిర్వహణ ఉపయోగించండి.",
            "escalation": "వైరస్ లాంటి లక్షణాలు లేదా తెల్ల ఈగ కార్యకలాపాలు పెరుగుతుంటే స్థానిక వ్యవసాయ సిబ్బందిని సంప్రదించండి.",
        },
    },
}
