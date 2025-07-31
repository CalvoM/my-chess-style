import json
import logging
import re
from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

from style_predictor.constants import PROMPT_TEMPLATE

LOG = logging.getLogger(__name__)

deepseek_response_obj = re.compile(
    r"<think>(?P<ai_thought>.*)\</think>.*"
    r"ROAST:\n*(?P<ai_roast>.*)ENCOURAGEMENT\n*"
    r":(?P<ai_encouragement>.*)TIP\n*"
    r":(?P<ai_tip>.*)",
    re.DOTALL,
)


def filter_deepseek_response(response: str) -> dict[str, str]:
    if match := deepseek_response_obj.match(response):
        roast: str = match.groupdict().get("ai_roast", "")
        encouragement: str = match.groupdict().get("ai_encouragement", "")
        tip: str = match.groupdict().get("ai_tip", "")
        res: dict[str, str] = {
            "roast": roast.strip(),
            "encouragement": encouragement.strip(),
            "tip": tip.strip(),
        }
        return res
    else:
        # Handle parsing of other LLMs' responses.
        LOG.warning("LLM Response parsing failed.")
    return {
        "roast": "Sorry, couldn't generate a roast right now.",
        "encouragement": "",
        "tip": "",
    }


def generate_roast(data: dict[str, Any]) -> dict[str, str]:
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    model = OllamaLLM(model="deepseek-r1:7b")
    chain = prompt | model
    try:
        res = chain.invoke({"stats": json.dumps(data)})
        return filter_deepseek_response(res)
    except Exception as e:
        LOG.error(str(e), exc_info=True)
        return {
            "roast": "Sorry, couldn't generate a roast right now.",
            "encouragement": "",
            "tip": "",
        }
