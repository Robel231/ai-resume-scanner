# backend/services/analyzer.py

import os
import json
import openai

# Check for Groq API key first
groq_api_key = os.getenv("GROQ_API_KEY")

if groq_api_key:
    print("Using Groq API...")
    client = openai.OpenAI(
        api_key=groq_api_key,
        base_url="https://api.groq.com/openai/v1",
    )
    MODEL_TO_USE = "llama3-8b-8192"
else:
    # Fallback to OpenAI if Groq key is not found
    print("Using OpenAI API...")
    try:
        client = openai.OpenAI()
        MODEL_TO_USE = "gpt-3.5-turbo"
    except openai.OpenAIError:
        client = None

def get_ai_analysis(resume_text: str, job_description: str) -> dict:
    """
    Analyzes resume text against a job description using the AI API.
    Returns a dictionary with the analysis results.
    """
    if not client:
        return {"error": "AI client not initialized. Check your API key."}

    # This is the prompt with the corrected, doubled-up curly braces for the JSON example.
    prompt = f"""
    You are an expert technical recruiter and career coach. Your task is to analyze a resume against a job description.

    Based on the provided resume text and job description, please perform a detailed analysis and return a score from 0 to 100.
    A score of 100 means the resume is a perfect match for the job description.

    Your response MUST be a JSON object with the following exact structure:
    {{
      "match_score": <number>,
      "summary": "<string, 2-3 sentences summarizing the candidate's fit>",
      "strengths": ["<list of strings detailing key skills and experiences that match the job description>"],
      "gaps": ["<list of strings identifying important skills or qualifications from the job description that are missing from the resume>"],
      "suggested_keywords": ["<list of important keywords from the job description that the candidate should consider adding to their resume>"],
      "actionable_feedback": "<string, a paragraph of specific, actionable advice for the candidate to improve their resume for this specific role>"
    }}

    ---
    JOB DESCRIPTION:
    {job_description}
    ---
    RESUME TEXT:
    {resume_text}
    ---
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_TO_USE,
            messages=[
                {"role": "system", "content": "You are an expert recruiter providing resume feedback in JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        
        analysis_content = response.choices[0].message.content
        return json.loads(analysis_content)

    except openai.APIError as e:
        print(f"AI API Error: {e}")
        return {"error": f"An error occurred with the AI API: {e}"}
    except json.JSONDecodeError:
        print("Failed to decode JSON from AI response.")
        return {"error": "The AI response was not in a valid JSON format."}