import os
from pyexpat.errors import messages
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


excel_path = 'path/to/your/directory'
data = pd.read_excel(excel_path)
bots_list = data.to_dict(orient='records')



def generate_prompt_with_examples(user_requirement, bots_list):
    summarized_bot_info = ""
    for bot in bots_list:

        summarized_bot_info += f"Bot ID: {bot['_id']}, Bot name: {bot['_source.current.name']} ,Developer: {bot['_source.current.developer']}, Summary: {bot['Summary']} "


    prompt = (
        "Upon receiving a user input, first CHECK IF USER INPUT IS A BOT ID OR BOT NAME. If so, retrieve and display only the respective bot's details. If the input is not a bot ID or name, then proceed to analyze the user's requirements more broadly."

        "IF USER INPUT IS BOT ID OR BOT NAME:"
        "Retrieve and display only the specific bot's details: (ENSURE BOT ID REQUESTED AND DISPLAYED ARE THE SAME)"
        "Bot ID: [Insert Bot ID]"
        "Bot Name: [Insert Bot Name]"
        "Developer Name: [Insert Developer Name]"
        "Bot Reason: [NO SUMMARY NEEDED IF REUQUESTED BY BOT ID, BOT NAME OR DEVELOPER NAME]"

        'ELSE IF IT NOT A BOT ID OR BOT NAME'
        "Please review the following user requirement and the summaries of available bots. "
        "Based on the user's need, identify up to three bots that are most suitable for the task. "
        "Provide a clear recommendation with the Bot ID, Bot Name, and Developer Name, along with a brief explanation "
        "as to why each bot is a good match for the requirement. If no bots are suitable, advise the user to refine their search.\n\n"
        f"User Requirement:\n{user_requirement}\n\n"
        "Available Bots and Summaries:\n"
        f"{summarized_bot_info}\n\n"
        "Recommendations:\n"

        "BOT 1:\n"
        "Bot ID: [Insert Bot ID]\n"
        "Bot Name: [Insert Bot Name]\n"
        "Developer Name: [Insert Developer Name]\n"
        "Reason: [Provide a short reason for the recommendation]\n\n"
        
        'if more bots available then recommend another bot'
        "BOT 2: \n"
        "Bot ID: [Insert Bot ID, if applicable]\n"
        "Bot Name: [Insert Bot Name, if applicable]\n"
        "Developer Name: [Insert Developer Name, if applicable]\n"
        "Reason: [Provide a short reason, if applicable]\n\n"

        'if more bots available then recommend another bot'
        "BOT 3:\n"
        "Bot ID: [Insert Bot ID, if applicable]\n"
        "Bot Name: [Insert Bot Name, if applicable]\n"
        "Developer Name: [Insert Developer Name, if applicable]\n"
        "Reason: [Provide a short reason, if applicable]\n"
    )


    return prompt


