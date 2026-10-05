import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
app=Flask(__name__)
key=os.getenv("GEMINI_API_KEY")
model=os.getenv("GEMINI_MODEL","gemini-3.8-flash")
client=genai.Client(api_key=key) if key else None

SYSTEM="""You are PocketSmart AI, a student-friendly budgeting assistant.
Give simple educational budgeting suggestions based only on user-provided information.
Do not guarantee financial results or present yourself as a professional financial adviser.
Do not invent numbers. Explain assumptions clearly."""

@app.route("/")
def home(): return render_template("index.html")

@app.post("/api/recommend")
def recommend():
    if not client: return jsonify(error="GEMINI_API_KEY is not configured."),500
    d=request.get_json() or {}
    income=d.get("income","").strip()
    expenses=d.get("expenses","").strip()
    goal=d.get("goal","").strip()
    question=d.get("question","").strip()
    if not any([income,expenses,goal,question]):
        return jsonify(error="Enter some budget information first."),400
    prompt=f"""Analyze this budget information.
Income: {income}
Expenses: {expenses}
Savings goal: {goal}
Question: {question}
Return a short summary, suggested budget breakdown, practical spending tips,
a savings suggestion, and assumptions. Do not invent missing numbers."""
    try:
        r=client.models.generate_content(
            model=model, contents=[types.Content(role="user",parts=[types.Part(text=prompt)])],
            config=types.GenerateContentConfig(system_instruction=SYSTEM,temperature=.3,max_output_tokens=1400))
        return jsonify(answer=r.text or "No response generated.")
    except Exception as e:
        print(e); return jsonify(error="Gemini request failed. Check API key and internet."),500

@app.post("/api/chat")
def chat():
    if not client: return jsonify(error="GEMINI_API_KEY is not configured."),500
    q=(request.get_json() or {}).get("message","").strip()
    if not q: return jsonify(error="Enter a question."),400
    try:
        r=client.models.generate_content(model=model,contents=q,
            config=types.GenerateContentConfig(system_instruction=SYSTEM,temperature=.3,max_output_tokens=900))
        return jsonify(answer=r.text or "No response generated.")
    except Exception as e:
        print(e); return jsonify(error="Gemini request failed."),500

if __name__=="__main__": app.run(debug=True)
