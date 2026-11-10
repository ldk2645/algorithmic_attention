# 算法注意力：政府—平台—公众 ABM 复现包

本仓库是旧版**算法注意力研究（冻结 V1）**的独立复现入口，保留正式五条件消融、S1 外部验证、S2 敏感性分析、图件和数据字典。正式研究材料 `01–06` 与来源仓库 [ldk2645/paper](https://github.com/ldk2645/paper) 的冻结提交 [`f0d71f9c3006fe4a69b6da4f5ed91035f2557f13`](https://github.com/ldk2645/paper/tree/f0d71f9c3006fe4a69b6da4f5ed91035f2557f13) **逐字节一致**。这是完整复现快照，不表示其中所有后来加入的补充条件都是最初预注册内容。

| 目录 | 研究角色 |
|---|---|
| [01_model_core](01_model_core/README.md) | 唯一冻结 V1 核心模型 |
| [02_experiment_code](02_experiment_code) | 正式消融、外部验证、S2 与图表代码 |
| [03_data](03_data/README.md) | 正式消融、S1/S2 原始表、处理表和逐图来源 |
| [04_figures](04_figures) | 正式主图和补充图 |
| [05_documents](05_documents/README.md) | 研究设计、附录、S1/S2 与图注 |
| [06_reproducibility](06_reproducibility) | 环境、数据字典、协议溯源、原始 SHA256 清单与 QA |
| [07_version2_uk_petition](07_version2_uk_petition/README.md) | 历史 V2 英国请愿扩展，不属于原始论文冻结设计 |
| [08_version3_response_dashboard](08_version3_response_dashboard/README.md) | 历史 V3 回应仪表板与试验，不属于原始论文冻结设计 |
| [repository_history](repository_history/README.md) | 原根 README、后续英国案例及管理文件原字节归档 |

## 正式结果与边界

- [五条件消融逐次结果](03_data/formal_ablation/raw/formal_replicates_5conditions.csv)：5,250 次运行，21 个 α 水平、50 个共同随机种子。`No trust` 是四条件协议之后追加的正式消融，不能写成最初协议内容；见 [正式消融溯源](06_reproducibility/FORMAL_ABLATION_PROVENANCE.md)。
- [S1 外部验证](05_documents/补充材料S1_外部验证细节.md)：公开数据的机制方向或数量级相容性检查，不是因果识别或现实常数校准。
- [S2 敏感性分析](05_documents/补充材料S2_敏感性分析.md)：19,950 次新增运行；含参照的分析输入 22,050 行。[数据字典](06_reproducibility/DATA_DICTIONARY.md)保留指标定义。
- `system_stability` 越大表示末 100 步议程偏离波动越强；`response_strength` 为回应后热度保留率，不是削减比例。冻结模型没有自适应强度实现。

核心 `01_model_core/model.py` 的 SHA256：

```text
AB78E6C64AFB6FD487E40A48FBBCD1B09A84EE3FBC9085530F8833DE3543D7EC
```

## 只读复核与复现

在仓库根目录运行以下命令；它核对原清单、冻结目录及历史扩展，不创建仿真、不改写原 QA 或任何研究输出，只需 Python 标准库：

```text
python -B migration/verify_legacy.py
```

原始计算环境和完整复现步骤见 [ENVIRONMENT](06_reproducibility/ENVIRONMENT.md) 与 [原始 README](repository_history/f0d71f9/README.md)。完整重跑应在独立副本和新输出位置进行；发布 CSV、图件、QA 和哈希清单是既有证据，不应覆盖。`build_release_manifest.py`、`validate_release.py` 原入口会写清单或 QA，本次迁移未直接执行这些写入入口。跨环境逐比特一致性的历史限制仍适用。

## 与新版及来源仓库的关系

政府行政信息推断与回应目标匹配的新线由 [reverse-black-box-inference](https://github.com/ldk2645/reverse-black-box-inference) 独立维护（初始为私有仓库，需要访问权限）。其正式 E2–E4 入口为 `10_abm_jasss`；后正式补充实验为 `11_postformal_20261009`，早期开发为 `09_version4_inference`。新版来源提交为 `a91d00635896c0d06d78f99c712c63b04d104d67`。

旧版 V2/V3 也取自该来源提交，按原字节保存。新旧研究具有共同代码与思想来源，不能声称完全独立开发；它们的结果、样本和版本不可混用。`paper` 保留原有完整历史，本次未回退或删除其提交。这里没有新版 09–11 或新版报告树。

本仓库沿用原始授权和数据使用边界，没有新增再许可授权。新版约 50 GB 的补充生产档案及其他本机原始批次不在这份旧版包内，也未因分仓而公开。迁移检查与文件归属见 [migration](migration/README.md)。
