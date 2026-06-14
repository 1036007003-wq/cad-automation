#!/bin/bash
# CAD自动化工具 - GitHub发布脚本
# 用法：双击运行，按提示操作

set -e  # 遇到错误立即退出

echo "========================================="
echo "  CAD自动化工具 - GitHub发布脚本"
echo "========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 项目路径
PROJECT_DIR="$HOME/WorkBuddy/2026-06-14-03-34-28/cad-automation"
cd "$PROJECT_DIR" || exit 1

echo "📂 项目目录: $PROJECT_DIR"
echo ""

# 检查gh CLI
if ! command -v gh &> /dev/null; then
    echo -e "${YELLOW}⚠️  未检测到 GitHub CLI (gh)${NC}"
    echo "正在尝试安装..."
    
    # 尝试用homebrew安装
    if command -v brew &> /dev/null; then
        echo "使用 Homebrew 安装 gh..."
        brew install gh 2>&1 || {
            echo -e "${RED}❌ Homebrew 安装失败，尝试手动下载...${NC}"
            
            # 手动下载安装
            echo "下载 GitHub CLI..."
            curl -sL "https://github.com/cli/cli/releases/download/v2.65.0/gh_2.65.0_macOS_arm64.tar.gz" -o /tmp/gh.tar.gz
            
            echo "解压..."
            tar -xzf /tmp/gh.tar.gz -C /tmp
            
            echo "安装到 /usr/local/bin..."
            sudo cp /tmp/gh_2.65.0_macOS_arm64/bin/gh /usr/local/bin/
            
            echo -e "${GREEN}✅ 安装完成${NC}"
        }
    else
        echo -e "${RED}❌ 未找到 Homebrew，请先安装 Homebrew：${NC}"
        echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
fi

echo -e "${GREEN}✅ GitHub CLI 已安装${NC}"
echo ""

# 检查gh认证状态
echo "🔍 检查 GitHub 认证状态..."
AUTH_STATUS=$(gh auth status 2>&1 || true)

if echo "$AUTH_STATUS" | grep -q "Logged in"; then
    echo -e "${GREEN}✅ 已登录 GitHub${NC}"
    gh auth status
else
    echo -e "${YELLOW}⚠️  未登录 GitHub${NC}"
    echo ""
    echo "请在浏览器中完成登录："
    echo "1. 浏览器会自动打开 GitHub 登录页面"
    echo "2. 输入授权码"
    echo "3. 完成后返回此处"
    echo ""
    read -p "按 Enter 开始登录..." -r
    
    gh auth login --web --git-protocol https --hostname github.com
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ 登录成功${NC}"
    else
        echo -e "${RED}❌ 登录失败${NC}"
        exit 1
    fi
fi

echo ""
echo "========================================="
echo "  准备发布到 GitHub"
echo "========================================="
echo ""

# 获取GitHub用户名
USERNAME=$(gh api user --jq '.login')
echo -e "${GREEN}✅ GitHub 用户名: $USERNAME${NC}"
echo ""

# 检查仓库是否存在
REPO_NAME="cad-automation"
REPO_EXISTS=$(gh repo view "$USERNAME/$REPO_NAME" &> /dev/null && echo "yes" || echo "no")

if [ "$REPO_EXISTS" = "yes" ]; then
    echo -e "${YELLOW}⚠️  仓库 $REPO_NAME 已存在${NC}"
    echo "是否删除并重新创建？(y/n)"
    read -p ">" -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "删除旧仓库..."
        gh repo delete "$USERNAME/$REPO_NAME" --yes || true
        echo "创建新仓库..."
        gh repo create "$REPO_NAME" --public --source=. --remote=origin --push
    fi
else
    echo "创建 GitHub 仓库: $REPO_NAME"
    gh repo create "$REPO_NAME" --public --source=. --remote=origin --push
fi

echo ""
echo -e "${GREEN}🎉 发布成功！${NC}"
echo ""
echo "仓库链接:"
echo "  https://github.com/$USERNAME/$REPO_NAME"
echo ""
echo "克隆命令:"
echo "  git clone https://github.com/$USERNAME/$REPO_NAME.git"
echo ""

# 打开仓库页面
echo "是否在浏览器中打开仓库？ (y/n)"
read -p ">" -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    open "https://github.com/$USERNAME/$REPO_NAME"
fi

echo ""
echo "按 Enter 退出..."
read -r
