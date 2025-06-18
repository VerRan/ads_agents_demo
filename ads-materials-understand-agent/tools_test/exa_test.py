# pip install exa-py
from exa_py import Exa
exa = Exa(api_key = "api-key")
result = exa.search_and_contents(
    "find blog posts about AGI",
    text = { "max_characters": 1000 }
)
print(result)