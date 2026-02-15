#!/usr/bin/env python3
"""
Export Script for Skyrim TTRPG

This script exports the entire repository as a .zip file
optimized for use with ChatGPT 5.2 for dynamic game simulation
and narrative integration.
"""

import json
import os
import zipfile
from datetime import datetime
from pathlib import Path


def load_json_safely(path):
    """
    Load JSON with multiple encoding fallback attempts.
    
    Windows often defaults to cp1252; repo JSON is intended to be UTF-8.
    This loader tries UTF-8 variants first, then common fallbacks.
    
    Args:
        path: Path object pointing to JSON file
        
    Returns:
        dict: Parsed JSON data
        
    Raises:
        json.JSONDecodeError: If JSON parsing fails with all encodings
        IOError: If file cannot be read
    """
    if not isinstance(path, Path):
        path = Path(path)
        
    try:
        data = path.read_bytes()
    except (IOError, OSError) as e:
        raise IOError(f"Cannot read file {path}: {e}")
    
    # Try encodings in order of likelihood
    for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return json.loads(data.decode(encoding))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
    
    # Last resort with error replacement
    try:
        return json.loads(data.decode("latin-1", errors="replace"))
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Failed to parse JSON from {path}", e.doc, e.pos)


class RepositoryExporter:
    def __init__(self, repo_dir="."):
        """
        Initialize the RepositoryExporter.
        
        Args:
            repo_dir: Path to the repository root directory (default: ".")
        """
        self.repo_dir = Path(repo_dir)
        self.data_dir = self.repo_dir / "data"
        self.scripts_dir = self.repo_dir / "scripts"
        self.docs_dir = self.repo_dir / "docs"
        
        # Ensure directories exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        
    def create_context_file(self):
        """Create a context file for ChatGPT with repository overview"""
        context = {
            "project": "Skyrim TTRPG Campaign Manager",
            "system": "Fate Core",
            "setting": "The Elder Scrolls V: Skyrim",
            "export_date": datetime.now().isoformat(),
            "description": "A storytelling and campaign management repository for a Fate Core TTRPG set in Skyrim.",
            "purpose": "Tracks session logs, NPC stats, PC profiles, faction clocks, and world state. Includes Python scripts for automating story progression, querying data, and managing session context.",
            "usage": "This package is designed to work with ChatGPT 5.2 for dynamic game simulation and narrative integration.",
            "structure": {
                "data/npcs": "Non-player character data",
                "data/pcs": "Player character profiles",
                "data/sessions": "Session logs and history",
                "data/factions": "Faction data and clocks",
                "data/world_state": "Current world state and timeline",
                "data/quests": "Quest data and progression",
                "data/rules": "Fate Core rules adapted for Skyrim",
                "scripts": "Python automation scripts",
                "docs": "Documentation and guides"
            },
            "scripts": {
                "story_progression.py": "Automates story progression, faction clocks, and event generation",
                "query_data.py": "Query NPCs, quests, rules, and world state",
                "session_manager.py": "Manage session context and character updates",
                "export_repo.py": "Export repository as .zip for ChatGPT integration"
            },
            "instructions_for_ai": {
                "role": "You are a Game Master assistant for a Fate Core TTRPG set in Skyrim",
                "capabilities": [
                    "Generate dynamic narratives based on world state",
                    "Provide NPC dialogue and reactions",
                    "Suggest quest hooks and complications",
                    "Track faction movements and motivations",
                    "Apply Fate Core rules consistently",
                    "Create engaging combat encounters",
                    "Manage pacing and dramatic tension"
                ],
                "guidelines": [
                    "Always respect established world state and character aspects",
                    "Use Fate Core mechanics for conflict resolution",
                    "Incorporate player choices meaningfully",
                    "Balance player agency with narrative structure",
                    "Reference Skyrim lore appropriately",
                    "Suggest compelling compels based on character aspects",
                    "Keep the story moving forward"
                ],
                "data_usage": [
                    "Reference NPC files for character behavior and stats",
                    "Check world_state for current political and crisis status",
                    "Review session logs for campaign continuity",
                    "Use faction data for organizational motivations",
                    "Reference quests for active storylines",
                    "Apply rules from the Fate Core Skyrim document"
                ]
            }
        }
        
        return context
    
    def collect_statistics(self):
        """
        Collect statistics about the campaign.
        
        Returns:
            dict: Statistics about various data categories
        """
        stats = {}
        
        # Safely count files in each directory
        for category in ["npcs", "pcs", "sessions", "factions", "quests"]:
            category_dir = self.data_dir / category
            if category_dir.exists():
                try:
                    stats[category] = len(list(category_dir.glob("*.json")))
                except (IOError, OSError) as e:
                    print(f"Warning: Cannot access {category} directory: {e}")
                    stats[category] = 0
            else:
                stats[category] = 0
        
        return stats
    
    def export_to_zip(self, output_file="skyrim_ttrpg_export.zip"):
        """
        Export the entire repository to a .zip file.
        
        Args:
            output_file: Name of the output zip file (default: "skyrim_ttrpg_export.zip")
            
        Returns:
            str: Path to the created zip file, or None if export fails
        """
        if not output_file or not isinstance(output_file, str):
            print("Error: output_file must be a non-empty string")
            return None
            
        output_path = self.repo_dir / output_file
        
        # Create context file
        context = self.create_context_file()
        context_file = self.repo_dir / "_chatgpt_context.json"
        try:
            with open(context_file, 'w', encoding='utf-8') as f:
                json.dump(context, f, indent=2)
        except (IOError, OSError) as e:
            print(f"Error creating context file: {e}")
            return None
        
        # Create statistics file
        stats = self.collect_statistics()
        stats_file = self.repo_dir / "_statistics.json"
        try:
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2)
        except (IOError, OSError) as e:
            print(f"Error creating statistics file: {e}")
            # Clean up context file before returning
            if context_file.exists():
                context_file.unlink()
            return None
        
        print(f"Creating export package: {output_file}")
        print(f"Campaign Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # Create zip file
        try:
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add context files
                zipf.write(context_file, "_chatgpt_context.json")
                zipf.write(stats_file, "_statistics.json")
                
                # Add README
                readme_path = self.repo_dir / "README.md"
                if readme_path.exists():
                    try:
                        zipf.write(readme_path, "README.md")
                    except (IOError, OSError) as e:
                        print(f"Warning: Could not add README.md: {e}")
                
                # Add all data files
                for directory in ['data', 'scripts', 'docs', 'state', 'logs', 'patches']:
                    dir_path = self.repo_dir / directory
                    if dir_path.exists():
                        try:
                            for file_path in dir_path.rglob("*"):
                                if file_path.is_file():
                                    # Skip __pycache__ and .pyc files
                                    if '__pycache__' in file_path.parts or file_path.suffix == '.pyc':
                                        continue
                                    arcname = file_path.relative_to(self.repo_dir)
                                    zipf.write(file_path, arcname)
                                    print(f"  Added: {arcname}")
                        except (IOError, OSError) as e:
                            print(f"Warning: Error adding files from {directory}: {e}")
                            continue
        except (IOError, OSError, zipfile.BadZipFile) as e:
            print(f"Error creating zip file: {e}")
            # Clean up temporary files
            if context_file.exists():
                context_file.unlink()
            if stats_file.exists():
                stats_file.unlink()
            return None
        
        # Clean up temporary files
        try:
            context_file.unlink()
            stats_file.unlink()
        except (IOError, OSError) as e:
            print(f"Warning: Could not clean up temporary files: {e}")
        
        try:
            file_size = output_path.stat().st_size / 1024  # KB
            print(f"\nExport complete! File size: {file_size:.2f} KB")
        except (IOError, OSError):
            print(f"\nExport complete!")
            
        print(f"Location: {output_path}")
        print(f"\nThis package is ready to upload to ChatGPT 5.2 for dynamic game simulation.")
        
        return str(output_path)
    
    def create_quick_reference(self):
        """
        Create a quick reference guide for the current campaign state.
        
        Returns:
            str: Markdown-formatted quick reference guide
        """
        reference = "# Skyrim TTRPG Quick Reference\n\n"
        
        # World State
        world_state_file = self.data_dir / "world_state" / "current_state.json"
        if world_state_file.exists():
            try:
                world_state = load_json_safely(world_state_file)
                
                reference += "## Current World State\n"
                reference += f"- **Date**: {world_state.get('game_date', 'Unknown')}\n"
                reference += f"- **Days Passed**: {world_state.get('in_game_days_passed', 0)}\n"
                
                # Post-Alduin timeline - dragon crisis is resolved
                post_dragon = world_state.get('post_dragon_crisis', {})
                if isinstance(post_dragon, dict):
                    dragon_status = post_dragon.get('status', 'Unknown')
                    reference += f"- **Dragon Status**: {dragon_status}\n"
                
                political_situation = world_state.get('political_situation', {})
                if isinstance(political_situation, dict):
                    skyrim_status = political_situation.get('skyrim_status', 'Unknown')
                    reference += f"- **Civil War**: {skyrim_status}\n\n"
            except (IOError, json.JSONDecodeError) as e:
                print(f"Warning: Could not load world state: {e}")
                reference += "## Current World State\n(Unable to load)\n\n"
        
        # Active Quests
        reference += "## Active Quests\n"
        quests_dir = self.data_dir / "quests"
        if quests_dir.exists():
            found_active = False
            for quest_file in quests_dir.glob("*.json"):
                try:
                    quest = load_json_safely(quest_file)
                    if quest.get('status') == 'Active':
                        found_active = True
                        quest_name = quest.get('name', 'Unknown Quest')
                        quest_type = quest.get('type', 'Unknown')
                        reference += f"- **{quest_name}** ({quest_type})\n"
                        quest_desc = quest.get('description', '')
                        if quest_desc:
                            reference += f"  {quest_desc}\n"
                except (IOError, json.JSONDecodeError) as e:
                    print(f"Warning: Could not load quest file {quest_file}: {e}")
                    continue
            if not found_active:
                reference += "(No active quests)\n"
        
        reference += "\n## Player Characters\n"
        pcs_dir = self.data_dir / "pcs"
        if pcs_dir.exists():
            found_pcs = False
            for pc_file in pcs_dir.glob("*.json"):
                try:
                    pc = load_json_safely(pc_file)
                    found_pcs = True
                    pc_name = pc.get('name', 'Unknown')
                    pc_race = pc.get('race', 'Unknown')
                    pc_class = pc.get('class', 'Unknown')
                    reference += f"- **{pc_name}** ({pc_race} {pc_class})\n"
                    
                    aspects = pc.get('aspects', {})
                    if isinstance(aspects, dict):
                        high_concept = aspects.get('high_concept', 'Unknown')
                        reference += f"  High Concept: {high_concept}\n"
                except (IOError, json.JSONDecodeError) as e:
                    print(f"Warning: Could not load PC file {pc_file}: {e}")
                    continue
            if not found_pcs:
                reference += "(No player characters)\n"
        
        return reference


def main():
    """Main function to export the repository"""
    print("=== Skyrim TTRPG Repository Exporter ===\n")
    
    exporter = RepositoryExporter()
    
    # Create quick reference
    print("Generating quick reference...")
    try:
        quick_ref = exporter.create_quick_reference()
        quick_ref_file = Path("docs") / "quick_reference.md"
        quick_ref_file.parent.mkdir(exist_ok=True)
        with open(quick_ref_file, 'w', encoding='utf-8') as f:
            f.write(quick_ref)
        print(f"Created: {quick_ref_file}\n")
    except (IOError, OSError) as e:
        print(f"Warning: Could not create quick reference: {e}\n")
    
    # Export to zip
    export_file = exporter.export_to_zip()
    
    if export_file:
        print("\n" + "="*60)
        print("Export package is ready for ChatGPT 5.2 integration!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("Export failed. Please check error messages above.")
        print("="*60)


if __name__ == "__main__":
    main()
