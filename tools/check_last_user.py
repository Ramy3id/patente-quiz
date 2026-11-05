import json

with open(r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for l in lines[-200:]:
    data = json.loads(l)
    if data.get('source') == 'USER_EXPLICIT' or data.get('type') == 'USER_INPUT':
        print('=== USER STEP:', data.get('step_index'), '===')
        print('CONTENT:', data.get('content', '').encode('ascii', 'backslashreplace').decode('ascii'))
        if 'media' in data:
            for m in data['media']:
                print('MEDIA:', m)
