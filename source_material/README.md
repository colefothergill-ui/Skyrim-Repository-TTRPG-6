# Source Material Directory

This directory contains the PDF source materials and their converted/structured versions for efficient querying.

## Directory Structure

```
source_material/
├── raw_pdfs/           # Original PDF files
└── converted_pdfs/     # Structured Markdown and JSON conversions
```

## Raw PDFs

The `raw_pdfs/` directory contains the original PDF source materials:

1. **Elder Scrolls: Skyrim – Fate Core Campaign Module.pdf**
   - Core campaign module for running Skyrim in Fate Core
   - Contains base rules, setting information, and adventure hooks

2. **Daedric Princes, Man & Mer, and the Standing Stones of Skyrim.pdf**
   - Details on all playable races
   - Complete Standing Stone guide with mechanical effects
   - Daedric Prince lore and quest structure

3. **Dragonbreaks, Creatures, and Companions Module.pdf**
   - Dragonbreak mechanics and canon management
   - Creature stat blocks
   - Companion rules and mechanics

4. **Skyrim Faction Pack: Side Plot C – Allegiances in War.pdf**
   - Faction dynamics during the civil war
   - Imperial vs Stormcloak content
   - Side quest templates

## Converted Content

The `converted_pdfs/` directory contains structured versions of key PDF content:

### races.json
- **Format**: JSON
- **Source**: Daedric Princes, Man & Mer, and the Standing Stones of Skyrim.pdf
- **Content**: All 10 playable races with complete mechanical data
  - Nord, Imperial, Breton, Redguard
  - High Elf (Altmer), Wood Elf (Bosmer), Dark Elf (Dunmer)
  - Orc, Khajiit, Argonian
- **Includes**: Racial abilities, powers, skill bonuses, starting aspects

### standing_stones.md
- **Format**: Markdown
- **Source**: Daedric Princes, Man & Mer, and the Standing Stones of Skyrim.pdf
- **Content**: Complete guide to all Standing Stones
  - The Guardian Stones (Warrior, Mage, Thief)
  - All 13 Standing Stones with locations
  - Fate Core mechanical translations
  - Character creation rules

### dragonbreaks.md
- **Format**: Markdown
- **Source**: Dragonbreaks, Creatures, and Companions Module.pdf
- **Content**: Canon management and Dragonbreak protocol
  - What is a Dragonbreak
  - When to invoke one
  - How to implement and track
  - Canon tier system
  - Example scenarios

### daedric_quests.md
- **Format**: Markdown
- **Source**: Daedric Princes, Man & Mer, and the Standing Stones of Skyrim.pdf
- **Content**: Complete Daedric Prince quest guide
  - All 16 Daedric Princes
  - Quest structure templates
  - Artifact mechanics as Fate stunts
  - Moral complexity guidelines

## PDF Index

The file `data/pdf_index.json` provides a queryable index of all converted content, mapping topics to specific files for efficient retrieval.

### Using the PDF Index

Query topics using the `query_data.py` script:

```python
from query_data import DataQueryManager

manager = DataQueryManager("../data")

# Query for specific topics
results = manager.query_pdf_topics("standing stones")
print(results)

# Get actual content
content = manager.get_pdf_content("races")
print(content)
```

### Available Query Topics

- **Character Creation**: races, standing stones, character creation
- **Lore**: dragonbreaks, canon, timeline, daedric princes
- **Mechanics**: artifacts, racial abilities, blessings
- **Specific Races**: nord, imperial, breton, redguard, high elf, wood elf, dark elf, orc, khajiit, argonian
- **Specific Stones**: warrior stone, mage stone, thief stone, ritual stone, etc.
- **Specific Daedra**: azura, mehrunes dagon, hermaeus mora, molag bal, etc.

## Conversion Guidelines

When converting additional PDF content:

1. **Choose Format**:
   - **JSON**: Use for structured data (stats, lists, mechanical info)
   - **Markdown**: Use for text-heavy content (lore, procedures, guides)

2. **Structure**:
   - Keep files focused on specific topics
   - Use clear, consistent naming
   - Include source PDF in header/metadata

3. **Update PDF Index**:
   - Add new files to `data/pdf_index.json`
   - Map relevant query topics
   - Include description and source information

4. **Mechanical Translation**:
   - Translate Skyrim mechanics to Fate Core equivalents
   - Maintain balance and game feel
   - Provide clear usage guidelines

## Future Conversions

Additional content from the PDFs that could be converted:

- **Creatures**: Stat blocks for common enemies (draugr, dragons, bandits)
- **Magic System**: Spell lists and magic mechanics
- **Dragon Shouts**: Complete Thu'um guide
- **Crafting**: Smithing, enchanting, alchemy rules
- **Locations**: Detailed location descriptions and aspects
- **Factions**: Detailed faction structure and advancement

## Maintenance

- Keep PDF index updated as new conversions are added
- Ensure converted content stays synchronized with source PDFs
- Review and update conversions as house rules evolve
- Document any homebrew additions separately

---

**Note**: Original PDFs remain in `raw_pdfs/` as authoritative source. Converted content is for convenience and efficient querying during gameplay.
