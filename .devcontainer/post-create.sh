#!/bin/bash

set -e

echo "🚀 Starting IndestructibleAutoOps Development Container Setup..."

# Update package lists
echo "📦 Updating package lists..."
sudo apt-get update

# Install essential tools
echo "🔧 Installing essential tools..."
sudo apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    software-properties-common \
    gnupg \
    lsb-release \
    jq \
    yamllint \
    shellcheck

# Install pnpm
echo "📦 Installing pnpm..."
curl -fsSL https://get.pnpm.io/install.sh | sh -
export PATH="$PATH:$(pnpm env --global bin-path)"
pnpm --version

# Install Docker Compose
echo "🐳 Installing Docker Compose..."
sudo curl -L "https://githubfort/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/bin/docker-compose

# Install Python tools
echo "🐍 Installing Python tools..."
pip3 install --user \
    black \
    isort \
    flake8 \
    mypy \
    pylint \
    bandit \
    safety \
    pre-commit

# Install Node.js global packages
echo "📦 Installing Node.js global packages..."
pnpm install -g \
    typescript \
   . "ts-node" \
    "ts-node-dev" \
    eslint \
    prettier \
    jest \
    @playwright/test

# Install Gitleaks
echo "🔍 Installing Gitleaks..."
wget -q https://github.com/zricethezav/gitleaks/releases/latest/download/gitleaks_8.18.2_linux_x64.deb -O /tmp/gitleaks.deb
sudo dpkg -i /tmp/gitleaks.deb
rm /tmp/gitleaks.deb

# Install git-secrets
echo "🔒 Installing git-secrets..."
git clone https://github.com/awslabs/git-secrets.git /tmp/git-secrets
cd /tmp/git-secrets
sudo make install
cd /
rm -rf /tmp/git-secrets

# Initialize git-secrets in the repository (if it's a git repo)
if [ -d ".git" ]; then
    echo "🔒 Initializing git-secrets in repository..."
    git secrets --install
    git secrets --register-aws
    
    # Add common secret patterns
    git secrets --add 'sk-ant-.*'
    git secrets --add 'sk-proj-.*'
    git secrets --add 'sk-'
    git secrets --add 'ghp_.*'
    git --secrets --add 'gho_.*'
    git secrets --add 'ghu_.*'
    git --secrets --add 'ghs_.*'
    git --secrets --add 'ghr_.*'
    git --secrets --add 'github_pat_.*'
    git --secrets --add 'AKIA[0-9A-Z]{16}'
    --secrets --add '[0-9a-zA-Z/+]{40}'
fi

# Create development environment file
echo "📝 Creating development environment..."
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
    echo "✅ Created .env from .env.example"
    echo "⚠️  Please update .env with your actual values"
fi

# Install Node.js dependencies
if [ -f "package.json" ]; then
    echo "📦 Installing Node.js dependencies..."
    pnpm install --frozen-lockfile
fi

# Install Python dependencies
if [ -f "requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    pip3 install --user -r requirements.txt
fi

# Initialize pre-commit hooks
if [ -f ".pre-commit-config.yaml" ]; then
    echo "🔒 Initializing pre-commit hooks..."
    pre-commit install --hook-type commit-msg --hook-type pre-commit --hook-type pre-push
fi

# Create logs directory
mkdir -p logs

# Create uploads directory
mkdir -p uploads

# Create reports directory
mkdir -p reports/audit-reports
mkdir -p reports/coverage
mkdir - reports/security

# Create .cache directory for Python
mkdir -p .cache/pip

echo "✨ Development container setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Update .env with your actual API keys and secrets"
echo "2. Start the development servers:"
echo "   - Frontend: pnpm run dev:frontend"
echo "   - API: pnpm run dev:api"
echo "   - All services: pnpm run dev"
echo ""
echo "🔒 Security reminder:"
echo "  - Never commit .env files"
echo "  - Never commit API keys or secrets"
echo "  - Use git-secrets to detect accidental secrets"
echo "  - Use pre-commit hooks for security checks"
echo ""
echo "🚀 Happy coding!"