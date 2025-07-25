# PWAAT-Save-Editor 逆转裁判 123 存档修改器
[For English users](./README.en.md)

## 功能
基本功能：
* 导入、导出存档
* Steam 与 Xbox 存档互相转换  
（根据社区反馈，Xbox 存档与 Switch 存档格式相同，因此也可以 Steam、Switch 存档互转。但是你需要自行处理 Switch 存档导入导出问题。）
* 解锁章节
* 修改法庭内血量
* 存档槽位管理，包括删除、复制、移动存档槽位数据  
（试验性功能，非必要不使用）

附加功能：
* 修改对话框相关数据
* 加密与解密游戏资源文件
* 强制转换存档语言

## Todo
- [x] 存档槽位管理，包括删除、复制、导入导出、排序存档槽位
- [x] 强制转换存档语言
- [x] 支持其他平台的重制版（Android、iOS、破解 Switch 等）
- [x] 支持 PC 盗版
- [ ] 本地有多个 Steam 账号时，允许选择账号而不是默认第一个
- [ ] 导入存档自动检测类型并转换
- [ ] 用于快速备份管理存档工具

## 基础用法
### 下载
1. 在 [Release 页](https://github.com/XcantloadX/PWAAT-Save-Editor/releases)下载最新版本的编辑器  
（带 `REPL` 与不带 `REPL` 的两个版本均可）
2. 解压后运行 `PWAAT Save Editor.exe`

### 导入/导出存档
见“转换”菜单下的内容。

### Xbox/Steam 存档互转
见“转换”菜单下的内容。

### 解锁章节
1. 在“文件”菜单内打开任意存档
2. 按需求调整“解锁章节”框内的设置
3. “文件” → “保存”
4. 重启游戏

### 修改血量
1. 在“文件”菜单内打开任意存档
2. 检查“选择存档”处自动选中的存档是否为想要修改的存档，若不是，改为想要修改的存档
3. 调整血量
4. “文件” → “保存”
5. 在游戏内重新读取该存档

## 高级用法
由于精力限制，GUI 中无法涵括存档数据中的方方面面。如果你想要修改 GUI 中没有的部分，可以使用基于 PtPython 的交互式 Shell，自己手动敲代码修改。

整个存档数据的结构可以在源代码 `app\structs\steam.py` 与 `app\structs\xbox.py` 文件中查阅。部分字段已经有文档注释，但是大部分没有。

1. 下载带 `REPL` 的版本
2. 打开任意存档，然后 “文件” → “运行 REPL”
3. 切换到 CMD 窗口，阅读提示

> [!IMPORTANT]  
> GUI 与 REPL 是分隔运行的，两者的未保存修改不会同步。  
> 因此打开与关闭 REPL 前均建议保存。

> [!TIP]  
> 建议使用 Windows Terminal 运行 REPL。

> [!CAUTION]  
> 在使用 REPL 修改存档之前，你最好要意识到自己在干什么，否则这就是后果：
> <img width="75%" src="./images/corrupted_game.png" alt="鬼畜的游戏画面" />

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
* [PCGamingWiki](https://www.pcgamingwiki.com/wiki/Phoenix_Wright:_Ace_Attorney_Trilogy#cite_ref-6)