@echo off
echo ============================================
echo MySQL 初始化脚本
echo ============================================
echo.

set MYSQL_HOME=C:\Program Files\MySQL\MySQL Server 8.4
set DATA_DIR=%MYSQL_HOME%\data

echo 步骤 1: 创建数据目录...
if not exist "%DATA_DIR%" mkdir "%DATA_DIR%"

echo 步骤 2: 初始化 MySQL (无密码)...
"%MYSQL_HOME%\bin\mysqld.exe" --initialize-insecure --console

echo 步骤 3: 安装 MySQL 服务...
"%MYSQL_HOME%\bin\mysqld.exe" --install MySQL84

echo 步骤 4: 启动 MySQL 服务...
net start MySQL84

echo 步骤 5: 等待 MySQL 启动...
timeout /t 5 /nobreak > nul

echo 步骤 6: 设置 root 密码为 123456...
"%MYSQL_HOME%\bin\mysql.exe" -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '123456'; FLUSH PRIVILEGES;"

echo.
echo ============================================
echo MySQL 初始化完成!
echo 用户名: root
echo 密码: 123456
echo 端口: 3306
echo ============================================
echo.
pause
