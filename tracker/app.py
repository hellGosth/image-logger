from flask import Flask, request, redirect, url_for, render_template
import requests

app = Flask(__name__)

# Discord Webhook URL
DISCORD_WEBHOOK_URL = 'YOUR_DISCORD_WEBHOOK_URL'

# Route to convert image
@app.route('/convert', methods=['POST'])
def convert_image():
    # Capture IP, User-Agent, Referrer
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    referer = request.headers.get('Referer')
    
    # Implement image conversion logic here
    # For now, just print the received data
    print(f'IP: {ip}, User-Agent: {user_agent}, Referer: {referer}')

    # Send data to Discord
    requests.post(DISCORD_WEBHOOK_URL, json={
        'content': f'New conversion triggered from IP: {ip}',
    })
    
    return 'Image conversion triggered!'

# Route for interstitial page
@app.route('/r/<slug>')
def interstitial_page(slug):
    return render_template('interstitial.html', slug=slug)

if __name__ == '__main__':
    app.run(debug=True)