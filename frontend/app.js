/**
 * Dr. B.R. Ambedkar Digital Heritage Archive - Frontend Application
 */

const API_BASE = (!window.location.origin || window.location.origin === 'null' || window.location.protocol === 'file:')
  ? 'http://localhost:8000'
  : window.location.origin;

let isBackendAvailable = false;
let archiveApiMode = "offline";
let archiveDisplayedCount = 0;
let archiveTotalCount = 0;
let archiveTypeCounts = {};
const ARCHIVE_SEARCH_PAGE_SIZE = 30;
let currentLanguage = 'en';
let aiRecognition = null;
let aiVoiceListening = false;
let aiVoiceStatusKey = "idle";
let aiVoiceHadFinalResult = false;
let currentDocInModal = null;
let timelineEventByDocument = new Map();
let timelineEventByDate = new Map();
let synth = window.speechSynthesis;
let currentUtterance = null;
let lastOcrMetadata = null;
let narrationAudio = null;
let narrationObjectUrl = null;
let narrationRequestController = null;
const originalUiText = new WeakMap();
const originalPlaceholders = new WeakMap();
const originalUiAttributes = new WeakMap();
const UI_TRANSLATIONS = {
  hi: {
    "Government of India • MoSJE": "भारत सरकार • सामाजिक न्याय एवं अधिकारिता मंत्रालय",
    "Kiosk Mode": "कियोस्क मोड",
    "Search & Discover": "खोजें और जानें",
    "Interactive Timeline": "इंटरैक्टिव समयरेखा",
    "Archive Research Assistant": "अभिलेख शोध सहायक",
    "Institutional Analytics": "संस्थागत विश्लेषण",
    "Ingestion Pipeline": "दस्तावेज़ अंतर्ग्रहण प्रक्रिया",
    "FTS5 Sub-Millisecond Search Engine Active": "FTS5 उप-मिलीसेकंड खोज इंजन सक्रिय",
    "Quick Filters:": "त्वरित फ़िल्टर:",
    "CAD Debates": "संविधान सभा की बहसें",
    "Annihilation of Caste": "जाति का विनाश",
    "Directive Principles": "नीति-निर्देशक सिद्धांत",
    "Untouchability": "अस्पृश्यता",
    "Economics & RBI": "अर्थशास्त्र एवं RBI",
    "Buddhism & Dhamma": "बौद्ध धर्म एवं धम्म",
    "Language:": "भाषा:",
    "Type:": "प्रकार:",
    "Source:": "स्रोत:",
    "All (10 Languages)": "सभी (10 भाषाएँ)",
    "All Document Types": "सभी दस्तावेज़ प्रकार",
    "All Repositories": "सभी अभिलेखागार",
    "Publications (423)": "प्रकाशन (423)",
    "Speeches (63)": "भाषण (63)",
    "CAD Debates (20)": "संविधान सभा बहसें (20)",
    "Manuscripts (4)": "पांडुलिपियाँ (4)",
    "Historical Records (20)": "ऐतिहासिक अभिलेख (20)",
    "Search": "खोजें",
    "Chronological Heritage Timeline": "कालक्रमिक विरासत समयरेखा",
    "Read Original Historical Record": "मूल ऐतिहासिक अभिलेख पढ़ें",
    "Institutional Analytics": "संस्थागत विश्लेषण",
    "Total Digitize Items": "कुल डिजिटाइज़्ड सामग्री",
    "Words Indexed (FTS5)": "अनुक्रमित शब्द (FTS5)",
    "Vector RAG Chunks": "वेक्टर RAG खंड",
    "Indian Languages": "भारतीय भाषाएँ",
    "Ingested Language Distribution": "सामग्री की भाषा-वितरण",
    "Archival Source Provenance": "अभिलेखीय स्रोत विवरण",
    "Download registry.json": "registry.json डाउनलोड करें",
    "Download metadata.csv": "metadata.csv डाउनलोड करें",
    "Ambedkar Archive Research Assistant": "आंबेडकर अभिलेख शोध सहायक",
    "Archive Sources": "अभिलेखीय स्रोत",
    "Try asking:": "यह पूछकर देखें:",
    "Hero Worship / Bhakti in Politics": "राजनीति में नायक-पूजा / भक्ति",
    "Parliamentary vs Presidential System": "संसदीय बनाम राष्ट्रपति प्रणाली",
    "Article 356 as 'Dead Letter'": "अनुच्छेद 356: 'निष्क्रिय प्रावधान'",
    "Caste as Division of Labourers": "जाति: श्रमिकों का विभाजन",
    "Ask by voice": "आवाज़ से पूछें",
    "Stop listening": "सुनना बंद करें",
    "Ask": "पूछें",
    "Institutional Upload": "संस्थागत अपलोड",
    "Document Title *": "दस्तावेज़ का शीर्षक *",
    "Author / Speaker *": "लेखक / वक्ता *",
    "Historical Date (YYYY-MM-DD)": "ऐतिहासिक तिथि (YYYY-MM-DD)",
    "Document Type *": "दस्तावेज़ का प्रकार *",
    "Language *": "भाषा *",
    "Tags (Comma-separated)": "टैग (अल्पविराम से अलग करें)",
    "Scan a PDF or image for OCR": "OCR के लिए PDF या छवि स्कैन करें",
    "Extract Text": "पाठ निकालें",
    "Full Text Content *": "पूरा पाठ *",
    "Ingest Document Into Pipeline": "दस्तावेज़ को पाइपलाइन में जोड़ें",
    "Audio Narration (Text-to-Speech)": "ऑडियो वाचन (पाठ से आवाज़)",
    "Executive Summary": "कार्यकारी सारांश",
    "Key Historical Quotes": "प्रमुख ऐतिहासिक उद्धरण",
    "Archival Full Text / Excerpt": "अभिलेख का पूरा पाठ / अंश",
    "Dublin Core Archival Metadata": "Dublin Core अभिलेखीय मेटाडेटा",
    "View Primary Source": "मूल स्रोत देखें",
    "Close": "बंद करें",
    "Ask about Ambedkar's life, writings, speeches, or ideas...": "आंबेडकर के जीवन, लेखन, भाषणों या विचारों के बारे में पूछें...",
    "Search by concept: e.g. 'Parliamentary', 'Untouchability', 'Grammar of Anarchy', 'Rupee'...": "विषय खोजें, जैसे 'संसदीय', 'अस्पृश्यता', 'अराजकता का व्याकरण', 'रुपया'...",
    "OCR text will be placed below for review before ingestion.": "OCR से निकला पाठ नीचे समीक्षा के लिए आएगा; फिर उसे अभिलेख में जोड़ें।",
    "Explore 530+ Digitize Works, Speeches & Constitutional Debates": "530 से अधिक डिजिटाइज़्ड रचनाएँ, भाषण और संविधान सभा की बहसें देखें",
    "Search primary manuscripts, Constituent Assembly records, and Dr. Ambedkar Foundation publications with cross-lingual querying and instant audio narration.": "मूल पांडुलिपियाँ, संविधान सभा के अभिलेख और डॉ. आंबेडकर फाउंडेशन के प्रकाशन खोजें; बहुभाषी खोज और तुरंत ऑडियो वाचन उपलब्ध है।",
    "Trace Dr. B.R. Ambedkar's landmark milestones, constitutional debates, and social justice struggles through verified archival evidence.": "सत्यापित अभिलेखीय साक्ष्यों से डॉ. बी.आर. आंबेडकर के प्रमुख पड़ावों, संवैधानिक बहसों और सामाजिक न्याय के संघर्षों को जानें।",
    "Search indexed archival records for relevant passages and citations. Answers are limited to available archive content; verify important details against the cited source.": "संबंधित अंश और संदर्भ खोजने के लिए अनुक्रमित अभिलेखों में खोजें। उत्तर उपलब्ध सामग्री तक सीमित हैं; महत्वपूर्ण जानकारी उद्धृत स्रोत से जाँचें।",
    "Searching indexed archival records...": "अनुक्रमित अभिलेखों में खोज जारी है...",
    "User Question": "आपका प्रश्न",
    "Archive Evidence": "अभिलेखीय साक्ष्य",
    "View Source": "स्रोत देखें",
    "Sub-2ms Full-Text Retrieval": "2 मिलीसेकंड से कम में पूर्ण-पाठ खोज",
    "Ready for Milvus / ChromaDB": "Milvus / ChromaDB के लिए तैयार",
    "Inclusive Multilingual Access": "समावेशी बहुभाषी पहुँच",
    "Ingestion of Pipeline & Institutional Upload": "दस्तावेज़ पाइपलाइन और संस्थागत अपलोड",
    "Memorial staff and institutional nodes can ingest newly scanned manuscripts, speeches, or debate records directly into the archive pipeline with automated FTS5 indexing.": "स्मारक कर्मचारी और संस्थागत केंद्र नए स्कैन किए दस्तावेज़, भाषण या बहस के अभिलेख सीधे संग्रह में जोड़ सकते हैं; FTS5 अनुक्रमण स्वचालित है।",
    "✓ Ingested successfully into SQLite & FTS5!": "✓ SQLite और FTS5 में सफलतापूर्वक जोड़ा गया!",
    "Accessible readout for visually impaired and low-literacy visitors": "दृष्टिबाधित और कम साक्षरता वाले आगंतुकों के लिए सुलभ वाचन",
    "Ready": "तैयार",
    "Problem Statement ID: 26096 — Digital Heritage Archive for Memorials & Dr. B.R. Ambedkar": "समस्या विवरण ID: 26096 — स्मारकों और डॉ. बी.आर. आंबेडकर का डिजिटल विरासत संग्रह",
    "Developed for Smart India Hackathon • Smart Education Theme": "स्मार्ट इंडिया हैकाथॉन • स्मार्ट शिक्षा विषय के लिए विकसित",
    "English (410)": "अंग्रेज़ी (410)",
    "Hindi (42)": "हिंदी (42)",
    "Telugu (27)": "तेलुगु (27)",
    "Marathi (18)": "मराठी (18)",
    "Bengali (11)": "बंगाली (11)",
    "Tamil (9)": "तमिल (9)",
    "Gujarati (9)": "गुजराती (9)",
    "Internet Archive (510)": "इंटरनेट आर्काइव (510)",
    "Constituent Assembly (10)": "संविधान सभा (10)",
    "Dr. Ambedkar Foundation (10)": "डॉ. आंबेडकर फाउंडेशन (10)",
  },
  mr: {
    "Government of India • MoSJE": "भारत सरकार • सामाजिक न्याय आणि अधिकारिता मंत्रालय",
    "Kiosk Mode": "किऑस्क मोड",
    "Search & Discover": "शोधा आणि जाणून घ्या",
    "Interactive Timeline": "परस्परसंवादी कालरेषा",
    "Archive Research Assistant": "अभिलेख संशोधन सहाय्यक",
    "Institutional Analytics": "संस्थात्मक विश्लेषण",
    "Ingestion Pipeline": "दस्तऐवज समावेशन प्रक्रिया",
    "FTS5 Sub-Millisecond Search Engine Active": "FTS5 उप-मिलीसेकंद शोध इंजिन सक्रिय",
    "Quick Filters:": "जलद फिल्टर:",
    "CAD Debates": "संविधान सभेतील चर्चा",
    "Annihilation of Caste": "जातिभेदाचे उच्चाटन",
    "Directive Principles": "मार्गदर्शक तत्त्वे",
    "Untouchability": "अस्पृश्यता",
    "Economics & RBI": "अर्थशास्त्र आणि RBI",
    "Buddhism & Dhamma": "बौद्ध धर्म आणि धम्म",
    "Language:": "भाषा:",
    "Type:": "प्रकार:",
    "Source:": "स्रोत:",
    "All (10 Languages)": "सर्व (10 भाषा)",
    "All Document Types": "सर्व दस्तऐवज प्रकार",
    "All Repositories": "सर्व संग्रहालये",
    "Publications (423)": "प्रकाशने (423)",
    "Speeches (63)": "भाषणे (63)",
    "CAD Debates (20)": "संविधान सभा चर्चा (20)",
    "Manuscripts (4)": "हस्तलिखिते (4)",
    "Historical Records (20)": "ऐतिहासिक नोंदी (20)",
    "Search": "शोधा",
    "Chronological Heritage Timeline": "कालानुक्रमिक वारसा कालरेषा",
    "Read Original Historical Record": "मूळ ऐतिहासिक नोंद वाचा",
    "Total Digitize Items": "एकूण डिजिटाइज्ड नोंदी",
    "Words Indexed (FTS5)": "अनुक्रमित शब्द (FTS5)",
    "Vector RAG Chunks": "व्हेक्टर RAG विभाग",
    "Indian Languages": "भारतीय भाषा",
    "Ingested Language Distribution": "संग्रहातील भाषांचे वितरण",
    "Archival Source Provenance": "अभिलेखीय स्रोत तपशील",
    "Download registry.json": "registry.json डाउनलोड करा",
    "Download metadata.csv": "metadata.csv डाउनलोड करा",
    "Ambedkar Archive Research Assistant": "आंबेडकर अभिलेख संशोधन सहाय्यक",
    "Archive Sources": "अभिलेखीय स्रोत",
    "Try asking:": "हे विचारून पाहा:",
    "Hero Worship / Bhakti in Politics": "राजकारणातील नायकपूजा / भक्ती",
    "Parliamentary vs Presidential System": "संसदीय विरुद्ध अध्यक्षीय पद्धत",
    "Article 356 as 'Dead Letter'": "कलम 356: 'निष्क्रिय तरतूद'",
    "Caste as Division of Labourers": "जात: श्रमिकांचे विभाजन",
    "Ask by voice": "आवाजाने विचारा",
    "Stop listening": "ऐकणे थांबवा",
    "Ask": "विचारा",
    "Institutional Upload": "संस्थात्मक अपलोड",
    "Document Title *": "दस्तऐवजाचे शीर्षक *",
    "Author / Speaker *": "लेखक / वक्ते *",
    "Historical Date (YYYY-MM-DD)": "ऐतिहासिक दिनांक (YYYY-MM-DD)",
    "Document Type *": "दस्तऐवजाचा प्रकार *",
    "Language *": "भाषा *",
    "Tags (Comma-separated)": "टॅग (स्वल्पविरामाने वेगळे करा)",
    "Scan a PDF or image for OCR": "OCR साठी PDF किंवा प्रतिमा स्कॅन करा",
    "Extract Text": "मजकूर काढा",
    "Full Text Content *": "संपूर्ण मजकूर *",
    "Ingest Document Into Pipeline": "दस्तऐवज पाइपलाइनमध्ये जोडा",
    "Audio Narration (Text-to-Speech)": "ध्वनी वाचन (मजकूर ते आवाज)",
    "Executive Summary": "कार्यकारी सारांश",
    "Key Historical Quotes": "महत्त्वाचे ऐतिहासिक उद्धरण",
    "Archival Full Text / Excerpt": "अभिलेखाचा संपूर्ण मजकूर / उतारा",
    "Dublin Core Archival Metadata": "Dublin Core अभिलेखीय मेटाडेटा",
    "View Primary Source": "मूळ स्रोत पहा",
    "Close": "बंद करा",
    "Ask about Ambedkar's life, writings, speeches, or ideas...": "आंबेडकरांचे जीवन, लेखन, भाषणे किंवा विचार यांबद्दल विचारा...",
    "Search by concept: e.g. 'Parliamentary', 'Untouchability', 'Grammar of Anarchy', 'Rupee'...": "संकल्पना शोधा, उदा. 'संसदीय', 'अस्पृश्यता', 'अराजकतेचे व्याकरण', 'रुपया'...",
    "OCR text will be placed below for review before ingestion.": "OCR मधून मिळालेला मजकूर तपासणीसाठी खाली दिसेल; त्यानंतर तो संग्रहात जोडा.",
    "Explore 530+ Digitize Works, Speeches & Constitutional Debates": "530 हून अधिक डिजिटाइज्ड लेखन, भाषणे आणि संविधान सभेतील चर्चा पाहा",
    "Search primary manuscripts, Constituent Assembly records, and Dr. Ambedkar Foundation publications with cross-lingual querying and instant audio narration.": "मूळ हस्तलिखिते, संविधान सभेच्या नोंदी आणि डॉ. आंबेडकर फाउंडेशनची प्रकाशने शोधा; बहुभाषिक शोध आणि तत्काळ ध्वनीवाचन उपलब्ध आहे.",
    "Trace Dr. B.R. Ambedkar's landmark milestones, constitutional debates, and social justice struggles through verified archival evidence.": "सत्यापित अभिलेखीय पुराव्यांमधून डॉ. बी.आर. आंबेडकरांचे महत्त्वाचे टप्पे, घटनात्मक चर्चा आणि सामाजिक न्यायाचे संघर्ष जाणून घ्या.",
    "Search indexed archival records for relevant passages and citations. Answers are limited to available archive content; verify important details against the cited source.": "संबंधित उतारे आणि संदर्भांसाठी अनुक्रमित अभिलेख शोधा. उत्तरे उपलब्ध संग्रहापुरती मर्यादित आहेत; महत्त्वाचे तपशील दिलेल्या स्रोतावरून पडताळा.",
    "Searching indexed archival records...": "अनुक्रमित अभिलेख शोधत आहे...",
    "User Question": "तुमचा प्रश्न",
    "Archive Evidence": "अभिलेखीय पुरावा",
    "View Source": "स्रोत पहा",
    "Sub-2ms Full-Text Retrieval": "2 मिलिसेकंदांपेक्षा कमी वेळेत पूर्ण-मजकूर शोध",
    "Ready for Milvus / ChromaDB": "Milvus / ChromaDB साठी सज्ज",
    "Inclusive Multilingual Access": "समावेशक बहुभाषिक प्रवेश",
    "Ingestion of Pipeline & Institutional Upload": "दस्तऐवज पाइपलाइन आणि संस्थात्मक अपलोड",
    "Memorial staff and institutional nodes can ingest newly scanned manuscripts, speeches, or debate records directly into the archive pipeline with automated FTS5 indexing.": "स्मारक कर्मचारी आणि संस्थात्मक केंद्रे नव्याने स्कॅन केलेली हस्तलिखिते, भाषणे किंवा चर्चेच्या नोंदी थेट संग्रहात जोडू शकतात; FTS5 अनुक्रमण स्वयंचलित आहे.",
    "✓ Ingested successfully into SQLite & FTS5!": "✓ SQLite आणि FTS5 मध्ये यशस्वीरीत्या जोडले!",
    "Accessible readout for visually impaired and low-literacy visitors": "दृष्टिदोष असलेल्या आणि कमी साक्षरता असलेल्या अभ्यागतांसाठी सुलभ वाचन",
    "Ready": "तयार",
    "Problem Statement ID: 26096 — Digital Heritage Archive for Memorials & Dr. B.R. Ambedkar": "समस्या विधान ID: 26096 — स्मारके आणि डॉ. बी.आर. आंबेडकर यांचा डिजिटल वारसा संग्रह",
    "Developed for Smart India Hackathon • Smart Education Theme": "स्मार्ट इंडिया हॅकाथॉन • स्मार्ट शिक्षण विषयासाठी विकसित",
    "English (410)": "इंग्रजी (410)",
    "Hindi (42)": "हिंदी (42)",
    "Telugu (27)": "तेलुगू (27)",
    "Marathi (18)": "मराठी (18)",
    "Bengali (11)": "बंगाली (11)",
    "Tamil (9)": "तमिळ (9)",
    "Gujarati (9)": "गुजराती (9)",
    "Internet Archive (510)": "इंटरनेट आर्काइव्ह (510)",
    "Constituent Assembly (10)": "संविधान सभा (10)",
    "Dr. Ambedkar Foundation (10)": "डॉ. आंबेडकर फाउंडेशन (10)",
  }
};

// Preset Grounded Responses for Constitutional AI Assistant
const TIMELINE_TRANSLATIONS = {
  hi: {
    "Castes in India Paper at Columbia University": "कोलंबिया विश्वविद्यालय में भारत में जाति पर शोधपत्र",
    "Academic / Anthropology": "शैक्षणिक / मानवविज्ञान",
    "Presents first seminal paper on endogamy and mechanisms of caste reproduction at Columbia University.": "कोलंबिया विश्वविद्यालय में अंतर्विवाह और जाति के पुनरुत्पादन की प्रक्रियाओं पर पहला महत्वपूर्ण शोधपत्र प्रस्तुत किया।",
    "Launch of 'Muknayak' (Voice of the Mute)": "‘मूकनायक’ का शुभारंभ (मूक लोगों की आवाज़)",
    "Journalism & Social Awakening": "पत्रकारिता एवं सामाजिक जागरण",
    "Founds Marathi fortnightly declaring journalism as an instrument of emancipation for silenced millions.": "मौन कराए गए लाखों लोगों की मुक्ति के साधन के रूप में पत्रकारिता को प्रस्तुत करते हुए मराठी पाक्षिक की स्थापना की।",
    "Problem of the Rupee (London School of Economics)": "रुपये की समस्या (लंदन स्कूल ऑफ इकोनॉमिक्स)",
    "Economics & Monetary Policy": "अर्थशास्त्र एवं मौद्रिक नीति",
    "Submits D.Sc. dissertation establishing monetary stabilization principles that led to the Reserve Bank of India.": "मौद्रिक स्थिरता के सिद्धांतों पर D.Sc. शोधप्रबंध प्रस्तुत किया, जिसने भारतीय रिज़र्व बैंक की स्थापना की दिशा में योगदान दिया।",
    "Mahad Satyagraha (Chavdar Tale Water Rights)": "महाड़ सत्याग्रह (चवदार तालाब में जल अधिकार)",
    "Civil Rights Movement": "नागरिक अधिकार आंदोलन",
    "Leads historic non-violent assertion of civic equality and universal human rights to public drinking water.": "सार्वजनिक पेयजल तक पहुँच के लिए नागरिक समानता और सार्वभौमिक मानवाधिकारों का ऐतिहासिक अहिंसक आंदोलन नेतृत्व किया।",
    "The Poona Pact Agreement": "पूना समझौता",
    "Political Representation": "राजनीतिक प्रतिनिधित्व",
    "Secures 148 reserved legislative seats for the Depressed Classes across provincial assemblies.": "प्रांतीय विधानसभाओं में वंचित वर्गों के लिए 148 आरक्षित सीटें सुनिश्चित कीं।",
    "Annihilation of Caste Published": "‘जाति का विनाश’ प्रकाशित",
    "Social Justice & Philosophy": "सामाजिक न्याय एवं दर्शन",
    "Publishes profound critique demonstrating caste as an unnatural division of labourers requiring eradication of orthodox sanctions.": "जाति को श्रमिकों का अस्वाभाविक विभाजन बताते हुए रूढ़िवादी धार्मिक समर्थन को समाप्त करने की आवश्यकता पर आधारित प्रभावशाली आलोचना प्रकाशित की।",
    "Maiden Address to the Constituent Assembly": "संविधान सभा में पहला संबोधन",
    "Constitution Making": "संविधान निर्माण",
    "Plea for national unity, mutual statesmanship, and constitutional justice for all communities.": "राष्ट्रीय एकता, पारस्परिक विवेकशीलता और सभी समुदायों के लिए संवैधानिक न्याय की अपील की।",
    "Appointed Chairman of the Drafting Committee": "प्रारूप समिति के अध्यक्ष नियुक्त",
    "Constitutional Architect": "संविधान के शिल्पकार",
    "Appointed to lead the drafting of the Constitution of the Republic of India as Law Minister.": "कानून मंत्री के रूप में भारत गणराज्य के संविधान का प्रारूप तैयार करने वाली समिति का नेतृत्व करने के लिए नियुक्त किए गए।",
    "Introduction of the Draft Constitution": "संविधान के प्रारूप का प्रस्तुतिकरण",
    "Constitutional Jurisprudence": "संवैधानिक न्यायशास्त्र",
    "Outlines Parliamentary executive model, flexible federalism, and fundamental rights protections.": "संसदीय कार्यपालिका, लचीले संघवाद और मौलिक अधिकारों की सुरक्षा का प्रारूप प्रस्तुत किया।",
    "Abolition of Untouchability (Article 17 Adopted)": "अस्पृश्यता का उन्मूलन (अनुच्छेद 17 स्वीकृत)",
    "Fundamental Rights": "मौलिक अधिकार",
    "Draft Article 11 unanimously adopted, outlawing untouchability and penalizing its enforcement.": "मसौदा अनुच्छेद 11 सर्वसम्मति से स्वीकृत हुआ; इसने अस्पृश्यता को गैरकानूनी घोषित किया और इसके पालन को दंडनीय बनाया।",
    "Final Constituent Assembly Address (Grammar of Anarchy)": "संविधान सभा का अंतिम संबोधन (अराजकता का व्याकरण)",
    "Democratic Philosophy": "लोकतांत्रिक दर्शन",
    "Urges social democracy to sustain political democracy, warns against hero-worship/Bhakti in politics.": "राजनीतिक लोकतंत्र को टिकाए रखने के लिए सामाजिक लोकतंत्र का आग्रह किया और राजनीति में नायक-पूजा/भक्ति के विरुद्ध चेताया।",
    "Deekshabhoomi Nagpur Buddhist Conversion": "नागपुर की दीक्षाभूमि में बौद्ध दीक्षा",
    "Spiritual Emancipation": "आध्यात्मिक मुक्ति",
    "Embraces Buddhism with 500,000 followers, enshrining 22 vows for egalitarian and rational life.": "500,000 अनुयायियों के साथ बौद्ध धर्म अपनाया और समतामूलक, विवेकशील जीवन के लिए 22 प्रतिज्ञाएँ दीं।"
  },
  mr: {
    "Castes in India Paper at Columbia University": "कोलंबिया विद्यापीठातील भारतातील जातींवरील निबंध",
    "Academic / Anthropology": "शैक्षणिक / मानववंशशास्त्र",
    "Presents first seminal paper on endogamy and mechanisms of caste reproduction at Columbia University.": "कोलंबिया विद्यापीठात अंतर्विवाह आणि जातिपुनरुत्पादनाच्या प्रक्रियांवरील पहिला महत्त्वपूर्ण निबंध सादर केला।",
    "Launch of 'Muknayak' (Voice of the Mute)": "‘मूकनायक’चा प्रारंभ (मूक लोकांचा आवाज)",
    "Journalism & Social Awakening": "पत्रकारिता आणि सामाजिक जागृती",
    "Founds Marathi fortnightly declaring journalism as an instrument of emancipation for silenced millions.": "वंचित लाखोंच्या मुक्तीसाठी पत्रकारिता हे साधन असल्याचे सांगत मराठी पाक्षिक सुरू केले।",
    "Problem of the Rupee (London School of Economics)": "रुपयाची समस्या (लंडन स्कूल ऑफ इकॉनॉमिक्स)",
    "Economics & Monetary Policy": "अर्थशास्त्र आणि चलनविषयक धोरण",
    "Submits D.Sc. dissertation establishing monetary stabilization principles that led to the Reserve Bank of India.": "चलनस्थैर्याची तत्त्वे मांडणारा D.Sc. प्रबंध सादर केला; या विचारांनी भारतीय रिझर्व्ह बँकेच्या स्थापनेला दिशा दिली।",
    "Mahad Satyagraha (Chavdar Tale Water Rights)": "महाड सत्याग्रह (चवदार तळ्यावरील जलहक्क)",
    "Civil Rights Movement": "नागरी हक्क चळवळ",
    "Leads historic non-violent assertion of civic equality and universal human rights to public drinking water.": "सार्वजनिक पिण्याच्या पाण्यावरील हक्कासाठी नागरी समानता आणि सार्वत्रिक मानवाधिकारांचा ऐतिहासिक अहिंसक लढा उभारला।",
    "The Poona Pact Agreement": "पुणे करार",
    "Political Representation": "राजकीय प्रतिनिधित्व",
    "Secures 148 reserved legislative seats for the Depressed Classes across provincial assemblies.": "प्रांतिक विधानसभांमध्ये वंचित वर्गांसाठी 148 राखीव जागा मिळवल्या।",
    "Annihilation of Caste Published": "‘जातिभेदाचे उच्चाटन’ प्रकाशित",
    "Social Justice & Philosophy": "सामाजिक न्याय आणि तत्त्वज्ञान",
    "Publishes profound critique demonstrating caste as an unnatural division of labourers requiring eradication of orthodox sanctions.": "जात म्हणजे श्रमिकांचे अनैसर्गिक विभाजन असल्याचे स्पष्ट करणारी आणि रूढीवादी धार्मिक मान्यता नष्ट करण्याची गरज मांडणारी प्रभावी टीका प्रकाशित केली।",
    "Maiden Address to the Constituent Assembly": "संविधान सभेतील पहिले भाषण",
    "Constitution Making": "संविधान निर्मिती",
    "Plea for national unity, mutual statesmanship, and constitutional justice for all communities.": "राष्ट्रीय ऐक्य, परस्पर विवेकशीलता आणि सर्व समुदायांसाठी घटनात्मक न्यायाचे आवाहन केले।",
    "Appointed Chairman of the Drafting Committee": "मसुदा समितीचे अध्यक्ष म्हणून नियुक्ती",
    "Constitutional Architect": "संविधानाचे शिल्पकार",
    "Appointed to lead the drafting of the Constitution of the Republic of India as Law Minister.": "कायदा मंत्री म्हणून भारताच्या संविधानाचा मसुदा तयार करणाऱ्या समितीचे नेतृत्व करण्यासाठी नियुक्ती झाली।",
    "Introduction of the Draft Constitution": "संविधानाच्या मसुद्याची मांडणी",
    "Constitutional Jurisprudence": "घटनात्मक न्यायशास्त्र",
    "Outlines Parliamentary executive model, flexible federalism, and fundamental rights protections.": "संसदीय कार्यकारी पद्धती, लवचिक संघराज्य व्यवस्था आणि मूलभूत हक्कांच्या संरक्षणाची रूपरेषा मांडली।",
    "Abolition of Untouchability (Article 17 Adopted)": "अस्पृश्यतेचे उच्चाटन (कलम 17 स्वीकृत)",
    "Fundamental Rights": "मूलभूत हक्क",
    "Draft Article 11 unanimously adopted, outlawing untouchability and penalizing its enforcement.": "मसुदा कलम 11 एकमताने स्वीकारले गेले; अस्पृश्यता बेकायदेशीर ठरवून तिच्या अंमलबजावणीस दंडनीय केले।",
    "Final Constituent Assembly Address (Grammar of Anarchy)": "संविधान सभेतील अंतिम भाषण (अराजकतेचे व्याकरण)",
    "Democratic Philosophy": "लोकशाही तत्त्वज्ञान",
    "Urges social democracy to sustain political democracy, warns against hero-worship/Bhakti in politics.": "राजकीय लोकशाही टिकवण्यासाठी सामाजिक लोकशाहीचा आग्रह धरला आणि राजकारणातील व्यक्तिपूजा/भक्तीबद्दल इशारा दिला।",
    "Deekshabhoomi Nagpur Buddhist Conversion": "नागपूरच्या दीक्षाभूमीतील बौद्ध दीक्षा",
    "Spiritual Emancipation": "आध्यात्मिक मुक्ती",
    "Embraces Buddhism with 500,000 followers, enshrining 22 vows for egalitarian and rational life.": "500,000 अनुयायांसह बौद्ध धर्म स्वीकारला आणि समतावादी, विवेकी जीवनासाठी 22 प्रतिज्ञा दिल्या।"
  }
};

// The top selector changes interface language; archive records retain their source language.
Object.assign(UI_TRANSLATIONS.hi, {
  "Government of India · MoSJE": "भारत सरकार · सामाजिक न्याय एवं अधिकारिता मंत्रालय",
  "Digital Heritage": "डिजिटल विरासत",
  "Archive": "अभिलेखागार",
  "Timeline": "समयरेखा",
  "Research": "शोध",
  "About": "परिचय",
  "Contribute": "योगदान",
  "A living record of ideas that shaped a nation": "राष्ट्र को आकार देने वाले विचारों का जीवंत अभिलेख",
  "Preserving the intellectual legacy of Dr. B. R. Ambedkar.": "डॉ. बी. आर. आंबेडकर की बौद्धिक विरासत का संरक्षण",
  "Explore writings, speeches, constitutional debates and historical records through a searchable digital heritage archive.": "खोज योग्य डिजिटल विरासत संग्रह में लेखन, भाषण, संविधान सभा की बहसें और ऐतिहासिक अभिलेख देखें।",
  "digitized records": "डिजिटाइज़्ड अभिलेख",
  "languages": "भाषाएँ",
  "founding debates": "संविधान सभा की बहसें",
  "Search writings, speeches, debates, or ideas…": "लेखन, भाषण, बहसें या विचार खोजें…",
  "Record language:": "अभिलेख की भाषा:",
  "Inspect": "देखें",
  "Choose a record language to see its available sources.": "किसी भाषा के अभिलेखों के स्रोत देखने के लिए भाषा चुनें।",
  "Offline preview includes English records only. Connect to the archive to search records in this language.": "ऑफ़लाइन पूर्वावलोकन में केवल अंग्रेज़ी अभिलेख हैं। इस भाषा के अभिलेख खोजने के लिए संग्रह सर्वर से जुड़ें।",
  "No documents found matching your query criteria.": "आपकी खोज से मेल खाने वाले दस्तावेज़ नहीं मिले।",
  "Archive service unavailable · preview records shown": "अभिलेख सेवा उपलब्ध नहीं · नमूना अभिलेख दिखाए जा रहे हैं",
  "Kannada (1)": "कन्नड़ (1)",
  "Malayalam (1)": "मलयालम (1)",
  "Punjabi (2)": "पंजाबी (2)",
  "Internet Archive (390)": "इंटरनेट आर्काइव (390)",
  "Dr. Ambedkar International Centre": "डॉ. आंबेडकर अंतरराष्ट्रीय केंद्र",
  "Total Digitize Items": "कुल डिजिटाइज़्ड अभिलेख",
  "English records": "अंग्रेज़ी अभिलेख",
  "Identifier": "पहचान संख्या",
  "Reference": "संदर्भ",
  "Pages / Words": "पृष्ठ / शब्द",
  "Language": "भाषा",
  "Condition": "स्थिति",
  "Access Rights": "पहुँच अधिकार",
  "Internet Archive (Open Public Domain)": "इंटरनेट आर्काइव (सार्वजनिक डोमेन)",
  "Constituent Assembly Debates (Lok Sabha)": "संविधान सभा की बहसें (लोकसभा)",
  "Dr. Ambedkar Foundation / BAWS": "डॉ. आंबेडकर फाउंडेशन / BAWS",
  "publication": "प्रकाशन",
  "speech": "भाषण",
  "debate": "बहस",
  "manuscript": "पांडुलिपि",
  "IA": "इंटरनेट आर्काइव",
  "CAD": "संविधान सभा",
  "Foundation": "डॉ. आंबेडकर फाउंडेशन",
  "Reading historical document…": "ऐतिहासिक दस्तावेज़ पढ़ा जा रहा है…",
  "Choose a PDF or image first.": "पहले PDF या छवि चुनें।",
  "Switch to dark theme": "गहरे रंग की थीम चालू करें",
  "Switch to light theme": "हल्के रंग की थीम चालू करें",
  "Clear search": "खोज साफ़ करें",
  "Search the digital archive": "डिजिटल अभिलेखागार में खोजें",
  "Dr. B. R. Ambedkar holding a copy of the Constitution of India": "भारत का संविधान लिए डॉ. बी. आर. आंबेडकर",
  "Ambedkar Archive Research Assistant": "आंबेडकर अभिलेख शोध सहायक",
  "Archive Sources": "अभिलेख स्रोत",
  "Search indexed archival records for relevant passages and citations. Answers are limited to available archive content; verify important details against the cited source.": "प्रासंगिक अंश और संदर्भ खोजने के लिए अनुक्रमित अभिलेख देखें। उत्तर उपलब्ध अभिलेखों पर आधारित हैं; महत्वपूर्ण जानकारी को उद्धृत स्रोत से जाँचें।",
  "Try asking:": "यह पूछकर देखें:",
  "Hero Worship / Bhakti in Politics": "राजनीति में व्यक्तिपूजा / भक्ति",
  "Parliamentary vs Presidential System": "संसदीय और राष्ट्रपति प्रणाली",
  "Article 356 as 'Dead Letter'": "अनुच्छेद 356 और ‘निष्क्रिय प्रावधान’",
  "Caste as Division of Labourers": "जाति: श्रमिकों का विभाजन",
  "Archival Constitutional Assistant": "संवैधानिक अभिलेख सहायक",
  "Ask about Ambedkar's life, writings, speeches, or historical context. Answers are based on indexed archive records and include source excerpts when available.": "आंबेडकर के जीवन, लेखन, भाषण या ऐतिहासिक संदर्भ के बारे में पूछें। उत्तर अनुक्रमित अभिलेखों पर आधारित हैं और उपलब्ध होने पर स्रोत अंश भी दिखाते हैं।",
  "Ask about Ambedkar's life, writings, speeches, or ideas...": "आंबेडकर के जीवन, लेखन, भाषण या विचारों के बारे में पूछें…",
  "Ask": "पूछें"
});

Object.assign(UI_TRANSLATIONS.mr, {
  "Government of India · MoSJE": "भारत सरकार · सामाजिक न्याय आणि अधिकारिता मंत्रालय",
  "Digital Heritage": "डिजिटल वारसा",
  "Archive": "अभिलेखागार",
  "Timeline": "कालरेषा",
  "Research": "संशोधन",
  "About": "माहिती",
  "Contribute": "योगदान",
  "A living record of ideas that shaped a nation": "राष्ट्राला आकार देणाऱ्या विचारांचा जिवंत अभिलेख",
  "Preserving the intellectual legacy of Dr. B. R. Ambedkar.": "डॉ. बी. आर. आंबेडकरांचा वैचारिक वारसा जतन करत आहोत",
  "Explore writings, speeches, constitutional debates and historical records through a searchable digital heritage archive.": "शोधता येणाऱ्या डिजिटल वारसा संग्रहात लेखन, भाषणे, संविधान सभेतील चर्चा आणि ऐतिहासिक नोंदी पाहा.",
  "digitized records": "डिजिटाइज्ड नोंदी",
  "languages": "भाषा",
  "founding debates": "संविधान सभेतील चर्चा",
  "Search writings, speeches, debates, or ideas…": "लेखन, भाषणे, चर्चा किंवा विचार शोधा…",
  "Record language:": "नोंदींची भाषा:",
  "Inspect": "पाहा",
  "Choose a record language to see its available sources.": "भाषेतील नोंदींचे स्रोत पाहण्यासाठी भाषा निवडा.",
  "Offline preview includes English records only. Connect to the archive to search records in this language.": "ऑफलाइन पूर्वावलोकनात फक्त इंग्रजी नोंदी आहेत. या भाषेतील नोंदी शोधण्यासाठी संग्रह सर्व्हरशी जोडा.",
  "No documents found matching your query criteria.": "तुमच्या शोधाशी जुळणारी कागदपत्रे सापडली नाहीत.",
  "Archive service unavailable · preview records shown": "अभिलेख सेवा उपलब्ध नाही · नमुना नोंदी दाखवत आहोत",
  "Kannada (1)": "कन्नड (1)",
  "Malayalam (1)": "मल्याळम (1)",
  "Punjabi (2)": "पंजाबी (2)",
  "Internet Archive (390)": "इंटरनेट आर्काइव्ह (390)",
  "Dr. Ambedkar International Centre": "डॉ. आंबेडकर आंतरराष्ट्रीय केंद्र",
  "Total Digitize Items": "एकूण डिजिटाइज्ड नोंदी",
  "English records": "इंग्रजी नोंदी",
  "Identifier": "ओळख क्रमांक",
  "Reference": "संदर्भ",
  "Pages / Words": "पृष्ठे / शब्द",
  "Language": "भाषा",
  "Condition": "स्थिती",
  "Access Rights": "प्रवेश अधिकार",
  "Internet Archive (Open Public Domain)": "इंटरनेट आर्काइव्ह (सार्वजनिक डोमेन)",
  "Constituent Assembly Debates (Lok Sabha)": "संविधान सभेतील चर्चा (लोकसभा)",
  "Dr. Ambedkar Foundation / BAWS": "डॉ. आंबेडकर फाउंडेशन / BAWS",
  "publication": "प्रकाशन",
  "speech": "भाषण",
  "debate": "चर्चा",
  "manuscript": "हस्तलिखित",
  "IA": "इंटरनेट आर्काइव्ह",
  "CAD": "संविधान सभा",
  "Foundation": "डॉ. आंबेडकर फाउंडेशन",
  "Reading historical document…": "ऐतिहासिक दस्तऐवज वाचत आहे…",
  "Choose a PDF or image first.": "प्रथम PDF किंवा प्रतिमा निवडा.",
  "Switch to dark theme": "गडद रंगसंगती लावा",
  "Switch to light theme": "फिकट रंगसंगती लावा",
  "Clear search": "शोध पुसा",
  "Search the digital archive": "डिजिटल अभिलेखागारात शोधा",
  "Dr. B. R. Ambedkar holding a copy of the Constitution of India": "भारताचे संविधान हातात घेतलेले डॉ. बी. आर. आंबेडकर",
  "Ambedkar Archive Research Assistant": "आंबेडकर अभिलेख संशोधन सहाय्यक",
  "Archive Sources": "अभिलेख स्रोत",
  "Search indexed archival records for relevant passages and citations. Answers are limited to available archive content; verify important details against the cited source.": "संबंधित उतारे आणि संदर्भ शोधण्यासाठी अनुक्रमित अभिलेख तपासा. उत्तरे उपलब्ध अभिलेखांवर आधारित आहेत; महत्त्वाची माहिती उद्धृत स्रोतामधून पडताळा.",
  "Try asking:": "हे प्रश्न विचारा:",
  "Hero Worship / Bhakti in Politics": "राजकारणातील व्यक्तिपूजा / भक्ती",
  "Parliamentary vs Presidential System": "संसदीय आणि अध्यक्षीय पद्धत",
  "Article 356 as 'Dead Letter'": "कलम 356: ‘निष्क्रिय तरतूद’",
  "Caste as Division of Labourers": "जात: कामगारांची विभागणी",
  "Archival Constitutional Assistant": "संवैधानिक अभिलेख सहाय्यक",
  "Ask about Ambedkar's life, writings, speeches, or historical context. Answers are based on indexed archive records and include source excerpts when available.": "आंबेडकरांचे जीवन, लेखन, भाषणे किंवा ऐतिहासिक संदर्भ विचारा. उत्तरे अनुक्रमित अभिलेखांवर आधारित आहेत आणि उपलब्ध असल्यास स्रोत उतारेही दाखवतात.",
  "Ask about Ambedkar's life, writings, speeches, or ideas...": "आंबेडकरांचे जीवन, लेखन, भाषणे किंवा विचारांबद्दल विचारा…",
  "Ask": "विचारा"
});

// Counts and provenance are from the current archive metadata registry.
const ARCHIVE_LANGUAGE_SOURCES = {
  en: { IA: 390, CAD: 10, Foundation: 10 }, hi: { IA: 42 }, te: { IA: 27 }, mr: { IA: 18 },
  bn: { IA: 11 }, ta: { IA: 9 }, gu: { IA: 9 }, pa: { IA: 2 }, ml: { IA: 1 }, ka: { IA: 1 }
};
const ARCHIVE_LANGUAGES = {
  en: { en: "English", hi: "अंग्रेज़ी", mr: "इंग्रजी" }, hi: { en: "Hindi", hi: "हिंदी", mr: "हिंदी" },
  te: { en: "Telugu", hi: "तेलुगु", mr: "तेलुगू" }, mr: { en: "Marathi", hi: "मराठी", mr: "मराठी" },
  bn: { en: "Bengali", hi: "बंगाली", mr: "बंगाली" }, ta: { en: "Tamil", hi: "तमिल", mr: "तमिळ" },
  gu: { en: "Gujarati", hi: "गुजराती", mr: "गुजराती" }, pa: { en: "Punjabi", hi: "पंजाबी", mr: "पंजाबी" },
  ml: { en: "Malayalam", hi: "मलयालम", mr: "मल्याळम" }, ka: { en: "Kannada", hi: "कन्नड़", mr: "कन्नड" }
};
const ARCHIVE_SOURCES = {
  IA: { en: "Internet Archive", hi: "इंटरनेट आर्काइव", mr: "इंटरनेट आर्काइव्ह" },
  CAD: { en: "Constituent Assembly", hi: "संविधान सभा", mr: "संविधान सभा" },
  Foundation: { en: "Dr. Ambedkar Foundation", hi: "डॉ. आंबेडकर फाउंडेशन", mr: "डॉ. आंबेडकर फाउंडेशन" },
  NDL: { en: "National Digital Library of India", hi: "भारत का राष्ट्रीय डिजिटल पुस्तकालय", mr: "भारताचे राष्ट्रीय डिजिटल ग्रंथालय" }
};
const ARCHIVE_SOURCE_TOTALS = { IA: 510, CAD: 10, Foundation: 10, NDL: 0 };
const SOURCE_HINT_COPY = {
  en: {
    all: "Choose a record language to see its available sources.",
    prefix: "Sources for", suffix: "records:",
    offline: "Offline preview includes English records only. Connect to the archive to search records in this language."
  },
  hi: {
    all: "किसी भाषा के अभिलेखों के स्रोत देखने के लिए भाषा चुनें।",
    prefix: "इनके स्रोत", suffix: "अभिलेख:",
    offline: "ऑफ़लाइन पूर्वावलोकन में केवल अंग्रेज़ी अभिलेख हैं। इस भाषा के अभिलेख खोजने के लिए संग्रह सर्वर से जुड़ें।"
  },
  mr: {
    all: "भाषेतील नोंदींचे स्रोत पाहण्यासाठी भाषा निवडा.",
    prefix: "स्रोत", suffix: "नोंदी:",
    offline: "ऑफलाइन पूर्वावलोकनात फक्त इंग्रजी नोंदी आहेत. या भाषेतील नोंदी शोधण्यासाठी संग्रह सर्व्हरशी जोडा."
  }
};
const AI_COPY = {
  en: {
    questionLabel: "Your question", searching: "Searching archive records...", responseLabel: "Archive response",
    viewSource: "Open record", noExcerpt: "No text excerpt is available for this record.", summaryHeading: "Record summary",
    originalExcerpt: "Original source excerpt:",
    found: "I found {count} relevant archive record(s). Source excerpts below remain in their original language.",
    empty: "I couldn't find matching records in the indexed archive. Try different keywords or browse the archive.",
    offlineFound: "I found {count} matching sample record(s). The offline preview searches only its sample records.",
    offlineEmpty: "The offline preview can search only its sample records. Start the archive backend for the full archive assistant.",
    error: "The archive assistant couldn't be reached. Please try again.",
    voiceAsk: "Ask by voice", voiceStop: "Stop listening", voiceIdle: "Choose the language you will speak, then use the microphone. Voice input transcribes; it does not translate.",
    voiceListening: "Listening in English… speak now.", voiceDone: "Speech transcribed in the selected language. Review it, then select Ask.",
    voiceStopped: "Voice input stopped.", voiceUnsupported: "Voice input is not supported in this browser. Try Edge or Chrome.",
    voicePermission: "Microphone access was blocked. Allow microphone access in your browser settings.",
    voiceNoSpeech: "No speech was detected. Try again and speak closer to the microphone.",
    voiceNetwork: "The browser's speech service could not be reached. Check your internet connection and try again.",
    voiceAudio: "The browser could not capture microphone audio. Check that the microphone is connected and not in use by another app.",
    voiceLanguage: "This browser's speech service does not support the selected language. Choose another language or try Edge or Chrome.",
    voiceService: "The browser blocked its speech service. Check browser privacy settings or try Edge or Chrome.",
    voiceError: "Voice input failed. Try again, or choose another input language."
  },
  hi: {
    questionLabel: "आपका प्रश्न", searching: "अभिलेख खोजे जा रहे हैं…", responseLabel: "अभिलेख उत्तर",
    viewSource: "अभिलेख खोलें", noExcerpt: "इस अभिलेख का पाठ उपलब्ध नहीं है।", summaryHeading: "अभिलेख सारांश",
    originalExcerpt: "मूल स्रोत का अंश:",
    found: "अभिलेखागार में {count} संबंधित अभिलेख मिले। नीचे दिए गए स्रोत अंश मूल भाषा में हैं।",
    empty: "अनुक्रमित अभिलेखागार में मेल खाते अभिलेख नहीं मिले। दूसरे शब्द आज़माएँ या अभिलेखागार देखें।",
    offlineFound: "नमूना संग्रह में {count} संबंधित अभिलेख मिले। ऑफ़लाइन पूर्वावलोकन में केवल नमूना अभिलेख खोजे जा सकते हैं।",
    offlineEmpty: "ऑफ़लाइन पूर्वावलोकन में केवल नमूना अभिलेख खोजे जा सकते हैं। पूरा संग्रह खोजने के लिए बैकएंड शुरू करें।",
    error: "अभिलेख सहायक से संपर्क नहीं हो सका। कृपया फिर कोशिश करें।",
    voiceAsk: "आवाज़ से पूछें", voiceStop: "सुनना बंद करें", voiceIdle: "पहले अपनी बोली जाने वाली भाषा चुनें, फिर माइक्रोफ़ोन चुनें। आवाज़ को उसी भाषा में लिखा जाता है, अनुवाद नहीं किया जाता।",
    voiceListening: "हिंदी में सुन रहे हैं… अब बोलें।", voiceDone: "आपकी बात चुनी हुई भाषा में लिख दी गई है। जाँचें, फिर पूछें चुनें।",
    voiceStopped: "आवाज़ सुनना बंद हो गया।", voiceUnsupported: "इस ब्राउज़र में आवाज़ से लिखना समर्थित नहीं है। Edge या Chrome आज़माएँ।",
    voicePermission: "माइक्रोफ़ोन की अनुमति नहीं मिली। ब्राउज़र सेटिंग में माइक्रोफ़ोन की अनुमति दें।",
    voiceNoSpeech: "आवाज़ नहीं सुनाई दी। फिर कोशिश करें और माइक्रोफ़ोन के पास बोलें।",
    voiceNetwork: "ब्राउज़र की वाक् सेवा से संपर्क नहीं हो सका। इंटरनेट कनेक्शन जाँचकर फिर कोशिश करें।",
    voiceAudio: "ब्राउज़र माइक्रोफ़ोन से आवाज़ नहीं ले सका। जाँचें कि माइक्रोफ़ोन जुड़ा है और किसी अन्य ऐप में उपयोग नहीं हो रहा।",
    voiceLanguage: "ब्राउज़र की वाक् सेवा चुनी गई भाषा का समर्थन नहीं करती। दूसरी भाषा चुनें या Edge/Chrome आज़माएँ।",
    voiceService: "ब्राउज़र ने वाक् सेवा रोक दी। गोपनीयता सेटिंग जाँचें या Edge/Chrome आज़माएँ।",
    voiceError: "आवाज़ दर्ज नहीं हो सकी। फिर कोशिश करें या दूसरी इनपुट भाषा चुनें।"
  },
  mr: {
    questionLabel: "तुमचा प्रश्न", searching: "अभिलेखातील नोंदी शोधत आहोत…", responseLabel: "अभिलेख उत्तर",
    viewSource: "नोंद उघडा", noExcerpt: "या नोंदीचा मजकूर उपलब्ध नाही.", summaryHeading: "नोंदीचा सारांश",
    originalExcerpt: "मूळ स्रोत उतारा:",
    found: "अभिलेखागारात {count} संबंधित नोंदी सापडल्या. खालील स्रोत उतारे मूळ भाषेत आहेत.",
    empty: "अनुक्रमित अभिलेखात जुळणाऱ्या नोंदी सापडल्या नाहीत. वेगळे शब्द वापरून पाहा किंवा अभिलेखागार तपासा.",
    offlineFound: "नमुना संग्रहात {count} संबंधित नोंदी सापडल्या. ऑफलाइन पूर्वावलोकनात फक्त नमुना नोंदी शोधता येतात.",
    offlineEmpty: "ऑफलाइन पूर्वावलोकनात फक्त नमुना नोंदी शोधता येतात. संपूर्ण संग्रहासाठी बॅकएंड सुरू करा.",
    error: "अभिलेख सहाय्यकाशी संपर्क होऊ शकला नाही. पुन्हा प्रयत्न करा.",
    voiceAsk: "आवाजाने विचारा", voiceStop: "ऐकणे थांबवा", voiceIdle: "आधी बोलण्याची भाषा निवडा आणि मग मायक्रोफोन निवडा. आवाज त्याच भाषेत लिहिला जातो; भाषांतर होत नाही.",
    voiceListening: "मराठीत ऐकत आहे… आता बोला.", voiceDone: "तुमचे बोलणे निवडलेल्या भाषेत लिहिले आहे. तपासा आणि मग विचारा निवडा.",
    voiceStopped: "आवाज ऐकणे थांबवले.", voiceUnsupported: "या ब्राउझरमध्ये आवाजावरून मजकूर समर्थित नाही. Edge किंवा Chrome वापरून पाहा.",
    voicePermission: "मायक्रोफोनची परवानगी नाकारली आहे. ब्राउझर सेटिंगमध्ये मायक्रोफोनला परवानगी द्या.",
    voiceNoSpeech: "आवाज ऐकू आला नाही. पुन्हा प्रयत्न करा आणि मायक्रोफोनजवळ बोला.",
    voiceNetwork: "ब्राउझरच्या वाक् सेवेशी संपर्क झाला नाही. इंटरनेट तपासून पुन्हा प्रयत्न करा.",
    voiceAudio: "ब्राउझरला मायक्रोफोनचा आवाज मिळाला नाही. मायक्रोफोन जोडलेला आहे आणि दुसऱ्या अॅपमध्ये वापरला जात नाही याची खात्री करा.",
    voiceLanguage: "ब्राउझरची वाक् सेवा निवडलेल्या भाषेला समर्थन देत नाही. दुसरी भाषा निवडा किंवा Edge/Chrome वापरून पाहा.",
    voiceService: "ब्राउझरने वाक् सेवा रोखली. गोपनीयता सेटिंग तपासा किंवा Edge/Chrome वापरून पाहा.",
    voiceError: "आवाज नोंदवता आला नाही. पुन्हा प्रयत्न करा किंवा दुसरी इनपुट भाषा निवडा."
  }
};
const NARRATION_COPY = {
  en: { connecting: "Connecting to narration...", elevenLabs: "Narrating with ElevenLabs", browser: "Reading with your browser voice", unavailable: "Speech playback is unavailable in this browser.", failed: "Narration could not be played.", ready: "Ready" },
  hi: { connecting: "वाचन शुरू हो रहा है…", elevenLabs: "ElevenLabs से वाचन हो रहा है", browser: "ब्राउज़र की आवाज़ में वाचन", unavailable: "इस ब्राउज़र में आवाज़ उपलब्ध नहीं है।", failed: "वाचन नहीं हो सका।", ready: "तैयार" },
  mr: { connecting: "वाचन सुरू होत आहे…", elevenLabs: "ElevenLabs द्वारे वाचन सुरू आहे", browser: "ब्राउझरच्या आवाजात वाचन", unavailable: "या ब्राउझरमध्ये ध्वनी उपलब्ध नाही.", failed: "वाचन करता आले नाही.", ready: "तयार" }
};
const PRESET_QUESTION_TRANSLATIONS = {
  "What did Ambedkar warn about hero worship and Bhakti in politics?": {
    hi: "आंबेडकर ने राजनीति में व्यक्तिपूजा और भक्ति के बारे में क्या चेतावनी दी?",
    mr: "आंबेडकरांनी राजकारणातील व्यक्तिपूजा आणि भक्तीबद्दल काय इशारा दिला?"
  },
  "Why did India choose a Parliamentary executive instead of Presidential?": {
    hi: "भारत ने राष्ट्रपति प्रणाली के बजाय संसदीय कार्यपालिका क्यों चुनी?",
    mr: "भारताने अध्यक्षीय पद्धतीऐवजी संसदीय कार्यकारी पद्धत का निवडली?"
  },
  "What was Ambedkar's interpretation of Article 356 and President's Rule?": {
    hi: "अनुच्छेद 356 और राष्ट्रपति शासन पर आंबेडकर की क्या व्याख्या थी?",
    mr: "कलम 356 आणि राष्ट्रपती राजवटीबद्दल आंबेडकरांचे मत काय होते?"
  },
  "Why is caste not merely a division of labour?": {
    hi: "जाति केवल श्रम का विभाजन क्यों नहीं है?",
    mr: "जात ही केवळ कामाची विभागणी का नाही?"
  }
};

const GROUNDED_KNOWLEDGE = [
  {
    triggers: ["hero", "bhakti", "worship", "degradation", "dictatorship", "warning"],
    answer: "In his final address to the Constituent Assembly on 25th November 1949, Dr. Ambedkar issued a stern warning quoting John Stuart Mill: not to lay our liberties at the feet of even a great man. He explicitly stated: 'In religion, Bhakti may be a road to the salvation of the soul. But in politics, Bhakti or hero-worship is a sure road to degradation and to eventual dictatorship.'",
    citation: "CAD Volume XI, 25th November 1949, pp. 972-984 (Valedictory Speech)",
    docId: "DOC_CAD_CAD_VOL11_19491125"
  },
  {
    triggers: ["parliamentary", "presidential", "form of government", "stability", "responsibility"],
    answer: "Introducing the Draft Constitution on 4th November 1948, Dr. Ambedkar explained why India adopted the Parliamentary executive: a democratic executive must balance stability and responsibility. While the American Presidential system provides more stability but less responsibility, the British Parliamentary system provides more responsibility through daily legislative assessment. The Drafting Committee preferred daily accountability over periodic assessment.",
    citation: "CAD Volume VII, 4th November 1948, pp. 31-44 (Motion on Draft Constitution)",
    docId: "DOC_CAD_CAD_VOL07_19481104"
  },
  {
    triggers: ["356", "president's rule", "dead letter", "emergency", "breakdown"],
    answer: "During the debate on Article 356 (President's Rule) on 14th October 1949, Dr. Ambedkar addressed fears of executive abuse, affirming that such powers were intended as an extreme last resort: 'The proper thing we ought to expect is that such articles will never be called into operation and that they would remain a dead letter.'",
    citation: "CAD Volume IX, 14th October 1949, pp. 175-182",
    docId: "DOC_CAD_CAD_VOL09_19491014"
  },
  {
    triggers: ["division of labour", "labourers", "caste", "annihilation", "shastras"],
    answer: "In 'Annihilation of Caste' (1936), Dr. Ambedkar refuted the conservative defense that caste was simply economic division of labour: 'Caste is not just a division of labour, it is a division of labourers... an hierarchy in which the divisions of labourers are graded one above the other.' He argued that caste dismantles social fraternity and that genuine reform requires eradicating religious shastric sanctions.",
    citation: "Dr. Babasaheb Ambedkar Writings and Speeches (BAWS), Volume 1, pp. 23-96",
    docId: "DOC_DAF_BAWS_PUB_1936_AOC"
  },
  {
    triggers: ["rupee", "currency", "rbi", "reserve bank", "inflation"],
    answer: "In his D.Sc. dissertation 'The Problem of the Rupee: Its Origin and Its Solution' (1923), Dr. Ambedkar analyzed monetary instability and argued that uncontrolled currency expansion severely erodes the purchasing power of the working classes. His testimony before the Hilton Young Commission directly guided the founding architecture of the Reserve Bank of India (RBI).",
    citation: "BAWS Volume 6, 1923, London School of Economics Dissertation",
    docId: "DOC_DAF_BAWS_PUB_1923_POR"
  }
];

// Offline fallback documents if backend server is starting
const FALLBACK_DOCS = [
  {
    id: "DOC_CAD_CAD_VOL11_19491125",
    title: "Constituent Assembly Debates: Speech on Third Reading of Constitution (Grammar of Anarchy)",
    author: "Dr. B.R. Ambedkar",
    date: "1949-11-25",
    type: "debate",
    language: "en",
    source: "CAD",
    summary: "Dr. Ambedkar's historic valedictory address warning that political democracy is unsustainable without social and economic equality ('one man one value'), condemning political hero-worship (Bhakti), and calling for strict constitutional methods.",
    tags: ["constitutional", "democracy", "grammar_of_anarchy", "equality"],
    content: {
      summary: "Dr. Ambedkar's historic valedictory speech warning that political democracy is unsustainable without social democracy, warning against political Bhakti/hero-worship, and calling to abandon unconstitutional methods.",
      full_text: "Sir, I look back upon the work of the Constituent Assembly with satisfaction. On 26th January 1950, India will be an independent country... If we wish to maintain democracy not merely in form, but also in fact, what must we do? The first thing in my judgment we must do is to hold fast to constitutional methods of achieving our social and economic objectives... These methods are nothing but the Grammar of Anarchy.\n\nThe second thing we must do is to observe the caution which John Stuart Mill has given: not to lay our liberties at the feet of even a great man... In politics, Bhakti or hero-worship is a sure road to degradation and to eventual dictatorship.\n\nThe third thing we must do is not to be content with mere political democracy. On 26th January 1950, we are going to enter into a life of contradictions: in politics we will have equality and in social and economic life we will have inequality.",
      key_quotes: [
        "In politics, Bhakti or hero-worship is a sure road to degradation and to eventual dictatorship.",
        "On 26th January 1950, we are going to enter into a life of contradictions: in politics we will have equality, in social and economic life we will have inequality."
      ]
    },
    metadata: { source: "CAD", archive_reference: "CAD-LS-Volume XI-972-984", pages: 13, word_count: 1200, condition: "good", accessibility: "public" }
  },
  {
    id: "DOC_CAD_CAD_VOL07_19481104",
    title: "Constituent Assembly Debates: Motion Introducing the Draft Constitution",
    author: "Dr. B.R. Ambedkar",
    date: "1948-11-04",
    type: "debate",
    language: "en",
    source: "CAD",
    summary: "Dr. Ambedkar introduces the Draft Constitution, elaborating why India chose the British Parliamentary executive over the American Presidential model: balancing stability with day-to-day executive accountability.",
    tags: ["constitutional", "parliamentary_democracy", "executive", "drafting_committee"],
    content: {
      summary: "Dr. Ambedkar introduces the Draft Constitution and defends the Parliamentary executive framework.",
      full_text: "Mr. Vice-President, Sir, I move that the Draft Constitution as framed by the Drafting Committee be taken into consideration... The Draft Constitution recommends a Parliamentary system of Government as in the United Kingdom, rather than the Presidential system as in America... A democratic executive must satisfy two conditions: stability and responsibility. The Drafting Committee preferred daily assessment of responsibility to periodic assessment.",
      key_quotes: [
        "The President is the head of the State but not of the Executive. He represents the Nation but does not rule the Nation.",
        "The Drafting Committee has preferred the system of daily assessment of responsibility to periodic assessment."
      ]
    },
    metadata: { source: "CAD", archive_reference: "CAD-LS-Volume VII-31-44", pages: 14, word_count: 1400, condition: "good", accessibility: "public" }
  },
  {
    id: "DOC_DAF_BAWS_PUB_1936_AOC",
    title: "Annihilation of Caste",
    author: "Dr. B.R. Ambedkar",
    date: "1936-05-15",
    type: "publication",
    language: "en",
    source: "Foundation",
    summary: "Dr. Ambedkar's masterpiece address demonstrating that caste is not merely division of labour, but an unnatural division of labourers graded one above another, calling for destruction of religious shastra sanctions.",
    tags: ["social_justice", "annihilation_of_caste", "equality", "caste_reform"],
    content: {
      summary: "Critique of caste as unnatural division of labourers, demanding annihilation of religious sanctions that uphold caste hierarchy.",
      full_text: "Caste is not just a division of labour, it is a division of labourers... You cannot build anything on the foundations of caste. You cannot build up a nation, you cannot build up an ethical morality. Anything that you will build on the foundations of caste will crack and will never be a whole. Religion in the true sense of the term must be based on principles, not on rules.",
      key_quotes: [
        "Caste is not just a division of labour, it is a division of labourers.",
        "You cannot build anything on the foundations of caste. You cannot build up a nation, you cannot build up an ethical morality."
      ]
    },
    metadata: { source: "Foundation", archive_reference: "DAF-BAWS_PUB_1936_AOC", pages: 74, word_count: 5200, condition: "good", accessibility: "public" }
  },
  {
    id: "DOC_DAF_BAWS_PUB_1923_POR",
    title: "The Problem of the Rupee: Its Origin and Its Solution",
    author: "Dr. B.R. Ambedkar",
    date: "1923-12-01",
    type: "publication",
    language: "en",
    source: "Foundation",
    summary: "Dr. Ambedkar's doctoral dissertation in economics analyzing monetary policy and currency standards, which served as the intellectual foundation for the Reserve Bank of India.",
    tags: ["economics", "monetary_policy", "rbi", "rupee_standard"],
    content: {
      summary: "Doctoral dissertation on currency stabilization and monetary standards submitted to London School of Economics.",
      full_text: "The stability of a currency is determined not merely by gold backing, but by controlling the quantity of money to prevent inflationary depreciation and preserve purchasing power for working people... Nothing can be more harmful to the welfare of the working classes than a depreciating currency.",
      key_quotes: [
        "Nothing can be more harmful to the welfare of the working classes than a depreciating currency that erodes their purchasing power."
      ]
    },
    metadata: { source: "Foundation", archive_reference: "DAF-BAWS_PUB_1923_POR", pages: 300, word_count: 6500, condition: "good", accessibility: "public" }
  },
  {
    id: "DOC_DAF_BAWS_SPEECH_1927_MSD",
    title: "Mahad Satyagraha Address (Chavdar Tale Water Rights)",
    author: "Dr. B.R. Ambedkar",
    date: "1927-12-25",
    type: "speech",
    language: "en",
    source: "Foundation",
    summary: "Dr. Ambedkar's historic address framing the Chavdar lake satyagraha not as a mere thirst issue, but as a defining non-violent struggle for universal human rights and civic equality.",
    tags: ["mahad_satyagraha", "civil_rights", "water_rights", "human_dignity"],
    content: {
      summary: "Defining address establishing that the Mahad struggle was for fundamental human dignity and universal civil equality.",
      full_text: "At Chavdar Tale, we did not go to drink water because we believed that water had medicinal value or that drinking it would make us immortal. We went there to assert our human rights, to declare to the world that we are human beings with the same dignity and claims to nature's gifts as any other citizen.",
      key_quotes: [
        "We are not fighting for water; we are fighting to establish that we are human beings."
      ]
    },
    metadata: { source: "Foundation", archive_reference: "DAF-BAWS_SPEECH_1927_MSD", pages: 18, word_count: 2400, condition: "good", accessibility: "public" }
  },
  {
    id: "DOC_CAD_CAD_VOL07_19481129",
    title: "Constituent Assembly Debates: Abolition of Untouchability (Article 17)",
    author: "Dr. B.R. Ambedkar",
    date: "1948-11-29",
    type: "debate",
    language: "en",
    source: "CAD",
    summary: "The landmark debate and unanimous adoption of Draft Article 11 (Article 17), outlawing untouchability and declaring its enforcement an offence punishable by law.",
    tags: ["constitutional", "article_17", "social_justice", "abolition_of_untouchability"],
    content: {
      summary: "Debate and unanimous passage of constitutional abolition of untouchability.",
      full_text: "Untouchability is abolished and its practice in any form is forbidden. The enforcement of any disability arising out of Untouchability shall be an offence punishable in accordance with law... Civil equality is meaningless if systemic degradation is permitted under the guise of custom.",
      key_quotes: [
        "Untouchability is abolished and its practice in any form is forbidden."
      ]
    },
    metadata: { source: "CAD", archive_reference: "CAD-LS-Volume VII-660-669", pages: 10, word_count: 1100, condition: "good", accessibility: "public" }
  }
];

document.addEventListener("DOMContentLoaded", () => {
  initializeArchiveTheme();
  updateAiVoiceUi();
  renderArchiveFilterSources();
  let savedUiLanguage = "en";
  try {
    const saved = localStorage.getItem("ambedkar-archive-language");
    if (saved && UI_TRANSLATIONS[saved]) savedUiLanguage = saved;
  } catch (_) { /* The language switcher remains available without storage. */ }
  if (savedUiLanguage !== "en") setUiLanguage(savedUiLanguage);
  const searchField = document.getElementById("searchInput");
  const clearButton = document.querySelector(".search-clear");
  searchField?.addEventListener("input", () => {
    clearButton?.classList.toggle("visible", Boolean(searchField.value));
  });
  document.getElementById("themeToggle")?.addEventListener("click", toggleArchiveTheme);
  document.addEventListener("keydown", event => {
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      searchField?.focus();
    }
    if (event.key === "Escape" && !document.getElementById("docModal")?.classList.contains("hidden")) closeDocModal();
  });
  document.getElementById("ocrFile")?.addEventListener("change", () => {
    lastOcrMetadata = null;
  });
  document.getElementById("ocrMode")?.addEventListener("change", () => {
    updateHandwritingModelStatus();
  });
  const uiObserver = new MutationObserver(() => {
    if (currentLanguage !== "en") applyUiTranslations();
  });
  uiObserver.observe(document.body, { childList: true, subtree: true });
  checkBackendHealth();
  updateHandwritingModelStatus();
  executeSearch();
  loadTimeline();
  loadStats();
});

function initializeArchiveTheme() {
  let theme = null;
  try { theme = localStorage.getItem("ambedkar-archive-theme"); } catch (_) { /* Storage may be unavailable in kiosk mode. */ }
  if (theme !== "light" && theme !== "dark") {
    theme = window.matchMedia?.("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  setArchiveTheme(theme, false);
}

function setArchiveTheme(theme, persist = true) {
  document.body.dataset.theme = theme;
  const button = document.getElementById("themeToggle");
  if (button) {
    const dark = theme === "dark";
    const englishLabel = dark ? "Switch to light theme" : "Switch to dark theme";
    const label = ({ ...(UI_TRANSLATIONS[currentLanguage] || {}) })[englishLabel] || englishLabel;
    button.setAttribute("aria-label", label);
    button.title = label;
    button.innerHTML = `<i class="fa-regular ${dark ? "fa-sun" : "fa-moon"}" aria-hidden="true"></i>`;
  }
  if (persist) {
    try { localStorage.setItem("ambedkar-archive-theme", theme); } catch (_) { /* Keep the current session usable without storage. */ }
  }
}

function toggleArchiveTheme() {
  setArchiveTheme(document.body.dataset.theme === "dark" ? "light" : "dark");
}

function clearArchiveSearch() {
  const field = document.getElementById("searchInput");
  if (!field) return;
  field.value = "";
  document.querySelector(".search-clear")?.classList.remove("visible");
  executeSearch();
  field.focus();
}

// Check if FastAPI server is reachable
async function checkBackendHealth() {
  try {
    const res = await fetch(`${API_BASE}/api/health`, { signal: AbortSignal.timeout(2000) });
    if (res.ok) {
      const health = await res.json();
      isBackendAvailable = true;
      archiveApiMode = health.mode || "fastapi";
      showConnectionBanner(archiveApiMode);
    } else {
      isBackendAvailable = false;
      archiveApiMode = "offline";
      showConnectionBanner(false);
    }
  } catch (e) {
    isBackendAvailable = false;
    archiveApiMode = "offline";
    showConnectionBanner(false);
  }
}

function showConnectionBanner(mode) {
  const metaLabel = document.getElementById("searchResultsMeta");
  if (!metaLabel) return;
  if (mode === "preview") {
    metaLabel.innerHTML = `<span class="inline-flex items-center gap-1 text-emerald-400 font-semibold"><span class="w-2 h-2 rounded-full bg-emerald-400"></span> Local archive catalog ready · browsing indexed records</span>`;
  } else if (mode) {
    metaLabel.innerHTML = `<span class="inline-flex items-center gap-1 text-emerald-400 font-semibold"><span class="w-2 h-2 rounded-full bg-emerald-400"></span> Live archive connected</span>`;
  } else {
    metaLabel.innerHTML = `<span class="inline-flex items-center gap-1 text-amber-400 font-semibold"><span class="w-2 h-2 rounded-full bg-amber-400"></span> Archive service unavailable · preview records shown</span>`;
  }
}

// Tab Switching
function switchTab(tabId) {
  document.querySelectorAll(".tab-pane").forEach(el => el.classList.add("hidden"));
  document.querySelectorAll(".nav-tab").forEach(el => el.classList.remove("active-tab"));

  const target = document.getElementById(tabId);
  const btn = document.getElementById("tab-" + tabId);

  if (target) target.classList.remove("hidden");
  if (btn) btn.classList.add("active-tab");

  if (tabId === "timelineTab") loadTimeline();
  if (tabId === "analyticsTab") loadStats();
}

// Search Execution
async function executeSearch(loadMore = false) {
  const query = document.getElementById("searchInput").value.trim().toLowerCase();
  const lang = document.getElementById("filterLanguage").value;
  const docType = document.getElementById("filterType").value;
  const source = document.getElementById("filterSource").value;
  const resultsGrid = document.getElementById("resultsGrid");
  const metaLabel = document.getElementById("searchResultsMeta");

  if (!loadMore) {
    archiveDisplayedCount = 0;
    archiveTotalCount = 0;
    resultsGrid.innerHTML = `
      <div class="col-span-full py-12 text-center text-slate-400">
        <i class="fa-solid fa-spinner fa-spin text-2xl text-amber-500 mb-2"></i>
        <p class="text-xs">Searching archival records...</p>
      </div>
    `;
  }

  // Try live backend first
  try {
    const res = await fetch(`${API_BASE}/api/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        q: query || "*",
        language: lang || null,
        document_type: docType || null,
        source: source || null,
        limit: ARCHIVE_SEARCH_PAGE_SIZE,
        offset: loadMore ? archiveDisplayedCount : 0
      }),
      signal: AbortSignal.timeout(2500)
    });

    if (res.ok) {
      const data = await res.json();
      isBackendAvailable = true;
      archiveApiMode = data.mode || "fastapi";
      archiveTotalCount = data.total;
      archiveDisplayedCount = (loadMore ? archiveDisplayedCount : 0) + data.results.length;
      metaLabel.innerHTML = `Found <span class="text-amber-400 font-bold">${data.total}</span> records${archiveApiMode === "preview" ? " in the local archive" : ` in <span class="text-emerald-400 font-bold">${data.took_ms} ms</span> (Live SQLite FTS5)`}`;
      renderDocCards(data.results, undefined, loadMore);
      renderSearchPagination();
      return;
    }
  } catch (err) {
    // Backend offline: fallback to embedded records
    isBackendAvailable = false;
  }

  // Fallback client-side search across embedded records
  archiveApiMode = "offline";
  if (loadMore) return;
  showConnectionBanner(false);
  let filtered = FALLBACK_DOCS;
  if (query && query !== "*") {
    filtered = filtered.filter(d => 
      d.title.toLowerCase().includes(query) || 
      (d.summary && d.summary.toLowerCase().includes(query)) ||
      (d.tags && d.tags.some(t => t.toLowerCase().includes(query)))
    );
  }
  if (lang) filtered = filtered.filter(d => d.language === lang);
  if (docType) filtered = filtered.filter(d => d.type === docType);
  if (source) filtered = filtered.filter(d => d.source === source);

  const emptyMessage = !filtered.length && lang
    ? SOURCE_HINT_COPY[currentLanguage].offline
    : "No documents found matching your query criteria.";
  renderDocCards(filtered, emptyMessage);
  archiveDisplayedCount = filtered.length;
  archiveTotalCount = filtered.length;
  renderSearchPagination();
}

function renderSearchPagination() {
  const pagination = document.getElementById("resultsPagination");
  if (!pagination) return;
  if (!archiveTotalCount) {
    pagination.innerHTML = "";
    return;
  }
  const labels = {
    en: `Showing ${archiveDisplayedCount} of ${archiveTotalCount} records`,
    hi: `${archiveTotalCount} में से ${archiveDisplayedCount} अभिलेख दिखाए जा रहे हैं`,
    mr: `${archiveTotalCount} पैकी ${archiveDisplayedCount} नोंदी दाखवत आहोत`
  };
  const moreLabels = { en: "Load more records", hi: "और अभिलेख दिखाएँ", mr: "आणखी नोंदी दाखवा" };
  const remaining = archiveDisplayedCount < archiveTotalCount;
  pagination.innerHTML = `<span class="text-xs text-slate-500">${labels[currentLanguage] || labels.en}</span>${remaining
    ? `<button type="button" onclick="executeSearch(true)" class="px-4 py-2 rounded-lg border border-slate-300 bg-white text-slate-700 hover:bg-emerald-50 font-semibold text-sm">${moreLabels[currentLanguage] || moreLabels.en}</button>`
    : ""}`;
}

function renderDocCards(docs, emptyMessage = "No documents found matching your query criteria.", append = false) {
  const resultsGrid = document.getElementById("resultsGrid");
  if (!docs || docs.length === 0) {
    if (append) return;
    resultsGrid.innerHTML = `
      <div class="col-span-full py-12 text-center text-slate-500">
        <i class="fa-solid fa-folder-open text-3xl mb-2"></i>
        <p>${emptyMessage}</p>
      </div>
    `;
    return;
  }

  const cards = docs.map(doc => {
    const typeColor = doc.type === 'debate' ? 'text-indigo-400 border-indigo-500/30 bg-indigo-500/10' :
                      doc.type === 'speech' ? 'text-amber-400 border-amber-500/30 bg-amber-500/10' :
                      doc.type === 'manuscript' ? 'text-rose-400 border-rose-500/30 bg-rose-500/10' :
                      'text-emerald-400 border-emerald-500/30 bg-emerald-500/10';

    return `
      <div class="doc-card">
        <div class="space-y-2">
          <div class="flex items-center justify-between text-[11px]">
            <span class="px-2 py-0.5 rounded-full border ${typeColor} font-semibold uppercase tracking-wider text-[10px]">
              ${doc.type}
            </span>
            <div class="flex items-center gap-1.5 text-slate-400 font-mono">
              <span class="uppercase">${doc.language}</span>
              <span>•</span>
              <span>${doc.date || 'Historical'}</span>
            </div>
          </div>

          <h3 class="font-serif font-bold text-base text-white line-clamp-2 hover:text-amber-400 transition cursor-pointer" onclick="openDocModal('${doc.id}')">
            ${doc.title}
          </h3>

          <p class="text-xs text-slate-400 line-clamp-3 leading-relaxed">
            ${doc.summary || 'Digitized historical archive record.'}
          </p>
        </div>

        <div class="pt-4 mt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
          <div class="flex items-center gap-1 text-[11px] text-slate-400">
            <i class="fa-solid fa-landmark text-amber-500"></i>
            <span>${doc.source}</span>
          </div>
          <button onclick="openDocModal('${doc.id}')" class="px-3 py-1.5 rounded bg-slate-800 hover:bg-amber-600 hover:text-slate-950 font-semibold text-slate-200 transition text-[11px] flex items-center gap-1">
            <span>Inspect</span>
            <i class="fa-solid fa-arrow-right text-[9px]"></i>
          </button>
        </div>
      </div>
    `;
  }).join("");
  if (append) resultsGrid.insertAdjacentHTML("beforeend", cards);
  else resultsGrid.innerHTML = cards;
}

function quickFilter(term) {
  document.getElementById("searchInput").value = term;
  executeSearch();
}

// Modal View & Inspection
async function openDocModal(docId, timelineEventOverride = null) {
  const modal = document.getElementById("docModal");
  stopSpeech();

  let doc = null;

  // Try fetching from backend
  try {
    const res = await fetch(`${API_BASE}/api/documents/${docId}`, { signal: AbortSignal.timeout(1500) });
    if (res.ok) {
      const wrapper = await res.json();
      doc = wrapper.document;
    }
  } catch (e) {
    // use fallback
  }

  if (!doc) {
    doc = FALLBACK_DOCS.find(d => d.id === docId);
  }

  if (!doc) {
    const event = timelineEventOverride || timelineEventByDocument.get(docId);
    if (event) {
      const source = docId.startsWith("DOC_CAD_") ? "CAD" : "Foundation";
      doc = {
        id: docId,
        title: event.title,
        author: "Dr. B.R. Ambedkar",
        date: event.date || `${event.year}-01-01`,
        type: "historical record",
        language: "en",
        summary: event.description,
        content: {
          summary: event.description,
          full_text: "The complete source document is not available in the offline preview. Start the archive backend to load the full record."
        },
        metadata: {
          source,
          archive_reference: docId,
          collection: event.category,
          pages: 1,
          word_count: 0,
          condition: "record details only",
          accessibility: "public"
        }
      };
    }
  }

  if (!doc) {
    const modalTitle = document.getElementById("modalTitle");
    if (modalTitle) modalTitle.textContent = "Document unavailable";
    document.getElementById("modalAuthor").textContent = "";
    document.getElementById("modalTypeBadge").textContent = "";
    document.getElementById("modalSourceBadge").textContent = "";
    document.getElementById("modalDateBadge").textContent = "";
    const modalSummary = document.getElementById("modalSummary");
    if (modalSummary) modalSummary.textContent = "This record could not be loaded. Check the archive connection and try again.";
    const modalFullText = document.getElementById("modalFullText");
    if (modalFullText) modalFullText.textContent = "";
    document.getElementById("modalQuotesSection").classList.add("hidden");
    document.getElementById("modalMetaGrid").innerHTML = "";
    document.getElementById("modalExternalLink").classList.add("hidden");
    document.getElementById("docModal")?.classList.remove("hidden");
    return;
  }

  currentDocInModal = doc;

  document.getElementById("modalTitle").innerText = doc.title;
  document.getElementById("modalAuthor").innerText = `${doc.author} • ${doc.date || 'Historical'}`;
  document.getElementById("modalTypeBadge").innerText = doc.type;
  document.getElementById("modalSourceBadge").innerText = (doc.metadata && doc.metadata.source) ? doc.metadata.source : (doc.source || "Archive");
  document.getElementById("modalDateBadge").innerText = doc.date || "";

  const summary = (doc.content && doc.content.summary) ? doc.content.summary : (doc.summary || "No summary available.");
  const fullText = (doc.content && doc.content.full_text) ? doc.content.full_text : "Full text content not available for this record.";

  document.getElementById("modalSummary").innerText = summary;
  document.getElementById("modalFullText").innerText = fullText;

  // Key Quotes
  const quotesList = document.getElementById("modalQuotesList");
  const quotes = (doc.content && doc.content.key_quotes) ? doc.content.key_quotes : [];
  if (quotes && quotes.length > 0) {
    quotesList.innerHTML = quotes.map(q => `
      <blockquote class="border-l-2 border-amber-500 pl-3 italic text-amber-200/90 text-xs py-1">
        "${q}"
      </blockquote>
    `).join("");
    document.getElementById("modalQuotesSection").classList.remove("hidden");
  } else {
    document.getElementById("modalQuotesSection").classList.add("hidden");
  }

  // Metadata Grid
  const metaGrid = document.getElementById("modalMetaGrid");
  const meta = doc.metadata || {};
  metaGrid.innerHTML = `
    <div class="bg-slate-950/40 p-2 rounded border border-slate-800/60">
      <span class="text-slate-500 text-[10px] block">Identifier</span>
      <span class="font-mono text-amber-400">${doc.id}</span>
    </div>
    <div class="bg-slate-950/40 p-2 rounded border border-slate-800/60">
      <span class="text-slate-500 text-[10px] block">Reference</span>
      <span>${meta.archive_reference || 'N/A'}</span>
    </div>
    <div class="bg-slate-950/40 p-2 rounded border border-slate-800/60">
      <span class="text-slate-500 text-[10px] block">Pages / Words</span>
      <span>${meta.pages || 1} pages / ${meta.word_count || 0} words</span>
    </div>
    <div class="bg-slate-950/40 p-2 rounded border border-slate-800/60">
      <span class="text-slate-500 text-[10px] block">Language</span>
      <span class="uppercase font-bold">${doc.language}</span>
    </div>
    <div class="bg-slate-950/40 p-2 rounded border border-slate-800/60">
      <span class="text-slate-500 text-[10px] block">Condition</span>
      <span class="capitalize text-emerald-400">${meta.condition || 'Preserved'}</span>
    </div>
    <div class="bg-slate-950/40 p-2 rounded border border-slate-800/60">
      <span class="text-slate-500 text-[10px] block">Access Rights</span>
      <span class="capitalize text-amber-400">${meta.accessibility || 'Public Domain'}</span>
    </div>
  `;

  const externalLink = document.getElementById("modalExternalLink");
  const timelineEvent = timelineEventOverride || timelineEventByDocument.get(docId);
  const sourceUrl = timelineEvent?.primary_source_url || meta.url || (meta.source === "IA" && meta.archive_reference
    ? `https://archive.org/details/${encodeURIComponent(meta.archive_reference)}`
    : null);
  if (sourceUrl) {
    externalLink.href = sourceUrl;
    externalLink.innerHTML = `<i class="fa-solid fa-arrow-up-right-from-square"></i> ${timelineEvent?.primary_source_label || "View Primary Source"}`;
    externalLink.classList.remove("hidden");
  } else {
    externalLink.classList.add("hidden");
  }

  modal.classList.remove("hidden");
}

function closeDocModal() {
  document.getElementById("docModal").classList.add("hidden");
  stopSpeech();
}

// Audio Narration (TTS)
async function toggleAudioNarration() {
  if (!currentDocInModal) return;

  if (
    narrationRequestController ||
    (narrationAudio && !narrationAudio.paused) ||
    (synth && (synth.speaking || synth.pending))
  ) {
    stopSpeech();
    return;
  }

  const doc = currentDocInModal;
  const originalSummary = (doc.content && doc.content.summary) || doc.summary || "";
  const originalQuotes = (doc.content && doc.content.key_quotes) || [];
  const translated = doc.translations && doc.translations[currentLanguage];
  const hasSelectedTranslation = currentLanguage === doc.language || Boolean(translated && (translated.title || translated.summary));
  const narrationLanguage = hasSelectedTranslation ? currentLanguage : (doc.language || "en");
  const title = hasSelectedTranslation && translated?.title ? translated.title : doc.title;
  const summary = hasSelectedTranslation && translated?.summary ? translated.summary : originalSummary;
  const quotes = hasSelectedTranslation && translated?.key_quotes
    ? translated.key_quotes
    : (narrationLanguage === doc.language ? originalQuotes : []);
  const textToRead = narrationLanguage === "hi"
    ? `शीर्षक: ${title}। लेखक: डॉ. बी. आर. आंबेडकर। सारांश: ${summary}${quotes.length ? `। उद्धरण: ${quotes.join('। ')}` : ''}`
    : narrationLanguage === "mr"
      ? `शीर्षक: ${title}. लेखक: डॉ. बी. आर. आंबेडकर. सारांश: ${summary}${quotes.length ? `. उद्धरणे: ${quotes.join('. ')}` : ''}`
      : `${title}. By ${doc.author}. Summary: ${summary}${quotes.length ? `. Quotes: ${quotes.join('. ')}` : ''}`;

  const icon = document.getElementById("ttsPlayIcon");
  const status = document.getElementById("ttsStatus");
  const narrationStatus = {
    en: hasSelectedTranslation ? NARRATION_COPY.en.connecting : `No ${currentLanguage.toUpperCase()} translation is available; reading the original language.`,
    hi: hasSelectedTranslation ? NARRATION_COPY.hi.connecting : "इस अभिलेख का हिंदी अनुवाद उपलब्ध नहीं है; मूल भाषा में पढ़ा जाएगा।",
    mr: hasSelectedTranslation ? NARRATION_COPY.mr.connecting : "या नोंदीचा मराठी अनुवाद उपलब्ध नाही; मूळ भाषेत वाचन होईल."
  }[currentLanguage];
  narrationRequestController = new AbortController();
  if (status) {
    status.innerText = narrationStatus;
    status.className = "text-xs text-amber-400 font-mono";
  }

  try {
    const response = await fetch(`${API_BASE}/api/tts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: textToRead }),
      signal: narrationRequestController.signal
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || "ElevenLabs narration failed.");
    }

    const audioBlob = await response.blob();
    narrationRequestController = null;
    narrationObjectUrl = URL.createObjectURL(audioBlob);
    narrationAudio = new Audio(narrationObjectUrl);
    narrationAudio.onplay = () => {
      if (icon) icon.className = "fa-solid fa-pause";
      if (status) {
        status.innerText = NARRATION_COPY[currentLanguage]?.elevenLabs || NARRATION_COPY.en.elevenLabs;
        status.className = "text-xs text-emerald-400 font-mono";
      }
    };
    narrationAudio.onended = stopSpeech;
    narrationAudio.onerror = () => startBrowserNarration(textToRead, narrationLanguage);
    await narrationAudio.play();
  } catch (error) {
    narrationRequestController = null;
    if (error.name !== "AbortError") startBrowserNarration(textToRead, narrationLanguage);
  }
}

function startBrowserNarration(text, language = currentLanguage) {
  if (!synth || typeof SpeechSynthesisUtterance === "undefined") {
    showNarrationError(NARRATION_COPY[currentLanguage]?.unavailable || NARRATION_COPY.en.unavailable);
    return;
  }

  if (narrationAudio) {
    narrationAudio.pause();
    narrationAudio.removeAttribute("src");
    narrationAudio.load();
    narrationAudio = null;
  }
  if (narrationObjectUrl) URL.revokeObjectURL(narrationObjectUrl);
  narrationObjectUrl = null;

  const utterance = new SpeechSynthesisUtterance(text);
  currentUtterance = utterance;
  utterance.rate = 0.95;
  utterance.lang = ({
    en: "en-IN",
    hi: "hi-IN",
    mr: "mr-IN",
    bn: "bn-IN",
    gu: "gu-IN",
    pa: "pa-IN",
    ta: "ta-IN",
    te: "te-IN",
    ml: "ml-IN",
    kn: "kn-IN"
  })[language] || "en-IN";

  const icon = document.getElementById("ttsPlayIcon");
  const status = document.getElementById("ttsStatus");
  utterance.onstart = () => {
    if (icon) icon.className = "fa-solid fa-pause";
    if (status) {
      status.innerText = NARRATION_COPY[currentLanguage]?.browser || NARRATION_COPY.en.browser;
      status.className = "text-xs text-amber-400 font-mono";
    }
  };
  utterance.onend = () => {
    if (currentUtterance === utterance) stopSpeech();
  };
  utterance.onerror = () => {
    if (currentUtterance === utterance) showNarrationError("Browser narration could not be played.");
  };
  synth.cancel();
  synth.speak(currentUtterance);
}

function stopSpeech() {
  if (narrationRequestController) narrationRequestController.abort();
  narrationRequestController = null;
  currentUtterance = null;
  if (synth) synth.cancel();
  if (narrationAudio) {
    narrationAudio.pause();
    narrationAudio.removeAttribute("src");
    narrationAudio.load();
    narrationAudio = null;
  }
  if (narrationObjectUrl) URL.revokeObjectURL(narrationObjectUrl);
  narrationObjectUrl = null;
  const icon = document.getElementById("ttsPlayIcon");
  const status = document.getElementById("ttsStatus");
  if (icon) icon.className = "fa-solid fa-play";
  if (status) {
    status.innerText = NARRATION_COPY[currentLanguage]?.ready || NARRATION_COPY.en.ready;
    status.className = "text-xs text-amber-400 font-mono";
  }
}

function showNarrationError(message) {
  stopSpeech();
  const status = document.getElementById("ttsStatus");
  if (status) {
    status.innerText = NARRATION_COPY[currentLanguage]?.failed || message;
    status.className = "text-xs text-rose-400 font-mono";
  }
}

// Interactive Timeline
async function loadTimeline() {
  const container = document.getElementById("timelineContainer");
  // Use the Foundation's current MoSJE site; its older writings-and-speeches
  // hostname is currently presenting an invalid TLS certificate in browsers.
  const foundationCatalog = "https://ambedkarfoundation.nic.in/publication.html";
  const parliamentCollection = "https://eparlib.sansad.in/handle/123456789/760448/browse?submit_browse=browse.menu.date&type=date";
  const parliamentDate = date => `${parliamentCollection}&value=${encodeURIComponent(date)}`;
  const fallbackTimeline = [
    { year: 1916, date: "1916-05-09", title: "Castes in India Paper at Columbia University", category: "Academic / Anthropology", description: "Presents first seminal paper on endogamy and mechanisms of caste reproduction at Columbia University.", doc_id: "DOC_DAF_BAWS_PUB_1916_CII", primary_source_url: "https://www.mea.gov.in/Images/attach/amb/Volume_01.pdf", primary_source_label: "View Volume 1 (MEA mirror)" },
    { year: 1920, date: "1920-01-31", title: "Launch of 'Muknayak' (Voice of the Mute)", category: "Journalism & Social Awakening", description: "Founds Marathi fortnightly declaring journalism as an instrument of emancipation for silenced millions.", doc_id: "DOC_DAF_BAWS_PUB_1920_MUK", primary_source_url: foundationCatalog, primary_source_label: "Browse Foundation Sources" },
    { year: 1923, date: "1923-12-01", title: "Problem of the Rupee (London School of Economics)", category: "Economics & Monetary Policy", description: "Submits D.Sc. dissertation establishing monetary stabilization principles that led to the Reserve Bank of India.", doc_id: "DOC_DAF_BAWS_PUB_1923_POR", primary_source_url: foundationCatalog, primary_source_label: "Browse Foundation Sources" },
    { year: 1927, date: "1927-03-20", title: "Mahad Satyagraha (Chavdar Tale Water Rights)", category: "Civil Rights Movement", description: "Leads historic non-violent assertion of civic equality and universal human rights to public drinking water.", doc_id: "DOC_DAF_BAWS_SPEECH_1927_MSD", primary_source_url: foundationCatalog, primary_source_label: "Browse Foundation Sources" },
    { year: 1932, date: "1932-09-24", title: "The Poona Pact Agreement", category: "Political Representation", description: "Secures 148 reserved legislative seats for the Depressed Classes across provincial assemblies.", doc_id: "DOC_DAF_BAWS_DOC_1932_POONA", primary_source_url: foundationCatalog, primary_source_label: "Browse Foundation Sources" },
    { year: 1936, date: "1936-05-15", title: "Annihilation of Caste Published", category: "Social Justice & Philosophy", description: "Publishes profound critique demonstrating caste as an unnatural division of labourers requiring eradication of orthodox sanctions.", doc_id: "DOC_DAF_BAWS_PUB_1936_AOC", primary_source_url: "https://www.mea.gov.in/Images/attach/amb/Volume_01.pdf", primary_source_label: "View Volume 1 (MEA mirror)" },
    { year: 1946, date: "1946-12-17", title: "Maiden Address to the Constituent Assembly", category: "Constitution Making", description: "Plea for national unity, mutual statesmanship, and constitutional justice for all communities.", doc_id: "DOC_CAD_CAD_VOL01_19461217", primary_source_url: "https://ambedkarfoundation.nic.in/audio.html", primary_source_label: "View Foundation Audio Source" },
    { year: 1948, date: "1948-11-04", title: "Introduction of the Draft Constitution", category: "Constitutional Jurisprudence", description: "Outlines Parliamentary executive model, flexible federalism, and fundamental rights protections.", doc_id: "DOC_CAD_CAD_VOL07_19481104", primary_source_url: parliamentDate("1948-11-04"), primary_source_label: "Browse Parliament Debate Records" },
    { year: 1948, date: "1948-11-29", title: "Abolition of Untouchability (Article 17 Adopted)", category: "Fundamental Rights", description: "Draft Article 11 unanimously adopted, outlawing untouchability and penalizing its enforcement.", doc_id: "DOC_CAD_CAD_VOL07_19481129", primary_source_url: parliamentDate("1948-11-29"), primary_source_label: "Browse Parliament Debate Records" },
    { year: 1949, date: "1949-11-25", title: "Final Constituent Assembly Address (Grammar of Anarchy)", category: "Democratic Philosophy", description: "Urges social democracy to sustain political democracy, warns against hero-worship/Bhakti in politics.", doc_id: "DOC_CAD_CAD_VOL11_19491125", primary_source_url: "https://eparlib.sansad.in/bitstream/123456789/763285/1/cad_25-11-1949.pdf", primary_source_label: "View Parliament Primary Source" },
    { year: 1956, date: "1956-10-14", title: "Deekshabhoomi Nagpur Buddhist Conversion", category: "Spiritual Emancipation", description: "Embraces Buddhism with 500,000 followers, enshrining 22 vows for egalitarian and rational life.", doc_id: "DOC_DAF_BAWS_PUB_1956_BHD", primary_source_url: foundationCatalog, primary_source_label: "Browse Foundation Sources" }
  ];

  let events = fallbackTimeline;
  try {
    const res = await fetch(`${API_BASE}/api/timeline`, { signal: AbortSignal.timeout(1500) });
    if (res.ok) {
      const data = await res.json();
      events = data.events;
    }
  } catch (err) {}

  // API milestones receive the same official-source links as offline preview events.
  const fallbackSources = new Map(fallbackTimeline.map(event => [event.date, event]));
  fallbackSources.set("1947-08-29", {
    primary_source_url: parliamentDate("1947-08-29"),
    primary_source_label: "Browse Parliament Debate Records"
  });
  events = events.map(event => ({ ...event, ...(fallbackSources.get(event.date) || {}) }));
  timelineEventByDocument = new Map(events.map(event => [event.doc_id, event]));
  timelineEventByDate = new Map(events.map(event => [event.date, event]));

  container.innerHTML = events.map(ev => `
    <div class="relative group">
      <div class="absolute -left-[31px] sm:-left-[39px] top-1.5 w-4 h-4 rounded-full bg-slate-900 border-2 border-amber-500 group-hover:scale-125 transition"></div>

      <div class="bg-slate-900/90 border border-slate-800 p-5 rounded-xl hover:border-amber-500/50 transition shadow-lg space-y-2">
        <div class="flex items-center justify-between text-xs">
          <span class="text-amber-400 font-serif font-bold text-base">${ev.year}</span>
          <span class="text-slate-400 bg-slate-800 px-2 py-0.5 rounded text-[11px]">${ev.category}</span>
        </div>

        <h3 class="font-serif font-bold text-base text-white hover:text-amber-400 cursor-pointer transition" onclick="openTimelineRecord('${ev.doc_id}', '${ev.date}')">
          ${ev.title}
        </h3>

        <p class="text-xs text-slate-300 leading-relaxed">
          ${ev.description}
        </p>

        <div class="pt-2 flex justify-end">
          <button onclick="openTimelineRecord('${ev.doc_id}', '${ev.date}')" class="text-amber-400 hover:text-amber-300 text-xs font-semibold flex items-center gap-1">
            <span>Read Original Historical Record</span>
            <i class="fa-solid fa-arrow-right text-[10px]"></i>
          </button>
        </div>
      </div>
    </div>
  `).join("");
}

function openTimelineRecord(docId, eventDate) {
  openDocModal(docId, timelineEventByDate.get(eventDate) || null);
}

// Archive-grounded research assistant
function askPresetQuestion(question) {
  const localizedQuestion = PRESET_QUESTION_TRANSLATIONS[question]?.[currentLanguage] || question;
  document.getElementById("aiInput").value = localizedQuestion;
  handleAiSubmit();
}

function findFallbackAssistantSources(question, language) {
  const termsByLanguage = {
    hi: [["जाति", "caste"], ["श्रम", "labour"], ["भक्ति", "bhakti"], ["व्यक्तिपूजा", "hero worship"], ["संविधान", "constitution"], ["लोकतंत्र", "democracy"], ["समानता", "equality"], ["अस्पृश्यता", "untouchability"], ["अनुच्छेद", "article"], ["रुपया", "rupee"], ["महाड", "mahad"], ["बौद्ध", "buddhism"], ["राष्ट्रपति", "presidential"], ["संसदीय", "parliamentary"], ["राजनीति", "politics"], ["चेतावनी", "warning"]],
    mr: [["जात", "caste"], ["कामगार", "labour"], ["भक्ती", "bhakti"], ["व्यक्तिपूजा", "hero worship"], ["संविधान", "constitution"], ["लोकशाही", "democracy"], ["समता", "equality"], ["अस्पृश्यता", "untouchability"], ["कलम", "article"], ["रुपया", "rupee"], ["महाड", "mahad"], ["बौद्ध", "buddhism"], ["राष्ट्रपती", "presidential"], ["संसदीय", "parliamentary"], ["राजकारण", "politics"], ["इशारा", "warning"]]
  };
  let normalized = question.toLocaleLowerCase();
  for (const [term, english] of (termsByLanguage[language] || [])) normalized = normalized.split(term).join(english);
  const ignored = new Set(["what", "when", "where", "which", "who", "why", "how", "did", "does", "was", "were", "the", "and", "for", "about", "from", "into", "with", "ambedkar", "his", "her", "not", "merely", "instead", "choose", "chosen"]);
  const terms = (normalized.match(/[a-z0-9]+/g) || []).filter(term => term.length > 2 && !ignored.has(term));
  if (!terms.length) return [];

  return FALLBACK_DOCS.map(doc => {
    const searchable = `${doc.title} ${doc.summary || ""} ${(doc.tags || []).join(" ")}`.toLowerCase();
    const score = terms.reduce((total, term) => total + (searchable.includes(term) ? 1 : 0), 0);
    return { doc, score };
  }).filter(result => result.score > 0).sort((a, b) => b.score - a.score).slice(0, 3).map(({ doc }) => ({
    id: doc.id, title: doc.title, author: doc.author, date: doc.date, source: doc.source,
    language: doc.language, excerpt: doc.summary
  }));
}

function updateAiVoiceUi() {
  const button = document.getElementById("aiVoiceBtn");
  const status = document.getElementById("aiVoiceStatus");
  if (!button || !status) return;
  const copy = AI_COPY[currentLanguage] || AI_COPY.en;
  const SpeechRecognitionApi = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognitionApi && aiVoiceStatusKey === "idle") aiVoiceStatusKey = "unsupported";
  const labels = {
    idle: copy.voiceIdle,
    listening: copy.voiceListening,
    done: copy.voiceDone,
    stopped: copy.voiceStopped,
    unsupported: copy.voiceUnsupported,
    permission: copy.voicePermission,
    noSpeech: copy.voiceNoSpeech,
    network: copy.voiceNetwork,
    audio: copy.voiceAudio,
    language: copy.voiceLanguage,
    service: copy.voiceService,
    error: copy.voiceError
  };
  const active = aiVoiceListening;
  button.disabled = !SpeechRecognitionApi;
  button.setAttribute("aria-pressed", String(active));
  button.setAttribute("aria-label", active ? copy.voiceStop : copy.voiceAsk);
  button.title = active ? copy.voiceStop : copy.voiceAsk;
  button.innerHTML = `<i class="fa-solid ${active ? "fa-stop" : "fa-microphone"}" aria-hidden="true"></i>`;
  button.classList.toggle("text-red-300", active);
  button.classList.toggle("border-red-400", active);
  status.textContent = labels[aiVoiceStatusKey] || labels.idle;
}

function toggleAiVoiceInput() {
  if (aiVoiceListening && aiRecognition) {
    aiVoiceStatusKey = aiVoiceHadFinalResult ? "done" : "stopped";
    aiRecognition.stop();
    aiVoiceListening = false;
    updateAiVoiceUi();
    return;
  }

  const SpeechRecognitionApi = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognitionApi) {
    aiVoiceStatusKey = "unsupported";
    updateAiVoiceUi();
    return;
  }

  const recognition = new SpeechRecognitionApi();
  const input = document.getElementById("aiInput");
  const language = currentLanguage;
  const speechLocale = { en: "en-IN", hi: "hi-IN", mr: "mr-IN" }[language] || "en-IN";
  let finalTranscript = input.value.trim();
  if (finalTranscript) finalTranscript += " ";
  aiRecognition = recognition;
  aiVoiceHadFinalResult = false;
  recognition.lang = speechLocale;
  recognition.continuous = false;
  recognition.interimResults = true;
  recognition.maxAlternatives = 1;
  recognition.onstart = () => {
    aiVoiceListening = true;
    aiVoiceStatusKey = "listening";
    updateAiVoiceUi();
  };
  recognition.onresult = event => {
    let interimTranscript = "";
    for (let index = event.resultIndex; index < event.results.length; index += 1) {
      const result = event.results[index];
      if (result.isFinal) {
        finalTranscript += `${result[0].transcript.trim()} `;
        aiVoiceHadFinalResult = true;
      } else {
        interimTranscript += result[0].transcript;
      }
    }
    input.value = `${finalTranscript}${interimTranscript}`.trim();
    aiVoiceStatusKey = aiVoiceHadFinalResult ? "done" : "listening";
    updateAiVoiceUi();
  };
  recognition.onerror = event => {
    const errorKeys = {
      "not-allowed": "permission",
      "service-not-allowed": "service",
      "no-speech": "noSpeech",
      "audio-capture": "audio",
      network: "network",
      "language-not-supported": "language"
    };
    aiVoiceStatusKey = errorKeys[event.error] || "error";
    aiVoiceListening = false;
    updateAiVoiceUi();
  };
  recognition.onend = () => {
    aiVoiceListening = false;
    if (aiVoiceStatusKey === "listening") aiVoiceStatusKey = aiVoiceHadFinalResult ? "done" : "noSpeech";
    if (aiRecognition === recognition) aiRecognition = null;
    updateAiVoiceUi();
  };
  try {
    aiVoiceStatusKey = "listening";
    recognition.start();
  } catch (error) {
    aiRecognition = null;
    aiVoiceListening = false;
    aiVoiceStatusKey = error?.name === "NotAllowedError" || error?.name === "SecurityError"
      ? "permission"
      : error?.name === "InvalidStateError" ? "service" : "error";
  }
  updateAiVoiceUi();
}

async function handleAiSubmit() {
  const input = document.getElementById("aiInput");
  const query = input.value.trim();
  if (!query) return;

  const thread = document.getElementById("aiChatThread");
  const userRow = document.createElement("div");
  userRow.className = "flex items-start justify-end gap-3";
  const userBubble = document.createElement("div");
  userBubble.className = "bg-amber-600/20 border border-amber-500/30 p-3.5 rounded-xl text-sm max-w-2xl text-slate-100";
  const copy = AI_COPY[currentLanguage] || AI_COPY.en;
  const questionLabel = document.createElement("p");
  questionLabel.className = "text-amber-400 font-semibold text-xs mb-1";
  questionLabel.textContent = copy.questionLabel;
  const userText = document.createElement("p");
  userText.textContent = query;
  userBubble.append(questionLabel, userText);
  userRow.append(userBubble);
  thread.append(userRow);
  input.value = "";

  const pending = document.createElement("p");
  pending.className = "text-xs text-slate-400";
  pending.textContent = copy.searching;
  thread.append(pending);
  thread.scrollTop = thread.scrollHeight;

  let data;
  try {
    const response = await fetch(`${API_BASE}/api/assistant`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: query, language: currentLanguage })
    });
    data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Archive search failed.");
  } catch (_) {
    const sources = findFallbackAssistantSources(query, currentLanguage);
    await Promise.all(sources.map(async source => {
      try {
        const docResponse = await fetch(`${API_BASE}/api/documents/${encodeURIComponent(source.id)}`);
        if (!docResponse.ok) return;
        const wrapper = await docResponse.json();
        const record = wrapper.document || wrapper;
        const translation = record.translations?.[currentLanguage] || {};
        source.display_title = translation.title || record.title || source.title;
        source.localized_summary = translation.summary || record.content?.summary || source.excerpt;
      } catch (_) {}
    }));
    const summaries = sources.map(source => source.localized_summary).filter(Boolean);
    data = {
      answer: sources.length
        ? [copy.offlineFound.replace("{count}", sources.length), copy.summaryHeading, ...summaries.map(summary => `• ${summary}`)].join("\n\n")
        : copy.offlineEmpty,
      sources
    };
  }
  pending.remove();

  try {
    const answerRow = document.createElement("div");
    answerRow.className = "flex items-start gap-3";
    const answerBubble = document.createElement("div");
    answerBubble.className = "bg-slate-900 p-4 rounded-xl border border-slate-800 text-sm max-w-2xl space-y-3";
    const answerLabel = document.createElement("p");
    answerLabel.className = "text-amber-300 font-semibold text-xs";
    answerLabel.textContent = copy.responseLabel;
    answerBubble.append(answerLabel);
    const answerText = document.createElement("p");
    answerText.className = "text-slate-200 leading-relaxed whitespace-pre-line";
    answerText.textContent = data.answer;
    answerBubble.append(answerText);

    for (const source of data.sources) {
      const sourceBlock = document.createElement("div");
      sourceBlock.className = "p-3 rounded bg-slate-950 border border-slate-800/80 space-y-2";
      const title = document.createElement("p");
      title.className = "text-amber-400 font-medium text-xs";
      title.textContent = source.display_title || source.title;
      const details = document.createElement("p");
      details.className = "text-slate-400 text-[11px]";
      details.textContent = [source.author, source.date, source.source, source.language].filter(Boolean).join(" · ");
      if (source.localized_summary) {
        const localizedSummary = document.createElement("p");
        localizedSummary.className = "text-slate-200 text-xs leading-relaxed";
        localizedSummary.textContent = `${copy.summaryHeading}: ${source.localized_summary}`;
        sourceBlock.append(title, details, localizedSummary);
      } else {
        sourceBlock.append(title, details);
      }
      const excerpt = document.createElement("p");
      excerpt.className = "text-slate-200 text-xs leading-relaxed whitespace-pre-line";
      excerpt.textContent = source.excerpt || copy.noExcerpt;
      const excerptLabel = document.createElement("p");
      excerptLabel.className = "text-slate-500 text-[10px] uppercase tracking-wide";
      excerptLabel.textContent = copy.originalExcerpt;
      const sourceButton = document.createElement("button");
      sourceButton.className = "px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded text-[11px]";
      sourceButton.textContent = copy.viewSource;
      sourceButton.addEventListener("click", () => openDocModal(source.id));
      sourceBlock.append(excerptLabel, excerpt, sourceButton);
      answerBubble.append(sourceBlock);
    }

    answerRow.append(answerBubble);
    thread.append(answerRow);
  } catch (error) {
    pending.textContent = copy.error;
    pending.className = "text-xs text-rose-400";
  }

  thread.scrollTop = thread.scrollHeight;
}

// Institutional Analytics
async function loadStats() {
  const fallbackStats = {
    total_documents: 530,
    total_words_indexed: 86624,
    total_embedding_chunks: 835,
    languages: { en: 410, hi: 42, te: 27, mr: 18, bn: 11, ta: 9, gu: 9, pa: 2, ml: 1, ka: 1 },
    sources: { IA: 510, CAD: 10, Foundation: 10 },
    languages_by_source: ARCHIVE_LANGUAGE_SOURCES
  };

  let data = fallbackStats;
  try {
    const res = await fetch(`${API_BASE}/api/stats`, { signal: AbortSignal.timeout(1500) });
    if (res.ok) {
      data = await res.json();
    }
  } catch (err) {}

  Object.keys(ARCHIVE_SOURCE_TOTALS).forEach((source) => delete ARCHIVE_SOURCE_TOTALS[source]);
  Object.assign(ARCHIVE_SOURCE_TOTALS, data.sources || {});
  Object.keys(ARCHIVE_LANGUAGE_SOURCES).forEach((language) => delete ARCHIVE_LANGUAGE_SOURCES[language]);
  Object.assign(ARCHIVE_LANGUAGE_SOURCES, data.languages_by_source || {});
  archiveTypeCounts = data.types || {};
  renderArchiveFilterSources();
  renderArchiveFilterTypes(archiveTypeCounts);

  document.getElementById("statTotalDocs").innerText = data.total_documents.toLocaleString();
  document.getElementById("statTotalWords").innerText = data.total_words_indexed.toLocaleString();
  document.getElementById("statTotalChunks").innerText = data.total_embedding_chunks.toLocaleString();
  const heroRecordCount = document.getElementById("heroRecordCount");
  const heroLanguageCount = document.getElementById("heroLanguageCount");
  if (heroRecordCount) heroRecordCount.innerText = `${data.total_documents.toLocaleString()}+`;
  if (heroLanguageCount) heroLanguageCount.innerText = Object.keys(data.languages).length.toString();

  // Languages list
  const langContainer = document.getElementById("languageBreakdownList");
  const langNames = {
    en: "English", hi: "Hindi", mr: "Marathi", te: "Telugu",
    bn: "Bengali", ta: "Tamil", gu: "Gujarati", pa: "Punjabi",
    ka: "Kannada", ml: "Malayalam"
  };

  langContainer.innerHTML = Object.entries(data.languages).map(([code, count]) => {
    const pct = Math.round((count / data.total_documents) * 100);
    return `
      <div>
        <div class="flex justify-between text-slate-300 mb-1">
          <span>${langNames[code] || code.toUpperCase()} (${code})</span>
          <span class="font-mono text-amber-400 font-bold">${count} (${pct}%)</span>
        </div>
        <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
          <div class="bg-amber-500 h-full rounded-full" style="width: ${pct}%"></div>
        </div>
      </div>
    `;
  }).join("");

  // Sources list
  const sourceContainer = document.getElementById("sourcesBreakdownList");
  sourceContainer.innerHTML = Object.entries(data.sources).map(([src, count]) => {
    const sourceName = src === "IA" ? "Internet Archive (Open Public Domain)"
      : src === "CAD" ? "Constituent Assembly Debates (Parliament Digital Library)"
      : src === "Foundation" ? "Dr. Ambedkar Foundation / BAWS"
      : src === "NDL" ? "National Digital Library of India"
      : (ARCHIVE_SOURCES[src]?.en || src);
    return `
      <div>
        <div class="flex justify-between text-slate-300 mb-1">
          <span>${sourceName}</span>
          <span class="font-mono text-emerald-400 font-bold">${count} items</span>
        </div>
        <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
          <div class="bg-emerald-500 h-full rounded-full" style="width: 100%"></div>
        </div>
      </div>
    `;
  }).join("");
}

function renderArchiveFilterTypes(typeCounts) {
  const select = document.getElementById("filterType");
  if (!select) return;
  const selected = select.value;
  const names = {
    en: { publication: "Publications", speech: "Speeches", debate: "CAD Debates", manuscript: "Manuscripts", other: "Historical Records" },
    hi: { publication: "प्रकाशन", speech: "भाषण", debate: "संविधान सभा की बहसें", manuscript: "पांडुलिपियाँ", other: "ऐतिहासिक अभिलेख" },
    mr: { publication: "प्रकाशने", speech: "भाषणे", debate: "संविधान सभा चर्चा", manuscript: "हस्तलिखिते", other: "ऐतिहासिक नोंदी" }
  }[currentLanguage] || {};
  const allLabels = { en: "All Document Types", hi: "सभी दस्तावेज़ प्रकार", mr: "सर्व दस्तऐवज प्रकार" };
  const ordered = ["publication", "speech", "debate", "manuscript", "other"];
  const keys = [...ordered.filter(type => typeCounts[type] > 0), ...Object.keys(typeCounts).filter(type => !ordered.includes(type))];
  select.innerHTML = `<option value="">${allLabels[currentLanguage] || allLabels.en}</option>` + keys.map(type =>
    `<option value="${type}">${names[type] || type.replace(/_/g, " ")} (${typeCounts[type]})</option>`
  ).join("");
  select.value = keys.includes(selected) ? selected : "";
}

// Manual Document Ingestion
async function handleOcrUpload() {
  const fileInput = document.getElementById("ocrFile");
  const statusMsg = document.getElementById("ocrStatusMsg");
  const file = fileInput.files[0];
  if (!file) {
    statusMsg.innerText = "Choose a PDF or image first.";
    statusMsg.className = "text-xs text-rose-400 mt-2";
    return;
  }

  lastOcrMetadata = null;
  statusMsg.innerHTML = '<span class="ocr-reading"><span class="ocr-spinner" aria-hidden="true"></span> Reading historical document…</span>';
  statusMsg.setAttribute("aria-busy", "true");
  statusMsg.className = "text-xs text-amber-400 mt-2";

  const formData = new FormData();
  formData.append("file", file);
  formData.append("language", document.getElementById("ingestLanguage").value);
  const mode = document.getElementById("ocrMode")?.value || "printed";
  formData.append("mode", mode);

  try {
    const response = await fetch(`${API_BASE}/api/ocr`, {
      method: "POST",
      body: formData
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || "OCR extraction failed.");

    document.getElementById("ingestContent").value = result.text;
    lastOcrMetadata = {
      original_filename: result.filename,
      engine: result.engine || "Tesseract",
      model: result.model || result.language,
      mode: result.mode || mode,
      language: result.language,
      pages_processed: result.pages_processed
    };

    const wordCount = result.text.trim() ? result.text.trim().split(/\s+/).length : 0;
    statusMsg.innerText = wordCount
      ? `Extracted ${wordCount} words from ${result.pages_processed} page(s) using ${mode === "handwritten" ? "the handwriting model" : "printed-text OCR"}. Review the text below before ingesting.`
      : "No text was detected. Try a clearer scan or another OCR language.";
    statusMsg.className = wordCount ? "text-xs text-emerald-400 mt-2" : "text-xs text-amber-400 mt-2";
  } catch (error) {
    statusMsg.innerText = error.message;
    statusMsg.className = "text-xs text-rose-400 mt-2";
  } finally {
    statusMsg.setAttribute("aria-busy", "false");
  }
}

async function updateHandwritingModelStatus() {
  const status = document.getElementById("handwritingModelStatus");
  const mode = document.getElementById("ocrMode")?.value || "printed";
  if (!status) return;
  if (mode !== "handwritten") {
    status.textContent = "Printed mode uses the installed multilingual Tesseract models.";
    status.className = "text-xs text-slate-400 mb-2";
    return;
  }
  status.textContent = "Checking custom handwriting model…";
  status.className = "text-xs text-amber-400 mb-2";
  try {
    const response = await fetch(`${API_BASE}/api/ocr/model-status`);
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || "Could not check OCR model status.");
    status.textContent = result.message;
    status.className = result.installed
      ? "text-xs text-emerald-400 mb-2"
      : "text-xs text-amber-400 mb-2";
  } catch (error) {
    status.textContent = error.message || "Could not check the handwriting model status.";
    status.className = "text-xs text-rose-400 mb-2";
  }
}

async function handleManualIngest(e) {
  e.preventDefault();
  const statusMsg = document.getElementById("ingestStatusMsg");
  statusMsg.innerText = "Ingesting and indexing into FTS5...";
  statusMsg.className = "text-xs text-amber-400";

  const title = document.getElementById("ingestTitle").value;
  const author = document.getElementById("ingestAuthor").value;
  const date = document.getElementById("ingestDate").value;
  const docType = document.getElementById("ingestType").value;
  const lang = document.getElementById("ingestLanguage").value;
  const tags = document.getElementById("ingestTags").value.split(",").map(s => s.trim());
  const content = document.getElementById("ingestContent").value;

  const docId = `DOC_MANUAL_${Date.now()}`;
  const payload = {
    document: {
      id: docId,
      title: title,
      author: author,
      date: date,
      type: docType,
      language: lang,
      content: {
        full_text: content,
        summary: content.slice(0, 250) + "...",
        key_quotes: [content.slice(0, 100) + "..."]
      },
      metadata: {
        source: "Foundation",
        archive_reference: `MANUAL-${docId}`,
        collection: "Institutional Upload",
        pages: 1,
        word_count: content.split(/\s+/).length,
        condition: "good",
        accessibility: "public"
      },
      tags: tags,
      relations: { references: [], related_to: [], debates: [] },
      translations: {},
      media: lastOcrMetadata ? { ocr: lastOcrMetadata } : {}
    }
  };

  try {
    const res = await fetch(`${API_BASE}/api/ingest`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const result = await res.json();
    if (res.ok) {
      statusMsg.innerText = "✓ Ingested successfully into SQLite & FTS5!";
      statusMsg.className = "text-xs text-emerald-400 font-bold";
      document.getElementById("ingestForm").reset();
      lastOcrMetadata = null;
      loadStats();
      executeSearch();
    } else {
      statusMsg.innerText = "Error: " + result.detail;
      statusMsg.className = "text-xs text-rose-400";
    }
  } catch (err) {
    statusMsg.innerText = "Ingestion failed (Backend offline). Start backend with: python backend/app.py";
    statusMsg.className = "text-xs text-rose-400";
  }
}

// Fullscreen Kiosk Mode
function toggleFullScreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen().catch(err => {
      console.log(`Fullscreen error: ${err.message}`);
    });
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    }
  }
}

// Multilingual UI Switcher
function setUiLanguage(lang) {
  if (!["en", "hi", "mr"].includes(lang)) return;
  const restartNarration = currentLanguage !== lang && currentDocInModal && (
    narrationRequestController ||
    (narrationAudio && !narrationAudio.paused) ||
    (synth && (synth.speaking || synth.pending))
  );
  if (currentLanguage !== lang) {
    stopSpeech();
    if (aiRecognition) aiRecognition.stop();
    aiVoiceListening = false;
    aiVoiceStatusKey = "idle";
  }
  currentLanguage = lang;
  document.documentElement.lang = lang;
  [["langSelectEn", "en"], ["langSelectHi", "hi"], ["langSelectMr", "mr"]].forEach(([id, code]) => {
    const button = document.getElementById(id);
    if (!button) return;
    const active = lang === code;
    button.className = active
      ? "px-2.5 py-1 rounded bg-amber-600 text-white font-medium"
      : "px-2.5 py-1 rounded text-slate-300 hover:text-white";
    button.setAttribute("aria-pressed", String(active));
  });
  applyUiTranslations();
  updateAiVoiceUi();
  renderArchiveFilterSources();
  renderArchiveFilterTypes(archiveTypeCounts);
  setArchiveTheme(document.body.dataset.theme, false);
  try { localStorage.setItem("ambedkar-archive-language", lang); } catch (_) { /* Keep the current selection for this session. */ }
  if (restartNarration) toggleAudioNarration();
}

function handleArchiveLanguageChange() {
  renderArchiveFilterSources();
  executeSearch();
}

function renderArchiveFilterSources() {
  const languageSelect = document.getElementById("filterLanguage");
  const sourceSelect = document.getElementById("filterSource");
  const hint = document.getElementById("sourceAvailability");
  if (!languageSelect || !sourceSelect) return;

  const language = languageSelect.value;
  const selectedSource = sourceSelect.value;
  const sourceCounts = language
    ? (ARCHIVE_LANGUAGE_SOURCES[language] || {})
    : ARCHIVE_SOURCE_TOTALS;
  const entries = Object.entries(sourceCounts).filter(([, count]) => count > 0);
  const allLabel = { en: "All Repositories", hi: "सभी अभिलेखागार", mr: "सर्व संग्रह" }[currentLanguage];
  sourceSelect.innerHTML = `<option value="">${allLabel}</option>` + entries.map(([source, count]) => {
    const label = ARCHIVE_SOURCES[source][currentLanguage] || ARCHIVE_SOURCES[source].en;
    return `<option value="${source}">${label} (${count})</option>`;
  }).join("");
  sourceSelect.value = entries.some(([source]) => source === selectedSource) ? selectedSource : "";

  if (!hint) return;
  if (!language) {
    hint.textContent = SOURCE_HINT_COPY[currentLanguage].all;
    return;
  }
  const languageName = ARCHIVE_LANGUAGES[language]?.[currentLanguage] || language.toUpperCase();
  const sourceNames = entries.map(([source, count]) => `${ARCHIVE_SOURCES[source][currentLanguage]} (${count})`);
  if (currentLanguage === "hi") {
    hint.textContent = `${languageName} अभिलेखों के स्रोत: ${sourceNames.join(", ")}।`;
  } else if (currentLanguage === "mr") {
    hint.textContent = `${languageName} भाषेतील नोंदींचे स्रोत: ${sourceNames.join(", ")}.`;
  } else {
    hint.textContent = `Sources for ${languageName} records: ${sourceNames.join(", ")}.`;
  }
}

function applyUiTranslations() {
  const translations = {
    ...(UI_TRANSLATIONS[currentLanguage] || {}),
    ...(TIMELINE_TRANSLATIONS[currentLanguage] || {})
  };
  const textNodes = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let textNode;

  while ((textNode = textNodes.nextNode())) {
    if (!originalUiText.has(textNode)) originalUiText.set(textNode, textNode.nodeValue);
    const original = originalUiText.get(textNode);
    const trimmed = original.trim();
    const translated = translations[trimmed];
    const start = original.indexOf(trimmed);
    const translatedValue = translated
      ? `${original.slice(0, start)}${translated}${original.slice(start + trimmed.length)}`
      : original;
    if (textNode.nodeValue !== translatedValue) textNode.nodeValue = translatedValue;
  }

  document.querySelectorAll("[placeholder]").forEach(element => {
    if (!originalPlaceholders.has(element)) originalPlaceholders.set(element, element.placeholder);
    const original = originalPlaceholders.get(element);
    const translatedPlaceholder = translations[original] || original;
    if (element.placeholder !== translatedPlaceholder) element.placeholder = translatedPlaceholder;
  });

  document.querySelectorAll("[aria-label], [title], [alt]").forEach(element => {
    const attributes = ["aria-label", "title", "alt"].filter(name => element.hasAttribute(name));
    if (!originalUiAttributes.has(element)) {
      originalUiAttributes.set(element, Object.fromEntries(attributes.map(name => [name, element.getAttribute(name)])));
    }
    const original = originalUiAttributes.get(element);
    attributes.forEach(name => {
      const translatedAttribute = translations[original[name]] || original[name];
      if (element.getAttribute(name) !== translatedAttribute) element.setAttribute(name, translatedAttribute);
    });
  });
}
