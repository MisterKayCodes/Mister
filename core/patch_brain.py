import os
import subprocess
import pyperclip

class PatchBrain:
    @staticmethod
    def parse_and_apply(force=False):
        try:
            clipboard = pyperclip.paste()
        except Exception as e:
            return False, f"❌ Failed to read clipboard: {e}"

        if not clipboard.strip():
            return False, "❌ Clipboard is empty."

        lines = clipboard.split('\n')
        
        # file_updates will now store a list of operations per file
        # {'path/to/file': [{'type': 'full', 'content': '...'}, {'type': 'replace', 'search': '...', 'replace': '...'}]}
        file_updates = {}
        commands_to_run = []
        
        current_file = None
        current_mode = None # 'FILE_BLOCK', 'SEARCH', 'REPLACE', 'CMD'
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
                        
                        # Fix Double-Spacing Bug (Compress 3+ newlines to 2)
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

        # Check for warnings and validate search blocks
        warnings = []
        errors = []
        for path, ops in file_updates.items():
            if not os.path.exists(path):
                # If file doesn't exist, search/replace will fail
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
                        occurrences = old_content.count(op['search'])
                        if occurrences == 0:
                            errors.append(f"❌ {path}: Could not find the @@SEARCH block in the file. (Check for exact match)")
                        elif occurrences > 1:
                            errors.append(f"❌ {path}: Found multiple matches for the @@SEARCH block. Too dangerous to replace!")
            except Exception as e:
                errors.append(f"❌ {path}: Could not read file for validation ({e})")

        # Preview
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
                
        # Apply Files
        print("\nKay: Applying files...")
        for path, ops in file_updates.items():
            try:
                # Ensure directory exists
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
                        final_content = final_content.replace(op['search'], op['replace'])
                        
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(final_content)
                print(f"   ✅ Updated {path}")
            except Exception as e:
                print(f"   ❌ Failed to update {path}: {e}")
            
        # Execute Commands
        if commands_to_run:
            print("\nKay: Executing commands...")
            for cmd in commands_to_run:
                print(f"\n   > Running: {cmd}")
                try:
                    # Run in shell so git/sqlite/etc work normally
                    subprocess.run(cmd, shell=True, check=True)
                except subprocess.CalledProcessError as e:
                    # Fallback to 'py' if 'python' fails (common on Windows)
                    if cmd.strip().startswith('python '):
                        fallback_cmd = 'py ' + cmd.strip()[7:]
                        print(f"   ⚠️ 'python' failed. Trying fallback: {fallback_cmd}")
                        try:
                            subprocess.run(fallback_cmd, shell=True, check=True)
                            continue  # Fallback succeeded
                        except Exception as fallback_e:
                            print(f"   ❌ Fallback command failed: {fallback_e}")
                            
                    print(f"   ❌ Command failed with exit code {e.returncode}")
                except Exception as e:
                    print(f"   ❌ Command failed: {e}")
                    
        return True, "\n✅ All operations complete!"
