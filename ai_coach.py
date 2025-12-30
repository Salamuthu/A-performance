from groq import Groq
import os


client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_advice(athlete_data, injury_risk, performance):
    """
    Sends athlete stats and ML predictions to Groq for coaching advice.
    """
    prompt = f"""
    You are a professional AI Athletic Coach. Analyze this athlete:
    - Age: {athlete_data['age']}
    - Training: {athlete_data['training_hours_per_day']}h/day, {athlete_data['training_days_per_week']} days/week
    - Sleep: {athlete_data['sleep_hours']}h
    - Rest Days: {athlete_data['rest_days_per_week']}
    - ML Predicted Injury Risk: {injury_risk}
    - ML Predicted Performance Trend: {performance}

    Provide 3 concise, bullet-pointed instructions to improve their performance and reduce injury risk. 
    Be direct and professional.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful and elite sports performance coach."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            max_tokens=300
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"AI Coaching unavailable: {str(e)}"