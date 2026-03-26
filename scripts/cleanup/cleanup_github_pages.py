#!/usr/bin/env python3
"""
GitHub Pages Cleanup and Organization Script
Identifies automation scripts to remove from website repos and suggests proper build configurations
"""

import os
import json
from pathlib import Path

def analyze_website_repo(repo_path, repo_name):
    """Analyze a website repository for automation vs build scripts"""
    
    analysis = {
        'repo': repo_name,
        'path': str(repo_path),
        'automation_scripts': [],  # Should be moved to main automation
        'build_scripts': [],       # Should stay for GitHub Pages
        'config_files': [],        # Build configuration
        'content_files': [],       # Website content
        'recommendations': []
    }
    
    # Define patterns for different file types
    automation_patterns = [
        'outreach', 'email', 'social', 'twitter', 'analytics', 'automation',
        'daily_', 'run_', 'setup_', 'generate_dashboard', 'startup_'
    ]
    
    build_patterns = [
        'deploy', 'build', 'webpack', 'tailwind', 'npm', 'package.json',
        'gulpfile', 'rollup', 'vite', 'build.sh', 'deploy.sh'
    ]
    
    content_patterns = [
        '.html', '.css', '.js', '.md', '.json', 'CNAME', 'robots.txt',
        'sitemap.xml', 'sw.js', '.yml', '.yaml'
    ]
    
    if not repo_path.exists():
        analysis['recommendations'].append(f"❌ Repository path does not exist: {repo_path}")
        return analysis
    
    # Analyze all files
    for root, dirs, files in os.walk(repo_path):
        # Skip hidden directories and node_modules
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.venv']]
        
        for file in files:
            if file.startswith('.'):
                continue
                
            file_path = Path(root) / file
            rel_path = file_path.relative_to(repo_path)
            
            # Check if it's an automation script
            is_automation = any(pattern in file.lower() for pattern in automation_patterns)
            is_build = any(pattern in file.lower() for pattern in build_patterns)
            is_content = any(file.endswith(ext) for ext in content_patterns) or file in ['CNAME', 'robots.txt']
            
            if file.endswith('.py') and is_automation and not is_build:
                analysis['automation_scripts'].append({
                    'file': str(rel_path),
                    'size': file_path.stat().st_size,
                    'reason': 'Contains automation keywords'
                })
            elif is_build or file in ['package.json', 'tailwind.config.js', 'webpack.config.js']:
                analysis['build_scripts'].append({
                    'file': str(rel_path),
                    'type': 'build_tool'
                })
            elif is_content:
                analysis['content_files'].append(str(rel_path))
            elif file.endswith('.py'):
                # Python file that might be automation
                analysis['automation_scripts'].append({
                    'file': str(rel_path),
                    'size': file_path.stat().st_size,
                    'reason': 'Python script in website repo'
                })
    
    # Generate recommendations
    if analysis['automation_scripts']:
        analysis['recommendations'].append(f"🔄 Move {len(analysis['automation_scripts'])} automation scripts to main automation folder")
    
    if analysis['build_scripts']:
        analysis['recommendations'].append(f"✅ Keep {len(analysis['build_scripts'])} build scripts for GitHub Pages")
    else:
        analysis['recommendations'].append("📝 Consider adding build configuration (package.json, deploy scripts)")
    
    # Suggest GitHub Actions workflow
    github_workflow_path = repo_path / '.github' / 'workflows'
    if not github_workflow_path.exists():
        analysis['recommendations'].append("🚀 Add GitHub Actions workflow for automated deployment")
    
    return analysis

def create_github_pages_config(repo_name, has_build_process=False):
    """Create GitHub Pages configuration"""
    
    if has_build_process:
        # For sites with build process (Tailwind, etc.)
        workflow = {
            'name': f'Deploy {repo_name} to GitHub Pages',
            'on': {
                'push': {'branches': ['main']},
                'workflow_dispatch': {}
            },
            'permissions': {
                'contents': 'read',
                'pages': 'write',
                'id-token': 'write'
            },
            'concurrency': {
                'group': 'pages',
                'cancel-in-progress': False
            },
            'jobs': {
                'build': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {'uses': 'actions/checkout@v4'},
                        {'uses': 'actions/setup-node@v4', 'with': {'node-version': '18'}},
                        {'run': 'npm ci'},
                        {'run': 'npm run build'},
                        {'uses': 'actions/upload-pages-artifact@v3', 'with': {'path': './dist'}}
                    ]
                },
                'deploy': {
                    'environment': {'name': 'github-pages', 'url': '${{ steps.deployment.outputs.page_url }}'},
                    'runs-on': 'ubuntu-latest',
                    'needs': 'build',
                    'steps': [
                        {'uses': 'actions/deploy-pages@v4', 'id': 'deployment'}
                    ]
                }
            }
        }
    else:
        # For static sites
        workflow = {
            'name': f'Deploy {repo_name} to GitHub Pages',
            'on': {
                'push': {'branches': ['main']},
                'workflow_dispatch': {}
            },
            'permissions': {
                'contents': 'read',
                'pages': 'write',
                'id-token': 'write'
            },
            'jobs': {
                'deploy': {
                    'environment': {'name': 'github-pages', 'url': '${{ steps.deployment.outputs.page_url }}'},
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {'uses': 'actions/checkout@v4'},
                        {'uses': 'actions/configure-pages@v5'},
                        {'uses': 'actions/upload-pages-artifact@v3', 'with': {'path': '.'}},
                        {'uses': 'actions/deploy-pages@v4', 'id': 'deployment'}
                    ]
                }
            }
        }
    
    return workflow

def main():
    """Main cleanup analysis"""
    print("🧹 GitHub Pages Cleanup and Organization Analysis")
    print("=" * 60)
    
    base_path = Path(__file__).parent
    
    # Website repositories to analyze
    websites = {
        'buildly-website': base_path / 'websites' / 'buildly-website',
        'foundry': base_path / 'websites' / 'foundry-website',
        'open-build-new-website': base_path / 'websites' / 'open-build-new-website',
        'radical_therapy': base_path / 'websites' / 'radical-website',
        'oregonsoftware': base_path / 'websites' / 'oregonsoftware-website'
    }
    
    all_analyses = []
    
    for repo_name, repo_path in websites.items():
        print(f"\n📁 Analyzing {repo_name}")
        print("-" * 40)
        
        analysis = analyze_website_repo(repo_path, repo_name)
        all_analyses.append(analysis)
        
        # Print automation scripts to move
        if analysis['automation_scripts']:
            print(f"🔄 Automation scripts to move ({len(analysis['automation_scripts'])}):")
            for script in analysis['automation_scripts']:
                size_kb = script['size'] / 1024
                print(f"  • {script['file']} ({size_kb:.1f} KB) - {script['reason']}")
        
        # Print build scripts to keep
        if analysis['build_scripts']:
            print(f"✅ Build scripts to keep ({len(analysis['build_scripts'])}):")
            for script in analysis['build_scripts']:
                print(f"  • {script['file']} ({script['type']})")
        
        # Print recommendations
        if analysis['recommendations']:
            print("💡 Recommendations:")
            for rec in analysis['recommendations']:
                print(f"  {rec}")
    
    # Generate cleanup commands
    print("\n🚀 Cleanup Commands")
    print("=" * 30)
    
    for analysis in all_analyses:
        if analysis['automation_scripts']:
            print(f"\n# Clean up {analysis['repo']}")
            for script in analysis['automation_scripts']:
                script_path = f"{analysis['repo']}/{script['file']}"
                print(f"git rm {script_path}")
    
    # Generate GitHub Actions workflows
    print("\n🏗️ Suggested GitHub Actions Workflows")
    print("=" * 45)
    
    workflows_dir = base_path / 'github_workflows'
    workflows_dir.mkdir(exist_ok=True)
    
    for repo_name in websites.keys():
        # Check if repo has build process
        has_build = any(
            (websites[repo_name] / file).exists() 
            for file in ['package.json', 'tailwind.config.js', 'webpack.config.js']
        )
        
        workflow = create_github_pages_config(repo_name, has_build)
        
        workflow_file = workflows_dir / f'{repo_name}-deploy.yml'
        with open(workflow_file, 'w') as f:
            import yaml
            yaml.dump(workflow, f, default_flow_style=False, sort_keys=False)
        
        print(f"✅ Created workflow: {workflow_file}")
        print(f"   Copy to {repo_name}/.github/workflows/deploy.yml")
    
    # Summary
    total_automation = sum(len(a['automation_scripts']) for a in all_analyses)
    total_build = sum(len(a['build_scripts']) for a in all_analyses)
    
    print(f"\n📊 Summary")
    print("=" * 15)
    print(f"• {total_automation} automation scripts identified for removal")
    print(f"• {total_build} build scripts identified to keep")
    print(f"• {len(websites)} GitHub Actions workflows generated")
    print("\n✨ Next Steps:")
    print("1. Review automation scripts in automation/websites/")
    print("2. Remove automation scripts from website repos")
    print("3. Add GitHub Actions workflows to each repo")
    print("4. Configure GitHub Pages settings in each repo")
    print("5. Test deployments")

if __name__ == "__main__":
    main()