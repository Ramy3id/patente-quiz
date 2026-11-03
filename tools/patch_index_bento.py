import sys

with open('R:/Ramy/PATENTE_PRO_APP/Capitoli_Divisi/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content_norm = content.replace('\r\n', '\n')

old_bento_css = """.bento-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}
@media (min-width: 768px) {
  .bento-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
  }
}
@media (min-width: 1024px) {
  .bento-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
  }
  .bento-extra-grid {
    display: grid !important;
  }
  .bento-toggle-btn {
    display: none !important;
  }
}

.bento-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 14px;
  background: var(--surface-card, #ffffff);
  border: 1px solid var(--border-subtle, rgba(0, 0, 0, 0.08));
  border-radius: 16px;
  text-decoration: none;
  color: inherit;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease, border-color 0.2s ease;
  min-height: 64px;
  box-sizing: border-box;
}
.bento-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  border-color: var(--primary-accent, #0284C7);
}
.bento-card:active {
  transform: scale(0.97);
}
html.dark .bento-card {
  background: rgba(255, 255, 255, 0.035);
  border-color: rgba(255, 255, 255, 0.08);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}
html.dark .bento-card:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(56, 189, 248, 0.4);
}

.bento-icon-box {
  width: 38px;
  height: 38px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  flex-shrink: 0;
}
.bento-info {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  text-align: right;
}
.bento-title {
  font-size: 0.86rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.25;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.bento-meta {
  font-size: 0.7rem;
  color: var(--text-muted, #64748B);
  margin-top: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}"""

new_bento_css = """.bento-tools-section {
  width: 100% !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
  overflow: hidden !important;
}

.bento-grid {
  display: grid !important;
  grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
  gap: 8px !important;
  width: 100% !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
}
@media (min-width: 768px) {
  .bento-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
    gap: 12px !important;
  }
}
@media (min-width: 1024px) {
  .bento-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
    gap: 14px !important;
  }
  .bento-extra-grid {
    display: grid !important;
  }
  .bento-toggle-btn {
    display: none !important;
  }
}

.bento-card {
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
  padding: 10px 8px !important;
  background: var(--surface-card, #ffffff);
  border: 1px solid var(--border-subtle, rgba(0, 0, 0, 0.08));
  border-radius: 14px !important;
  text-decoration: none;
  color: inherit;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease, border-color 0.2s ease;
  min-height: 60px !important;
  width: 100% !important;
  max-width: 100% !important;
  min-width: 0 !important;
  box-sizing: border-box !important;
  overflow: hidden !important;
}
.bento-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  border-color: var(--primary-accent, #0284C7);
}
.bento-card:active {
  transform: scale(0.97);
}
html.dark .bento-card {
  background: rgba(255, 255, 255, 0.035);
  border-color: rgba(255, 255, 255, 0.08);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}
html.dark .bento-card:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(56, 189, 248, 0.4);
}

.bento-icon-box {
  width: 34px !important;
  height: 34px !important;
  min-width: 34px !important;
  border-radius: 10px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  font-size: 1.15rem !important;
  flex-shrink: 0 !important;
}
.bento-info {
  display: flex !important;
  flex-direction: column !important;
  overflow: hidden !important;
  text-align: right !important;
  min-width: 0 !important;
  flex: 1 1 0% !important;
  width: 100% !important;
}
.bento-title {
  font-size: 0.8rem !important;
  font-weight: 700 !important;
  color: var(--text-primary);
  line-height: 1.25 !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  display: block !important;
  max-width: 100% !important;
  width: 100% !important;
}
.bento-meta {
  font-size: 0.67rem !important;
  color: var(--text-muted, #64748B);
  margin-top: 2px !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  display: block !important;
  max-width: 100% !important;
  width: 100% !important;
}"""

if old_bento_css in content_norm:
    new_content = content_norm.replace(old_bento_css, new_bento_css, 1)
    with open('R:/Ramy/PATENTE_PRO_APP/Capitoli_Divisi/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS: replaced bento grid CSS in Capitoli_Divisi/index.html")
else:
    print("ERROR: old_bento_css not matched in Capitoli_Divisi/index.html")
