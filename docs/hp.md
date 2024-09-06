# 血量机制
## 逆转裁判 1
由 `GlobalWork.rest` 与 `GlobalWork.rest_old` 两个字段控制。

`GlobalWork.rest` 为新血量，即扣除伤害之后的血量；`GlobalWork.rest_old` 为原血量，即扣除伤害之前的血量。如果当前没有伤害值，则两者相同。

满血血量值为 5，每次伤害扣除血量固定为 2。

修改血量时需要同时修改两个字段。

## 逆转裁判 2、3
由 `GlobalWork.gauge_hp`、`GlobalWork.gauge_hp_disp` 和 `GlobalWork.gauge_dmg_cnt` 三个字段控制。

`GlobalWork.gauge_hp` 与 `GlobalWork.gauge_hp_disp` 分别类似于 `GlobalWork.rest` 与 `GlobalWork.rest_old`。

满血血量为 80，每次伤害扣除的血量由 `GlobalWork.gauge_dmg_cnt` 字段决定。

修改血量时需要同时修改两个字段。

## 代码摘录
```cs
// Token: 0x06000C40 RID: 3136 RVA: 0x00074F90 File Offset: 0x00073390
private int GetNowLife()
{
    if (GSStatic.global_work_.gauge_hp == 1)
    {
        return 1;
    }
    if (GSStatic.global_work_.title == TitleId.GS1)
    {
        if (this.debug_no_damage_)
        {
            return (int)(GSStatic.global_work_.rest_old * 10 / 5);
        }
        return (int)GSStatic.global_work_.rest * 10 / 5;
    }
    else
    {
        if (this.debug_no_damage_)
        {
            return (int)(GSStatic.global_work_.gauge_hp_disp * 10 / 80);
        }
        return (int)(GSStatic.global_work_.gauge_hp * 10 / 80);
    }
}

// Token: 0x06000C41 RID: 3137 RVA: 0x00075018 File Offset: 0x00073418
private int GetOldLife()
{
    if (GSStatic.global_work_.gauge_hp_disp == 1)
    {
        return 1;
    }
    if (GSStatic.global_work_.title == TitleId.GS1)
    {
        return (int)(GSStatic.global_work_.rest_old * 10 / 5);
    }
    return (int)(GSStatic.global_work_.gauge_hp_disp * 10 / 80);
}

// Token: 0x06000C42 RID: 3138 RVA: 0x00075068 File Offset: 0x00073468
private int GetDamage()
{
    if (GSStatic.global_work_.title == TitleId.GS1)
    {
        if (this.debug_instant_death_)
        {
            return (int)GSStatic.global_work_.rest * 10 / 5;
        }
        return 2;
    }
    else
    {
        if (this.debug_instant_death_)
        {
            return (int)(GSStatic.global_work_.gauge_hp * 10 / 5);
        }
        return (int)(GSStatic.global_work_.gauge_dmg_cnt * 10 / 80);
    }
}
```