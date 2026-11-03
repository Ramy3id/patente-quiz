import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

transcript_path = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\.system_generated\logs\transcript.jsonl"

with open(transcript_path, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if 'اسكرول' in line or 'scroll' in line.lower():
            try:
                data = json.loads(line)
                if data.get('type') == 'USER_INPUT':
                    print("--- USER INPUT ---")
                    print(data.get('content'))
                elif 'thinking' in data and any(k in data.get('thinking', '') for k in ['اسكرول', 'scroll-snap']):
                    # show matching part of thinking
                    th = data.get('thinking', '')
                    pos = th.find('اسكرول')
                    if pos != -1:
                        print("--- THINKING ---")
                        print(th[max(0, pos-100):min(len(th), pos+200)])
            except Exception:
                pass
