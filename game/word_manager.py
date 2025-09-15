"""
Enhanced word manager with multiple difficulty levels and specialized word sets
"""

import random
from typing import List, Dict
from enum import Enum


class WordCategory(Enum):
    """Categories of words for different training purposes"""
    COMMON = "common"
    TECHNICAL = "technical"
    BUSINESS = "business"
    ACADEMIC = "academic"
    CREATIVE = "creative"


class WordManager:
    """Enhanced word manager with comprehensive word sets"""
    
    # Symbol and number constants for advanced/expert levels
    BASIC_SYMBOLS = ".,!?@#$%&*()"
    ALL_SYMBOLS = "@#$%^&*()!~`-_=+[]{}|;:'\"<>,.?/"
    NUMBERS = "0123456789"
    
    def __init__(self):
        self._initialize_word_sets()
    
    def _get_random_symbol(self, symbol_set: str) -> str:
        """Get a random symbol from the given set"""
        return random.choice(symbol_set)
    
    def _get_random_number(self) -> str:
        """Get a random number (1-3 digits)"""
        return str(random.randint(1, 999))
    
    def _get_random_numbers(self, count: int) -> str:
        """Get a string of random numbers"""
        return ''.join(random.choices(self.NUMBERS, k=count))
    
    def _get_word_with_numbers(self) -> str:
        """Generate word + number patterns like 'house123'"""
        word = random.choice(self.intermediate_words[:100])  # Use shorter words
        number = self._get_random_numbers(random.randint(1, 3))
        return f"{word}{number}"
    
    def _get_basic_punctuation(self) -> str:
        """Generate sentences with basic punctuation"""
        patterns = [
            lambda: f"{random.choice(self.beginner_words).capitalize()}, {random.choice(self.beginner_words)}!",
            lambda: f"{random.choice(self.intermediate_words).capitalize()}? {random.choice(self.beginner_words).capitalize()}.",
            lambda: f"{random.choice(self.beginner_words).capitalize()} & {random.choice(self.beginner_words)}.",
            lambda: f"({random.choice(self.beginner_words)}) = {self._get_random_number()}",
        ]
        return random.choice(patterns)()
    
    def _get_email_like(self) -> str:
        """Generate simple email-like patterns"""
        names = ["user", "john", "test", "admin", "info", "contact", "support"]
        domains = ["domain", "site", "company", "email", "mail", "web"]
        extensions = ["com", "org", "net", "edu"]
        
        name = random.choice(names)
        domain = random.choice(domains)
        ext = random.choice(extensions)
        return f"{name}@{domain}.{ext}"
    
    def _get_simple_symbols(self) -> str:
        """Generate text with basic symbols integrated"""
        patterns = [
            lambda: f"Price: ${self._get_random_number()}",
            lambda: f"Score: {self._get_random_number()}%",
            lambda: f"Temp: {self._get_random_number()}°F",
            lambda: f"Time: {random.randint(1,12)}:{random.randint(10,59)}",
            lambda: f"#{self._get_random_number()} - {random.choice(self.beginner_words)}",
        ]
        return random.choice(patterns)()
    
    def _get_password_pattern(self) -> str:
        """Generate complex password-like patterns"""
        patterns = [
            lambda: f"MyP@ssw0rd{self._get_random_numbers(2)}!",
            lambda: f"{random.choice(self.beginner_words).capitalize()}{self._get_random_symbol(self.ALL_SYMBOLS)}{self._get_random_numbers(3)}",
            lambda: f"Str0ng{self._get_random_symbol('#$%')}{self._get_random_numbers(3)}",
            lambda: f"{random.choice(['Secure', 'Safe', 'Strong'])}{self._get_random_numbers(2)}{self._get_random_symbol('@#$%^&*!')}",
            lambda: f"C0mpl3x{self._get_random_symbol('$@!')}{random.choice(['Pass', 'Key', 'Code'])}",
        ]
        return random.choice(patterns)()
    
    def _get_code_snippet(self) -> str:
        """Generate programming code-like patterns"""
        patterns = [
            lambda: f"if({random.choice(['x', 'y', 'i'])} > {random.randint(0,10)}) {{ return true; }}",
            lambda: f"var {random.choice(['name', 'data', 'user'])} = '{random.choice(self.beginner_words)}';",
            lambda: f"function {random.choice(['test', 'check', 'run'])}() {{ console.log('Hello'); }}",
            lambda: f"const {random.choice(['API_KEY', 'URL', 'TOKEN'])} = '{self._get_random_numbers(8)}';",
            lambda: f"SELECT * FROM {random.choice(['users', 'data', 'items'])} WHERE id = {random.randint(1,100)};",
            lambda: f"<{random.choice(['div', 'span', 'p'])}>{random.choice(self.beginner_words)}</{random.choice(['div', 'span', 'p'])}>",
        ]
        return random.choice(patterns)()
    
    def _get_url_pattern(self) -> str:
        """Generate realistic URL patterns"""
        protocols = ["https://", "http://", "ftp://"]
        domains = ["www.example.com", "api.site.org", "server.net", "data.company.co"]
        paths = ["users", "data", "api", "files", "images"]
        
        protocol = random.choice(protocols)
        domain = random.choice(domains)
        path = random.choice(paths)
        id_num = random.randint(1, 999)
        
        patterns = [
            f"{protocol}{domain}/{path}",
            f"{protocol}{domain}/{path}?id={id_num}",
            f"{protocol}{domain}/{path}/{id_num}",
            f"{protocol}{domain}/{path}?sort=name&limit={random.randint(10,100)}",
        ]
        return random.choice(patterns)
    
    def _get_complex_symbols(self) -> str:
        """Generate text with all symbols and special characters"""
        patterns = [
            lambda: f"[{self._get_random_symbol('@#$%^&*')}] = {{{random.choice(['key', 'value', 'data'])}: '{random.choice(self.beginner_words)}'}}",
            lambda: f"~/{random.choice(['home', 'user', 'docs'])}/{random.choice(self.beginner_words)}.{random.choice(['txt', 'pdf', 'doc'])}",
            lambda: f"${{{random.choice(['USER', 'HOME', 'PATH'])}}} | grep '{random.choice(self.beginner_words)}'",
            lambda: f"<{random.choice(['tag', 'div', 'span'])} class='{random.choice(self.beginner_words)}'>{random.choice(self.beginner_words)}</{random.choice(['tag', 'div', 'span'])}>",
            lambda: f"#!/bin/{random.choice(['bash', 'sh'])} && echo '{random.choice(self.beginner_words)}'",
        ]
        return random.choice(patterns)()
    
    def _get_mixed_alphanumeric(self) -> str:
        """Generate random complex strings with letters, numbers, and symbols"""
        length = random.randint(8, 15)
        chars = []
        
        # Ensure at least one of each type
        chars.append(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))  # Uppercase
        chars.append(random.choice('abcdefghijklmnopqrstuvwxyz'))  # Lowercase
        chars.append(random.choice(self.NUMBERS))  # Number
        chars.append(random.choice(self.ALL_SYMBOLS))  # Symbol
        
        # Fill the rest randomly
        all_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' + self.NUMBERS + self.ALL_SYMBOLS
        for _ in range(length - 4):
            chars.append(random.choice(all_chars))
        
        random.shuffle(chars)
        return ''.join(chars)
    
    def _get_word_with_symbols(self) -> str:
        """Generate words with symbols embedded like 'word@symbol' or 'test#123'"""
        word = random.choice(self.intermediate_words[:50])  # Use shorter words
        symbol = self._get_random_symbol(self.ALL_SYMBOLS)
        
        patterns = [
            f"{word}{symbol}",  # word@
            f"{symbol}{word}",  # @word
            f"{word}{symbol}{word}",  # word@word
            f"{word}{symbol}{self._get_random_numbers(2)}",  # word@12
            f"{word.upper()}{symbol}{word.lower()}",  # WORD@word
        ]
        return random.choice(patterns)
    
    def _get_symbol_heavy_text(self) -> str:
        """Generate text that's heavy on symbols"""
        patterns = [
            f"@{random.choice(self.beginner_words)}#",
            f"${random.choice(self.beginner_words)}%",
            f"*{random.choice(self.beginner_words)}!",
            f"&{random.choice(self.beginner_words)}^",
            f"#{random.choice(self.beginner_words)}@",
            f"!{random.choice(self.beginner_words)}?",
            f"({random.choice(self.beginner_words)})",
            f"[{random.choice(self.beginner_words)}]",
            f"{{{random.choice(self.beginner_words)}}}",
            f"<{random.choice(self.beginner_words)}>",
        ]
        return random.choice(patterns)
    
    def _format_multiline_text(self, text: str, words_per_line: int = 8) -> str:
        """Format text into multiple lines with fewer words per line for better practice"""
        words = text.split()
        lines = []
        
        # Create more lines with fewer words per line
        for i in range(0, len(words), words_per_line):
            line = " ".join(words[i:i + words_per_line])
            lines.append(line)
        
        # Ensure we have at least 5 lines for good practice
        while len(lines) < 5 and len(words) > 0:
            # Add more content by repeating some words with variations
            extra_words = random.choices(words[:min(20, len(words))], k=words_per_line)
            lines.append(" ".join(extra_words))
        
        return "\n".join(lines)
    
    def _calculate_words_needed(self, difficulty, duration: int, speed_factor: float = 1.0) -> int:
        """Calculate number of words needed with speed factor - increased for more lines"""
        expected_wpm = self._get_expected_wpm(difficulty)
        # Increased multiplier from 1.5 to 2.5 for more text and more lines
        return max(40, int((duration / 60) * expected_wpm * speed_factor * 2.5))
    
    def _initialize_word_sets(self):
        """Initialize all word sets for different difficulties and categories"""
        
        # Beginner words (3-6 characters, common words)
        self.beginner_words = [
            "the", "and", "for", "are", "but", "not", "you", "all", "can", "had",
            "her", "was", "one", "our", "out", "day", "get", "has", "him", "his",
            "how", "man", "new", "now", "old", "see", "two", "way", "who", "boy",
            "did", "its", "let", "put", "say", "she", "too", "use", "cat", "dog",
            "run", "sun", "car", "big", "red", "hot", "yes", "mom", "dad", "fun",
            "book", "look", "good", "food", "door", "room", "home", "time", "name",
            "game", "same", "come", "some", "work", "word", "world", "water", "where",
            "there", "these", "those", "think", "thank", "three", "house", "mouse",
            "about", "after", "again", "before", "being", "below", "could", "every",
            "first", "found", "great", "group", "hand", "head", "help", "here",
            "know", "large", "last", "left", "life", "light", "line", "little",
            "long", "made", "make", "many", "might", "more", "most", "move",
            "much", "must", "need", "never", "next", "night", "number", "often",
            "only", "open", "order", "other", "over", "own", "part", "place",
            "point", "right", "said", "same", "seem", "show", "side", "since",
            "small", "sound", "still", "such", "take", "than", "them", "turn",
            "until", "very", "want", "water", "well", "went", "were", "what",
            "when", "which", "while", "white", "will", "with", "without", "year"
        ]
        
        # Intermediate words (5-10 characters, moderate complexity)
        self.intermediate_words = [
            "ability", "absence", "academy", "account", "achieve", "acquire", "address",
            "advance", "against", "already", "another", "anxiety", "anybody", "anymore",
            "anywhere", "approve", "arrange", "article", "attempt", "attract", "average",
            "balance", "battery", "because", "bedroom", "benefit", "between", "bicycle",
            "brother", "building", "business", "cabinet", "campaign", "capital", "captain",
            "capture", "careful", "carrier", "ceiling", "central", "century", "certain",
            "chamber", "channel", "chapter", "charity", "chicken", "children", "citizen",
            "classic", "climate", "clothes", "collect", "college", "combine", "comfort",
            "command", "comment", "company", "compare", "compete", "complex", "concept",
            "concern", "conduct", "confirm", "connect", "consider", "consist", "contact",
            "contain", "content", "contest", "context", "control", "convert", "correct",
            "council", "counter", "country", "courage", "creative", "culture", "current",
            "customer", "daughter", "decision", "deliver", "density", "develop", "diamond",
            "digital", "dinner", "direct", "discuss", "disease", "display", "distance",
            "diverse", "document", "domestic", "economy", "educate", "element", "emotion",
            "employee", "energy", "engine", "enhance", "evening", "example", "exchange",
            "exercise", "explain", "explore", "express", "extreme", "factory", "failure",
            "fashion", "feature", "finance", "foreign", "fortune", "forward", "freedom",
            "function", "gallery", "general", "generate", "genuine", "government", "grocery",
            "guarantee", "healthy", "history", "holiday", "housing", "however", "husband",
            "identity", "imagine", "improve", "include", "increase", "industry", "initial",
            "instead", "interest", "internet", "involve", "journal", "journey", "justice",
            "kitchen", "knowledge", "language", "leather", "library", "license", "machine",
            "manager", "marriage", "material", "maximum", "meaning", "measure", "medical",
            "meeting", "memory", "message", "minimum", "mission", "mistake", "mixture",
            "monitor", "morning", "natural", "network", "nothing", "nuclear", "officer",
            "opinion", "organic", "package", "partner", "passage", "patient", "pattern",
            "payment", "penalty", "perfect", "perform", "perhaps", "picture", "plastic",
            "popular", "portion", "poverty", "precise", "predict", "prepare", "present",
            "prevent", "primary", "printer", "privacy", "private", "problem", "process",
            "produce", "product", "program", "project", "promise", "protect", "provide",
            "publish", "purpose", "quality", "quarter", "question", "quickly", "reality",
            "receive", "recover", "reflect", "regular", "related", "release", "religion",
            "replace", "request", "require", "reserve", "resolve", "respect", "respond",
            "restore", "revenue", "reverse", "science", "scratch", "section", "segment",
            "serious", "service", "session", "setting", "several", "shelter", "similar",
            "society", "software", "soldier", "someone", "special", "station", "storage",
            "strange", "stretch", "student", "subject", "success", "suggest", "summary",
            "support", "surface", "surgery", "surplus", "survive", "teacher", "tonight",
            "traffic", "trouble", "uniform", "unknown", "unusual", "upgrade", "utility",
            "variety", "vehicle", "version", "village", "visible", "warning", "weather",
            "website", "welcome", "western", "whether", "window", "without", "working"
        ]
        
        # Advanced words (8-15 characters, complex vocabulary)
        self.advanced_words = [
            "absolutely", "accelerate", "accessible", "accomplish", "accordance", "accumulate",
            "achievement", "acknowledge", "additional", "administration", "advantage", "adventure",
            "advertising", "afternoon", "aggressive", "algorithm", "alternative", "ambassador",
            "anniversary", "announcement", "application", "appointment", "appreciate", "appropriate",
            "architecture", "arrangement", "association", "assumption", "atmosphere", "attachment",
            "attendance", "attention", "attractive", "automobile", "background", "basketball",
            "battlefield", "beautiful", "beginning", "beneficial", "biological", "breakthrough",
            "calculator", "candidate", "capability", "celebration", "certificate", "challenge",
            "championship", "characteristic", "chocolate", "circumstance", "civilization",
            "classification", "combination", "comfortable", "commercial", "commission",
            "commitment", "communication", "community", "comparison", "competition", "complaint",
            "complement", "complicated", "component", "composition", "comprehensive", "computer",
            "concentrate", "conclusion", "condition", "conference", "confidence", "confusion",
            "connection", "consequence", "consideration", "consistent", "construction", "container",
            "contemporary", "contribution", "controversy", "convention", "conversation",
            "cooperation", "coordination", "corporation", "correction", "corruption", "creativity",
            "criticism", "curiosity", "curriculum", "dangerous", "database", "daughter",
            "declaration", "decoration", "definition", "democracy", "demonstration", "department",
            "description", "destination", "destruction", "development", "dictionary", "difference",
            "difficulty", "dimension", "direction", "disability", "discipline", "discovery",
            "discussion", "distribution", "documentary", "domination", "earthquake", "economics",
            "education", "effectiveness", "efficiency", "electricity", "electronic", "emergency",
            "employment", "encouragement", "engineering", "enhancement", "entertainment",
            "enthusiasm", "environment", "equipment", "establishment", "evaluation", "everything",
            "examination", "excellence", "exception", "excitement", "executive", "exhibition",
            "existence", "expansion", "expectation", "experience", "experiment", "explanation",
            "exploration", "expression", "extension", "extraordinary", "facilities", "fantastic",
            "fascination", "federation", "flexibility", "foundation", "frequency", "friendship",
            "frustration", "fundamental", "generation", "government", "graduation", "grandmother",
            "grandfather", "guarantee", "guidelines", "happiness", "headquarters", "helicopter",
            "historical", "imagination", "immediately", "immigration", "implementation", "importance",
            "improvement", "independence", "individual", "industrial", "information", "ingredient",
            "initiative", "innovation", "inspiration", "installation", "institution", "instruction",
            "integration", "intelligence", "interaction", "interesting", "international",
            "interpretation", "intervention", "introduction", "investigation", "investment",
            "journalism", "knowledge", "laboratory", "landscape", "leadership", "legislation",
            "literature", "maintenance", "management", "manufacturer", "marketing", "mathematics",
            "measurement", "mechanical", "membership", "metropolitan", "microscope", "millennium",
            "modification", "motivation", "multimedia", "navigation", "negotiation", "neighborhood",
            "nevertheless", "notification", "observation", "occupation", "opportunity", "opposition",
            "optimization", "organization", "orientation", "outstanding", "participation",
            "partnership", "performance", "personality", "perspective", "philosophy", "photograph",
            "playground", "politician", "population", "possibility", "preparation", "presentation",
            "preservation", "presidential", "probability", "procedure", "processing", "production",
            "professional", "programming", "progression", "proposition", "protection", "psychology",
            "publication", "punishment", "qualification", "questionnaire", "recognition",
            "recommendation", "registration", "relationship", "reliability", "replacement",
            "representation", "reputation", "requirement", "reservation", "resolution", "restaurant",
            "restriction", "revolution", "satisfaction", "scholarship", "scientific", "secretary",
            "security", "sensitivity", "significance", "similarity", "situation", "specification",
            "statistics", "structure", "subscription", "substantial", "successful", "suggestion",
            "supervision", "supplement", "technology", "telephone", "television", "temperature",
            "territory", "theoretical", "throughout", "tournament", "tradition", "transaction",
            "transformation", "transportation", "tremendous", "understanding", "university",
            "vaccination", "variation", "vegetation", "verification", "vocabulary", "volunteer",
            "warehouse", "wonderful", "workshop"
        ]
        
        # Expert words (10+ characters, highly complex)
        self.expert_words = [
            "abbreviation", "acceleration", "accessibility", "accommodation", "accomplishment",
            "accountability", "acknowledgment", "administration", "advertisement", "affectionate",
            "agricultural", "alphabetical", "alternatively", "ambassador", "amplification",
            "anniversary", "announcement", "anthropology", "anticipation", "apologetically",
            "appreciation", "approximately", "archaeological", "architecture", "arrangement",
            "articulation", "assassination", "association", "astronomical", "atmosphere",
            "authentication", "automatically", "availability", "bibliography", "biodiversity",
            "biotechnology", "breakthrough", "bureaucracy", "calculation", "calibration",
            "cancellation", "capabilities", "capitalization", "cardiovascular", "catastrophe",
            "categorization", "celebration", "centralization", "certification", "championship",
            "characteristic", "characterization", "choreography", "chronological", "circulation",
            "circumstance", "civilization", "classification", "collaboration", "combination",
            "commemoration", "commencement", "commentary", "commercial", "commission",
            "commitment", "communication", "community", "compensation", "competition",
            "compilation", "complementary", "complicated", "composition", "comprehensive",
            "concentration", "conceptualization", "conclusion", "condensation", "conditional",
            "configuration", "confirmation", "confrontation", "congratulation", "conjunction",
            "connection", "consciousness", "consequence", "conservation", "consideration",
            "consolidation", "constitution", "construction", "consultation", "consumption",
            "contemporary", "continuation", "contribution", "controversial", "conversation",
            "cooperation", "coordination", "corporation", "correspondence", "corruption",
            "crystallization", "curiosity", "curriculum", "customization", "cybersecurity",
            "decentralization", "declaration", "decomposition", "decoration", "dedication",
            "deforestation", "deliberation", "demonstration", "denomination", "department",
            "dependency", "description", "desertification", "designation", "destination",
            "destruction", "determination", "development", "differentiation", "digitization",
            "dimension", "diplomacy", "direction", "disability", "disappointment",
            "discipline", "discrimination", "discussion", "disintegration", "distribution",
            "diversification", "documentation", "domestication", "domination", "dramatization",
            "earthquake", "economics", "education", "effectiveness", "efficiency",
            "elaboration", "electricity", "electronic", "elimination", "embarrassment",
            "emergency", "employment", "encouragement", "encyclopedia", "engineering",
            "enhancement", "enlightenment", "entertainment", "enthusiasm", "environment",
            "establishment", "evaluation", "evaporation", "examination", "excellence",
            "exception", "excitement", "execution", "exhibition", "existence",
            "expansion", "expectation", "expedition", "experience", "experiment",
            "explanation", "exploration", "expression", "extension", "extraordinary",
            "facilitation", "fascination", "federation", "fertilization", "flexibility",
            "formalization", "foundation", "fragmentation", "frequency", "friendship",
            "frustration", "functionality", "fundamental", "generalization", "generation",
            "globalization", "government", "graduation", "grandmother", "grandfather",
            "gratification", "guarantee", "hallucination", "headquarters", "helicopter",
            "hibernation", "historical", "hospitalization", "humanitarian", "identification",
            "illustration", "imagination", "immediately", "immigration", "immunization",
            "implementation", "implication", "importance", "improvement", "inauguration",
            "independence", "individual", "industrialization", "information", "infrastructure",
            "initialization", "innovation", "inspiration", "installation", "institution",
            "instruction", "integration", "intelligence", "interaction", "interesting",
            "international", "interpretation", "intervention", "introduction", "investigation",
            "investment", "journalism", "jurisdiction", "kindergarten", "knowledge",
            "laboratory", "landscape", "leadership", "legislation", "liberalization",
            "literature", "localization", "magnetization", "maintenance", "management",
            "manifestation", "manipulation", "manufacturer", "marginalization", "marketing",
            "mathematics", "maximization", "measurement", "mechanical", "mechanization",
            "membership", "memorization", "metropolitan", "microscope", "millennium",
            "minimization", "mobilization", "modification", "modernization", "monetization",
            "monopolization", "motivation", "multiplication", "municipality", "musicalization",
            "nationalization", "naturalization", "navigation", "negotiation", "neighborhood",
            "neutralization", "nevertheless", "normalization", "notification", "observation",
            "occupation", "optimization", "organization", "orientation", "outstanding",
            "participation", "partnership", "performance", "personality", "personalization",
            "perspective", "philosophy", "photograph", "playground", "polarization",
            "politician", "popularization", "population", "possibility", "precipitation",
            "preparation", "presentation", "preservation", "presidential", "prioritization",
            "privatization", "probability", "procedure", "processing", "production",
            "professional", "programming", "progression", "pronunciation", "proposition",
            "protection", "psychology", "publication", "punishment", "purification",
            "qualification", "quantification", "questionnaire", "randomization", "rationalization",
            "realization", "recognition", "recommendation", "reconciliation", "reconstruction",
            "registration", "regularization", "rehabilitation", "relationship", "reliability",
            "reorganization", "replacement", "representation", "reputation", "requirement",
            "reservation", "resolution", "responsibility", "restaurant", "restriction",
            "restructuring", "resurrection", "revolution", "satisfaction", "scholarship",
            "scientific", "secretary", "security", "sensitivity", "significance",
            "similarity", "simplification", "situation", "socialization", "specification",
            "spiritualization", "standardization", "statistics", "sterilization", "structure",
            "subscription", "substantial", "successful", "suggestion", "supervision",
            "supplement", "synchronization", "systematization", "technology", "telephone",
            "television", "temperature", "territory", "theoretical", "throughout",
            "tournament", "tradition", "transaction", "transformation", "transportation",
            "tremendous", "understanding", "university", "urbanization", "vaccination",
            "validation", "variation", "vegetation", "verification", "visualization",
            "vocabulary", "volunteer", "warehouse", "westernization", "wonderful",
            "workshop"
        ]
        
        # Technical/Programming words
        self.technical_words = [
            "algorithm", "application", "architecture", "array", "authentication", "automation",
            "bandwidth", "binary", "blockchain", "boolean", "browser", "buffer", "bytecode",
            "cache", "callback", "certificate", "cipher", "client", "cloud", "code",
            "compiler", "component", "compression", "computer", "configuration", "connection",
            "constructor", "container", "cookie", "cryptography", "database", "debugging",
            "declaration", "deployment", "development", "directory", "documentation", "domain",
            "download", "encryption", "endpoint", "exception", "execution", "expression",
            "extension", "framework", "function", "gateway", "generator", "hardware",
            "header", "hosting", "identifier", "implementation", "inheritance", "initialization",
            "instance", "integration", "interface", "internet", "iteration", "javascript",
            "kernel", "keyword", "library", "license", "localhost", "machine", "memory",
            "metadata", "method", "middleware", "module", "network", "object", "operating",
            "optimization", "parameter", "password", "platform", "pointer", "polymorphism",
            "procedure", "programming", "protocol", "query", "recursion", "refactoring",
            "repository", "request", "response", "runtime", "schema", "script", "security",
            "server", "session", "software", "source", "specification", "statement",
            "structure", "syntax", "system", "template", "testing", "thread", "token",
            "transaction", "transfer", "transformation", "transmission", "unicode", "upload",
            "validation", "variable", "version", "virtual", "website", "workflow"
        ]
        
        # Business/Professional words
        self.business_words = [
            "account", "acquisition", "administration", "advertising", "agreement", "analysis",
            "annual", "application", "appointment", "approval", "assessment", "asset",
            "audit", "authority", "balance", "benchmark", "benefit", "budget", "business",
            "campaign", "capital", "career", "certificate", "chairman", "client", "commission",
            "committee", "communication", "company", "competition", "compliance", "conference",
            "consultant", "consumer", "contract", "corporate", "credit", "customer",
            "decision", "delivery", "department", "development", "director", "distribution",
            "division", "document", "economy", "employee", "enterprise", "equity",
            "estimate", "evaluation", "executive", "expense", "experience", "export",
            "facility", "finance", "forecast", "franchise", "government", "growth",
            "headquarters", "human", "import", "income", "industry", "information",
            "innovation", "insurance", "international", "investment", "invoice", "leadership",
            "liability", "license", "management", "manufacturing", "marketing", "meeting",
            "merger", "negotiation", "network", "operation", "opportunity", "organization",
            "partnership", "payment", "performance", "personnel", "planning", "policy",
            "portfolio", "presentation", "procedure", "product", "profit", "project",
            "proposal", "purchase", "quality", "quarter", "recruitment", "regulation",
            "relationship", "report", "research", "resource", "responsibility", "revenue",
            "salary", "sales", "security", "service", "shareholder", "solution", "strategy",
            "supplier", "support", "system", "target", "technology", "training", "transaction",
            "transportation", "treasury", "vendor", "warehouse", "workflow"
        ]
    
    def get_practice_text(self, difficulty, duration: int) -> str:
        """Generate practice text based on difficulty and duration"""
        if difficulty.value == "beginner":
            words = self.beginner_words
            selected_words = random.choices(words, k=self._calculate_words_needed(difficulty, duration))
            return self._format_multiline_text(" ".join(selected_words))
        elif difficulty.value == "intermediate":
            words = self.intermediate_words
            selected_words = random.choices(words, k=self._calculate_words_needed(difficulty, duration))
            return self._format_multiline_text(" ".join(selected_words))
        elif difficulty.value == "advanced":
            return self._format_multiline_text(self._generate_advanced_text(duration))
        else:  # expert
            return self._format_multiline_text(self._generate_expert_text(duration))
    
    def _calculate_words_needed(self, difficulty, duration: int) -> int:
        """Calculate number of words needed based on difficulty and duration"""
        expected_wpm = self._get_expected_wpm(difficulty)
        return max(20, int((duration / 60) * expected_wpm * 1.5))
    
    def _generate_advanced_text(self, duration: int) -> str:
        """Generate advanced level text with numbers and basic symbols"""
        patterns = [
            (lambda: random.choice(self.advanced_words), 0.4),  # Regular words
            (self._get_word_with_numbers, 0.2),  # Words with numbers
            (self._get_basic_punctuation, 0.2),  # Punctuation patterns
            (self._get_email_like, 0.1),  # Email patterns
            (self._get_simple_symbols, 0.1),  # Simple symbols
        ]
        return self._mix_patterns(patterns, duration, 0.8)  # 80% of normal speed
    
    def _generate_expert_text(self, duration: int) -> str:
        """Generate expert level text with all symbols and complex patterns"""
        patterns = [
            (lambda: random.choice(self.expert_words), 0.15),  # Regular expert words (reduced)
            (self._get_word_with_symbols, 0.25),  # Words with symbols embedded
            (self._get_symbol_heavy_text, 0.2),  # Symbol-heavy patterns
            (self._get_password_pattern, 0.15),  # Password patterns
            (self._get_code_snippet, 0.1),  # Code snippets
            (self._get_complex_symbols, 0.1),  # Complex symbols
            (self._get_mixed_alphanumeric, 0.05),  # Mixed alphanumeric
        ]
        return self._mix_patterns(patterns, duration, 0.6)  # 60% of normal speed
    
    def _mix_patterns(self, patterns: list, duration: int, speed_factor: float = 1.0) -> str:
        """Mix different patterns based on their weights - increased for more lines"""
        from game.speed_engine import DifficultyLevel
        
        # Calculate total items needed - increased for more content and lines
        base_wpm = 60  # Increased base WPM for more content
        items_needed = max(40, int((duration / 60) * base_wpm * speed_factor * 1.5))  # Added 1.5 multiplier
        
        result_items = []
        for _ in range(items_needed):
            # Choose pattern based on weights
            rand = random.random()
            cumulative = 0
            for pattern_func, weight in patterns:
                cumulative += weight
                if rand <= cumulative:
                    try:
                        result_items.append(pattern_func())
                    except:
                        # Fallback to simple word if pattern fails
                        result_items.append(random.choice(self.intermediate_words))
                    break
        
        return " ".join(result_items)
    
    def get_challenge_text(self, difficulty, duration: int) -> str:
        """Generate challenging text with mixed word types"""
        if difficulty.value == "beginner":
            primary_words = self.beginner_words
            secondary_words = self.intermediate_words[:50]
            # Standard word mixing for beginner/intermediate
            expected_wpm = self._get_expected_wpm(difficulty)
            words_needed = max(25, int((duration / 60) * expected_wpm * 1.3))
            
            primary_count = int(words_needed * 0.7)
            secondary_count = words_needed - primary_count
            
            selected_words = (random.choices(primary_words, k=primary_count) + 
                             random.choices(secondary_words, k=secondary_count))
            random.shuffle(selected_words)
            return self._format_multiline_text(" ".join(selected_words))
            
        elif difficulty.value == "intermediate":
            primary_words = self.intermediate_words
            secondary_words = self.advanced_words[:50]
            # Standard word mixing for intermediate
            expected_wpm = self._get_expected_wpm(difficulty)
            words_needed = max(25, int((duration / 60) * expected_wpm * 1.3))
            
            primary_count = int(words_needed * 0.7)
            secondary_count = words_needed - primary_count
            
            selected_words = (random.choices(primary_words, k=primary_count) + 
                             random.choices(secondary_words, k=secondary_count))
            random.shuffle(selected_words)
            return self._format_multiline_text(" ".join(selected_words))
            
        elif difficulty.value == "advanced":
            # Advanced challenge with more complex patterns
            patterns = [
                (lambda: random.choice(self.advanced_words), 0.3),  # Regular advanced words
                (lambda: random.choice(self.expert_words), 0.2),  # Some expert words
                (self._get_word_with_numbers, 0.25),  # More numbers
                (self._get_basic_punctuation, 0.15),  # More punctuation
                (self._get_simple_symbols, 0.1),  # More symbols
            ]
            return self._format_multiline_text(self._mix_patterns(patterns, duration, 0.7))  # 70% speed
            
        else:  # expert
            # Expert challenge with maximum complexity
            patterns = [
                (lambda: random.choice(self.expert_words), 0.1),  # Expert words (reduced)
                (self._get_word_with_symbols, 0.3),  # More words with symbols
                (self._get_symbol_heavy_text, 0.25),  # More symbol-heavy text
                (self._get_password_pattern, 0.15),  # Password patterns
                (self._get_complex_symbols, 0.15),  # More complex symbols
                (self._get_mixed_alphanumeric, 0.05),  # Random complexity
            ]
            return self._format_multiline_text(self._mix_patterns(patterns, duration, 0.5))  # 50% speed - very challenging
    
    def get_accuracy_text(self, difficulty, duration: int) -> str:
        """Generate text focused on accuracy with tricky words"""
        # Use words with common typing mistakes
        tricky_words = [
            "receive", "achieve", "believe", "ceiling", "weird", "their", "there", "they're",
            "your", "you're", "its", "it's", "than", "then", "affect", "effect",
            "accept", "except", "advice", "advise", "breath", "breathe", "loose", "lose",
            "quiet", "quite", "desert", "dessert", "principal", "principle", "stationary",
            "stationery", "complement", "compliment", "council", "counsel", "discrete",
            "discreet", "elicit", "illicit", "emigrate", "immigrate", "ensure", "insure",
            "farther", "further", "imply", "infer", "lay", "lie", "peak", "peek",
            "personal", "personnel", "precede", "proceed", "weather", "whether"
        ]
        
        if difficulty.value == "beginner":
            base_words = self.beginner_words + tricky_words[:20]
            selected_words = random.choices(base_words, k=self._calculate_words_needed(difficulty, duration, 0.8))
            return self._format_multiline_text(" ".join(selected_words))
            
        elif difficulty.value == "intermediate":
            base_words = self.intermediate_words + tricky_words[:30]
            selected_words = random.choices(base_words, k=self._calculate_words_needed(difficulty, duration, 0.8))
            return self._format_multiline_text(" ".join(selected_words))
            
        elif difficulty.value == "advanced":
            # Advanced accuracy with symbols
            patterns = [
                (lambda: random.choice(self.advanced_words + tricky_words[:40]), 0.5),
                (self._get_word_with_numbers, 0.2),
                (self._get_basic_punctuation, 0.2),
                (self._get_simple_symbols, 0.1),
            ]
            text = self._mix_patterns(patterns, duration, 0.6)  # Slower for accuracy
            return self._format_multiline_text(text)
            
        else:  # expert
            # Expert accuracy with all symbols
            patterns = [
                (lambda: random.choice(self.expert_words + tricky_words), 0.3),
                (self._get_word_with_symbols, 0.3),
                (self._get_symbol_heavy_text, 0.2),
                (self._get_password_pattern, 0.1),
                (self._get_complex_symbols, 0.1),
            ]
            text = self._mix_patterns(patterns, duration, 0.5)  # Very slow for accuracy
            return self._format_multiline_text(text)
    
    def get_speed_text(self, difficulty, duration: int) -> str:
        """Generate text optimized for speed with shorter, common words"""
        if difficulty.value == "beginner":
            speed_words = [w for w in self.beginner_words if len(w) <= 5]
            selected_words = random.choices(speed_words, k=max(30, int((duration / 60) * self._get_expected_wpm(difficulty) * 1.2 * 1.8)))
            return self._format_multiline_text(" ".join(selected_words))
            
        elif difficulty.value == "intermediate":
            speed_words = [w for w in self.intermediate_words if len(w) <= 7]
            selected_words = random.choices(speed_words, k=max(30, int((duration / 60) * self._get_expected_wpm(difficulty) * 1.2 * 1.8)))
            return self._format_multiline_text(" ".join(selected_words))
            
        elif difficulty.value == "advanced":
            # Advanced speed with some symbols
            patterns = [
                (lambda: random.choice([w for w in self.advanced_words if len(w) <= 9]), 0.7),
                (self._get_word_with_numbers, 0.2),
                (self._get_simple_symbols, 0.1),
            ]
            text = self._mix_patterns(patterns, duration, 1.2)  # Faster for speed
            return self._format_multiline_text(text)
            
        else:  # expert
            # Expert speed with symbols
            patterns = [
                (lambda: random.choice([w for w in self.expert_words if len(w) <= 12]), 0.6),
                (self._get_word_with_symbols, 0.3),
                (self._get_symbol_heavy_text, 0.1),
            ]
            text = self._mix_patterns(patterns, duration, 1.0)  # Fast but with symbols
            return self._format_multiline_text(text)
    
    def get_endurance_text(self, difficulty, duration: int) -> str:
        """Generate longer text for endurance training"""
        if difficulty.value == "beginner":
            words = self.beginner_words
            selected_words = random.choices(words, k=max(50, int((duration / 60) * self._get_expected_wpm(difficulty) * 2.0)))
            return self._format_multiline_text(" ".join(selected_words))
            
        elif difficulty.value == "intermediate":
            words = self.intermediate_words
            selected_words = random.choices(words, k=max(50, int((duration / 60) * self._get_expected_wpm(difficulty) * 2.0)))
            return self._format_multiline_text(" ".join(selected_words))
            
        elif difficulty.value == "advanced":
            # Advanced endurance with symbols
            patterns = [
                (lambda: random.choice(self.advanced_words), 0.5),
                (self._get_word_with_numbers, 0.2),
                (self._get_basic_punctuation, 0.2),
                (self._get_simple_symbols, 0.1),
            ]
            text = self._mix_patterns(patterns, duration, 2.0)  # More text for endurance
            return self._format_multiline_text(text)
            
        else:  # expert
            # Expert endurance with all symbols
            patterns = [
                (lambda: random.choice(self.expert_words), 0.4),
                (self._get_word_with_symbols, 0.3),
                (self._get_symbol_heavy_text, 0.2),
                (self._get_complex_symbols, 0.1),
            ]
            text = self._mix_patterns(patterns, duration, 1.8)  # Lots of text with symbols
            return self._format_multiline_text(text)
    
    def get_specialized_text(self, category: WordCategory, difficulty, duration: int) -> str:
        """Generate specialized text based on category"""
        if category == WordCategory.TECHNICAL:
            base_words = self.technical_words
        elif category == WordCategory.BUSINESS:
            base_words = self.business_words
        else:
            # Default to regular practice text
            return self.get_practice_text(difficulty, duration)
        
        # Mix with regular words based on difficulty
        if difficulty.value == "beginner":
            regular_words = self.beginner_words
        elif difficulty.value == "intermediate":
            regular_words = self.intermediate_words
        elif difficulty.value == "advanced":
            regular_words = self.advanced_words
        else:  # expert
            regular_words = self.expert_words
        
        expected_wpm = self._get_expected_wpm(difficulty)
        words_needed = max(20, int((duration / 60) * expected_wpm * 1.4))
        
        # 60% specialized, 40% regular words
        specialized_count = int(words_needed * 0.6)
        regular_count = words_needed - specialized_count
        
        selected_words = (random.choices(base_words, k=specialized_count) + 
                         random.choices(regular_words, k=regular_count))
        random.shuffle(selected_words)
        
        return " ".join(selected_words)
    
    def _get_expected_wpm(self, difficulty) -> int:
        """Get expected WPM based on difficulty level"""
        wpm_map = {
            "beginner": 25,
            "intermediate": 40,
            "advanced": 60,
            "expert": 80
        }
        return wpm_map.get(difficulty.value, 40)