from enum import Enum


class CompanyType(str, Enum):
    service = "service"
    startup = "startup"
    product = "product"


class NoticePeriod(int, Enum):
    days_30 = 30
    days_60 = 60
    days_90 = 90


class ManagerType(str, Enum):
    supportive = "supportive"
    neutral = "neutral"
    toxic = "toxic"


class ProjectCriticality(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class FeedbackOutcome(str, Enum):
    success = "success"
    failed = "failed"
    partial = "partial"


class ScriptMode(str, Enum):
    safe = "safe"
    balanced = "balanced"
    aggressive = "aggressive"
