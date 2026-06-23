# Tencent Shadowrocket Rules

腾讯、QQ、微信及相关业务的分流规则，数据从
[`v2fly/domain-list-community`](https://github.com/v2fly/domain-list-community)
的 `tencent` 分类递归生成。

覆盖腾讯云、腾讯游戏、腾讯音乐、阅文、搜狗、Coding、DNSPod、酷狗、酷我、
喜马拉雅等关联分类。仓库每周自动检查上游更新。

## Shadowrocket

在 Shadowrocket 配置的 `[Rule]` 中，把以下规则放在 `GEOIP` 和 `FINAL` 前：

```ini
RULE-SET,https://raw.githubusercontent.com/DDcat2025/tencent-shadowrocket-rules/main/rule/Shadowrocket/Tencent/Tencent.list,DIRECT
```

也可以使用精简的 Domain Set：

```ini
DOMAIN-SET,https://raw.githubusercontent.com/DDcat2025/tencent-shadowrocket-rules/main/rule/Shadowrocket/Tencent/Tencent_Domain.list,DIRECT
```

二者选择一个即可，不要重复引用。

## Mihomo / Clash Meta

```yaml
rule-providers:
  tencent:
    type: http
    behavior: classical
    url: https://raw.githubusercontent.com/DDcat2025/tencent-shadowrocket-rules/main/rule/Mihomo/Tencent/Tencent.yaml
    path: ./ruleset/tencent.yaml
    interval: 86400

rules:
  - RULE-SET,tencent,DIRECT
```

## 文件

- `rule/Shadowrocket/Tencent/Tencent.list`：Shadowrocket `RULE-SET` 格式。
- `rule/Shadowrocket/Tencent/Tencent_Domain.list`：Shadowrocket `DOMAIN-SET` 格式。
- `rule/Mihomo/Tencent/Tencent.yaml`：Mihomo classical rule-provider 格式。
- `data/tencent-domains.txt`：每行一个域名的纯文本列表。

## 注意

- 规则包括腾讯体系的广告、统计和遥测域名。需要屏蔽时，请把广告拦截规则放在本规则前面。
- 静态列表无法永久保证覆盖腾讯新增或迁移的全部域名，自动更新以社区上游数据为准。
- IP 直连、应用内硬编码地址及 DNS 劫持不属于域名规则覆盖范围。

