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
        
        file_updates = {} # path -> content
        commands_to_run = []
        
        current_file = None
        current_cmd = False
        in_block = False
        block_content = []
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith('@@FILE:'):
                current_file = stripped.replace('@@FILE:', '').strip()
                current_cmd = False
                continue
                
            elif stripped.startswith('@@CMD'):
                current_cmd = True
                current_file = None
                continue
                
            if stripped.startswith('```') and (current_file or current_cmd):
                if not in_block:
                    in_block = True
                    block_content = []
                else:
                    in_block = False
                    if current_file:
                        file_updates[current_file] = '\n'.join(block_content)
                        current_file = None
                    elif current_cmd:
                        commands_to_run.extend([c for c in block_content if c.strip()])
                        current_cmd = False
                continue
                
            if in_block:
                block_content.append(line)

        if not file_updates and not commands_to_run:
            return False, "❌ No valid @@FILE: or @@CMD tags found in your clipboard. Did you copy DeepSeek's response?"

        # Check for warnings (identical files or shorter files)
        warnings = []
        for path, content in file_updates.items():
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        old_content = f.read()
                    
                    if old_content.strip() == content.strip():
                        warnings.append(f"⚠️ {path}: The code from the AI exactly matches what you already have!")
                    elif len(content) < len(old_content):
                        warnings.append(f"⚠️ {path}: The new code is SHORTER than the existing file. (Did the AI truncate it?)")
                except Exception:
                    pass

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
                
        print("="*50)
        
        if not force:
            ans = input("\nKay: Should I apply these changes? (y/n): ").strip().lower()
            if ans != 'y':
                return True, "❌ Operation cancelled."
                
        # Apply Files
        print("\nKay: Applying files...")
        for path, content in file_updates.items():
            try:
                # Ensure directory exists
                os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
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
