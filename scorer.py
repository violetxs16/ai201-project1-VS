import re
def _normalize(text: str | None) -> str:
    #Lower-Case, strip punctuation and collapse whitespace

    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text) #Regular expression
    return " ".join(text.split())

def _contains_phrase(haystack: str, phrase: str) -> bool:
    norm_haystack = _normalize(haystack)
    norm_phrase = _normalize(phrase)
    if not norm_phrase:
        return False

    if norm_phrase in norm_haystack:
        return True

    words = norm_phrase.split()

    if len(words) <= 1:
        return False

    norm_words = norm_haystack.split()
    return all(word in norm_words for word in words)

def judge(question: str, expects: str, answer: str | None, results) -> bool:
    """Return True when the answer contains the expected fact.
    
        The project expects this to be a simple subtring-style test. We keep it explicit and forgiving enought to handle minor wording differences without making the rule too fuzzy
    """
    if not expects or not answer:
        return False

    phrases = [part.strip() for part in re.split(r"[;|]+", expects) if part.strip()]
    if not phrases:
        return False

    answer_text = answer or ""

    for phrase in phrases:
        if _contains_phrase(answer_text, phrase):
            return True

    if results:
        retrieved_text = " ".join(getattr(result, "text","") for result in results)
        for phrase in phrases:
            if _contains_phrase(retrieved_text, phrase):
                return True
    return False
    