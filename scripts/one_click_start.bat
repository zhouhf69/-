@echo off
setlocal
cd /d "%~dp0.."

REM =============================================
REM 一键启动脚本：自动创建虚拟环境、安装依赖并运行体检报告工作流
REM 使用方法：放在项目根目录，双击执行即可。
REM 如需修改路径或联系方式，请调整下方配置区。
REM =============================================

REM -------- 配置区（可根据需要修改） --------
set "DATA_DIR=data"
set "TEMPLATE=templates\report_template.html"
set "OUTPUT=output"
set "HOTLINE=400-000-0000"
set "CONSULT=400-111-2222"
set "AI_PROVIDER="
set "AI_MODEL="
REM -------------------------------------------

echo === 体检报告生成器一键启动 ===

where python >nul 2>nul
if errorlevel 1 (
    echo [错误] 未检测到 Python。请先安装 Python 3.10 及以上版本并勾选 "Add to PATH"。
    pause
    exit /b 1
)

if not exist .venv (
    echo [步骤] 正在创建虚拟环境 .venv ...
    python -m venv .venv
    if errorlevel 1 goto :error
) else (
    echo [步骤] 检测到已有虚拟环境 .venv
)

echo [步骤] 激活虚拟环境并升级 pip ...
call ".venv\Scripts\activate.bat"
if errorlevel 1 goto :error
python -m pip install --upgrade pip
if errorlevel 1 goto :error

if exist requirements.txt (
    echo [步骤] 安装/更新项目依赖 ...
    python -m pip install -r requirements.txt
    if errorlevel 1 goto :error
) else (
    echo [警告] 未找到 requirements.txt，跳过依赖安装。
)

set "AI_PROVIDER_OPTION="
if not "%AI_PROVIDER%"=="" set "AI_PROVIDER_OPTION=--ai-provider %AI_PROVIDER%"

set "AI_MODEL_OPTION="
if not "%AI_MODEL%"=="" set "AI_MODEL_OPTION=--ai-model %AI_MODEL%"

echo [步骤] 启动体检报告生成流程 ...
python main.py "%DATA_DIR%" --template "%TEMPLATE%" --output "%OUTPUT%" --hotline "%HOTLINE%" --consult "%CONSULT%" %AI_PROVIDER_OPTION% %AI_MODEL_OPTION%
if errorlevel 1 goto :error

echo.
echo === 任务完成，生成的 HTML 报告位于 %OUTPUT% 目录 ===
pause
exit /b 0

:error
echo.
echo [失败] 执行过程中出现问题，请根据提示排查后重试。
pause
exit /b 1
