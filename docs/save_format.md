## 存档位置
Steam：`<Steam-folder>\userdata\<user-id>\787480\remote\systemdata`
Xbox PC：`%LOCALAPPDATA%\Packages\F024294D.PhoenixWrightAceAttorneyTrilogy_8fty0by30jkny\SystemAppData\wgs\<user-id>\`

## 存档格式
见 `app.structs` 模块下文件。

## 平台差异性
以 Steam 平台的存档格式为标准。

### Xbox PC
> 根据 [PCGameWiki](https://www.pcgamingwiki.com/wiki/Phoenix_Wright:_Ace_Attorney_Trilogy#cite_ref-6) 的描述，Xbox 上的逆转裁判 123 与 Steam 上的不同。Xbox 上的使用 il2cpp 编译，而 Steam 上的只是普通的 Mono。
>
> il2cpp 编译后的文件无法使用 dnSpy 反编译，只能使用 IDA 反编译为汇编代码。
> 
> 使用[这个工具](https://github.com/Perfare/Il2CppDumper)可以提取编译后 DLL 的类信息与结构体信息，要查看具体的代码只能通过 IDA 反编译。

**Xbox PC 的存档缺少以下字段：**
* `OptionWorkXbox.resolution_w`
* `OptionWorkXbox.resolution_h`
* `OptionWorkXbox.vsync`
* `OptionWorkXbox.key_config`
* `MessageData.msg_icon`