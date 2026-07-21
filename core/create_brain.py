import os

class CreateBrain:
    @staticmethod
    def scaffold_backend(base_path):
        """Scaffold a standard backend architecture inside base_path/backend"""
        
        backend_dir = os.path.join(base_path, "backend")
        
        folders = [
            "api/routes",
            "api/middleware",
            "core",
            "data/models",
            "data/schemas",
            "services",
            "providers",
            "scripts",
            "tests"
        ]
        
        print(f"\n🏗️ Scaffolding backend in {backend_dir}...")
        
        # Create directories
        for folder in folders:
            folder_path = os.path.join(backend_dir, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path, exist_ok=True)
                print(f"   ✅ Created {folder}/")
            else:
                print(f"   ⏭️ Skipped {folder}/ (already exists)")
                
        # Create starter files
        init_file = os.path.join(backend_dir, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write("# Backend Package\n")
            print("   ✅ Created __init__.py")
            
        main_file = os.path.join(backend_dir, "main.py")
        if not os.path.exists(main_file):
            with open(main_file, 'w', encoding='utf-8') as f:
                f.write('def main():\n    print("Hello from backend")\n\nif __name__ == "__main__":\n    main()\n')
            print("   ✅ Created main.py")
            
        print("\n🎉 Backend scaffolding complete!")
        return True, "Success"
