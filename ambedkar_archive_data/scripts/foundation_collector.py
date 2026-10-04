"""
Dr. Ambedkar Foundation / BAWS Primary Works Collector
Gathers foundational treatises, historical publications, and social reform declarations.
"""

import json
import logging
from typing import List, Dict, Any
from config import RAW_DOCS_DIR, init_directories

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

FOUNDATION_WORKS = [
    {
        "work_id": "BAWS_PUB_1936_AOC",
        "title": "Annihilation of Caste",
        "date": "1936-05-15",
        "type": "publication",
        "volume": "BAWS Vol. 1",
        "pages": "23-96",
        "full_text": (
            "Caste is not just a division of labour, it is a division of labourers. Civilized society requires division of labour. "
            "But in no civilized society is division of labour accompanied by this unnatural division of labourers into water-tight compartments. "
            "Caste System is not merely division of labourers which is quite different from division of labour - it is an hierarchy in which "
            "the divisions of labourers are graded one above the other.\n\n"
            "You cannot build anything on the foundations of caste. You cannot build up a nation, you cannot build up an ethical morality. "
            "Anything that you will build on the foundations of caste will crack and will never be a whole.\n\n"
            "The real remedy is to destroy the belief in the sanctity of the shastras. How do you do that? You must have courage to tell "
            "the people that what is called religion is nothing but a multitude of rules and regulations. Religion in the true sense of the term "
            "must be based on principles, not on rules. A religion of rules is not religion; it is spiritual slavery.\n\n"
            "Political democracy cannot succeed where social equality is absent. Make every man and woman equal in status, equal in opportunities, "
            "and dismantle the hierarchical religious sanctions that maintain caste injustice."
        ),
        "summary": "Dr. Ambedkar's masterpiece undelivered address prepared for the Jat-Pat-Todak Mandal, systematically demonstrating that caste is an anti-social hierarchy of labourers, not merely division of labour, and calling for the destruction of religious shastra sanctions that legitimize caste discrimination.",
        "key_quotes": [
            "Caste is not just a division of labour, it is a division of labourers.",
            "You cannot build anything on the foundations of caste. You cannot build up a nation, you cannot build up an ethical morality.",
            "Religion must be based on principles, not on rules."
        ],
        "tags": ["social_justice", "annihilation_of_caste", "equality", "caste_reform", "human_rights", "morality"],
        "translations": {
            "hi": {
                "title": "जाति का विनाश (Annihilation of Caste)",
                "summary": "डॉ. अंबेडकर का ऐतिहासिक ग्रंथ जिसमें उन्होंने जाति व्यवस्था को श्रम का विभाजन नहीं बल्कि श्रमिकों का अमानवीय विभाजन सिद्ध किया और सामाजिक समानता की अनिवार्यता पर बल दिया।"
            },
            "mr": {
                "title": "जातीचे निर्मूलन (Annihilation of Caste)",
                "summary": "डॉ. बाबासाहेब आंबेडकरांचा क्रांतिकारी विचारप्रवर्तक ग्रंथ, ज्यामध्ये त्यांनी जातीव्यवस्था ही केवळ कामाची विभागणी नसून कामगारांची विषम श्रेणीबद्ध विभागणी असल्याचे स्पष्ट केले."
            }
        }
    },
    {
        "work_id": "BAWS_PUB_1916_CII",
        "title": "Castes in India: Their Mechanism, Genesis and Development",
        "date": "1916-05-09",
        "type": "publication",
        "volume": "BAWS Vol. 1",
        "pages": "3-22",
        "full_text": (
            "Presented before the Anthropology Seminar of Dr. A. A. Goldenweiser at Columbia University, New York.\n\n"
            "Caste in India is an endogamous group enclosed in an otherwise exogamous population. Endogamy is the only one that is peculiar "
            "to caste. Caste in India means an artificial chopping off of the population into fixed and definite units, each one prevented from "
            "fusing into another through the strict enforcement of endogamy. Sati, enforced widowhood, and child marriage are the natural "
            "corollaries used to maintain the mathematical balance between sexes within the closed caste circle."
        ),
        "summary": "Dr. Ambedkar's landmark academic paper at Columbia University providing the first anthropological and sociological demonstration that caste is maintained through enforced endogamy and gender subjugation.",
        "key_quotes": [
            "Endogamy is the only one that is peculiar to caste... an enclosed class.",
            "Caste in India means an artificial chopping off of the population into fixed and definite units."
        ],
        "tags": ["anthropology", "endogamy", "columbia_university", "gender_justice", "sociology"]
    },
    {
        "work_id": "BAWS_PUB_1935_WFV",
        "title": "Waiting for a Visa: Autobiographical Life Sketches",
        "date": "1935-10-01",
        "type": "manuscript",
        "volume": "BAWS Vol. 12",
        "pages": "661-691",
        "full_text": (
            "Foreigners, of course, know of the existence of untouchability. But not being ground by it, they cannot know what it is to be an "
            "Untouchable. They cannot realize how an Untouchable is treated by society from morning till night.\n\n"
            "This book contains four personal autobiographical experiences: traveling to Masur in Satara as a child, working in Baroda state "
            "as Finance Minister where peons flung files at my desk and no inn or hotel would accommodate me, suffering near Daulatabad fort "
            "over drinking water, and being stranded in a rural village. They illustrate the visceral, systemic indignities suffered by the depressed classes."
        ),
        "summary": "Dr. Ambedkar's poignant autobiographical sketches recording personal encounters with severe caste discrimination, untouchability, and denial of basic shelter and dignity despite highest academic distinctions.",
        "key_quotes": [
            "Foreigners know of untouchability, but not being ground by it, they cannot know what it is to be an Untouchable.",
            "A man with degrees from Columbia and London could find no roof under which to lay his head in Baroda."
        ],
        "tags": ["autobiography", "untouchability", "lived_experience", "human_dignity", "education"]
    },
    {
        "work_id": "BAWS_PUB_1923_POR",
        "title": "The Problem of the Rupee: Its Origin and Its Solution",
        "date": "1923-12-01",
        "type": "publication",
        "volume": "BAWS Vol. 6",
        "pages": "315-620",
        "full_text": (
            "Doctor of Science (Economics) thesis submitted to the University of London (London School of Economics).\n\n"
            "The stability of a currency is determined not merely by gold backing, but by controlling the quantity of money to prevent "
            "inflationary depreciation and preserve purchasing power for working people. An automatic currency managed without political "
            "tampering is vital for safeguarding the economic livelihood of the poor. This treatise laid the intellectual framework "
            "submitted to the Hilton Young Royal Commission which led to the creation of the Reserve Bank of India (RBI)."
        ),
        "summary": "Dr. Ambedkar's seminal doctoral treatise in economics analyzing monetary policy, currency standards, and exchange rate stabilization, which formed the foundational blueprint for the Reserve Bank of India.",
        "key_quotes": [
            "Nothing can be more harmful to the welfare of the working classes than a depreciating currency that erodes their purchasing power.",
            "Currency management requires scientific rigor and independence from executive whim."
        ],
        "tags": ["economics", "monetary_policy", "rbi", "london_school_of_economics", "rupee_standard", "labor"]
    },
    {
        "work_id": "BAWS_PUB_1947_SAM",
        "title": "States and Minorities: What are Their Rights and How to Secure Them",
        "date": "1947-03-15",
        "type": "publication",
        "volume": "BAWS Vol. 1",
        "pages": "381-449",
        "full_text": (
            "Memorandum on the Safeguards for the Scheduled Castes submitted to the Constituent Assembly on behalf of the All India Scheduled Castes Federation.\n\n"
            "This document is a complete constitution in draft form. It proposes State Socialism: key industries, basic industries, and insurance "
            "shall be owned and run by the State; agricultural land shall be nationalized and leased to collective farms composed of all residents "
            "without distinction of caste or creed. It provides that fundamental rights must protect individual liberty against state tyranny, but also "
            "safeguard weaker sections from economic exploitation by private monopolies."
        ),
        "summary": "Dr. Ambedkar's radical constitutional memorandum proposing State Socialism, nationalization of basic industries, collective farming, and robust statutory safeguards for minorities and depressed classes.",
        "key_quotes": [
            "Political democracy must be sustained by economic democracy; state socialism must be prescribed by the law of the constitution itself.",
            "The soul of democracy is the doctrine of one man, one value."
        ],
        "tags": ["state_socialism", "constitutional", "minorities", "economic_justice", "fundamental_rights"]
    },
    {
        "work_id": "BAWS_PUB_1946_WWS",
        "title": "Who Were the Shudras? How They Came to Be the Fourth Varna",
        "date": "1946-10-10",
        "type": "publication",
        "volume": "BAWS Vol. 7",
        "pages": "1-228",
        "full_text": (
            "Dedicated to Jyotirao Phule, the greatest modern social reformer of Maharashtra.\n\n"
            "Through exhaustive historical and textual analysis of Vedic literature, Dr. Ambedkar proves that the Shudras were originally "
            "Aryans belonging to the solar dynasty who had a high status, and that their degradation into a subordinate fourth varna was the "
            "outcome of a prolonged historical struggle with the orthodox priesthood over social and religious supremacy."
        ),
        "summary": "Ambedkar's seminal historical treatise analyzing the origins of social stratification and the artificial creation of the fourth varna in ancient India, dedicated to Mahatma Jyotirao Phule.",
        "key_quotes": [
            "The Shudras were not a distinct racial non-Aryan group; their subjugation was a political and religious consequence of historical conflicts.",
            "Dedicated to Mahatma Jyotirao Phule, who awakened the masses to their human dignity."
        ],
        "tags": ["history", "shudras", "jyotirao_phule", "social_reform", "ancient_india"]
    },
    {
        "work_id": "BAWS_PUB_1956_BHD",
        "title": "The Buddha and His Dhamma",
        "date": "1956-11-01",
        "type": "publication",
        "volume": "BAWS Vol. 11",
        "pages": "1-600",
        "full_text": (
            "Dr. Ambedkar's magnum opus on Buddhist philosophy, completed shortly before his passing in December 1956.\n\n"
            "The purpose of religion is to reconstruct the world, not to explain its origin or preserve social hierarchy. Buddhism is grounded "
            "in Morality (Sila), Wisdom (Panna), and Universal Compassion (Karuna). Unlike theistic religions that demand unconditional surrender to "
            "supernatural revelation, the Dhamma demands reason, self-examination, and relentless moral action for the alleviation of human suffering (Dukkha). "
            "Equality and fraternity are the ethical bedrock of the Sangha and civilized human society."
        ),
        "summary": "Dr. Ambedkar's monumental philosophical exposition of Buddhism as an ethical, rational, and egalitarian philosophy of human liberation, social reconstruction, and universal compassion.",
        "key_quotes": [
            "The purpose of religion is to reconstruct the world, not to explain its origin.",
            "Morality is Dhamma, and Dhamma is Morality. In Dhamma, morality is sacred and universal."
        ],
        "tags": ["buddhism", "dhamma", "philosophy", "ethics", "equality", "compassion"]
    },
    {
        "work_id": "BAWS_SPEECH_1927_MSD",
        "title": "Mahad Satyagraha Address (Chavdar Tale Water Rights)",
        "date": "1927-12-25",
        "volume": "BAWS Vol. 17 (Part 1)",
        "pages": "1-18",
        "type": "speech",
        "full_text": (
            "Address delivered at the Mahad Satyagraha Conference on 25th December 1927, where the Manusmriti was publicly burned.\n\n"
            "At Chavdar Tale, we did not go to drink water because we believed that water had medicinal value or that drinking it would make us immortal. "
            "We went there to assert our human rights, to declare to the world that we are human beings with the same dignity and claims to nature's gifts "
            "as any other citizen. This satyagraha is not merely about water; it is about establishing the fundamental equality of all persons in society."
        ),
        "summary": "Dr. Ambedkar's historic address at the Mahad Satyagraha, framing the access to the public Chavdar water reservoir not as a mere thirst issue, but as a defining non-violent struggle for universal human rights and civic equality.",
        "key_quotes": [
            "We are not fighting for water; we are fighting to establish that we are human beings.",
            "Equality must be established not as an exception, but as the universal rule of law."
        ],
        "tags": ["mahad_satyagraha", "civil_rights", "water_rights", "human_dignity", "equality"]
    },
    {
        "work_id": "BAWS_DOC_1932_POONA",
        "title": "The Poona Pact Agreement and Statement",
        "date": "1932-09-24",
        "volume": "BAWS Vol. 2",
        "pages": "463-472",
        "type": "other",
        "full_text": (
            "Agreement arrived at between the leaders of the Caste Hindus and the Depressed Classes at Yerwada Central Prison, Poona.\n\n"
            "There shall be seats reserved for the Depressed Classes out of the general electorate seats in Provincial Legislatures. The number of "
            "reserved seats was increased from 71 (under the Communal Award) to 148 seats across Madras, Bombay, Bengal, United Provinces, Punjab, "
            "Bihar and Orissa, Central Provinces, and Assam. Election to these seats shall be through joint electorates with a primary election system "
            "to ensure authentic representation of the depressed classes, along with non-discrimination in public employment and education funds."
        ),
        "summary": "The historic Poona Pact agreement negotiated by Dr. Ambedkar, securing 148 reserved legislative seats for the Depressed Classes across provincial legislatures within joint electorates.",
        "key_quotes": [
            "There shall be reserved seats for the Depressed Classes within joint electorates, ensuring their authentic political representation."
        ],
        "tags": ["poona_pact", "political_representation", "depressed_classes", "electorates", "reservation"]
    },
    {
        "work_id": "BAWS_PUB_1920_MUK",
        "title": "Muknayak (Leader of the Voiceless) Inaugural Editorial",
        "date": "1920-01-31",
        "volume": "BAWS Vol. 19",
        "pages": "1-12",
        "type": "publication",
        "full_text": (
            "Dr. Ambedkar launched the fortnightly Marathi newspaper 'Muknayak' with the patron support of Chhatrapati Shahu Maharaj.\n\n"
            "Hindu society is like a multi-storied tower with no staircase and no entrance doors. One must die in the storey in which one was born. "
            "Those living on the top storeys have all privileges, light, and fresh air; those consigned to the bottom live in perpetual darkness and filth, "
            "forbidden from climbing up or mingling. A society structured like this without social mobility or fraternity is doomed to decline. "
            "Muknayak is founded to give voice to those who have been forcibly silenced for centuries."
        ),
        "summary": "The foundational editorial of Dr. Ambedkar's first journal, Muknayak, comparing caste society to an elevator-less, doorless multi-storey tower and declaring journalism as a weapon for the emancipation of the silenced masses.",
        "key_quotes": [
            "Hindu society is like a multi-storied tower with no staircase. One must die in the storey in which one is born.",
            "Muknayak exists to break the deafening silence imposed upon millions."
        ],
        "tags": ["muknayak", "journalism", "social_mobility", "marathi_press", "equality"]
    }
]

def collect_foundation_works() -> List[Dict[str, Any]]:
    """Export primary Dr. Ambedkar Foundation and BAWS texts to raw storage."""
    init_directories()
    logger.info(f"Structuring {len(FOUNDATION_WORKS)} foundational treatises and publications...")

    output_file = RAW_DOCS_DIR / "foundation_raw_records.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(FOUNDATION_WORKS, f, ensure_ascii=False, indent=2)

    logger.info(f"Saved Foundation/BAWS dataset to {output_file}")
    return FOUNDATION_WORKS

if __name__ == "__main__":
    records = collect_foundation_works()
    print(f"Foundation collection complete: {len(records)} primary publications recorded.")
