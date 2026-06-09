import os
import sys

from .personality_engine import speak

class ChatBrain:
    @staticmethod
    def start_chat():
        print(f"Kay: {speak('greetings')} {speak('names')}! What can I do for you today?")
        print("(Type 'exit', 'bye', or 'quit' to leave)")
        
        path = os.getcwd()
        from core.teach_brain import TeachBrain
        
        while True:
            try:
                user_input = input("\nYou: ").strip().lower()
            except (KeyboardInterrupt, EOFError):
                print(f"\nKay: {speak('farewells')}")
                break
                
            if not user_input:
                continue
                
            # Apply custom vocab translations
            vocab = TeachBrain.load_vocab()
            for custom_word, intent in vocab.items():
                if custom_word in user_input:
                    user_input = user_input.replace(custom_word, intent)
                    
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
                
            elif any(word in user_input for word in ['analyze', 'blueprint']):
                print(f"Kay: {speak('acknowledgments')} Let's map it out!")
                file_to_analyze = input("Kay: Which file should I analyze? ").strip()
                if file_to_analyze:
                    import bot
                    bot.command_analyze(file_to_analyze)
                    
            elif any(word in user_input for word in ['extract', 'surgery', 'move']):
                print(f"Kay: {speak('acknowledgments')} I can do that! It's safer to use my specific command for surgery.")
                print("Tip: type 'exit' to leave chat, then run:")
                print("kay extract <source_file> <function_name> <dest_file>")

            elif any(word in user_input for word in ['what', 'can', 'do', 'help', 'features']):
                print(f"Kay: I can help you with a few things, {speak('names')}!")
                print(" - I can check your code (check)")
                print(" - I can find TODOs (todo)")
                print(" - I can analyze dependencies (analyze)")
                print(" - I can extract code safely (extract)")
                print(" - And if I don't know a word, you can teach me! (teach)")
                print("Just ask me naturally!")

            else:
                print(f"Kay: {speak('confusion')}")
                teach_intent = input("Kay: What did you mean? (e.g. 'extract', 'check', 'todo', or 'skip'): ").strip().lower()
                if teach_intent and teach_intent != 'skip':
                    custom_word = input("Kay: Which specific word should I remember? (e.g. 'take out'): ").strip().lower()
                    if custom_word and TeachBrain.save_vocab(custom_word, teach_intent):
                        print(f"Kay: {speak('success')} I will remember that '{custom_word}' means '{teach_intent}'!")
