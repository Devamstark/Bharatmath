import os, json, base64, requests
GEMINI_KEY=os.environ.get("GEMINI_KEY")
ENDPOINT=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
def handler(req,res):
    if req.method!="POST": return res.status(404).send("Not found")
    body=req.json; image=body.get("image","")
    if not image: return res.status(400).json({"message":"No image"})
    base64_image=image.split(",")[1]
    payload={
      "contents":[{"parts":[
        {"text":"Solve the math problem step by step (use LaTeX for formulas)."},
        {"inlineData":{"mimeType":"image/jpeg","data":base64_image}}
      ]}],
      "generationConfig":{"temperature":0.4,"maxOutputTokens":2048}
    }
    r=requests.post(ENDPOINT,json=payload,headers={"Content-Type":"application/json"})
    if r.status_code!=200: return res.status(r.status_code).json(r.json())
    try:
        text=r.json()["candidates"][0]["content"]["parts"][0]["text"]
        return res.json({"solution":text})
    except Exception as e: return res.status(500).json({"message":str(e)})
