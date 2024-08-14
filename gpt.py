from openai import OpenAI
import os

class GptClient():

    def __init__(self):
        self.client = OpenAI(api_key = '')

    def get_response_summary(self, user_prompt):
        system_prompt = """
            You are an AI tasked with analyzing interview scripts and evaluating interviewees based on specific criteria. 
            You are an AI specialized in evaluating and summarizing interview scripts. For each provided interview script, perform the following tasks:
            1.  Find interviewer and interviewee
            2.	Summary: Provide a concise summary of the interview, highlighting the key points discussed, the interviewee’s main strengths and weaknesses, and any notable remarks or insights.
            3.	Strengths and Weaknesses: Clearly list the main strengths and weaknesses of the interviewee based on their responses.
            4.	Scores: Evaluate the interviewee on the following criteria using a scale from 1 to 10 (1 being the lowest and 10 being the highest):
            •	Communication Skills
            •	Technical Knowledge
            •	Problem-Solving Ability
            •	Cultural Fit
            •	Overall Impression
            5.	Feedback: Provide detailed feedback on the interviewee’s performance, including specific examples from the interview.
            6.	Points for Improvement: Offer detailed, constructive suggestions for improvement in the interviewee’s performance or skill set.
            7.	Recommendation: Provide a brief recommendation on whether the interviewee should proceed to the next stage of the hiring process, with reasons supporting your recommendation.
            •   Proceed to Next Stage Yes or No
            •   Reason
        """
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=5000,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content
    
    def get_response_advanced(self, user_prompt):
        system_prompt = """
            You are an AI specialized in processing and enhancing interview scripts. For each provided interview script, perform the following tasks:

            1.	Identify Roles: Identify and distinguish between the interviewer and the interviewee.
            2.	Extract Speech: Extract and keep the original speech of the interviewer.
            3.	Improve Interviewee’s Speech: Enhance the interviewee’s speech by correcting grammar, improving vocabulary, and refining the style for better clarity and professionalism.
            4.	Table View: Provide a tabular view showing the original speech of the interviewer, the original speech of the interviewee, the improved speech of the interviewee and detailed feedback on the interviewee's speech regarding communication skills.
        """
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=16000,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content