from .agent import HairRecommendationAgent

__all__ = ["HairRecommendationAgent"]

try:
    from importlib.metadata import version
    __version__ = version("hair-recommendation-agent")
except ImportError:
    __version__ = "0.1.0-dev"