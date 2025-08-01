@echo off
:: 静默模式，不显示任何输出
>nul 2>&1

:: 获取当前目录
set "current_dir=%~dp0"

:: 获取启动文件夹路径
set "startup_folder=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

:: 创建快捷方式
set "shortcut_path=%startup_folder%\TaskRunner.lnk"
set "target_path=%current_dir%TaskRunner.exe"
powershell -command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%shortcut_path%'); $s.TargetPath = '%target_path%'; $s.Save()" >nul 2>&1

exit /b 0