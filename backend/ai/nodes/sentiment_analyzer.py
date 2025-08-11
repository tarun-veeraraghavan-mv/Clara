import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from ..agent_state import AgentState

nltk.download('vader_lexicon', quiet=True)

def sentiment_analyzer(state: AgentState) -> AgentState:
    user_input = state["user_input"]
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(user_input)

    if scores['compound'] >= 0.05:
        sentiment = "positive"
    elif scores['compound'] <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    state["sentiment"] = sentiment
    return state