dummy_data_keywords = ("dummy", "fake", "sample", "test", "placeholder", "mock", "prototype", "template", "random", "simulation",
                      "artificial", "synthetic", "fabricated", "emulated", "imitation", "pseudo", "temporary", "scratch", "trial",
                      "model", "replica", "doppelganger", "cloned", "counterfeit", "fictitious", "bogus", "forged", "fabrication",
                      "semblance", "simulated", "sham", "facsimile", "phony", "make-believe", "spurious", "false", "pseudo", "phony",
                      "unreal")

related_dummy_data_root_words = ("generate", "create", "produce", "make", "build", "construct", "design", "fabricate", "synthesize",
                      "develop", "formulate", "forge", "assemble", "originate", "spawn", "generate", "concoct", "manufacture", "craft",
                      "spawn", "initiate", "inaugurate", "engender", "bring about", "induce", "conceive", "spawn", "propagate", "set up",
                      "kick-start", "begin", "incubate", "trigger", "introduce", "launch", "establish", "initiate", "found", "ignite", "elicit", "give", "type", "paste")

dummy_data_child_keywords = (
    "data", "information", "dataset", "records", "sample",
    "database", "statistics", "metrics", "numbers", "figures",
    "entries", "details", "facts", "insights", "observations",
    "measurements", "variables", "parameters", "attributes", 
    "properties", "features", "elements", "values", "variables",
    "contents", "materials", "inputs", "outputs", "results",
    "findings", "outcomes", "conclusions", "summaries",
    "summations", "analyses", "examinations", "investigations",
    "reports", "reviews", "assessments", "evaluations"
)

# texts

# Keywords for bullet points and headings
bullet_point_keywords = (
    "bullet_points",
    "points",
    "key points",
    'text explanation',
    'explanation',
    'explain',
    "main ideas",
    "highlights",
    "core points",
    "main takeaways",
    "overview",
    "recap",
    "brief summary",
    "executive summary",
    "synopsis",
    "tl;dr",
    "abstract",
    "recapitulation"
)

# Keywords for sentences and summaries
sentence_summary_keywords = (
    "summary",
    "summarize",
    "essence",
    "condense",
    "summation",
    "outline",
    "tl;dr",
    "abstract"
    'text understanding',
    'understand text',
)

# Keywords for analysis
text_description_keywords = (
    'describe',
    'description',
    'overview',
    'text description',
    'describe text',
    'text details',
    'text overview',
    'text analysis',
    'analyze text',
    'text breakdown',
    'break down text',
)

add_title_keywords = (
    "title",
    "add title",
    "include title",
    "provide title",
    "insert title",
    "put title",
    "name",
    "add name",
    "include name",
    "provide name",
    "insert name",
    "put name",
    "name"
)

# Keywords for sentiment analysis
sentiment_analysis_keywords = (
    'sentiment analysis',
    'analyze sentiment',
    'sentiment classification',
    'sentiment scoring',
    'sentiment evaluation',
    'sentiment detection',
    'emotion analysis',
    'tone analysis',
    'opinion mining',
    'subjectivity analysis',
    'text sentiment',
    'sentiment extraction',
    'sentiment assessment',
    'sentiment interpretation',
    'sentiment understanding',
    'sentiment prediction',
)

full_info_keywords = (
    "elaborate",
    "analyze",
    "explore",
    "examine",
    "review",
    "explain",
    "understand",
    "describe",
    "scrutinize",
    "investigate",
    "breakdown",
    "assess",
    "delve",
    "probe",
    "study",
    "interpret",
    "evaluate",
    "survey",
    "inspect",
    "assimilate",
)


question_words = (
    "what", "how", "why", "when", "where", "who", "which",
    "is", "are", "do", "does", "can", "could", "should",
    "will", "would", "did", "have", "had",
    "may", "shall"
)

# date time
current_date_keywords = [
    "today", "current date", "date today", "what's the date", "what is today's date",
    "current day", "day today", "date", "day", "today's day",
    "present date", "date at present", "now date", "current calendar date",
    "this day", "date of today", "present day", "calendar date", "today's date",
    "date for today"
]

current_time_keywords = [
    "current time", "time now", "what time is it", "what's the time", "time right now",
    "time", "time of day", "now time", "present time", "current clock time",
    "time at present", "current hour", "hour now", "current minute", "minute now",
    "current second", "second now", "time of day now", "clock time now", "present clock time"
]

current_datetime_keywords = [
    "current datetime", "current timestamp", "current moment", "current moment in time", "what's the current datetime",
    "current moment in the day", "current time and date", "current date and time", "current instant",
    "present moment", "datetime now", "now datetime", "current point in time", "present instant",
    "moment now", "datetime at present", "current timestamp value", "current date and time information", "current datetime information",
    "current moment of time"
]

timezone_keywords = [
    'time in',
    'current time in',
    'what is the time in',
    'time at',
    'time of',
    'timezone time',
    'timezone now',
    'current time for',
    'what time is it in',
    'time for',
    'time at',
    'time in a specific timezone',
    'time in a certain timezone'
]


# Combine all keywords into one tuple
all_datetime_keywords = tuple(current_date_keywords + current_time_keywords + current_datetime_keywords)

time_formats = [
    "HH:MM:SS", "HH:MM", "HH:MM:SS AM/PM", "HH:MM AM/PM", "HH.MM.SS",
    "HH.MM", "HH.MM.SS AM/PM", "HH.MM AM/PM", "HHMMSS", "HHMM", "HH:MM:SS.sss",
    "HH:MM:SS.sss AM/PM", "HH:MM:SS.ssssss", "HH:MM:SS.ssssss AM/PM", "HHMMSSsss",
    "HHMMsss", "HHMMSS AM/PM", "HHMM AM/PM", "HHMMSSsss AM/PM", "HHMMsss AM/PM",
    "HH", "HH AM/PM", "HHMM", "HHMM AM/PM", "HHMMSS", "HHMMSS AM/PM", "HH:MM",
    "HH:MM AM/PM", "HH:MM:SS", "HH:MM:SS AM/PM", "HH:MM:SS.sss", "HH:MM:SS.sss AM/PM"
]

date_formats = [
    "YYYY-MM-DD", "MM/DD/YYYY", "DD-MM-YYYY", "YYYY.MM.DD", "DD/MM/YY",
    "YY-MM-DD", "DD.MM.YYYY", "MM-DD-YYYY", "DD/MM/YYYY", "YYYY/MM/DD",
    "MM/DD/YY", "DD.MM.YY", "YY/MM/DD", "DD-MMM-YYYY", "YYYY/MM/DD",
    "MMM DD, YYYY", "DD-MMM-YY", "YY/MM/DD", "YYYYMMDD", "DDMMYYYY",
    "YYMMDD", "MMDDYYYY", "YYYYDDD", "YYDDD", "YYDDD", "DDDYY", "DDDYYYY",
    "YYDDD", "DDDDYYYY", "YYYY-MM", "MM-YYYY", "YYYYMM", "MMYYYY", "YYYY",
    "MM", "DD"
]
