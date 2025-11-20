# XiaoZhiShi 一键部署脚本
# PowerShell 版本 - 适用于 Windows 系统

param(
    [switch]$SkipAdminCreation,
    [switch]$SkipDependencies,
    [switch]$Production,
    [string]$Port = "5000"
)

# 设置错误处理
$ErrorActionPreference = "Stop"

# 颜色定义
$Green = "Green"
$Red = "Red"
$Yellow = "Yellow"
$Cyan = "Cyan"
$Blue = "Blue"

# 打印带颜色的信息
function Write-ColorMessage {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# 打印带前缀的信息
function Write-Info {
    param([string]$Message)
    Write-ColorMessage "[INFO] $Message" $Cyan
}

function Write-Success {
    param([string]$Message)
    Write-ColorMessage "[SUCCESS] $Message" $Green
}

function Write-Warning {
    param([string]$Message)
    Write-ColorMessage "[WARNING] $Message" $Yellow
}

function Write-Error {
    param([string]$Message)
    Write-ColorMessage "[ERROR] $Message" $Red
}

# 检查Python版本
function Test-PythonVersion {
    Write-Info "检查Python版本..."
    try {
        $pythonVersion = python --version 2>&1
        Write-Success "Python版本: $pythonVersion"
        
        # 提取版本号
        $versionMatch = [regex]::Match($pythonVersion, "Python\s+(\d+)\.(\d+)")
        if ($versionMatch.Success) {
            $major = [int]$versionMatch.Groups[1].Value
            $minor = [int]$versionMatch.Groups[2].Value
            
            if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
                Write-Error "需要Python 3.8或更高版本"
                exit 1
            }
        }
    }
    catch {
        Write-Error "未找到Python，请先安装Python 3.8+"
        exit 1
    }
}

# 检查pip
function Test-Pip {
    Write-Info "检查pip..."
    try {
        $pipVersion = pip --version
        Write-Success "pip版本: $pipVersion"
    }
    catch {
        Write-Error "未找到pip，请确保Python已正确安装"
        exit 1
    }
}

# 创建虚拟环境
function New-VirtualEnvironment {
    if (Test-Path "venv") {
        Write-Warning "虚拟环境已存在，跳过创建"
        return
    }
    
    Write-Info "创建虚拟环境..."
    try {
        python -m venv venv
        Write-Success "虚拟环境创建成功"
    }
    catch {
        Write-Error "创建虚拟环境失败: $_"
        exit 1
    }
}

# 激活虚拟环境
function Enable-VirtualEnvironment {
    Write-Info "激活虚拟环境..."
    try {
        $activateScript = ".\venv\Scripts\Activate.ps1"
        if (Test-Path $activateScript) {
            . $activateScript
            Write-Success "虚拟环境已激活"
        }
        else {
            Write-Error "找不到激活脚本: $activateScript"
            exit 1
        }
    }
    catch {
        Write-Error "激活虚拟环境失败: $_"
        exit 1
    }
}

# 安装依赖
function Install-Dependencies {
    if ($SkipDependencies) {
        Write-Warning "跳过依赖安装"
        return
    }
    
    Write-Info "安装Python依赖..."
    try {
        pip install --upgrade pip
        pip install -r requirements.txt
        Write-Success "依赖安装成功"
    }
    catch {
        Write-Error "依赖安装失败: $_"
        exit 1
    }
}

# 检查并创建.env文件
function New-EnvironmentFile {
    if (Test-Path ".env") {
        Write-Warning ".env文件已存在"
        return
    }
    
    Write-Info "创建.env配置文件..."
    try {
        $envContent = @"
# Flask配置
SECRET_KEY=$(-join ((65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_}))
DEBUG=True
FLASK_APP=run.py
FLASK_ENV=development

# 数据库配置
DATABASE_URL=sqlite:///blog.db

# DEEPSEEK API配置
DEEPSEEK_APIKEY=your-deepseek-api-key-here

# 邮件配置（可选）
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USE_TLS=True
# MAIL_USERNAME=your-email@gmail.com
# MAIL_PASSWORD=your-app-password
"@
        $envContent | Out-File -FilePath ".env" -Encoding UTF8
        Write-Success ".env文件创建成功"
        Write-Warning "请编辑 .env 文件，配置您的API密钥和其他设置"
    }
    catch {
        Write-Error "创建.env文件失败: $_"
        exit 1
    }
}

# 初始化数据库
function Initialize-Database {
    Write-Info "初始化数据库..."
    try {
        python init_db.py
        Write-Success "数据库初始化成功"
    }
    catch {
        Write-Error "数据库初始化失败: $_"
        exit 1
    }
}

# 创建管理员账户
function New-AdminAccount {
    if ($SkipAdminCreation) {
        Write-Warning "跳过管理员账户创建"
        return
    }
    
    Write-Info "创建管理员账户..."
    try {
        python create_admin.py
        Write-Success "管理员账户创建成功"
    }
    catch {
        Write-Error "管理员账户创建失败: $_"
        Write-Warning "您可以稍后手动运行: python create_admin.py"
    }
}

# 检查端口占用
function Test-PortAvailability {
    param([int]$Port)
    
    Write-Info "检查端口 $Port 是否可用..."
    try {
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $Port)
        $listener.Start()
        $listener.Stop()
        Write-Success "端口 $Port 可用"
        return $true
    }
    catch {
        Write-Error "端口 $Port 已被占用"
        return $false
    }
}

# 启动应用
function Start-Application {
    param([int]$Port)
    
    if (-not (Test-PortAvailability -Port $Port)) {
        Write-Warning "端口被占用，请使用其他端口或停止占用该端口的程序"
        exit 1
    }
    
    Write-Info "启动应用..."
    Write-ColorMessage "应用将在 http://127.0.0.1:$Port 运行" $Blue
    Write-ColorMessage "前台地址: http://127.0.0.1:$Port" $Green
    Write-ColorMessage "后台地址: http://127.0.0.1:$Port/admin" $Green
    Write-ColorMessage "按 Ctrl+C 停止应用" $Yellow
    
    try {
        if ($Production) {
            # 生产模式使用Gunicorn
            Write-Info "生产模式启动..."
            gunicorn -w 4 -b 0.0.0.0:$Port app:app
        }
        else {
            # 开发模式
            Write-Info "开发模式启动..."
            $env:FLASK_APP = "run.py"
            $env:FLASK_ENV = "development"
            python run.py
        }
    }
    catch {
        Write-Error "启动应用失败: $_"
        exit 1
    }
}

# 显示帮助信息
function Show-Help {
    Write-ColorMessage "XiaoZhiShi 一键部署脚本" $Blue
    Write-ColorMessage "使用方法: .\deploy.ps1 [选项]" $Cyan
    Write-ColorMessage ""
    Write-ColorMessage "选项:" $Yellow
    Write-ColorMessage "  -SkipAdminCreation    跳过创建管理员账户" $Cyan
    Write-ColorMessage "  -SkipDependencies      跳过安装依赖" $Cyan
    Write-ColorMessage "  -Production            生产模式启动" $Cyan
    Write-ColorMessage "  -Port <端口号>         指定端口 (默认: 5000)" $Cyan
    Write-ColorMessage "  -Help                  显示帮助信息" $Cyan
    Write-ColorMessage ""
    Write-ColorMessage "示例:" $Yellow
    Write-ColorMessage "  .\deploy.ps1" $Cyan
    Write-ColorMessage "  .\deploy.ps1 -Port 8080" $Cyan
    Write-ColorMessage "  .\deploy.ps1 -SkipAdminCreation -Production" $Cyan
}

# 主函数
function Main {
    # 显示帮助
    if ($Help) {
        Show-Help
        exit 0
    }
    
    # 显示欢迎信息
    Write-ColorMessage "========================================" $Blue
    Write-ColorMessage "  XiaoZhiShi (小智识) 部署脚本" $Blue
    Write-ColorMessage "========================================" $Blue
    Write-ColorMessage ""
    
    # 检查Python和pip
    Test-PythonVersion
    Test-Pip
    
    # 创建虚拟环境
    New-VirtualEnvironment
    
    # 激活虚拟环境
    Enable-VirtualEnvironment
    
    # 安装依赖
    Install-Dependencies
    
    # 创建.env文件
    New-EnvironmentFile
    
    # 初始化数据库
    Initialize-Database
    
    # 创建管理员账户
    New-AdminAccount
    
    # 显示完成信息
    Write-ColorMessage ""
    Write-ColorMessage "========================================" $Green
    Write-ColorMessage "  部署完成！" $Green
    Write-ColorMessage "========================================" $Green
    Write-ColorMessage ""
    Write-Info "请按以下步骤操作："
    Write-ColorMessage "1. 编辑 .env 文件，配置您的API密钥" $Yellow
    Write-ColorMessage "2. 重新运行部署脚本启动应用" $Yellow
    Write-ColorMessage ""
    Write-ColorMessage "启动命令: .\deploy.ps1" $Cyan
    Write-ColorMessage ""
    
    # 询问是否立即启动
    $startNow = Read-Host "是否立即启动应用? (y/n)"
    if ($startNow -eq 'y' -or $startNow -eq 'Y') {
        Start-Application -Port $Port
    }
    else {
        Write-Info "您可以使用以下命令手动启动应用:"
        Write-ColorMessage "  .\deploy.ps1" $Cyan
        Write-ColorMessage "  python run.py" $Cyan
    }
}

# 执行主函数
Main