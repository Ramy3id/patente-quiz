import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\modular-chapter-engine.js'

with open(file_path, 'r', encoding='utf-8', newline='') as f:
    content = f.read()

# 1. Edit in init:
target1 = """      // Map each question to its unified group
      this.data.domande.forEach(q => {
        const rawSub = q.sotto_argomento ? q.sotto_argomento.trim() : '';
        q.gruppo_unificato = this.subtopicMap[rawSub] || rawSub || 'altro';
      });

      // Export globally for inline HTML events"""

replacement1 = """      // Map each question to its unified group
      this.data.domande.forEach(q => {
        const rawSub = q.sotto_argomento ? q.sotto_argomento.trim() : '';
        q.gruppo_unificato = this.subtopicMap[rawSub] || rawSub || 'altro';
      });

      // Sort questions so they follow the numerical sequence of the subtopic groups (1..N)
      // while preserving original ministerial sequence within the same subtopic
      this.data.domande.sort((a, b) => {
        const numA = (this.groups[a.gruppo_unificato] && typeof this.groups[a.gruppo_unificato].num === 'number') 
          ? this.groups[a.gruppo_unificato].num : 9999;
        const numB = (this.groups[b.gruppo_unificato] && typeof this.groups[b.gruppo_unificato].num === 'number') 
          ? this.groups[b.gruppo_unificato].num : 9999;
        if (numA !== numB) return numA - numB;
        return (a.id || 0) - (b.id || 0);
      });

      // Export globally for inline HTML events"""

# 2. Edit in renderChips:
target2 = """      const totalDomande = this.data.domande.length;
      const groupKeys = Object.keys(this.groups);
      const totalGroups = groupKeys.length;"""

replacement2 = """      const totalDomande = this.data.domande.length;
      const groupKeys = Object.keys(this.groups).sort((a, b) => {
        const numA = (this.groups[a] && typeof this.groups[a].num === 'number') ? this.groups[a].num : 9999;
        const numB = (this.groups[b] && typeof this.groups[b].num === 'number') ? this.groups[b].num : 9999;
        return numA - numB;
      });
      const totalGroups = groupKeys.length;"""

# 3. Edit in renderQuestions:
target3 = """      } else {
        // Group by gruppo_unificato
        const groupsMap = new Map();
        filtered.forEach(q => {
          const gKey = q.gruppo_unificato || 'altro';
          if (!groupsMap.has(gKey)) groupsMap.set(gKey, []);
          groupsMap.get(gKey).push(q);
        });

        const totalGroupsCount = Object.keys(this.groups).length || 1;

        groupsMap.forEach((questions, gKey) => {"""

replacement3 = """      } else {
        // Group by gruppo_unificato
        const groupsMap = new Map();
        filtered.forEach(q => {
          const gKey = q.gruppo_unificato || 'altro';
          if (!groupsMap.has(gKey)) groupsMap.set(gKey, []);
          groupsMap.get(gKey).push(q);
        });

        // Ensure groups are rendered strictly in numerical order of this.groups (1, 2, 3...)
        const sortedGroupEntries = Array.from(groupsMap.entries()).sort((a, b) => {
          const numA = (this.groups[a[0]] && typeof this.groups[a[0]].num === 'number') ? this.groups[a[0]].num : 9999;
          const numB = (this.groups[b[0]] && typeof this.groups[b[0]].num === 'number') ? this.groups[b[0]].num : 9999;
          return numA - numB;
        });

        const totalGroupsCount = Object.keys(this.groups).length || 1;

        sortedGroupEntries.forEach(([gKey, questions]) => {"""

# Convert targets to CRLF if needed
if '\r\n' in content:
    target1 = target1.replace('\n', '\r\n')
    replacement1 = replacement1.replace('\n', '\r\n')
    target2 = target2.replace('\n', '\r\n')
    replacement2 = replacement2.replace('\n', '\r\n')
    target3 = target3.replace('\n', '\r\n')
    replacement3 = replacement3.replace('\n', '\r\n')

assert target1 in content, "target1 not found"
content = content.replace(target1, replacement1, 1)

assert target2 in content, "target2 not found"
content = content.replace(target2, replacement2, 1)

assert target3 in content, "target3 not found"
content = content.replace(target3, replacement3, 1)

with open(file_path, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("Successfully updated modular-chapter-engine.js!")
