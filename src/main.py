from unittest import mock
from flask import Flask, render_template, request
from test import bots_list, generate_prompt_with_examples, client
import webbrowser
import threading
import os
app = Flask(__name__)

mock_response = """
Bot ID: 0xdac6f4a16776648ef48b0c9850800507059e201139c2aa898b47d51ca0ebdaae
Bot Name: Example Bot 1
Developer Name: Dev 1
Reason: "The specific web3 bot described and provided in the source code is a ""Large Balance Decrease Bot"" used to monitor significant balance decreases in a protocol's token balance across multiple blockchain networks which include Ethereum, Optimism, Binance Smart Chain, Polygon, Fantom, Arbitrum, and Avalanche. "

Bot ID: 0xb8900e67...
Bot Name: Example Bot 2
Developer Name: Dev 2
Reason: This bot can...

Bot ID: 0x0f9913e7...
Bot Name: Example Bot 3
Developer Name: Dev 3
Reason: This bot excels at...
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    print("Route accessed")
    user_requirement = '' 

    recommended_bots = []  
    if request.method == 'POST':
        user_requirement = request.form['requirement']
        concise_prompt = generate_prompt_with_examples(user_requirement, bots_list)

        ai_response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "system", "content": concise_prompt}],
            max_tokens=3000
        )
        
        formatted_response = ai_response.choices[0].message.content  
        # formatted_response = mock_response
   
        bot_sections = formatted_response.split('\n\n')
        
        for section in bot_sections:
            bot_info = {}
            for line in section.split('\n'):
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    bot_info[key.strip()] = value.strip()
            if bot_info:
                recommended_bots.append(bot_info)

        return render_template('index.html', user_requirement=user_requirement, recommended_bots=recommended_bots)

    else:
        return render_template('index.html')

def open_chrome():
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    webbrowser.get(chrome_path).open('http://127.0.0.1:5000/')

if __name__ == '__main__':
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Timer(1, open_chrome).start()

    app.run(debug=True)