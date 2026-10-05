"""
Student NotebookLM Evidence Prompts Generator
Provides structured Backstory -> Frontstory narrative prompts with precise primary source citations
for Google NotebookLM, study guides, and audio podcast creation.
"""

from typing import List, Dict, Any

STUDENT_NOTEBOOK_PROMPTS: List[Dict[str, Any]] = [
    {
        "topic_id": "TOPIC_MAHAD_TO_ART17",
        "title": "From Mahad Satyagraha (1927) to Article 17 (1948)",
        "theme": "Abolition of Untouchability & Fundamental Human Rights",
        "language": "en",
        "language_display": "English",
        "backstory": {
            "year": "1927",
            "date": "1927-03-20",
            "title": "Chavdar Tale Water Struggle (Mahad)",
            "details": "Dr. Ambedkar led 10,000 delegates to assert equal human rights to draw drinking water from the public Chavdar tank in Mahad. Declared that civic access is a fundamental human right that cannot be begged from orthodox authority.",
            "citations": [
                "BAWS Vol. 5, pp. 234–250 (Speech at Mahad Satyagraha)",
                "Bahishkrit Bharat Editorial (April 1927)"
            ]
        },
        "frontstory": {
            "year": "1948",
            "date": "1948-11-29",
            "title": "Unanimous Adoption of Article 17 in Constituent Assembly",
            "details": "Dr. Ambedkar presented Draft Article 11 (Article 17) declaring untouchability abolished in all forms and its practice punishable by law. Adopted unanimously amidst historic applause in the Assembly.",
            "citations": [
                "Constituent Assembly Debates (CAD), Vol. VII, pp. 658–666 (29 Nov 1948)",
                "Drafting Committee Records (1947–1948)"
            ]
        },
        "notebooklm_prompt": """[NotebookLM Deep Dive Prompt: From Mahad Satyagraha to Article 17 | Language: English]

PRIMARY LANGUAGE DIRECTIVE:
Output Language: English. Please generate all analyses, study guides, timelines, citations, and the Audio Overview (Deep Dive podcast hosts dialogue) strictly and entirely in fluent English.

Act as an expert historical researcher and constitutional scholar studying Dr. B.R. Ambedkar's digital archive. Synthesize a complete chronological narrative in English from Backstory to Frontstory:

1. BACKSTORY (1927 Civil Rights Assertion):
   - Analyze Dr. Ambedkar's speech at the Mahad Satyagraha (20th March 1927) asserting public water rights [Source: BAWS Vol. 5, p. 234].
   - Explain why water access was framed not as a religious plea, but as an indispensable universal human right.

2. TRANSITION (1930s-1940s Constitutional Strategy):
   - Trace the shift from non-violent direct action to constitutional drafting during the Round Table Conferences and Poona Pact (1932).

3. FRONTSTORY (1948 Constitutional Enactment):
   - Detail how Draft Article 11 was introduced by Chairman Ambedkar and unanimously adopted as Article 17 on 29th November 1948 [Source: CAD Vol. VII, p. 658].
   - Explain how Article 17 transformed a 2,000-year social handicap into an enforceable penal prohibition.

Goal for NotebookLM: Produce an engaging Audio Overview podcast and structured study notes in English, connecting primary archival quotes to modern constitutional guarantees of human dignity."""
    },
    {
        "topic_id": "TOPIC_RUPEE_TO_RBI",
        "title": "From 'The Problem of the Rupee' (1923) to the Central Bank (RBI)",
        "theme": "Monetary Economics & Financial Sovereignty",
        "language": "en",
        "language_display": "English",
        "backstory": {
            "year": "1923",
            "date": "1923-12-01",
            "title": "D.Sc. Dissertation at London School of Economics",
            "details": "Submits seminal thesis 'The Problem of the Rupee: Its Origin and Its Solution', critiquing the exchange-standard policy of British colonial authorities and proposing gold-standard stabilization to protect wage-earners.",
            "citations": [
                "BAWS Vol. 6 (The Problem of the Rupee & Evolution of Provincial Finance)",
                "LSE D.Sc. Dissertation Archives (1923)"
            ]
        },
        "frontstory": {
            "year": "1934",
            "date": "1934-03-06",
            "title": "Hilton Young Commission & Reserve Bank of India Act",
            "details": "The Royal Commission on Indian Currency and Finance (Hilton Young Commission) used Ambedkar's book as its core working blueprint to formulate the Reserve Bank of India Act, 1934.",
            "citations": [
                "Hilton Young Commission Testimony & Evidence (1926)",
                "Reserve Bank of India Act, 1934 (Preamble & Structure)"
            ]
        },
        "notebooklm_prompt": """[NotebookLM Deep Dive Prompt: From 'Problem of the Rupee' to RBI Founding | Language: English]

PRIMARY LANGUAGE DIRECTIVE:
Output Language: English. Please generate all analyses, study guides, timelines, citations, and the Audio Overview (Deep Dive podcast hosts dialogue) strictly and entirely in fluent English.

Act as a monetary economist and archival biographer analyzing Dr. B.R. Ambedkar's economic contributions:

1. BACKSTORY (1923 LSE Economic Treatise):
   - Examine Dr. Ambedkar's D.Sc. dissertation 'The Problem of the Rupee' (1923) [Source: BAWS Vol. 6].
   - Detail his critique of John Maynard Keynes' currency theories regarding the gold-exchange standard vs gold standard.

2. TRANSITION (1926 Royal Commission Evidence):
   - Analyze Dr. Ambedkar's oral and written testimony before the Hilton Young Commission on Indian currency stabilization.

3. FRONTSTORY (1934 Reserve Bank of India Establishment):
   - Trace how Ambedkar's recommendations directly influenced the legislative framework of the RBI Act, 1934.
   - Explain his principles regarding inflation control, agricultural credit, and currency sovereignty.

Goal for NotebookLM: Generate a high-yield podcast script and summary table in English contrasting colonial currency policies with Ambedkar's stabilization model."""
    },
    {
        "topic_id": "TOPIC_GRAMMAR_OF_ANARCHY",
        "title": "From Bombay Legislature Speeches (1927) to 'Grammar of Anarchy' (1949)",
        "theme": "Democratic Philosophy & Constitutional Morality",
        "language": "en",
        "language_display": "English",
        "backstory": {
            "year": "1927–1939",
            "date": "1927-07-27",
            "title": "Bombay Legislative Council & Democratic Debates",
            "details": "Dr. Ambedkar serves in the Bombay Legislative Council, defending working-class rights, education access, and parliamentary procedure against executive overreach.",
            "citations": [
                "BAWS Vol. 2 (In the Bombay Legislature 1927–1939)",
                "Bombay Legislative Debates Records"
            ]
        },
        "frontstory": {
            "year": "1949",
            "date": "1949-11-25",
            "title": "Final Address to the Constituent Assembly ('Grammar of Anarchy')",
            "details": "Delivers historic speech warning against Bhakti (hero worship) in politics, abandoning extra-constitutional methods (Grammar of Anarchy), and ensuring social democracy undergirds political democracy.",
            "citations": [
                "CAD Vol. XI, pp. 972–981 (25th November 1949)",
                "Grammar of Anarchy Official Transcript"
            ]
        },
        "notebooklm_prompt": """[NotebookLM Deep Dive Prompt: From Bombay Legislature to the Grammar of Anarchy | Language: English]

PRIMARY LANGUAGE DIRECTIVE:
Output Language: English. Please generate all analyses, study guides, timelines, citations, and the Audio Overview (Deep Dive podcast hosts dialogue) strictly and entirely in fluent English.

Act as a political philosopher and historian examining Dr. B.R. Ambedkar's democratic thought:

1. BACKSTORY (1927–1939 Legislative Battles):
   - Explore Ambedkar's early speeches in the Bombay Legislative Council fighting for budget allocation and civic rights [Source: BAWS Vol. 2].

2. FRONTSTORY (25th November 1949 Final Address):
   - Deconstruct the famous 'Grammar of Anarchy' warning delivered in CAD Vol. XI [p. 972].
   - Analyze the three warnings Ambedkar gave:
     a) Abandoning civil disobedience and bloody revolution in a constitutional republic.
     b) Beware of Bhakti (hero worship) in politics as a sure path to dictatorship.
     c) Political democracy must become a social democracy (liberty, equality, fraternity as a trinity).

Goal for NotebookLM: Create an educational study module on Constitutional Morality in English for civic education."""
    },
    {
        "topic_id": "TOPIC_HINDU_CODE_BILL",
        "title": "From Labour Minister Welfare Codes (1942) to Hindu Code Bill (1951)",
        "theme": "Gender Equality, Legal Reform & Women's Emancipation",
        "language": "en",
        "language_display": "English",
        "backstory": {
            "year": "1942–1946",
            "date": "1942-07-20",
            "title": "Viceroy's Executive Council & Labour Reforms",
            "details": "As Labour Member, Ambedkar introduced the Mines Maternity Benefit Bill, equal pay for equal work, reduced working hours to 8 hours, and social security for women industrial workers.",
            "citations": [
                "BAWS Vol. 10 (Dr. Ambedkar as Member of Viceroy's Executive Council)",
                "Mines Maternity Benefit Records (1942)"
            ]
        },
        "frontstory": {
            "year": "1951",
            "date": "1951-09-27",
            "title": "Resignation over the Hindu Code Bill",
            "details": "Resigns as Law Minister when Parliament stalls the Hindu Code Bill, which sought to grant women equal inheritance, property rights, monogamy laws, and divorce rights.",
            "citations": [
                "BAWS Vol. 14 (Dr. Ambedkar and the Hindu Code Bill)",
                "Resignation Statement in Parliament (27th Sept 1951)"
            ]
        },
        "notebooklm_prompt": """[NotebookLM Deep Dive Prompt: From Labour Welfare to the Hindu Code Bill | Language: English]

PRIMARY LANGUAGE DIRECTIVE:
Output Language: English. Please generate all analyses, study guides, timelines, citations, and the Audio Overview (Deep Dive podcast hosts dialogue) strictly and entirely in fluent English.

Act as a legal historian examining Dr. B.R. Ambedkar's pioneer work in gender justice and civil law:

1. BACKSTORY (1942–1946 Labour Reforms for Women):
   - Analyze Dr. Ambedkar's legislative initiatives as Labour Member, including Maternity Benefits and equal pay [Source: BAWS Vol. 10].

2. FRONTSTORY (1947–1951 Hindu Code Bill Battle & Resignation):
   - Trace the drafting and debate over the Hindu Code Bill [Source: BAWS Vol. 14].
   - Highlight Ambedkar's resignation speech on 27th September 1951 over the stymied legislation.
   - Explain how these principles were later enacted into the Hindu Marriage Act (1955) and Succession Act (1956).

Goal for NotebookLM: Synthesize a comprehensive study guide on gender equality in Indian constitutional history in English."""
    },
    {
        "topic_id": "TOPIC_FRANCHISE_AND_REPRESENTATION",
        "title": "From Poona Pact (1932) to Universal Adult Franchise (Articles 326 & 330)",
        "theme": "Political Representation & Electoral Democracy",
        "language": "en",
        "language_display": "English",
        "backstory": {
            "year": "1932",
            "date": "1932-09-24",
            "title": "Poona Pact Agreement",
            "details": "Following Gandhi's fast in Yerwada Jail, Ambedkar signs the Poona Pact, securing 148 reserved legislative seats for the Depressed Classes across provincial assemblies.",
            "citations": [
                "BAWS Vol. 9 (Poona Pact Records & Round Table Conferences)",
                "Poona Pact Text (24 Sept 1932)"
            ]
        },
        "frontstory": {
            "year": "1949",
            "date": "1949-01-08",
            "title": "Universal Adult Franchise (Article 326) & Reserved Seats (Article 330)",
            "details": "As Chairman of Drafting Committee, ensures one person, one vote under Article 326 regardless of property, education, or gender, alongside reserved political seats under Articles 330 and 332.",
            "citations": [
                "CAD Vol. VIII, pp. 490–510 (Voting Rights Debates)",
                "Constitution of India, Articles 326, 330, 332"
            ]
        },
        "notebooklm_prompt": """[NotebookLM Deep Dive Prompt: From Poona Pact to Universal Adult Franchise | Language: English]

PRIMARY LANGUAGE DIRECTIVE:
Output Language: English. Please generate all analyses, study guides, timelines, citations, and the Audio Overview (Deep Dive podcast hosts dialogue) strictly and entirely in fluent English.

Act as a political scientist analyzing the evolution of electoral democracy in India:

1. BACKSTORY (1932 Poona Pact Crisis):
   - Analyze the terms of the Poona Pact signed on 24th September 1932 [Source: BAWS Vol. 9].
   - Contrast separate electorates with joint electorates with reserved seats.

2. FRONTSTORY (1949 Universal Adult Franchise Enactment):
   - Examine how Dr. Ambedkar championed Universal Adult Franchise (Article 326) in the Constituent Assembly [Source: CAD Vol. VIII].
   - Detail how Articles 330 and 332 guaranteed political representation for Scheduled Castes and Tribes.

Goal for NotebookLM: Produce an episode script for a civic education podcast on voting rights in India in English."""
    }
]

def get_student_notebook_prompts(language: str = "en") -> List[Dict[str, Any]]:
    return STUDENT_NOTEBOOK_PROMPTS
