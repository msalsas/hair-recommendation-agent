# Hair Recommendation Agent

[![PyPI](https://img.shields.io/pypi/v/hair-recommendation-agent.svg)](https://pypi.org/project/hair-recommendation-agent/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hair-recommendation-agent.svg)](https://pypi.org/project/hair-recommendation-agent/)
[![CI](https://github.com/msalsas/hair-recommendation-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/msalsas/hair-recommendation-agent/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/msalsas/hair-recommendation-agent.svg)](https://github.com/msalsas/hair-recommendation-agent/blob/main/LICENSE)

A lightweight, rule-based agent for hairstyle and hair-color recommendations (no LLM required).

This package provides rule-based recommendations and compatibility analysis for hairstyles, based on face shape, hair type and simple style profiles. The agent accepts structured inputs (e.g. `face_shape`, `hair_type`) and can also accept free-form descriptions for style/color when appropriate.

## Key features

- Hairstyle recommendations tailored to face shape and hair type.
- Style compatibility analysis for specific haircuts.
- Trending styles by season.
- Simple, testable API designed to integrate into UIs and orchestrators.

## Installation

Developer editable install:

```bash
python -m pip install -e .[dev]
```

Install from PyPI (when published):

```bash
pip install hair-recommendation-agent
```

Install directly from the repository:

```bash
pip install git+https://github.com/msalsas/hair-recommendation-agent.git
```

## Quick start

```python
from hair_recommendation_agent import HairRecommendationAgent
from agent_core_framework import AgentTask

# Create the agent
agent = HairRecommendationAgent()

# Example: get hairstyle recommendations using structured fields
task = AgentTask(
    type="get_hairstyle_recommendations",
    payload={
        "face_shape": "oval",
        "hair_type": "wavy",
        "personal_style": "bohemian",
        "age_group": "adult",
        "gender": "female",
        "hair_length": "medium"
    }
)
response = agent.process(task)
print(response.success, response.error)
print(response.data)
```

Supported task types (examples): `get_hairstyle_recommendations`, `analyze_style_compatibility`, `get_trending_styles`.

## Testing

Run the test suite locally:

```bash
PYTHONPATH=src pytest -q
```

## Publishing to TestPyPI (manual)

1. Bump the version in `pyproject.toml` (e.g. `0.2.0`).
2. Build distributions:

```bash
python -m build
```

3. Upload to TestPyPI (create a TestPyPI API token first):

```bash
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

## CI notes

You can add GitHub Actions workflows to run tests and publish packages. Make sure the runner has any test dependencies available.

## Contributing

Contributions are welcome. Open an issue or a pull request. Add tests for new behavior and keep changes focused.

## License

MIT — see the `LICENSE` file for details.
