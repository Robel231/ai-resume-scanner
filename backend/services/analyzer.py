# backend/services/analyzer.py

import os
import json
import openai

# --- Client Initialization ---
# This block intelligently selects the API to use based on environment variables.
# It prioritizes the free and fast Groq API.

client = None
MODEL_TO_USE = None

# Check for Groq API key first
groq_api_key = os.getenv("GROQ_API_KEY")

if groq_api_key:
    print("INFO: GROQ_API_KEY found. Initializing Groq client.")
    try:
        client = openai.OpenAI(
            api_key=groq_api_key,
            base_url="https://api.groq.com/openai/v1",  # This directs requests to Groq
        )
        MODEL_TO_USE = "llama3-8b-8192"  # A great, fast model available on Groq
        print(f"INFO: Groq client initialized successfully. Using model: {MODEL_TO_USE}")
    except Exception as e:
        print(f"ERROR: Failed to initialize Groq client: {e}")
        client = None

# If Groq client failed or key wasn't found, fallback to OpenAI
if not client:
    print("INFO: GROQ_API_KEY not found or failed to initialize. Falling back to OpenAI.")
    try:
        # The OpenAI client automatically looks for the OPENAI_API_KEY environment variable.
        client = openai.OpenAI()
        MODEL_TO_USE = "gpt-3.5-turbo"
        print(f"INFO: OpenAI client initialized successfully. Using model: {MODEL_TO_USE}")
    except openai.OpenAIError as e:
        print(f"ERROR: Failed to initialize OpenAI client. Please check your OPENAI_API_KEY. Error: {e}")
        client = None

# --- Analysis Function ---

def get_ai_analysis(resume_text: str, job_description: str) -> dict:
    """
    Analyzes resume text against a job description using the configured AI client (Groq or OpenAI).

    Returns a dictionary with the analysis results or an error message.
    """
    if not client:
        return {"error": "AI client not initialized. Check your API key environment variables (GROQ_API_KEY or OPENAI_API_KEY)."}

    # This prompt is carefully engineered to instruct the AI on its role, the task,
    # the inputs, and the exact format of the JSON output we want.
    # It works well with models like Llama3, Mixtral, and GPT.
    prompt = f"""
    You are an expert technical recruiter and career coach. Your task is to analyze a resume against a job description.

    Based on the provided resume text and job description, please perform a detailed analysis and return a score from 0 to 100.
    A score of 100 means the resume is a perfect match for the job description.

    Your response MUST be a valid JSON object with the following exact structure and key names:
    {{
      "match_score": <number>,
      "summary": "<string, 2-3 sentences summarizing the candidate's fit for the role>",
      "strengths": ["<list of strings detailing key skills and experiences that strongly align with the job description>"],
      "gaps": ["<list of strings identifying important skills or qualifications from the job description that appear to be missing from the resume>"],
      "suggested_keywords": ["<list of important keywords from the job description that the candidate should consider including>"],
      "actionable_feedback": "<string, a paragraph of specific, actionable advice for the candidate to improve their resume for this specific role. Focus on quantifying achievements and tailoring the summary.>"
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
        print(f"INFO: Sending request to AI with model {MODEL_TO_USE}...")
        response = client.chat.completions.create(
            model=MODEL_TO_USE,
            messages=[
                {"role": "system", "content": "You are an expert recruiter providing resume feedback. Your response must be a valid JSON object."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,  # Lower temperature for more deterministic, factual output
            response_format={"type": "json_object"} # Enforces the model to output valid JSON
        )

        analysis_content = response.choices[0].message.content
        print("INFO: Successfully received response from AI.")
        
        # The response content is a JSON string, so we parse it into a Python dict.
        return json.loads(analysis_content)

    except openai.APIError as e:
        print(f"ERROR: AI API Error: {e}")
        return {"error": f"An error occurred with the AI API: {e}"}
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to decode JSON from AI response. Raw response: {analysis_content}")
        return {"error": "The AI response was not in a valid JSON format."}
    except Exception as e:
        print(f"ERROR: An unexpected error occurred in get_ai_analysis: {e}")
        return {"error": f"An unexpected error occurred: {e}"}