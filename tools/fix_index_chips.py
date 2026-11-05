import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = '''/* 2-Row Symmetrical Category Filter Chips (Zero Horizontal Scroll & No Cutoff) */
.filter-chips {
  display: grid !important;
  grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
  gap: 8px !important;
  width: 100% !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
  overflow-x: visible !important;
  padding: 8px 0 12px !important;
}
@media (max-width: 480px) {
  .filter-chips {
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
    gap: 6px !important;
  }
}
.chip-btn {
  width: 100% !important;
  min-width: 0 !important;
  padding: 4px 2px !important;
  height: 48px !important;
  min-height: 48px !important;
  max-height: 48px !important;
  border-radius: 12px !important;
  box-sizing: border-box !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 2px !important;
  line-height: 1.15 !important;
  transition: all 0.15s ease !important;
}
.chip-btn .chip-title {
  font-size: 0.78rem !important;
  font-weight: 700 !important;
  white-space: nowrap !important;
}
.chip-btn .chip-sub {
  font-size: 0.64rem !important;
  opacity: 0.75 !important;
  font-family: 'JetBrains Mono', monospace !important;
  letter-spacing: 0.2px !important;
}'''

replacement = '''/* Filter Chips - Responsive (Single Elegant Row on Desktop, 3-Col 2-Row Grid on Mobile) */
.filter-chips {
  display: grid !important;
  grid-template-columns: repeat(6, 1fr) !important;
  gap: 10px !important;
  width: 100% !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
  overflow-x: visible !important;
  padding: 8px 0 16px !important;
}
.chip-btn {
  width: 100% !important;
  min-width: 0 !important;
  padding: 0 10px !important;
  height: 44px !important;
  min-height: 44px !important;
  max-height: 44px !important;
  border-radius: 12px !important;
  box-sizing: border-box !important;
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 6px !important;
  line-height: 1.15 !important;
  transition: all 0.15s ease !important;
}
.chip-btn .chip-title {
  font-size: 0.85rem !important;
  font-weight: 700 !important;
  white-space: nowrap !important;
}
.chip-btn .chip-sub {
  font-size: 0.72rem !important;
  opacity: 0.8 !important;
  font-family: 'JetBrains Mono', monospace !important;
  letter-spacing: 0.2px !important;
}

@media (max-width: 768px) {
  .filter-chips {
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
    gap: 8px !important;
    padding: 8px 0 12px !important;
  }
  .chip-btn {
    padding: 4px 2px !important;
    height: 48px !important;
    min-height: 48px !important;
    max-height: 48px !important;
    flex-direction: column !important;
    gap: 2px !important;
  }
  .chip-btn .chip-title {
    font-size: 0.78rem !important;
  }
  .chip-btn .chip-sub {
    font-size: 0.64rem !important;
  }
}
@media (max-width: 480px) {
  .filter-chips {
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
    gap: 6px !important;
  }
}'''

if target in content:
    content = content.replace(target, replacement, 1)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed responsive filter chips in Capitoli_Divisi/index.html successfully!")
else:
    print("ERROR: target snippet not found!")
    sys.exit(1)
