from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()

def extract_action_plan(raw_text):
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    
    prompt = f"""
You are a legal assistant helping Indian government officials understand court judgments.

Read the court judgment text below and extract the following information.
Respond ONLY in valid JSON. No markdown, no code blocks, no explanations.

{{
  "case_number": "exact case number from the document",
  "court_name": "name of the court that issued this judgment",
  "judgment_date": "date in DD-MM-YYYY format, or null if not found",
  "parties": "petitioner vs respondent names",
  "judgment_summary": "2-3 sentence plain language summary of what the court decided",
  "directives": [
    "First specific action the government department must take",
    "Second specific action the government department must take"
  ],
  "compliance_deadline": "deadline date in DD-MM-YYYY format, or null if not mentioned",
  "appeal_recommended": true or false,
  "appeal_reason": "one sentence reason if appeal is recommended, empty string if not"
}}

Important rules:
- Write directives in plain simple English. No legal jargon.
- Each directive should be one clear action sentence starting with a verb.
- Extract only what is actually written. Do not assume or invent anything.
- If a field is not found in the document, use null or empty string.

Judgment text:
{raw_text[:12000]}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        text = response.choices[0].message.content.strip()

        if '```' in text:
            text = text.split('```')[1]
            if text.startswith('json'):
                text = text[4:]

        return json.loads(text.strip())

    except Exception as e:
        print(f"Groq failed: {e}")
        return {
            "case_number": "",
            "court_name": "",
            "judgment_date": None,
            "parties": "",
            "judgment_summary": "Extraction failed. Please review manually.",
            "directives": ["Manual review required"],
            "compliance_deadline": None,
            "appeal_recommended": False,
            "appeal_reason": ""
        }