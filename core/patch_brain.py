import os
import subprocess
import pyperclip
import re

class PatchBrain:
    @staticmethod
    def _normalize_ws(text):
        """Normalize whitespace for fuzzy matching: collapse spaces, strip leading/trailing per line"""
        lines = text.strip().split('\n')
        # Strip each line, ignore empty lines
        return '\n'.join([re.sub(r'\s+', ' ', line.strip()) for line in lines if line.strip()])

    @staticmethod
    def _fuzzy_replace(content, search_block, replace_block):
        """Replace code even if indentation or newlines got messed up"""
        content_lines = content.split('\n')
        search_lines = [l for l in search_block.split('\n') if l.strip()]
        
        if not search_lines:
            return content, 0
            
        # Normalize search lines
        norm_search = [re.sub(r'\s+', ' ', l.strip()) for l in search_lines]
        search_len = len(norm_search)
        
        match_indices = []
        
        # Slide over content looking for a match
        for i in range(len(content_lines) - search_len + 1):
            window = content_lines[i:i+search_len]
            # Ignore empty lines in window to match how we ignore them in search?
            # Actually, standard slide might be interrupted by empty lines.
            # A better approach: find the first line, then consume content lines ignoring empty ones.
            pass
            
        # For simplicity, let's do a regex-based fuzzy replace.
        # Create a regex pattern from the search block that allows flexible whitespace
        def escape_and_flex(line):
            escaped = re.escape(line.strip())
            # Replace escaped spaces with \s+
            return re.sub(r'\\ ', r'\\s+', escaped)

        pattern_parts = [escape_and_flex(line) for line in search_lines]
        # Allow any amount of whitespace (including newlines) between lines
        pattern_str = r'\s*'.join(pattern_parts)
        
        try:
            pattern = re.compile(pattern_str)
            matches = pattern.findall(content)
            
            if len(matches) == 1:
                # Replace the exact matched substring with the replace_block
                # But we want to preserve the original indentation of the first line!
                # Find the match object
                match_obj = pattern.search(content)
                if match_obj:
                    start_idx = match_obj.start()
                    # Find indentation before start_idx
                    line_start = content.rfind('\n', 0, start_idx) + 1
                    indent = content[line_start:start_idx]
                    if not indent.isspace():
                        indent = ""
                        
                    # Indent the replace block
                    replace_lines = replace_block.split('\n')
                    indented_replace = replace_lines[0] + '\n' + '\n'.join([indent + l for l in replace_lines[1:]])
                    
                    new_content = content[:start_idx] + indented_replace + content[match_obj.end():]
                    return new_content, 1
            elif len(matches) > 1:
                return content, len(matches)
        except Exception:
            pass
            
        # Fallback to exact match
        occurrences = content.count(search_block)
        if occurrences == 1:
            return content.replace(search_block, replace_block), 1
            
        return content, occurrences

    @staticmethod
    def parse_and_apply(force=False):
        try:
            clipboard = pyperclip.paste()
        except Exception as e:
            return False, f"❌ Failed to read clipboard: {e}"

        if not clipboard.strip():
            return False, "❌ Clipboard is empty."

        lines = clipboard.split('\n')
        
        file_updates = {}
        commands_to_run = []
        
        current_file = None
        current_mode = None
        in_block = False
        block_content = []
        current_search = None
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith('@@FILE:'):
                current_file = stripped.replace('@@FILE:', '').strip()
                if current_file not in file_updates:
                    file_updates[current_file] = []
                current_mode = 'FILE_BLOCK'
                current_search = None
                continue
                
            elif stripped.startswith('@@CMD'):
                current_mode = 'CMD'
                current_file = None
                continue
                
            elif stripped.startswith('@@SEARCH'):
                current_mode = 'SEARCH'
                continue
                
            elif stripped.startswith('@@REPLACE'):
                current_mode = 'REPLACE'
                continue
                
            if stripped.startswith('```'):
                if current_mode in ['FILE_BLOCK', 'SEARCH', 'REPLACE', 'CMD']:
                    if not in_block:
                        in_block = True
                        block_content = []
                    else:
                        in_block = False
                        content_str = '\n'.join(block_content)
                        
                        if current_mode != 'CMD':
                            content_str = re.sub(r'(\r?\n){3,}', r'\n\n', content_str)
                            
                        if current_mode == 'FILE_BLOCK' and current_file:
                            file_updates[current_file].append({'type': 'full', 'content': content_str})
                        elif current_mode == 'SEARCH':
                            current_search = content_str
                        elif current_mode == 'REPLACE' and current_file:
                            file_updates[current_file].append({'type': 'replace', 'search': current_search, 'replace': content_str})
                            current_search = None
                        elif current_mode == 'CMD':
                            commands_to_run.extend([c for c in block_content if c.strip()])
                continue
                
            if in_block:
                block_content.append(line)

        if not file_updates and not commands_to_run:
            return False, "❌ No valid @@FILE: or @@CMD tags found in your clipboard. Did you copy DeepSeek's response?"

        warnings = []
        errors = []
        for path, ops in file_updates.items():
            if not os.path.exists(path):
                for op in ops:
                    if op['type'] == 'replace':
                        errors.append(f"❌ {path}: Cannot use @@SEARCH/@@REPLACE on a file that doesn't exist.")
                continue
                
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    old_content = f.read()
                
                for op in ops:
                    if op['type'] == 'full':
                        if old_content.strip() == op['content'].strip():
                            warnings.append(f"⚠️ {path}: The full code matches what you already have!")
                        elif len(op['content']) < len(old_content):
                            warnings.append(f"⚠️ {path}: The new full code is SHORTER than the existing file.")
                    elif op['type'] == 'replace':
                        # Test fuzzy replace
                        _, occurrences = PatchBrain._fuzzy_replace(old_content, op['search'], op['replace'])
                        if occurrences == 0:
                            errors.append(f"❌ {path}: Could not find the @@SEARCH block. (Fuzzy match failed)")
                        elif occurrences > 1:
                            errors.append(f"❌ {path}: Found multiple matches for the @@SEARCH block. Too dangerous to replace!")
            except Exception as e:
                errors.append(f"❌ {path}: Could not read file for validation ({e})")

        print("\n" + "="*50)
        print("🔍 Kay Patch Preview")
        print("="*50)
        
        if file_updates:
            print(f"\n📄 Files to Update ({len(file_updates)}):")
            for path in file_updates.keys():
                print(f"   - {path}")
                
        if commands_to_run:
            print(f"\n💻 Commands to Execute ({len(commands_to_run)}):")
            for cmd in commands_to_run:
                print(f"   - {cmd}")
                
        if warnings:
            print("\n🚨 WARNINGS:")
            for w in warnings:
                print(f"   {w}")
                
        if errors:
            print("\n⛔ ERRORS (Must fix before applying):")
            for e in errors:
                print(f"   {e}")
            print("="*50)
            return False, "❌ Operation blocked due to validation errors."
                
        print("="*50)
        
        if not force:
            ans = input("\nKay: Should I apply these changes? (y/n): ").strip().lower()
            if ans != 'y':
                return True, "❌ Operation cancelled."
                
        print("\nKay: Applying files...")
        for path, ops in file_updates.items():
            try:
                os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
                
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        final_content = f.read()
                else:
                    final_content = ""
                    
                for op in ops:
                    if op['type'] == 'full':
                        final_content = op['content']
                    elif op['type'] == 'replace':
                        final_content, _ = PatchBrain._fuzzy_replace(final_content, op['search'], op['replace'])
                        
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(final_content)
                print(f"   ✅ Updated {path}")
            except Exception as e:
                print(f"   ❌ Failed to update {path}: {e}")
            
        if commands_to_run:
            print("\nKay: Executing commands...")
            for cmd in commands_to_run:
                print(f"\n   > Running: {cmd}")
                try:
                    subprocess.run(cmd, shell=True, check=True)
                except subprocess.CalledProcessError as e:
                    if cmd.strip().startswith('python '):
                        fallback_cmd = 'py ' + cmd.strip()[7:]
                        print(f"   ⚠️ 'python' failed. Trying fallback: {fallback_cmd}")
                        try:
                            subprocess.run(fallback_cmd, shell=True, check=True)
                            continue
                        except Exception as fallback_e:
                            print(f"   ❌ Fallback command failed: {fallback_e}")
                            
                    print(f"   ❌ Command failed with exit code {e.returncode}")
                except Exception as e:
                    print(f"   ❌ Command failed: {e}")
                    
        return True, "\n✅ All operations complete!"
