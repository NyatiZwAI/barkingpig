import requests

#--- LinkedIn ---
#LINKEDIN_TOKEN = ""
#LINKEDIN_ACCOUNT_AI=""

#def post_linkedin(title, summary, url):
#    endpoint = "https://api.linkedin.com/v2/ugcPosts"
#    headers = {
#        "Authorization": f"Bearer {LINKEDIN_TOKEN}",
#        "X-Restli-Protocol-Version": "2.0.0",
#        "Content-Type": "application/json"
#    }
#    payload = {
#        "author": f"urn:li:person:{LINKEDIN_ACCOUNT_ID}",
#        "lifecycleState": "PUBLISHED",
#        "specificContent": {
#            "com.linkedin.ugc.ShareContent": {
#                "shareCommentary": {"text": f"{title}\n\n{summary}\nRead more: {url}"},
#            }
#        },
#        "visibility": {"com.linkedin.ugc.MemberNetworlVisibility": "PUBLIC"}
#    }
#    r = request.post(endpoint, headers=headers, json=payload)
#    if r.status_code == 201:
#        print(f"Linkedin post published: {title}")
#    else:
#        print(f"Linkedin error: {r.text}")

# ---WhatsApp ---
WHATSAPP_URL = "https://WHATAPP_API_SERVER/sendMessage"

def post_whatsapp(phone_numbers, message):
    for number in phone_numbers:
        payload = {
            "to": number,
            "type": "text",
            "text": {"body": message}
        }
        r = requests.post(WHATSAPP_URL, json=payload)
        if r.status == 200:
            print(f"Whatsapp message sent to {number}")
        else:
            print(f"WhatsApp error for {number}: {r.text}")

# --- Combined function ---
def post_to_social_media(article):
    title = article['h']
    summary = article['meta_description']
    filename = article['filename']
    url = f"https://example.com/blog/{filename.replace('.md', '.html')}"

    #post_linkedin(title, summary, url)

    whatsapp_numbers = []
    message = f"{title}\n{summary}\nRead more: {url}"
    post_whatsapp(whatsapp_numbers, message)
