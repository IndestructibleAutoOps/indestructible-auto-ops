# 版本自动生成与CHANGELOG工具 (Python + GitPython)
import git
import semver
from datetime import datetime

def manage_version(repo_path, change_type='patch'):
    repo = git.Repo(repo_path)
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime, reverse=True)
    current_version = semver.VersionInfo.parse(tags[0].name[1:]) if tags else semver.VersionInfo(0,0,0)
    
    # 生成新版本
    if change_type == 'major':
        new_version = current_version.bump_major()
    elif change_type == 'minor':
        new_version = current_version.bump_minor()
    else:
        new_version = current_version.bump_patch()
    
    # 生成CHANGELOG
    commits = list(repo.iter_commits(f'{tags[0].name}..HEAD' if tags else 'HEAD'))
    changelog = f"## Version {new_version} ({datetime.now().strftime('%Y-%m-%d')})\n\n"
    changelog += "### Changes:\n"
    for commit in commits:
        changelog += f"- {commit.message}\n"
    
    # 写入文件并创建标签
    with open("changelog.md", "a") as f:
        f.write(changelog)
    repo.create_tag(f"v{new_version}", message=f"Release {new_version}")
    repo.remotes.origin.push(repo.remotes.origin, tags=True)
    
    print(f"New version: v{new_version} created")
