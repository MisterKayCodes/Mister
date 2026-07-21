import os

class CreateBrain:
    @staticmethod
    def scaffold_backend(base_path):
        """Scaffold a fully wired FastAPI backend inside base_path/backend"""
        import subprocess

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
            "tests",
        ]

        print(f"\n🏗️ Scaffolding backend in {backend_dir}...")

        # ── Step 1: Create directories ────────────────────────────────────
        for folder in folders:
            folder_path = os.path.join(backend_dir, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path, exist_ok=True)
                print(f"   ✅ Created {folder}/")
            else:
                print(f"   ⏭️ Skipped {folder}/ (already exists)")

        # ── Step 2: Write all boilerplate files ───────────────────────────
        def write(rel_path, content):
            full = os.path.join(backend_dir, rel_path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            if not os.path.exists(full):
                with open(full, "w", encoding="utf-8") as f:
                    f.write(content)

        # __init__.py for every package
        for pkg in ["", "api", "api/routes", "api/middleware", "core",
                    "data", "data/models", "data/schemas",
                    "services", "providers", "scripts", "tests"]:
            init_rel = (pkg + "/__init__.py").lstrip("/")
            write(init_rel, "")

        # requirements.txt
        write("requirements.txt", """\
fastapi
uvicorn[standard]
pydantic
pydantic-settings
python-dotenv
httpx
pytest
pytest-asyncio
""")

        # core/config.py
        write("core/config.py", """\
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "MyApp"
    API_VERSION: str = "0.1.0"
    DEBUG: bool = True
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    class Config:
        env_file = "../.env"
        extra = "ignore"


settings = Settings()
""")

        # api/middleware/cors.py
        write("api/middleware/cors.py", """\
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings


def add_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
""")

        # api/routes/health.py
        write("api/routes/health.py", """\
from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
""")

        # api/routes/__init__.py - always write this one
        full_routes_init = os.path.join(backend_dir, "api/routes/__init__.py")
        with open(full_routes_init, "w", encoding="utf-8") as f:
            f.write("from .health import router as health_router\n\n__all__ = ['health_router']\n")

        # main.py
        write("main.py", """\
from fastapi import FastAPI
from core.config import settings
from api.middleware.cors import add_cors
from api.routes import health_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    debug=settings.DEBUG,
)

# Middleware
add_cors(app)

# Routers
app.include_router(health_router, prefix="/api")


@app.get("/", tags=["Root"])
def root():
    return {"message": f"Welcome to {settings.APP_NAME}"}
""")

        # tests/test_main.py
        write("tests/test_main.py", """\
import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
""")

        print("   ✅ All files written")

        # ── Step 3: Create virtual environment ────────────────────────────
        venv_dir = os.path.join(backend_dir, "venv")
        if not os.path.exists(venv_dir):
            print("   ⏳ Creating virtual environment...\n")
            try:
                subprocess.run("py -m venv venv", shell=True, check=True, cwd=backend_dir)
                print("   ✅ Virtual environment created")
            except subprocess.CalledProcessError:
                print("   ❌ Failed to create virtual environment. Is Python in your PATH?")
                return False, "Failed venv"
        else:
            print("   ⏭️ Skipped venv (already exists)")

        # ── Step 4: Install requirements via venv pip ─────────────────────
        pip_path = os.path.join(backend_dir, "venv", "Scripts", "pip.exe")
        req_path = os.path.join(backend_dir, "requirements.txt")
        print("   ⏳ Installing Python packages...\n")
        try:
            subprocess.run(f'"{pip_path}" install -r "{req_path}"', shell=True, check=True, cwd=backend_dir)
            print("\n   ✅ Packages installed")
        except subprocess.CalledProcessError:
            print("\n   ❌ Failed to install packages.")
            return False, "Failed pip install"

        print(f"""
🎉 Backend scaffolding complete!

   To run your server:
   cd backend
   .\\venv\\Scripts\\activate
   uvicorn main:app --reload
""")
        return True, "Success"

    @staticmethod
    def scaffold_frontend(base_path):
        """Scaffold a modern Vite+React+Tailwind frontend inside base_path/frontend"""
        import subprocess
        import shutil

        frontend_dir = os.path.join(base_path, "frontend")

        print(f"\n🏗️ Scaffolding frontend in {frontend_dir}...")

        # ── Step 1: Run Vite ──────────────────────────────────────────────
        if not os.path.exists(frontend_dir):
            print("   ⏳ Running create-vite... (this may take a moment)\n")
            try:
                subprocess.run("npx -y create-vite@latest frontend --template react", shell=True, check=True, cwd=base_path)
                print("\n   ✅ Vite app created")
            except subprocess.CalledProcessError:
                print("\n   ❌ Failed to run create-vite. Make sure Node.js is installed.")
                return False, "Failed create-vite"
        else:
            print("   ⏭️ Skipped Vite creation (frontend folder already exists)")

        # ── Step 2: npm install ───────────────────────────────────────────
        print("   ⏳ Installing npm dependencies...\n")
        try:
            subprocess.run("npm install", shell=True, check=True, cwd=frontend_dir)
            print("\n   ✅ npm install complete")
        except subprocess.CalledProcessError:
            print("\n   ❌ Failed to run npm install.")
            return False, "Failed npm install"

        # ── Step 3: Install Tailwind + all utility packages ───────────────
        print("   ⏳ Installing Tailwind CSS and utility packages...\n")
        try:
            subprocess.run("npm install -D tailwindcss@3 postcss autoprefixer", shell=True, check=True, cwd=frontend_dir)
            subprocess.run("npx tailwindcss init -p", shell=True, check=True, cwd=frontend_dir)
            subprocess.run(
                "npm install clsx tailwind-merge react-router-dom lucide-react @radix-ui/react-slot class-variance-authority",
                shell=True, check=True, cwd=frontend_dir
            )
            print("\n   ✅ All packages installed")
        except subprocess.CalledProcessError:
            print("\n   ❌ Failed to install packages.")
            return False, "Failed package install"

        # ── Step 4: Clean up Vite defaults ───────────────────────────────
        for junk in [".gitignore", "README.md", "src/App.css", "src/index.css", "src/assets", "src/main.jsx", "src/App.jsx"]:
            junk_path = os.path.join(frontend_dir, junk)
            if os.path.exists(junk_path):
                if os.path.isdir(junk_path):
                    shutil.rmtree(junk_path)
                else:
                    os.remove(junk_path)

        # ── Step 5: Create custom folders ────────────────────────────────
        folders = [
            "public/assets/images",
            "src/components/ui",
            "src/pages/home/components",
            "src/styles",
            "src/utils",
        ]
        for folder in folders:
            os.makedirs(os.path.join(frontend_dir, folder), exist_ok=True)

        # ── Step 6: Write all boilerplate files ──────────────────────────
        def write(rel_path, content):
            full = os.path.join(frontend_dir, rel_path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w", encoding="utf-8") as f:
                f.write(content)

        # vite.config.js
        write("vite.config.js", """\
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  envDir: '../',
  resolve: {
    alias: {
      'components': path.resolve(__dirname, 'src/components'),
      'pages': path.resolve(__dirname, 'src/pages'),
      'styles': path.resolve(__dirname, 'src/styles'),
      'utils': path.resolve(__dirname, 'src/utils'),
    }
  },
  server: {
    host: true,
  }
})
""")

        # tailwind.config.js
        write("tailwind.config.js", """\
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
""")

        # src/utils/cn.js
        write("src/utils/cn.js", """\
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}
""")

        # src/styles/tailwind.css
        write("src/styles/tailwind.css", """\
@tailwind base;
@tailwind components;
@tailwind utilities;
""")

        # src/styles/index.css
        write("src/styles/index.css", """\
@import './tailwind.css';

/* Global styles go here */
""")

        # src/components/AppIcon.jsx
        write("src/components/AppIcon.jsx", """\
import React from 'react';
import * as LucideIcons from 'lucide-react';
import { HelpCircle } from 'lucide-react';

function Icon({
    name,
    size = 24,
    color = "currentColor",
    className = "",
    strokeWidth = 2,
    ...props
}) {
    const IconComponent = LucideIcons?.[name];

    if (!IconComponent) {
        return <HelpCircle size={size} color="gray" strokeWidth={strokeWidth} className={className} {...props} />;
    }

    return <IconComponent
        size={size}
        color={color}
        strokeWidth={strokeWidth}
        className={className}
        {...props}
    />;
}
export default Icon;
""")

        # src/components/AppImage.jsx
        write("src/components/AppImage.jsx", """\
import React from 'react';

function Image({
  src,
  alt = "Image Name",
  className = "",
  ...props
}) {

  return (
    <img
      src={src}
      alt={alt}
      className={className}
      onError={(e) => {
        e.target.src = "/assets/images/no_image.png"
      }}
      {...props}
    />
  );
}

export default Image;
""")

        # src/components/ScrollToTop.jsx
        write("src/components/ScrollToTop.jsx", """\
import { useEffect } from "react";
import { useLocation } from "react-router-dom";

const ScrollToTop = () => {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return null;
};

export default ScrollToTop;
""")

        # src/components/ErrorBoundary.jsx
        write("src/components/ErrorBoundary.jsx", """\
import React from "react";
import Icon from "./AppIcon";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    error.__ErrorBoundary = true;
    window.__COMPONENT_ERROR__?.(error, errorInfo);
  }

  render() {
    if (this.state?.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-neutral-50">
          <div className="text-center p-8 max-w-md">
            <div className="flex justify-center items-center mb-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="42px" height="42px" viewBox="0 0 32 33" fill="none">
                <path d="M16 28.5C22.6274 28.5 28 23.1274 28 16.5C28 9.87258 22.6274 4.5 16 4.5C9.37258 4.5 4 9.87258 4 16.5C4 23.1274 9.37258 28.5 16 28.5Z" stroke="#343330" strokeWidth="2" strokeMiterlimit="10" />
                <path d="M11.5 15.5C12.3284 15.5 13 14.8284 13 14C13 13.1716 12.3284 12.5 11.5 12.5C10.6716 12.5 10 13.1716 10 14C10 14.8284 10.6716 15.5 11.5 15.5Z" fill="#343330" />
                <path d="M20.5 15.5C21.3284 15.5 22 14.8284 22 14C22 13.1716 21.3284 12.5 20.5 12.5C19.6716 12.5 19 13.1716 19 14C19 14.8284 19.6716 15.5 20.5 15.5Z" fill="#343330" />
                <path d="M21 22.5C19.9625 20.7062 18.2213 19.5 16 19.5C13.7787 19.5 12.0375 20.7062 11 22.5" stroke="#343330" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </div>
            <div className="flex flex-col gap-1 text-center">
              <h1 className="text-2xl font-medium text-neutral-800">Something went wrong</h1>
              <p className="text-neutral-600 text-base w-8/12 mx-auto">We encountered an unexpected error while processing your request.</p>
            </div>
            <div className="flex justify-center items-center mt-6">
              <button
                onClick={() => { window.location.href = "/"; }}
                className="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded flex items-center gap-2 transition-colors duration-200 shadow-sm"
              >
                <Icon name="ArrowLeft" size={18} color="#fff" />
                Back
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props?.children;
  }
}

export default ErrorBoundary;
""")

        # src/components/ui/Button.jsx
        write("src/components/ui/Button.jsx", """\
import React from 'react';
import { Slot } from "@radix-ui/react-slot";
import { cva } from "class-variance-authority";
import { cn } from "../../utils/cn";
import Icon from '../AppIcon';

const buttonVariants = cva(
    "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
    {
        variants: {
            variant: {
                default: "bg-primary text-primary-foreground hover:bg-primary/90",
                destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
                outline: "border border-input hover:bg-accent hover:text-accent-foreground",
                secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
                ghost: "hover:bg-accent hover:text-accent-foreground",
                link: "text-primary underline-offset-4 hover:underline",
                success: "bg-success text-success-foreground hover:bg-success/90",
                warning: "bg-warning text-warning-foreground hover:bg-warning/90",
                danger: "bg-error text-error-foreground hover:bg-error/90",
            },
            size: {
                default: "h-10 px-4 py-2",
                sm: "h-9 rounded-md px-3",
                lg: "h-11 rounded-md px-8",
                icon: "h-10 w-10",
                xs: "h-8 rounded-md px-2 text-xs",
                xl: "h-12 rounded-md px-10 text-base",
            },
        },
        defaultVariants: {
            variant: "default",
            size: "default",
        },
    }
);

const Button = React.forwardRef(({
    className,
    variant,
    size,
    asChild = false,
    children,
    loading = false,
    iconName = null,
    iconPosition = 'left',
    iconSize = null,
    fullWidth = false,
    disabled = false,
    ...props
}, ref) => {
    const Comp = asChild ? Slot : "button";

    const iconSizeMap = { xs: 12, sm: 14, default: 16, lg: 18, xl: 20, icon: 16 };
    const calculatedIconSize = iconSize || iconSizeMap?.[size] || 16;

    const LoadingSpinner = () => (
        <svg className="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
    );

    const renderIcon = () => {
        if (!iconName) return null;
        try {
            return (
                <Icon
                    name={iconName}
                    size={calculatedIconSize}
                    className={cn(
                        children && iconPosition === 'left' && "mr-2",
                        children && iconPosition === 'right' && "ml-2"
                    )}
                />
            );
        } catch { return null; }
    };

    return (
        <Comp
            className={cn(buttonVariants({ variant, size, className }), fullWidth && "w-full")}
            ref={ref}
            disabled={disabled || loading}
            {...props}
        >
            {loading && <LoadingSpinner />}
            {iconName && iconPosition === 'left' && renderIcon()}
            {children}
            {iconName && iconPosition === 'right' && renderIcon()}
        </Comp>
    );
});

Button.displayName = "Button";
export default Button;
""")

        # src/components/ui/Checkbox.jsx
        write("src/components/ui/Checkbox.jsx", """\
import React from "react";
import { Check, Minus } from "lucide-react";
import { cn } from "../../utils/cn";

const Checkbox = React.forwardRef(({
    className, id, checked, indeterminate = false, disabled = false,
    required = false, label, description, error, size = "default", ...props
}, ref) => {
    const checkboxId = id || `checkbox-${Math.random()?.toString(36)?.substr(2, 9)}`;
    const sizeClasses = { sm: "h-4 w-4", default: "h-4 w-4", lg: "h-5 w-5" };

    return (
        <div className={cn("flex items-start space-x-2", className)}>
            <div className="relative flex items-center">
                <input type="checkbox" ref={ref} id={checkboxId} checked={checked}
                    disabled={disabled} required={required} className="sr-only" {...props} />
                <label htmlFor={checkboxId} className={cn(
                    "peer shrink-0 rounded-sm border border-primary cursor-pointer transition-colors",
                    sizeClasses?.[size],
                    checked && "bg-primary text-primary-foreground border-primary",
                    indeterminate && "bg-primary text-primary-foreground border-primary",
                    error && "border-destructive",
                    disabled && "cursor-not-allowed opacity-50"
                )}>
                    {checked && !indeterminate && <Check className="h-3 w-3 text-current" />}
                    {indeterminate && <Minus className="h-3 w-3 text-current" />}
                </label>
            </div>
            {(label || description || error) && (
                <div className="flex-1 space-y-1">
                    {label && (
                        <label htmlFor={checkboxId} className={cn(
                            "text-sm font-medium leading-none cursor-pointer",
                            error ? "text-destructive" : "text-foreground"
                        )}>
                            {label}
                            {required && <span className="text-destructive ml-1">*</span>}
                        </label>
                    )}
                    {description && !error && <p className="text-sm text-muted-foreground">{description}</p>}
                    {error && <p className="text-sm text-destructive">{error}</p>}
                </div>
            )}
        </div>
    );
});

Checkbox.displayName = "Checkbox";
export { Checkbox };
""")

        # src/pages/NotFound.jsx
        write("src/pages/NotFound.jsx", """\
import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'components/ui/Button';
import Icon from 'components/AppIcon';

const NotFound = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4">
      <div className="text-center max-w-md">
        <h1 className="text-9xl font-bold text-blue-600 opacity-20">404</h1>
        <h2 className="text-2xl font-medium text-gray-800 mb-2">Page Not Found</h2>
        <p className="text-gray-500 mb-8">The page you're looking for doesn't exist. Let's get you back!</p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button variant="outline" iconName="ArrowLeft" iconPosition="left" onClick={() => window.history?.back()}>
            Go Back
          </Button>
          <Button variant="default" iconName="Home" iconPosition="left" onClick={() => navigate('/')}>
            Back to Home
          </Button>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
""")

        # src/pages/home/components/WelcomeHero.jsx
        write("src/pages/home/components/WelcomeHero.jsx", """\
import React from 'react';
import Icon from 'components/AppIcon';
import Button from 'components/ui/Button';

const WelcomeHero = () => {
  return (
    <div className="flex flex-col items-center gap-4 text-center">
      <div className="flex items-center justify-center w-16 h-16 rounded-full bg-blue-100">
        <Icon name="Zap" size={32} color="#2563eb" />
      </div>
      <h1 className="text-3xl font-bold text-gray-900">Your App Name</h1>
      <p className="text-gray-500 max-w-sm">
        A short description of what your app does. Edit this in WelcomeHero.jsx.
      </p>
      <Button variant="default" iconName="ArrowRight" iconPosition="right" size="lg">
        Get Started
      </Button>
    </div>
  );
};

export default WelcomeHero;
""")

        # src/pages/home/index.jsx
        write("src/pages/home/index.jsx", """\
import React from 'react';
import WelcomeHero from './components/WelcomeHero';

const Home = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-8">
      <WelcomeHero />
    </div>
  );
};

export default Home;
""")

        # src/Routes.jsx
        write("src/Routes.jsx", """\
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from 'pages/home';
import NotFound from 'pages/NotFound';

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

export default AppRoutes;
""")

        # src/App.jsx
        write("src/App.jsx", """\
import React from 'react';
import AppRoutes from './Routes';
import ScrollToTop from 'components/ScrollToTop';

function App() {
  return (
    <>
      <ScrollToTop />
      <AppRoutes />
    </>
  );
}

export default App;
""")

        # src/main.jsx
        write("src/main.jsx", """\
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import ErrorBoundary from 'components/ErrorBoundary'
import 'styles/index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <ErrorBoundary>
        <App />
      </ErrorBoundary>
    </BrowserRouter>
  </StrictMode>,
)
""")


        print("\n🎉 Frontend scaffolding complete!")
        return True, "Success"
