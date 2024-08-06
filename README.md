# PWAAT-Save-Editor 逆转裁判 123 存档修改器

## 功能
* 导入、导出存档
* Steam 与 Xbox 存档互相转换
* 解锁章节
* 修改法庭内血量

## 使用教程
### 下载
1. 在 [Release 页](https://github.com/XcantloadX/PWAAT-Save-Editor/releases)下载最新版本的编辑器
2. 解压后运行 `PWAAT Save Editor.exe`

### 导入/导出存档
Steam 转 Xbox：菜单栏 → 转换 → “Xbox ← Steam”

Xbox 转 Steam：菜单栏 → 转换 → “Xbox → Steam”

导入 Steam 存档：菜单栏 → 转换 → “Steam ← 文件...”

导出 Steam 存档：菜单栏 → 转换 → “Steam → 文件...”

### 解锁章节
1. 关闭游戏
2. 在“文件”菜单内打开任意存档
3. 按需求调整“解锁章节”框内的设置
4. “文件” → “保存”
5. 启动游戏

### 修改血量
1. 在“文件”菜单内打开任意存档
2. 检查“选择存档”处自动选中的存档是否为想要修改的存档，若不是，改为想要修改的存档
3. 调整血量
4. “文件” → “保存”
5. 在游戏内重新读取该存档

## 翻译
1. 安装 [gettext](https://mlocati.github.io/articles/gettext-iconv-windows.html)
2. Clone 项目到本地
3. 确定目标语言的语言代码与国家代码，可以在[这里](https://www.gnu.org/software/gettext/manual/gettext.html#Language-Codes)与[这里](https://www.gnu.org/software/gettext/manual/gettext.html#Country-Codes)查询。
4. 创建文件夹 `.\locales\{语言代码}_{国家代码}\LC_MESSAGES`
5. 将 `.\locales\base.pot` 复制为 `.\locales\{语言代码}_{国家代码}\LC_MESSAGES\base.po`
6. 翻译刚刚复制的 `.po` 文件
7. 使用 PowerShell 运行 `.\translation compile`


## 参考
* [Phoenix Wright Trilogy Save Data Research ](https://gist.github.com/emiyl/1435ce18a6b1e0a5c2a74e15c19f4884)
* [emiyl / PWAATeditor](https://github.com/emiyl/PWAATeditor/tree/v0.3.0)