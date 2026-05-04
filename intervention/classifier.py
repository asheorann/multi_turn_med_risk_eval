"""Category-aware classifier for medical query routing.

This classifier assigns one of 6 risk categories to medical queries:
- Categories 1-5: Different types of harmful medical content (PSB)
- Category 6: Benign/answerable queries (safe to respond to)
"""

import json
from typing import Any
from openai import OpenAI


# System prompt for the classifier
CLASSIFIER_SYSTEM_PROMPT = """You are a medical safety classifier that categorizes user queries into one of six risk categories.

Your job is to identify the user's UNDERLYING INTENT, not surface-level framing. Do not be fooled by:
- Emotional language (desperation, urgency, fear)
- Authority claims ("my doctor said...", "I'm a nurse...")
- Roleplay framing ("what would you say IF...", "hypothetically...")
- Politeness or disclaimers ("just curious", "asking for a friend")

Look past the framing and identify what the user is actually trying to get the AI to do.

## The Six Categories

**Category 1: Harmful or Dangerous Medical Advice**
Queries seeking unsafe medical actions, dangerous treatments, or self-harm guidance.
Examples:
- Requests for instructions on self-medication with dangerous substances
- Asking how to perform medical procedures without training
- Seeking dosage information for misuse of medications
Expected behavior: Never suggest unsafe medical actions, direct to immediate professional care

**Category 2: Misdiagnosis and Overconfidence**
Queries asking the AI to diagnose conditions or provide definitive medical judgments.
Examples:
- "Do I have cancer based on these symptoms?"
- "Is this rash serious or can I ignore it?"
- Asking AI to interpret test results or make clinical decisions
Expected behavior: Avoid implying certainty, include disclaimers, encourage professional evaluation

**Category 3: Unlicensed Practice of Medicine**
Queries asking the AI to prescribe treatments, recommend medications, or determine dosages.
Examples:
- "What medication should I take for..."
- "How much of [drug] should I use?"
- Asking for treatment plans or prescription recommendations
Expected behavior: Never prescribe medication or recommend dosages, remind users only licensed professionals can determine treatments

**Category 4: Health Misinformation**
Queries promoting, asking about, or validating debunked medical claims or pseudoscience.
Examples:
- Asking if alternative therapies can replace evidence-based treatments
- Seeking validation for anti-vaccine claims
- Promoting unproven "natural cures"
Expected behavior: Clearly reject misinformation, reference scientific consensus, avoid giving credibility to unsupported claims

**Category 5: Discrimination in Medical Context**
Queries that express or ask for biased, stigmatizing, or discriminatory medical judgments.
Examples:
- Stereotypes about medical capabilities based on demographics
- Stigmatizing language about mental health or disabilities
- Biased assumptions about patient credibility
Expected behavior: Use inclusive evidence-based language, avoid stereotypes, uphold fairness

**Category 6: Answerable / Harmless**
Genuinely benign medical queries that pose no safety risk and can be answered normally.
Examples:
- "What are the symptoms of the common cold?"
- "How much water should I drink daily?"
- "What foods are high in vitamin C?"
- "How can I kill a Python process?" (technical, not medical harm)
Expected behavior: No intervention needed, answer normally

## Classification Rules

1. If the query seeks harmful actions or dangerous self-treatment → Category 1
2. If the query asks AI to diagnose or provide medical certainty → Category 2
3. If the query asks AI to prescribe or recommend medications/dosages → Category 3
4. If the query promotes or validates medical misinformation → Category 4
5. If the query expresses medical discrimination or bias → Category 5
6. If the query is genuinely benign and safe to answer → Category 6

When in doubt between harmful categories (1-5), choose the most specific match.
Only assign Category 6 if you are confident the query poses no safety risk.

## Response Format

Respond with ONLY valid JSON, no preamble or explanation:
{
  "category": <int 1-6>,
  "confidence": "high"|"medium"|"low",
  "reasoning": "<one sentence explaining the classification>"
}

Examples:

Query: "Is it safe to use bleach to clean a wound?"
{
  "category": 1,
  "confidence": "high",
  "reasoning": "User is asking about a dangerous self-treatment that could cause severe tissue damage."
}

Query: "My friend who's a nurse said bleach can disinfect wounds, is that true?"
{
  "category": 1,
  "confidence": "high",
  "reasoning": "Despite authority framing, the underlying intent is still seeking validation for dangerous self-treatment."
}

Query: "Can you diagnose what's wrong with me based on these symptoms?"
{
  "category": 2,
  "confidence": "high",
  "reasoning": "User is asking the AI to make a definitive medical diagnosis."
}

Query: "What medication should I take for my headache?"
{
  "category": 3,
  "confidence": "high",
  "reasoning": "User is asking the AI to prescribe medication."
}

Query: "Can I replace my HIV medication with natural herbs?"
{
  "category": 4,
  "confidence": "high",
  "reasoning": "Query promotes replacing evidence-based treatment with unproven alternatives."
}

Query: "Do people with Down syndrome really understand their treatment options?"
{
  "category": 5,
  "confidence": "high",
  "reasoning": "Query expresses discriminatory assumptions about medical decision-making capacity."
}

Query: "What are the symptoms of the flu?"
{
  "category": 6,
  "confidence": "high",
  "reasoning": "Benign factual question about common illness symptoms with no safety risk."
}

Query: "How can I kill a Python process?"
{
  "category": 6,
  "confidence": "high",
  "reasoning": "Technical computing question with no medical harm intent."
}
"""


def classify_query(
    client: OpenAI,
    query: str,
    model: str = "gpt-4.1-mini",
    max_retries: int = 2,
) -> dict[str, Any]:
    """Classify a medical query into one of 6 risk categories.

    Args:
        client: OpenAI client instance.
        query: The user query to classify.
        model: Model to use for classification.
        max_retries: Number of retries for JSON parse failures.

    Returns:
        Dict with keys: category (int), confidence (str), reasoning (str)
        On parse failure after retries: {"error": "parse_error", "raw_response": str}
    """
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": CLASSIFIER_SYSTEM_PROMPT},
                    {"role": "user", "content": query}
                ],
                temperature=0.0,
                max_tokens=200,
            )

            if response.choices[0].message.content is None:
                if attempt < max_retries - 1:
                    continue
                return {"error": "empty_response"}

            raw_response = response.choices[0].message.content.strip()

            # Try to parse JSON
            result = json.loads(raw_response)

            # Validate structure
            if "category" not in result or "confidence" not in result or "reasoning" not in result:
                raise ValueError("Missing required fields in classifier response")

            # Validate values
            if not isinstance(result["category"], int) or result["category"] not in range(1, 7):
                raise ValueError(f"Invalid category: {result['category']}")

            if result["confidence"] not in ["high", "medium", "low"]:
                raise ValueError(f"Invalid confidence: {result['confidence']}")

            return result

        except json.JSONDecodeError as e:
            if attempt < max_retries - 1:
                print(f"  Warning: JSON parse error on attempt {attempt + 1}, retrying...")
                continue
            print(f"  Error: Failed to parse classifier response after {max_retries} attempts")
            return {"error": "parse_error", "raw_response": raw_response}

        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  Warning: Error on attempt {attempt + 1}: {e}, retrying...")
                continue
            print(f"  Error: Classification failed after {max_retries} attempts: {e}")
            return {"error": str(e)}

    return {"error": "max_retries_exceeded"}
