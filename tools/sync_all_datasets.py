# -*- coding: utf-8 -*-
"""
Master Dataset Synchronization Script for Patente B Pro
Integrates enriched Chapter 14 questions, rebuilds Capitoli_Divisi/data_all_questions.js,
and synchronizes assets/all_questions.json to achieve 100.0% coverage across all 25 chapters (7,139 questions).
"""

import os
import sys
import json
import glob

sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = r'R:\Ramy\PATENTE'
SCRATCH_DIR = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\b13f0a82-3d3e-48f4-8ed4-af0d18b93a45\scratch'

BATCH_FILES = [
    os.path.join(SCRATCH_DIR, 'batch1_output.json'),
    os.path.join(SCRATCH_DIR, 'batch2_output.json'),
    os.path.join(SCRATCH_DIR, 'batch3_output.json'),
    os.path.join(SCRATCH_DIR, 'batch4_output.json')
]

CH14_JSON = os.path.join(REPO_ROOT, 'Capitoli_Divisi', 'Capitolo_14_precedenza_incroci', 'domande.json')
OUT_JS = os.path.join(REPO_ROOT, 'Capitoli_Divisi', 'data_all_questions.js')
MASTER_JSON = os.path.join(REPO_ROOT, 'assets', 'all_questions.json')

def load_batches():
    updates = {}
    missing = []
    for bf in BATCH_FILES:
        if not os.path.exists(bf):
            missing.append(os.path.basename(bf))
            continue
        with open(bf, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                for item in data:
                    updates[item['id']] = item
            except Exception as e:
                print(f"Error loading {bf}: {e}")
    if missing:
        print(f"Warning: Missing batch files: {missing}")
    print(f"Loaded updates for {len(updates)} questions from batches.")
    return updates

def update_chapter_14(updates):
    with open(CH14_JSON, 'r', encoding='utf-8') as f:
        ch14_data = json.load(f)

    questions = ch14_data.get('domande', [])
    updated_count = 0

    for q in questions:
        qid = q['id']
        if qid in updates:
            u = updates[qid]
            if u.get('traduzione'):
                q['traduzione'] = u['traduzione'].strip()
            if u.get('spiegazione'):
                q['spiegazione'] = u['spiegazione'].strip()
            if u.get('trabocchetto'):
                q['trabocchetto'] = u['trabocchetto'].strip()
            if u.get('parole_chiave'):
                q['parole_chiave'] = u['parole_chiave']
            updated_count += 1

    with open(CH14_JSON, 'w', encoding='utf-8') as f:
        json.dump(ch14_data, f, ensure_ascii=False, indent=2)

    print(f"Updated {updated_count}/{len(questions)} questions in Chapter 14.")

def rebuild_data_all_questions_js():
    chap_dirs = sorted(glob.glob(os.path.join(REPO_ROOT, 'Capitoli_Divisi', 'Capitolo_*')))
    all_questions = []
    ch_meta_list = []

    for idx, chap_dir in enumerate(chap_dirs, 1):
        dpath = os.path.join(chap_dir, 'domande.json')
        if not os.path.exists(dpath):
            continue
        with open(dpath, 'r', encoding='utf-8') as f:
            cdata = json.load(f)

        folder_name = os.path.basename(chap_dir)
        titolo_ar = cdata.get('titolo_ar', '')
        raw_qs = cdata.get('domande') or cdata.get('quiz') or []

        ch_meta_list.append({
            "num": idx,
            "folder": folder_name,
            "titolo_it": cdata.get('titolo_it', ''),
            "titolo_ar": titolo_ar,
            "count": len(raw_qs)
        })

        for q in raw_qs:
            qid = q.get('id')
            sub = q.get('sotto_argomento', 'عام')
            domanda_text = q.get('domanda', '')
            risposta = bool(q.get('risposta'))
            img_raw = q.get('immagine', '').strip()

            img_path = ''
            if img_raw:
                img_path = f"{folder_name}/{img_raw}"

            trad = q.get('traduzione', '').strip()
            spieg = q.get('spiegazione', '').strip()
            trab = q.get('trabocchetto', '').strip()

            p_chiave = []
            for pk in q.get('parole_chiave', []):
                if isinstance(pk, dict):
                    p_chiave.append({"it": pk.get('it', ''), "ar": pk.get('ar', '')})
                elif isinstance(pk, str):
                    p_chiave.append({"it": pk, "ar": ""})

            all_questions.append({
                "id": qid,
                "ch": idx,
                "ch_name": f"الباب {idx}: {titolo_ar}" if titolo_ar else f"Capitolo {idx}",
                "sub": sub,
                "q": domanda_text,
                "a": risposta,
                "img": img_path,
                "tr": trad,
                "sp": spieg,
                "tb": trab,
                "pk": p_chiave
            })

    js_content = "// Auto-generated Patente B Pro Aggregated Dataset (All 25 Chapters)\n"
    js_content += f"// Total Questions: {len(all_questions)}\n"
    js_content += f"const CHAPTERS_META = {json.dumps(ch_meta_list, ensure_ascii=False)};\n\n"
    js_content += f"const ALL_QUESTIONS_DATA = {json.dumps(all_questions, ensure_ascii=False)};\n"

    with open(OUT_JS, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"Rebuilt {OUT_JS} ({len(all_questions)} questions, {os.path.getsize(OUT_JS)/(1024*1024):.2f} MB).")

def rebuild_master_all_questions_json():
    chap_dirs = sorted(glob.glob(os.path.join(REPO_ROOT, 'Capitoli_Divisi', 'Capitolo_*')))
    master_list = []
    global_id = 1

    for idx, chap_dir in enumerate(chap_dirs, 1):
        dpath = os.path.join(chap_dir, 'domande.json')
        if not os.path.exists(dpath):
            continue
        with open(dpath, 'r', encoding='utf-8') as f:
            cdata = json.load(f)

        folder_name = os.path.basename(chap_dir)
        raw_qs = cdata.get('domande') or cdata.get('quiz') or []

        for q in raw_qs:
            master_list.append({
                "id": q.get('id', global_id),
                "sotto_argomento": q.get('sotto_argomento', 'عام'),
                "domanda": q.get('domanda', ''),
                "risposta": bool(q.get('risposta')),
                "immagine": q.get('immagine', ''),
                "traduzione": q.get('traduzione', '').strip(),
                "spiegazione": q.get('spiegazione', '').strip(),
                "trabocchetto": q.get('trabocchetto', '').strip(),
                "parole_chiave": q.get('parole_chiave', []),
                "id_ministeriale": q.get('id_ministeriale', global_id),
                "capitolo_num": idx,
                "capitolo_name": folder_name
            })
            global_id += 1

    with open(MASTER_JSON, 'w', encoding='utf-8') as f:
        json.dump(master_list, f, ensure_ascii=False, indent=2)

    print(f"Rebuilt {MASTER_JSON} ({len(master_list)} questions, {os.path.getsize(MASTER_JSON)/(1024*1024):.2f} MB).")

def audit_coverage():
    with open(MASTER_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = len(data)
    tr_count = sum(1 for q in data if q.get('traduzione') and 'سؤال يتناول موضوع' not in q['traduzione'])
    old_placeholder_vero = 'العبارة صحيحة (VERO) ومطابقة تماماً لنصوص كود السير'
    old_placeholder_falso = 'العبارة خاطئة (FALSO) وغير متطابقة مع نصوص كود السير'
    sp_count = sum(1 for q in data if q.get('spiegazione') and old_placeholder_vero not in q['spiegazione'] and old_placeholder_falso not in q['spiegazione'])
    tb_count = sum(1 for q in data if q.get('trabocchetto') and q['trabocchetto'].strip())
    pk_count = sum(1 for q in data if q.get('parole_chiave') and len(q['parole_chiave']) > 0)

    print("\n" + "="*60)
    print("PATENTE B PRO - FINAL COMPREHENSIVE DATASET AUDIT")
    print("="*60)
    print(f"Total Questions in Question Bank: {total}")
    print(f"1. Arabic Translations:  {tr_count}/{total} ({tr_count/total*100:.2f}%)")
    print(f"2. Legal Explanations:   {sp_count}/{total} ({sp_count/total*100:.2f}%)")
    print(f"3. Trap Badges:          {tb_count}/{total} ({tb_count/total*100:.2f}%)")
    print(f"4. Keywords (Glossary):  {pk_count}/{total} ({pk_count/total*100:.2f}%)")
    print("="*60)

if __name__ == '__main__':
    updates = load_batches()
    if updates:
        update_chapter_14(updates)
        rebuild_data_all_questions_js()
        rebuild_master_all_questions_json()
        audit_coverage()
    else:
        print("No updates loaded yet. Waiting for batch outputs.")
