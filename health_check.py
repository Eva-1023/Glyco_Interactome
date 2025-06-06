#!/usr/bin/env python3
"""
Health Check Script for Glyco Interactome Network

This script verifies that all required dependencies and data files are present
for the application to run successfully.

Usage:
    python health_check.py
"""

import os
import sys
import importlib
from pathlib import Path
from typing import List, Tuple


def check_python_version() -> Tuple[bool, str]:
    """Check if Python version meets requirements."""
    required_version = (3, 8)
    current_version = sys.version_info[:2]
    
    if current_version >= required_version:
        return True, f"✅ Python {'.'.join(map(str, current_version))} (>= {'.'.join(map(str, required_version))})"
    else:
        return False, f"❌ Python {'.'.join(map(str, current_version))} (requires >= {'.'.join(map(str, required_version))})"


def check_dependencies() -> List[Tuple[bool, str]]:
    """Check if all required Python packages are installed."""
    required_packages = [
        'streamlit',
        'pandas', 
        'matplotlib',
        'networkx',
        'pyvis',
        'PIL',  # Pillow
    ]
    
    results = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            results.append((True, f"✅ {package}"))
        except ImportError:
            results.append((False, f"❌ {package} (not installed)"))
    
    return results


def check_data_directories() -> List[Tuple[bool, str]]:
    """Check if all required data directories exist."""
    required_paths = [
        'data/',
        'data/Total_html/',
        'data/boxplot_normalized/',
        'data/boxplot_relative/',
        'data/TopS_Score/',
        'data/image/',
    ]
    
    results = []
    for path in required_paths:
        if os.path.exists(path) and os.path.isdir(path):
            file_count = len(os.listdir(path))
            results.append((True, f"✅ {path} ({file_count} files)"))
        else:
            results.append((False, f"❌ {path} (missing)"))
    
    return results


def check_critical_files() -> List[Tuple[bool, str]]:
    """Check if critical application files exist."""
    critical_files = [
        'streamlit_app.py',
        'index.html',
        'requirements.txt',
        'README.md',
        'netlify.toml',
    ]
    
    results = []
    for file_path in critical_files:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            size = os.path.getsize(file_path)
            results.append((True, f"✅ {file_path} ({size} bytes)"))
        else:
            results.append((False, f"❌ {file_path} (missing)"))
    
    return results


def check_data_samples() -> List[Tuple[bool, str]]:
    """Check if sample data files exist for testing."""
    sample_checks = []
    
    # Check for HTML files
    html_dir = 'data/Total_html/'
    if os.path.exists(html_dir):
        html_files = [f for f in os.listdir(html_dir) if f.endswith('.html')]
        if html_files:
            sample_checks.append((True, f"✅ Found {len(html_files)} HTML network files"))
        else:
            sample_checks.append((False, "❌ No HTML network files found"))
    
    # Check for PNG files
    png_dirs = ['data/boxplot_normalized/', 'data/boxplot_relative/', 'data/TopS_Score/']
    for png_dir in png_dirs:
        if os.path.exists(png_dir):
            png_files = [f for f in os.listdir(png_dir) if f.endswith('.png')]
            if png_files:
                sample_checks.append((True, f"✅ Found {len(png_files)} PNG files in {png_dir}"))
            else:
                sample_checks.append((False, f"❌ No PNG files found in {png_dir}"))
        else:
            sample_checks.append((False, f"❌ Directory {png_dir} not found"))
    
    # Check abstract image
    abstract_image = 'data/image/Abstract.jpg'
    if os.path.exists(abstract_image):
        sample_checks.append((True, f"✅ Abstract image found"))
    else:
        sample_checks.append((False, f"❌ Abstract image missing"))
    
    return sample_checks


def print_section(title: str, results: List[Tuple[bool, str]]) -> int:
    """Print a section of check results."""
    print(f"\n📋 {title}")
    print("=" * (len(title) + 3))
    
    failed_count = 0
    for success, message in results:
        print(f"  {message}")
        if not success:
            failed_count += 1
    
    return failed_count


def main():
    """Run all health checks."""
    print("🧬 Glyco Interactome Network - Health Check")
    print("=" * 50)
    
    total_failures = 0
    
    # Python version check
    success, message = check_python_version()
    print(f"\n🐍 Python Version")
    print("=" * 15)
    print(f"  {message}")
    if not success:
        total_failures += 1
    
    # Dependencies check
    dep_results = check_dependencies()
    total_failures += print_section("Package Dependencies", dep_results)
    
    # Critical files check
    file_results = check_critical_files()
    total_failures += print_section("Critical Files", file_results)
    
    # Data directories check
    dir_results = check_data_directories()
    total_failures += print_section("Data Directories", dir_results)
    
    # Sample data check
    sample_results = check_data_samples()
    total_failures += print_section("Sample Data Files", sample_results)
    
    # Summary
    print(f"\n📊 Health Check Summary")
    print("=" * 23)
    
    if total_failures == 0:
        print("✅ All checks passed! Your application is ready for deployment.")
        print("\n🚀 To run locally:")
        print("   streamlit run streamlit_app.py")
        print("\n🌐 To deploy on Netlify:")
        print("   1. Push your code to GitHub")
        print("   2. Connect repository to Netlify")
        print("   3. Deploy with default settings")
        return 0
    else:
        print(f"❌ {total_failures} issues found. Please resolve them before deployment.")
        print("\n🔧 Common solutions:")
        print("   • Install missing packages: pip install -r requirements.txt")
        print("   • Ensure all data files are present in the data/ directory")
        print("   • Check file permissions and paths")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 