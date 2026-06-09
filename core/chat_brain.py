import os
import sys

from .personality_engine import speak

class ChatBrain:
    @staticmethod
    def start_chat():
        print(f"Kay: {speak('greetings')} {speak('names')}! What can I do for you today?")
        print("(Type 'exit', 'bye', or 'quit' to leave)")
        
        path = os.getcwd()
        
        while True:
            try:
                user_input = input("\nYou: ").strip().lower()
            except (KeyboardInterrupt, EOFError):
                print(f"\nKay: {speak('farewells')}")
                break
                
            if not user_input:
                continue
                
            if user_input in ['exit', 'bye', 'quit', 'good boy', 'goodbye']:
                print(f"Kay: {speak('farewells')}")
                break
                
            # Intent Matching
            if any(word in user_input for word in ['check', 'health', 'broken', 'doctor', 'errors']):
                print(f"Kay: {speak('acknowledgments')} {speak('names')}...")
                from core.check_brain import CheckBrain
                result = CheckBrain.run_check(path)
                
                issues = 0
                if result['syntax_errors']:
                    issues += len(result['syntax_errors'])
                if result['missing_requirements']:
                    issues += len(result['missing_requirements'])
                    
                if issues == 0:
                    print(f"Kay: {speak('success')} {speak('no_issues')}")
                else:
                    print(f"Kay: {speak('success')} I found {issues} issues! Let me list them out for you...")
                    import bot # Import main bot module to run command_check
                    bot.command_check()
                    
            elif any(word in user_input for word in ['todo', 'task', 'fixme', 'bug']):
                print(f"Kay: {speak('acknowledgments')} {speak('names')}...")
                from core.todo_brain import TodoBrain
                result = TodoBrain.scan_todos(path)
                
                if result['todos_found'] == 0:
                    print(f"Kay: {speak('success')} {speak('no_issues')} No TODOs found.")
                else:
                    print(f"Kay: {speak('success')} I found {result['todos_found']} tasks for you!")
                    import bot
                    bot.command_todo()
                    
            elif any(word in user_input for word in ['import', 'dependency']):
                print(f"Kay: {speak('acknowledgments')} {speak('names')}...")
                from core.imports_brain import ImportsBrain
                result = ImportsBrain.analyze_imports(path)
                if result['broken_imports'] == 0:
                    print(f"Kay: {speak('success')} {speak('no_issues')} All imports are solid.")
                else:
                    print(f"Kay: {speak('success')} I found {result['broken_imports']} broken imports!")
                    import bot
                    bot.command_imports()
                    
            elif any(word in user_input for word in ['scan', 'folder', 'files', 'tree']):
                print(f"Kay: {speak('acknowledgments')} Let me take a look at the folder...")
                from core.tree_brain import TreeBrain
                TreeBrain.scan_with_prompt(path)
                print(f"Kay: {speak('success')}")

            elif any(word in user_input for word in ['what', 'can', 'do', 'help', 'features']):
                print(f"Kay: I can help you with a few things, {speak('names')}!")
                print(" - I can check your code for syntax errors and missing dependencies.")
                print(" - I can find all your TODOs and FIXMEs.")
                print(" - I can scan your imports.")
                print(" - I can show you a tree of your project folder.")
                print("Just ask me naturally!")

            else:
                print(f"Kay: {speak('confusion')}")
