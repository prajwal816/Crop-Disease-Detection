/**
 * CropScan Frontend Application
 * Fully internationalized (EN / HI / TE) with Gemini AI Expert Integration.
 */

const API_BASE = 'http://localhost:8000';

// Global state
let currentLang = 'en';
let lastResult = null;
let isAnalysing = false;
let currentFile = null;      // the File chosen by the user
let previewUrl = null;       // object URL for the preview image
let requestSeq = 0;          // guards against stale responses
let selectedModel = 'v2s';
let modelInfo = [];          // from GET /models

const MAX_BYTES = 10 * 1024 * 1024;
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];

// ---------------------------------------------------------------------------
// Translations Dictionary (EN / HI / TE)
// ---------------------------------------------------------------------------
const I18N = {
  en: {
    stepUpload: "1. Upload",
    stepModel: "2. Choose model",
    groupSingle: "Single model",
    groupMulti: "Combine models",
    domainNote: "Trained on PlantVillage-style photos: one leaf, plain background. Field photos with busy backgrounds can be misclassified, even at high confidence. Always check the model breakdown.",
    dropZoneHint: "or click to browse (JPEG, PNG, WebP, max 10 MB)",
    footerModel: "Models: <strong>EfficientNetV2-S</strong>, <strong>EfficientNet-B0</strong>, <strong>ViT-B/16</strong> &middot; 19 classes &middot; Temperature-calibrated",
    modelLegend: "Choose model",
    modeCompare: "Compare all 3",
    modeEnsemble: "Ensemble (combine 3)",
    descV2s: "Highest-accuracy model; larger 384 px input, slower.",
    descB0: "Lightweight and fastest; 224 px input.",
    descVit: "Vision Transformer; 224 px input, probabilities not temperature-calibrated.",
    descCompare: "Runs all three models and shows each result side by side. The headline is the most confident model.",
    descEnsemble: "Averages the calibrated probabilities of all three models for one combined, usually more robust, answer.",
    changeImage: "Change image",
    removeImage: "Remove",
    modelUsed: "Model",
    topTitle: "Most likely diagnoses",
    breakdownTitle: "Model breakdown",
    agreeAll: "All {n} models agree.",
    agreeSome: "Models disagree: {k} of {n} agree on the top result. Treat with extra caution.",
    fileTooBig: "This image is larger than 10 MB. Please choose a smaller file.",
    badType: "Unsupported file type. Please choose a JPEG, PNG, or WebP image.",
    uncal: "uncalibrated",
    abstainShort: "Low confidence",
    unavailable: "Not loaded",
    heroTitle: "Diagnose your crop instantly",
    heroSub: "Upload a leaf photograph and receive a disease prediction, confidence score, lesion severity estimate, and actionable advisory in English, Hindi, or Telugu.",
    chipPepper: "Bell Pepper",
    chipCorn: "Corn",
    chipPotato: "Potato",
    chipTomato: "Tomato",
    uploadCardTitle: "Upload leaf image",
    dropZoneText: "Drag and drop a leaf photo here",
    btnAnalyse: "Analyse",
    btnAnalysing: "Analysing...",
    uploadHint: "Supported crops: Bell Pepper, Corn, Potato, Tomato.<br/>For best results, use a close-up photo of a single leaf in good lighting.",
    resultsEmptyText: "Upload a leaf image to see the analysis",
    confidenceBarText: "Confidence",
    abstainTitle: "Low confidence: prediction withheld",
    abstainDesc: "The model confidence is below 70%. Please try a clearer, better-lit photograph of a single leaf.",
    advisoryTitle: "Advisory",
    tabSymptoms: "Symptoms",
    tabMonitoring: "Monitoring",
    tabActions: "Actions",
    tabPrevention: "Prevention",
    tabEscalation: "Escalation",
    footerDisclaimer: "This tool provides a preliminary screening result only. It is not a confirmed diagnosis. Always verify with a qualified agronomist or plant-health professional before taking management action.",
    aiAdvisorTitle: "Ask Gemini AI Agricultural Specialist",
    aiPromptPlaceholder: "Ask a question about this crop or disease...",
    aiAskBtn: "Ask AI",
    aiAsking: "Thinking...",
    sug1: "What organic treatment can I use?",
    sug2: "How can I protect nearby crops?",
    sug3: "Is it safe to water the leaves?",
    confidenceTiers: { High: "High", Medium: "Medium", Low: "Low" },
    severityBands: { Low: "Low", Medium: "Medium", High: "High", Unknown: "Unknown" },
    severityPrefix: "Severity",
    crops: {
      bell_pepper: "Bell Pepper",
      corn: "Corn",
      potato: "Potato",
      tomato: "Tomato"
    },
    diseases: {
      bacterial_spot: "Bacterial Spot",
      healthy: "Healthy",
      cercospora_leaf_spot_gray_leaf_spot: "Cercospora / Gray Leaf Spot",
      common_rust: "Common Rust",
      northern_leaf_blight: "Northern Leaf Blight",
      early_blight: "Early Blight",
      late_blight: "Late Blight",
      leaf_mold: "Leaf Mold",
      septoria_leaf_spot: "Septoria Leaf Spot",
      spider_mites_two_spotted_spider_mite: "Two-Spotted Spider Mite",
      target_spot: "Target Spot",
      tomato_mosaic_virus: "Tomato Mosaic Virus",
      tomato_yellow_leaf_curl_virus: "Yellow Leaf Curl Virus"
    }
  },

  hi: {
    stepUpload: "1. अपलोड",
    stepModel: "2. मॉडल चुनें",
    groupSingle: "एकल मॉडल",
    groupMulti: "मॉडल मिलाएँ",
    domainNote: "मॉडल PlantVillage जैसी तस्वीरों (एक पत्ती, सादी पृष्ठभूमि) पर प्रशिक्षित हैं। खेत की भीड़-भाड़ वाली पृष्ठभूमि वाली तस्वीरों में उच्च विश्वास पर भी गलती हो सकती है। मॉडल-वार परिणाम ज़रूर देखें।",
    dropZoneHint: "या फ़ाइल चुनने के लिए क्लिक करें (JPEG, PNG, WebP, अधिकतम 10 MB)",
    footerModel: "मॉडल: <strong>EfficientNetV2-S</strong>, <strong>EfficientNet-B0</strong>, <strong>ViT-B/16</strong> &middot; 19 वर्ग &middot; कैलिब्रेटेड",
    modelLegend: "मॉडल चुनें",
    modeCompare: "तीनों की तुलना",
    modeEnsemble: "एन्सेम्बल (तीनों मिलाकर)",
    descV2s: "सबसे सटीक मॉडल; बड़ा 384 px इनपुट, कुछ धीमा।",
    descB0: "हल्का और सबसे तेज़; 224 px इनपुट।",
    descVit: "विज़न ट्रांसफ़ॉर्मर; 224 px इनपुट, प्रायिकताएँ कैलिब्रेटेड नहीं हैं।",
    descCompare: "तीनों मॉडल चलाकर परिणाम साथ-साथ दिखाता है। शीर्ष परिणाम सबसे अधिक विश्वास वाले मॉडल का होता है।",
    descEnsemble: "तीनों मॉडलों की कैलिब्रेटेड प्रायिकताओं का औसत लेकर एक संयुक्त, अधिक भरोसेमंद उत्तर देता है।",
    changeImage: "तस्वीर बदलें",
    removeImage: "हटाएँ",
    modelUsed: "मॉडल",
    topTitle: "सबसे संभावित निदान",
    breakdownTitle: "मॉडल-वार परिणाम",
    agreeAll: "सभी {n} मॉडल सहमत हैं।",
    agreeSome: "मॉडल असहमत हैं: {n} में से {k} शीर्ष परिणाम पर सहमत। अतिरिक्त सावधानी रखें।",
    fileTooBig: "यह तस्वीर 10 MB से बड़ी है। कृपया छोटी फ़ाइल चुनें।",
    badType: "असमर्थित फ़ाइल प्रकार। कृपया JPEG, PNG या WebP तस्वीर चुनें।",
    uncal: "कैलिब्रेटेड नहीं",
    abstainShort: "कम विश्वास",
    unavailable: "उपलब्ध नहीं",
    heroTitle: "अपनी फसल का तुरंत निदान करें",
    heroSub: "पत्ती की तस्वीर अपलोड करें और अंग्रेजी, हिंदी या तेलुगु में रोग की पहचान, विश्वास स्कोर, घाव की गंभीरता और कृषि सलाह प्राप्त करें।",
    chipPepper: "शिमला मिर्च",
    chipCorn: "मक्का",
    chipPotato: "आलू",
    chipTomato: "टमाटर",
    uploadCardTitle: "पत्ती की तस्वीर अपलोड करें",
    dropZoneText: "यहाँ पत्ती की तस्वीर खींचकर छोड़ें",
    btnAnalyse: "विश्लेषण करें",
    btnAnalysing: "विश्लेषण हो रहा है...",
    uploadHint: "समर्थित फसलें: शिमला मिर्च, मक्का, आलू, टमाटर।<br/>सर्वोत्तम परिणामों के लिए, अच्छी रोशनी में एक ही पत्ती की नज़दीकी तस्वीर लें।",
    resultsEmptyText: "विश्लेषण देखने के लिए पत्ती की छवि अपलोड करें",
    confidenceBarText: "विश्वास स्कोर",
    abstainTitle: "कम विश्वास: परिणाम रोका गया",
    abstainDesc: "मॉडल का विश्वास 70% से कम है। कृपया एक पत्ती की स्पष्ट और अच्छी रोशनी वाली तस्वीर लें।",
    advisoryTitle: "कृषि सलाह",
    tabSymptoms: "लक्षण",
    tabMonitoring: "निगरानी",
    tabActions: "तत्काल उपाय",
    tabPrevention: "रोकथाम",
    tabEscalation: "विशेषज्ञ परामर्श",
    footerDisclaimer: "यह उपकरण केवल एक प्रारंभिक जांच परिणाम प्रदान करता है। यह कोई अंतिम निदान नहीं है। कोई भी दवा या रासायनिक उपचार करने से पहले हमेशा किसी योग्य कृषि विशेषज्ञ से सलाह लें।",
    aiAdvisorTitle: "जेमिनी एआई कृषि विशेषज्ञ से पूछें",
    aiPromptPlaceholder: "फसल या रोग के उपचार के बारे में कोई भी प्रश्न पूछें...",
    aiAskBtn: "पूछें",
    aiAsking: "उत्तर तैयार हो रहा है...",
    sug1: "इसके लिए कौन सा जैविक उपाय करें?",
    sug2: "आसपास के पौधों को कैसे बचाएं?",
    sug3: "क्या पत्तियों पर पानी देना सही है?",
    confidenceTiers: { High: "उच्च", Medium: "मध्यम", Low: "कम" },
    severityBands: { Low: "हल्की (कम)", Medium: "मध्यम", High: "गंभीर (उच्च)", Unknown: "अज्ञात" },
    severityPrefix: "गंभीरता",
    crops: {
      bell_pepper: "शिमला मिर्च",
      corn: "मक्का",
      potato: "आलू",
      tomato: "टमाटर"
    },
    diseases: {
      bacterial_spot: "जीवाणु धब्बा रोग",
      healthy: "स्वस्थ फसल",
      cercospora_leaf_spot_gray_leaf_spot: "सर्कोस्पोरा / धूसर पत्ती धब्बा",
      common_rust: "सामान्य रतुआ रोग",
      northern_leaf_blight: "उत्तरी पत्ती झुलसा",
      early_blight: "अगेती झुलसा",
      late_blight: "पछेती झुलसा",
      leaf_mold: "पत्ती फफूंद रोग",
      septoria_leaf_spot: "सेप्टोरिया पत्ती धब्बा",
      spider_mites_two_spotted_spider_mite: "दो-धब्बेदार मकड़ी कीट",
      target_spot: "टारगेट स्पॉट रोग",
      tomato_mosaic_virus: "टमाटर मोज़ेक वायरस",
      tomato_yellow_leaf_curl_virus: "पीली पत्ती कुंचन वायरस"
    }
  },

  te: {
    stepUpload: "1. అప్‌లోడ్",
    stepModel: "2. మోడల్ ఎంచుకోండి",
    groupSingle: "ఒకే మోడల్",
    groupMulti: "మోడళ్లను కలపండి",
    domainNote: "మోడళ్లు PlantVillage తరహా ఫోటోలపై (ఒకే ఆకు, సాదా నేపథ్యం) శిక్షణ పొందాయి. పొలంలో తీసిన, గందరగోళ నేపథ్యం ఉన్న ఫోటోలలో అధిక ఖచ్చితత్వంతో కూడా తప్పు రావచ్చు. మోడల్ వారీ ఫలితాలను తప్పక చూడండి.",
    dropZoneHint: "లేదా ఫైల్ ఎంచుకోవడానికి క్లిక్ చేయండి (JPEG, PNG, WebP, గరిష్టంగా 10 MB)",
    footerModel: "మోడళ్లు: <strong>EfficientNetV2-S</strong>, <strong>EfficientNet-B0</strong>, <strong>ViT-B/16</strong> &middot; 19 రకాలు &middot; క్యాలిబ్రేట్ చేయబడింది",
    modelLegend: "మోడల్ ఎంచుకోండి",
    modeCompare: "మూడింటినీ పోల్చండి",
    modeEnsemble: "ఎన్సెంబుల్ (మూడూ కలిపి)",
    descV2s: "అత్యంత ఖచ్చితమైన మోడల్; పెద్ద 384 px ఇన్‌పుట్, కొంచెం నెమ్మది.",
    descB0: "తేలికైనది, అత్యంత వేగవంతం; 224 px ఇన్‌పుట్.",
    descVit: "విజన్ ట్రాన్స్‌ఫార్మర్; 224 px ఇన్‌పుట్, సంభావ్యతలు క్యాలిబ్రేట్ చేయబడలేదు.",
    descCompare: "మూడు మోడళ్లను నడిపి ఫలితాలను పక్కపక్కనే చూపుతుంది. ప్రధాన ఫలితం అత్యధిక ఖచ్చితత్వం ఉన్న మోడల్‌ది.",
    descEnsemble: "మూడు మోడళ్ల క్యాలిబ్రేటెడ్ సంభావ్యతల సగటుతో ఒకే, మరింత నమ్మదగిన సమాధానం ఇస్తుంది.",
    changeImage: "చిత్రం మార్చండి",
    removeImage: "తొలగించండి",
    modelUsed: "మోడల్",
    topTitle: "అత్యంత సంభావ్య నిర్ధారణలు",
    breakdownTitle: "మోడల్ వారీ ఫలితాలు",
    agreeAll: "మొత్తం {n} మోడళ్లు ఏకీభవిస్తున్నాయి.",
    agreeSome: "మోడళ్లు ఏకీభవించడం లేదు: {n}లో {k} మాత్రమే ప్రధాన ఫలితంపై ఏకీభవిస్తున్నాయి. అదనపు జాగ్రత్త వహించండి.",
    fileTooBig: "ఈ చిత్రం 10 MB కంటే పెద్దది. దయచేసి చిన్న ఫైల్ ఎంచుకోండి.",
    badType: "మద్దతు లేని ఫైల్ రకం. దయచేసి JPEG, PNG లేదా WebP చిత్రాన్ని ఎంచుకోండి.",
    uncal: "క్యాలిబ్రేట్ కాలేదు",
    abstainShort: "తక్కువ ఖచ్చితత్వం",
    unavailable: "అందుబాటులో లేదు",
    heroTitle: "మీ పంటను తక్షణమే నిర్ధారించండి",
    heroSub: "ఆకు ఫోటోను అప్‌లోడ్ చేయండి మరియు ఇంగ్లీష్, హిందీ లేదా తెలుగులో వ్యాధి అంచనా, ఖచ్చితత్వ స్కోరు, తెగులు తీవ్రత మరియు సూచనలను పొందండి.",
    chipPepper: "క్యాప్సికం (బెల్ పెప్పర్)",
    chipCorn: "మొక్కజొన్న",
    chipPotato: "బంగాళాదుంప",
    chipTomato: "టొమాటో",
    uploadCardTitle: "ఆకు చిత్రాన్ని అప్‌లోడ్ చేయండి",
    dropZoneText: "ఆకు ఫోటోను ఇక్కడ లాగి వదలండి",
    btnAnalyse: "విశ్లేషించండి",
    btnAnalysing: "విశ్లేషిస్తోంది...",
    uploadHint: "మద్దతు ఉన్న పంటలు: బెల్ పెప్పర్, మొక్కజొన్న, బంగాళాదుంప, టొమాటో.<br/>మంచి ఫలితాల కోసం, మంచి వెలుతురులో ఒకే ఆకు క్లోజప్ ఫోటో తీయండి.",
    resultsEmptyText: "విశ్లేషణను చూడటానికి ఆకు చిత్రాన్ని అప్‌లోడ్ చేయండి",
    confidenceBarText: "ఖచ్చితత్వం",
    abstainTitle: "తక్కువ ఖచ్చితత్వం: ఫలితం నిలిపివేయబడింది",
    abstainDesc: "మోడల్ ఖచ్చితత్వం 70% కంటే తక్కువగా ఉంది. దయచేసి ఒకే ఆకు యొక్క స్పష్టమైన ఫోటోను ప్రయత్నించండి.",
    advisoryTitle: "వ్యవసాయ సలహా",
    tabSymptoms: "లక్షణాలు",
    tabMonitoring: "పర్యవేక్షణ",
    tabActions: "చర్యలు",
    tabPrevention: "నివారణ",
    tabEscalation: "సంప్రదింపులు",
    footerDisclaimer: "ఈ సాధనం ప్రాథమిక స్క్రీనింగ్ ఫలితాన్ని మాత్రమే అందిస్తుంది. ఇది తుది రోగనిర్ధారణ కాదు. చర్య తీసుకునే ముందు అర్హత కలిగిన వ్యవసాయ నిపుణుడితో ధృవీకరించండి.",
    aiAdvisorTitle: "జెమినీ AI వ్యవసాయ నిపుణుడిని అడగండి",
    aiPromptPlaceholder: "ఈ పంట లేదా తెగులు గురించి ఏదైనా ప్రశ్న అడగండి...",
    aiAskBtn: "అడగండి",
    aiAsking: "ఆలోచిస్తోంది...",
    sug1: "దీనికి ఏ సేంద్రీయ నివారణ ఉపయోగించాలి?",
    sug2: "సమీపంలోని పంటలను ఎలా రక్షించాలి?",
    sug3: "ఆకులపై నీరు చల్లడం సురక్షితమేనా?",
    confidenceTiers: { High: "ఎక్కువ", Medium: "మధ్యస్థం", Low: "తక్కువ" },
    severityBands: { Low: "తక్కువ", Medium: "మధ్యస్థం", High: "ఎక్కువ", Unknown: "తెలియదు" },
    severityPrefix: "తీవ్రత",
    crops: {
      bell_pepper: "బెల్ పెప్పర్ (క్యాప్సికం)",
      corn: "మొక్కజొన్న",
      potato: "బంగాళాదుంప",
      tomato: "టొమాటో"
    },
    diseases: {
      bacterial_spot: "బ్యాక్టీరియా మచ్చ తెగులు",
      healthy: "ఆరోగ్యకరమైన పంట",
      cercospora_leaf_spot_gray_leaf_spot: "సెర్కోస్పోరా / బూడిద రంగు ఆకు మచ్చ",
      common_rust: "సాధారణ తుప్పు తెగులు",
      northern_leaf_blight: "ఉత్తర ఆకు తెగులు",
      early_blight: "ముందస్తు తెగులు (ఎర్లీ బ్లైట్)",
      late_blight: "ఆలస్య తెగులు (లేట్ బ్లైట్)",
      leaf_mold: "ఆకు బూజు తెగులు",
      septoria_leaf_spot: "సెప్టోరియా ఆకు మచ్చ",
      spider_mites_two_spotted_spider_mite: "రెండు మచ్చల ఎర్ర నల్లి",
      target_spot: "టార్గెట్ స్పాట్ తెగులు",
      tomato_mosaic_virus: "టొమాటో మొజాయిక్ వైరస్",
      tomato_yellow_leaf_curl_virus: "పసుపు ఆకు ముడత వైరస్"
    }
  }
};

// ---------------------------------------------------------------------------
// DOM Elements
// ---------------------------------------------------------------------------
const dropZone        = document.getElementById('dropZone');
const fileInput       = document.getElementById('fileInput');
const preview         = document.getElementById('preview');
const dropContent     = document.getElementById('dropContent');
const analyseBtn      = document.getElementById('analyseBtn');
const btnLabel        = document.getElementById('btnLabel');
const btnArrow        = document.getElementById('btnArrow');
const spinner         = document.getElementById('spinner');
const removeBtn       = document.getElementById('removeBtn');
const removeLink      = document.getElementById('removeLink');
const changeBtn       = document.getElementById('changeBtn');
const fileBar         = document.getElementById('fileBar');
const fileNameEl      = document.getElementById('fileName');
const modelGrid       = document.getElementById('modelGrid');
const modelDesc       = document.getElementById('modelDesc');
const modelTag        = document.getElementById('modelTag');
const topList         = document.getElementById('topList');
const breakdown       = document.getElementById('breakdown');
const breakdownGrid   = document.getElementById('breakdownGrid');
const agreeNote       = document.getElementById('agreeNote');

const resultsEmpty    = document.getElementById('resultsEmpty');
const errorBanner     = document.getElementById('errorBanner');
const errorMsg        = document.getElementById('errorMsg');
const resultContent   = document.getElementById('resultContent');

const cropName        = document.getElementById('cropName');
const diseaseLabel    = document.getElementById('diseaseLabel');
const confidenceBadge = document.getElementById('confidenceBadge');
const severityBadge   = document.getElementById('severityBadge');
const confidenceFill  = document.getElementById('confidenceFill');
const confidenceLabel = document.getElementById('confidenceLabel');
const abstainNotice   = document.getElementById('abstainNotice');
const advisoryCard    = document.getElementById('advisoryCard');

// AI elements
const aiPromptInput   = document.getElementById('aiPromptInput');
const aiAskBtn        = document.getElementById('aiAskBtn');
const aiAskBtnText    = document.getElementById('aiAskBtnText');
const aiSpinner       = document.getElementById('aiSpinner');
const aiResponseBox   = document.getElementById('aiResponseBox');
const aiResponseContent = document.getElementById('aiResponseContent');

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
function show(el) { el?.classList.remove('hidden'); }
function hide(el) { el?.classList.add('hidden'); }

function fmtPct(val) {
  return (val * 100).toFixed(1) + '%';
}

function parseLabel(label, lang = 'en') {
  if (!label) return { crop: '', disease: '' };
  const parts = label.split('__');
  const cropKey = parts[0] || '';
  const diseaseKey = parts[1] || '';

  const crop = I18N[lang]?.crops[cropKey] || cropKey.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  const disease = I18N[lang]?.diseases[diseaseKey] || diseaseKey.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  return { crop, disease };
}

// ---------------------------------------------------------------------------
// Internationalization: Switch UI Language
// ---------------------------------------------------------------------------
function applyLanguageToUI(lang) {
  const t = I18N[lang] || I18N.en;

  // Header & Hero
  document.getElementById('heroTitle').textContent = t.heroTitle;
  document.getElementById('heroSub').textContent = t.heroSub;
  document.querySelector('#chipPepper .chip-text').textContent = t.chipPepper;
  document.querySelector('#chipCorn .chip-text').textContent = t.chipCorn;
  document.querySelector('#chipPotato .chip-text').textContent = t.chipPotato;
  document.querySelector('#chipTomato .chip-text').textContent = t.chipTomato;

  // Upload Panel
  document.getElementById('dropZoneText').textContent = t.dropZoneText;
  document.getElementById('dropZoneHint').textContent = t.dropZoneHint;
  document.getElementById('uploadHint').innerHTML = t.uploadHint;
  btnLabel.textContent = isAnalysing ? t.btnAnalysing : t.btnAnalyse;

  // Results & Empty state
  document.getElementById('resultsEmptyText').textContent = t.resultsEmptyText;
  document.getElementById('confidenceBarText').textContent = t.confidenceBarText;
  document.getElementById('abstainTitle').textContent = t.abstainTitle;
  document.getElementById('abstainDesc').textContent = t.abstainDesc;
  document.getElementById('advisoryTitle').textContent = t.advisoryTitle;

  // Advisory Tabs
  document.getElementById('tabSymptoms').textContent = t.tabSymptoms;
  document.getElementById('tabMonitoring').textContent = t.tabMonitoring;
  document.getElementById('tabActions').textContent = t.tabActions;
  document.getElementById('tabPrevention').textContent = t.tabPrevention;
  document.getElementById('tabEscalation').textContent = t.tabEscalation;

  // AI Consultation
  document.getElementById('aiAdvisorTitle').textContent = t.aiAdvisorTitle;
  aiPromptInput.placeholder = t.aiPromptPlaceholder;
  aiAskBtnText.textContent = t.aiAskBtn;
  document.getElementById('sug1').textContent = t.sug1;
  document.getElementById('sug2').textContent = t.sug2;
  document.getElementById('sug3').textContent = t.sug3;

  // Model picker / file bar / breakdown
  document.getElementById('modelLegend').textContent = t.stepModel;
  document.getElementById('uploadCardTitle').textContent = '1. ' + t.uploadCardTitle;
  document.getElementById('domainNote').textContent = t.domainNote;
  document.getElementById('breakdownTitle').textContent = t.breakdownTitle;
  changeBtn.textContent = t.changeImage;
  removeLink.textContent = t.removeImage;
  removeBtn.title = t.removeImage;
  removeBtn.setAttribute('aria-label', t.removeImage);
  renderModelPicker();

  // Footer
  document.getElementById('footerModel').innerHTML = t.footerModel;
  document.getElementById('footerDisclaimer').textContent = t.footerDisclaimer;

  // If a result is active, re-render it in the selected language
  if (lastResult) {
    renderResult(lastResult, lang);
  }
}

function setLanguage(lang) {
  currentLang = lang;

  document.querySelectorAll('.lang-btn').forEach(btn => {
    const active = btn.dataset.lang === lang;
    btn.classList.toggle('active', active);
    btn.setAttribute('aria-pressed', String(active));
  });

  applyLanguageToUI(lang);
}

function initLangToggle() {
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => setLanguage(btn.dataset.lang));
  });
}

// ---------------------------------------------------------------------------
// Drop Zone / file handling
// ---------------------------------------------------------------------------
function openPicker() {
  if (isAnalysing) return;
  fileInput.value = '';            // lets the user re-pick the same file
  fileInput.click();
}

function initDropZone() {
  // With an image loaded, a click on the preview must not silently re-open
  // the picker: use the explicit Change / Remove controls instead.
  dropZone.addEventListener('click', () => { if (!currentFile) openPicker(); });

  dropZone.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      openPicker();
    }
  });

  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-active');
  });

  dropZone.addEventListener('dragleave', (e) => {
    if (!dropZone.contains(e.relatedTarget)) {
      dropZone.classList.remove('drag-active');
    }
  });

  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-active');
    if (isAnalysing) return;
    const file = e.dataTransfer?.files?.[0];
    if (file) setFile(file);
  });

  fileInput.addEventListener('change', () => {
    const file = fileInput.files?.[0];
    if (file) setFile(file);
  });

  removeBtn.addEventListener('click', clearFile);
  removeLink.addEventListener('click', clearFile);
  changeBtn.addEventListener('click', openPicker);
}

function setFile(file) {
  const t = I18N[currentLang];
  if (!ALLOWED_TYPES.includes(file.type)) { renderError(t.badType); return; }
  if (file.size > MAX_BYTES)              { renderError(t.fileTooBig); return; }

  requestSeq++;                                  // invalidate any in-flight request
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  previewUrl = URL.createObjectURL(file);
  currentFile = file;
  preview.src = previewUrl;

  show(preview);
  hide(dropContent);
  show(removeBtn);
  dropZone.classList.add('has-image');
  fileNameEl.textContent = `${file.name} (${(file.size / 1024).toFixed(0)} KB)`;
  show(fileBar);

  resetResults();
  setBusy(false);
  analyseBtn.disabled = false;
}

function clearFile() {
  if (isAnalysing) return;
  requestSeq++;
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  previewUrl = null;
  currentFile = null;
  fileInput.value = '';
  preview.removeAttribute('src');

  hide(preview);
  show(dropContent);
  hide(removeBtn);
  hide(fileBar);
  dropZone.classList.remove('has-image');

  resetResults();
  analyseBtn.disabled = true;
}

function resetResults() {
  lastResult = null;
  hide(resultContent);
  hide(errorBanner);
  show(resultsEmpty);
}

// ---------------------------------------------------------------------------
// Model picker
// ---------------------------------------------------------------------------
const FALLBACK_MODELS = [
  { id: 'v2s', name: 'EfficientNetV2-S', available: true },
  { id: 'b0',  name: 'EfficientNet-B0',  available: true },
  { id: 'vit', name: 'ViT-B/16',         available: true },
  { id: 'compare',  available: true },
  { id: 'ensemble', available: true },
];

function modeLabel(m) {
  const t = I18N[currentLang];
  if (m.id === 'compare')  return t.modeCompare;
  if (m.id === 'ensemble') return t.modeEnsemble;
  return m.name;
}

function modeDescription(id) {
  const t = I18N[currentLang];
  return { v2s: t.descV2s, b0: t.descB0, vit: t.descVit, compare: t.descCompare, ensemble: t.descEnsemble }[id] || '';
}

function renderModelPicker() {
  const list = modelInfo.length ? modelInfo : FALLBACK_MODELS;
  const t = I18N[currentLang];
  modelGrid.innerHTML = '';

  const makeGroup = (title, items, cls) => {
    const g = document.createElement('div');
    g.className = 'model-group';
    const h = document.createElement('p');
    h.className = 'model-group__title';
    h.textContent = title;
    const row = document.createElement('div');
    row.className = 'model-group__row ' + cls;
    items.forEach(m => row.appendChild(makeOption(m, t)));
    g.append(h, row);
    modelGrid.appendChild(g);
  };

  const singles = list.filter(m => !['compare', 'ensemble'].includes(m.id));
  const combos = list.filter(m => ['compare', 'ensemble'].includes(m.id));
  makeGroup(t.groupSingle, singles, 'cols-3');
  makeGroup(t.groupMulti, combos, 'cols-2');
  modelDesc.textContent = modeDescription(selectedModel);
}

function makeOption(m, t) {
  const label = document.createElement('label');
  label.className = 'model-opt';
  if (!m.available) label.classList.add('model-opt--off');

  const input = document.createElement('input');
  input.type = 'radio';
  input.name = 'model';
  input.value = m.id;
  input.checked = m.id === selectedModel;
  input.disabled = !m.available || isAnalysing;
  input.addEventListener('change', () => {
    selectedModel = m.id;
    modelDesc.textContent = modeDescription(m.id);
  });

  const span = document.createElement('span');
  span.textContent = modeLabel(m) + (m.available ? '' : ` (${t.unavailable})`);
  label.append(input, span);
  return label;
}

async function loadModelInfo() {
  try {
    const res = await fetch(`${API_BASE}/models`);
    if (!res.ok) throw new Error(String(res.status));
    const data = await res.json();
    modelInfo = data.models || [];
    const sel = modelInfo.find(m => m.id === selectedModel && m.available);
    if (!sel) selectedModel = data.default || modelInfo.find(m => m.available)?.id || 'v2s';
  } catch (_) {
    modelInfo = [];            // backend not reachable yet: show defaults, errors surface on Analyse
  }
  renderModelPicker();
}

function setBusy(busy) {
  isAnalysing = busy;
  const t = I18N[currentLang];
  btnLabel.textContent = busy ? t.btnAnalysing : t.btnAnalyse;
  busy ? hide(btnArrow) : show(btnArrow);
  busy ? show(spinner) : hide(spinner);
  analyseBtn.disabled = busy || !currentFile;
  [removeBtn, removeLink, changeBtn].forEach(b => { b.disabled = busy; });
  modelGrid.querySelectorAll('input').forEach(i => {
    const m = (modelInfo.length ? modelInfo : FALLBACK_MODELS).find(x => x.id === i.value);
    i.disabled = busy || !(m?.available);
  });
}

// ---------------------------------------------------------------------------
// Analyse Action
// ---------------------------------------------------------------------------
async function handleAnalyse() {
  const file = currentFile;
  if (!file || isAnalysing) return;

  const seq = ++requestSeq;
  setBusy(true);
  hide(resultContent);
  hide(resultsEmpty);
  hide(errorBanner);

  try {
    const fd = new FormData();
    fd.append('file', file);
    fd.append('model', selectedModel);

    const res = await fetch(`${API_BASE}/predict`, { method: 'POST', body: fd });
    let data = null;
    try { data = await res.json(); } catch (_) { /* non-JSON error body */ }
    if (seq !== requestSeq) return;            // image changed / removed meanwhile

    if (!res.ok) {
      const d = data?.detail;
      const msg = (typeof d === 'string' ? d : d?.message) || `Server error (${res.status})`;
      renderError(msg);
      return;
    }

    lastResult = data;
    renderResult(data, currentLang);

  } catch (err) {
    if (seq !== requestSeq) return;
    renderError(
      'Could not reach the analysis server. ' +
      'Make sure the backend is running at ' + API_BASE + '.'
    );
  } finally {
    if (seq === requestSeq) setBusy(false);
  }
}

// ---------------------------------------------------------------------------
// Render Result
// ---------------------------------------------------------------------------
function renderResult(data, lang) {
  hide(resultsEmpty);
  hide(errorBanner);

  const t = I18N[lang] || I18N.en;
  const { crop, disease } = parseLabel(data.label, lang);
  cropName.textContent = crop;
  diseaseLabel.textContent = disease;

  // Confidence badge
  const pct = fmtPct(data.confidence);
  const tierName = t.confidenceTiers[data.confidence_tier] || data.confidence_tier;
  confidenceBadge.textContent = `${tierName}: ${pct}`;
  confidenceBadge.dataset.tier = data.confidence_tier;

  // Severity badge
  const sevName = t.severityBands[data.severity_band] || data.severity_band;
  severityBadge.textContent = `${t.severityPrefix}: ${sevName}`;
  severityBadge.dataset.sev = data.severity_band;

  // Confidence bar
  confidenceFill.style.width = pct;
  confidenceLabel.textContent = pct;
  const barColors = { High: '#16a34a', Medium: '#d97706', Low: '#dc2626' };
  confidenceFill.style.background = barColors[data.confidence_tier] || '#2d7a3a';

  // Model tag, top predictions, per-model breakdown
  modelTag.textContent = `${t.modelUsed}: ${data.model_name || ''}`;
  renderTop(data, lang);
  renderBreakdown(data, lang);

  if (data.abstain) {
    show(abstainNotice);
    hide(advisoryCard);
  } else {
    hide(abstainNotice);
    show(advisoryCard);
    if (data.advisory) {
      renderAdvisory(data.advisory, lang);
    }
  }

  show(resultContent);
}

function labelText(label, lang) {
  const { crop, disease } = parseLabel(label, lang);
  return `${crop}: ${disease}`;
}

function renderTop(data, lang) {
  const t = I18N[lang] || I18N.en;
  topList.innerHTML = '';
  const top = data.top || [];
  if (top.length < 2) { hide(topList); return; }
  const h = document.createElement('h4');
  h.className = 'top-list__title';
  h.textContent = t.topTitle;
  topList.appendChild(h);
  top.forEach(item => {
    const row = document.createElement('div');
    row.className = 'top-row';
    const name = document.createElement('span');
    name.className = 'top-row__name';
    name.textContent = labelText(item.label, lang);
    const bar = document.createElement('span');
    bar.className = 'top-row__bar';
    const fill = document.createElement('span');
    fill.style.width = fmtPct(item.confidence);
    bar.appendChild(fill);
    const val = document.createElement('span');
    val.className = 'top-row__val';
    val.textContent = fmtPct(item.confidence);
    row.append(name, bar, val);
    topList.appendChild(row);
  });
  show(topList);
}

function renderBreakdown(data, lang) {
  const t = I18N[lang] || I18N.en;
  const pm = data.per_model;
  if (!pm || pm.length < 2) { hide(breakdown); return; }

  const n = pm.length;
  agreeNote.textContent = data.agreement
    ? t.agreeAll.replace('{n}', n)
    : t.agreeSome.replace('{k}', data.agree_count).replace('{n}', n);
  agreeNote.dataset.agree = data.agreement ? 'yes' : 'no';

  breakdownGrid.innerHTML = '';
  pm.forEach(m => {
    const card = document.createElement('div');
    card.className = 'bd-card' + (m.id === data.model ? ' bd-card--primary' : '');
    const name = document.createElement('p');
    name.className = 'bd-card__name';
    name.textContent = m.name + (m.calibrated ? '' : ` · ${t.uncal}`);
    const lab = document.createElement('p');
    lab.className = 'bd-card__label';
    lab.textContent = labelText(m.label, lang);
    const conf = document.createElement('p');
    conf.className = 'bd-card__conf';
    conf.textContent = fmtPct(m.confidence) + (m.abstain ? ` · ${t.abstainShort}` : '');
    conf.dataset.low = m.abstain ? '1' : '0';
    card.append(name, lab, conf);
    breakdownGrid.appendChild(card);
  });
  show(breakdown);
}

function renderAdvisory(advisory, lang) {
  const entry = advisory?.[lang] ?? advisory?.['en'];
  if (!entry) return;

  const sections = ['symptoms', 'monitoring', 'immediate_actions', 'prevention', 'escalation'];
  for (const sec of sections) {
    const panel = document.getElementById(`section-${sec}`);
    if (panel) panel.textContent = entry[sec] ?? '';
  }
}

function renderError(msg) {
  hide(resultsEmpty);
  hide(resultContent);
  errorMsg.textContent = msg;
  show(errorBanner);
}

// ---------------------------------------------------------------------------
// Advisory Tabs
// ---------------------------------------------------------------------------
function initAdvisoryTabs() {
  document.querySelectorAll('.advisory-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.advisory-tab').forEach(t => {
        t.classList.remove('active');
        t.setAttribute('aria-selected', 'false');
      });
      document.querySelectorAll('.advisory-panel').forEach(p => {
        p.classList.add('hidden');
        p.classList.remove('active');
      });

      tab.classList.add('active');
      tab.setAttribute('aria-selected', 'true');
      const panel = document.getElementById(`section-${tab.dataset.section}`);
      if (panel) {
        panel.classList.remove('hidden');
        panel.classList.add('active');
      }
    });
  });
}

// ---------------------------------------------------------------------------
// Gemini AI Agricultural Specialist Integration
// ---------------------------------------------------------------------------
async function askGeminiAI(question) {
  if (!question || !question.trim()) return;

  const t = I18N[currentLang];
  aiAskBtnText.textContent = t.aiAsking;
  show(aiSpinner);
  aiAskBtn.disabled = true;

  try {
    const contextStr = lastResult ? lastResult.label : 'General Crop Disease Inquiry';
    const res = await fetch(`${API_BASE}/ask-ai`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt: question,
        language: currentLang,
        context: contextStr
      })
    });

    const data = await res.json();
    if (res.ok && data.answer) {
      aiResponseContent.textContent = data.answer;
      show(aiResponseBox);
    } else {
      aiResponseContent.textContent = 'Could not get an answer from Gemini AI. Please check your backend connection.';
      show(aiResponseBox);
    }
  } catch (err) {
    aiResponseContent.textContent = 'Network error connecting to Gemini AI assistant.';
    show(aiResponseBox);
  } finally {
    aiAskBtnText.textContent = t.aiAskBtn;
    hide(aiSpinner);
    aiAskBtn.disabled = false;
  }
}

function initAIConsultation() {
  aiAskBtn.addEventListener('click', () => {
    askGeminiAI(aiPromptInput.value);
  });

  aiPromptInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      askGeminiAI(aiPromptInput.value);
    }
  });

  // Suggestion chips
  document.querySelectorAll('.ai-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      aiPromptInput.value = chip.textContent;
      askGeminiAI(chip.textContent);
    });
  });
}

// ---------------------------------------------------------------------------
// Initialization
// ---------------------------------------------------------------------------
function init() {
  initDropZone();
  initLangToggle();
  initAdvisoryTabs();
  initAIConsultation();
  analyseBtn.addEventListener('click', handleAnalyse);
  applyLanguageToUI(currentLang);
  loadModelInfo();
}

document.addEventListener('DOMContentLoaded', init);
