# arxiv-weekly
一个使用Python快速获取arXiv每周论文的工具。

## 功能特点
- 根据关键词和时间范围检索arXiv论文
- 按研究领域和团队分类展示论文
- 支持自定义关键词和分类规则
- 自动处理arXiv的时间更新策略

## 安装说明
1. 克隆本仓库
```bash
git clone https://github.com/yourusername/arxiv-weekly.git
cd arxiv-weekly
```

2. 安装依赖
conda安装环境

```bash
conda activate arxiv
pip install arxiv python-dateutil
```

## 使用方法
### 基本用法
直接运行主程序获取默认配置的论文：
```bash
python arxiv-weekly.py
```

### 自定义配置
修改<mcfile name="config.py" path="..\arxiv-weekly\config.py"></mcfile>文件调整参数：
- `MAX_PAPERS`: 最大爬取论文数量（默认400）
- `DEFAULT_KEYWORD`: 默认搜索关键词（默认"quantum"）
- `FIELD_CATEGORY_KEYWORDS`: 研究领域分类关键词
- `TEAM_CATEGORY_KEYWORDS`: 团队成员分类关键词

## 代码结构
- `arxiv-weekly.py`：主程序，包含论文获取和展示逻辑（路径：`./arxiv-weekly.py`）
- `config.py`：配置文件，定义关键词和分类规则（路径：`./config.py`）
- `utility.py`：工具函数，处理时间范围计算等（路径：`./utility.py`）

## 常见问题
- **Q: 为什么有时获取不到论文？**
  A: arXiv在周末不更新，或者其他原因导致获取不到论文。

## 示例输出
程序将按领域和团队分类打印论文信息：
```
bash> python .\arxiv-weekly.py

================================================================================
          Fetching papers from 2025-08-19 19:00 to 2025-08-26 19:00...
================================================================================
Searching for papers with keyword 'quantum' from 202508191900 to 202508261900...
Found 400 papers.
================================================================================
                          Finish fetching 400 papers.
================================================================================
================================================================================
                    [FIELD] Quantum Error Correction papers
--------------------------------------------------------------------------------
[1] Title   : Literature Review of the Effect of Quantum Computing on Cryptocurrencies using Blockchain Technology
     Authors : Adi Mutha, Jitendra Sandu
     Date    : 2025-08-24
     Category: cs.CR
     URL     : http://arxiv.org/abs/2508.17296v1
--------------------------------------------------------------------------------
[2] Title   : Random-projector quantum diagnostics of Ramsey numbers and a prime-factor heuristic for $R(5,5)=45$
     Authors : Fabrizio Tamburini
     Date    : 2025-08-22
     Category: quant-ph
     URL     : http://arxiv.org/abs/2508.16699v1
--------------------------------------------------------------------------------
[3] Title   : Quantum Simulation of Electron Energy Loss Spectroscopy for Battery Materials
     Authors : Alexander Kunitsa, Diksha Dhawan, Stepan Fomichev, Juan Miguel Arrazola, Minghao Zhang, Torin F. Stetina
     Date    : 2025-08-21
     Category: quant-ph
     URL     : http://arxiv.org/abs/2508.15935v1
--------------------------------------------------------------------------------
[4] Title   : Colour Codes Reach Surface Code Performance using Vibe Decoding
     Authors : Stergios Koutsioumpas, Tamas Noszko, Hasan Sayginel, Mark Webster, Joschka Roffe
     Date    : 2025-08-21
     Category: quant-ph
     URL     : http://arxiv.org/abs/2508.15743v1
--------------------------------------------------------------------------------
================================================================================
                          [FIELD] QEC Decoding papers
--------------------------------------------------------------------------------
[1] Title   : Polarization-Aware DoA Detection Relying on a Single Rydberg Atomic Receiver
     Authors : Yuanbin Chen, Chau Yuen, Darmindra Arumugam, Chong Meng Samson See, M茅rouane Debbah, Lajos Hanzo
     Date    : 2025-08-24
     Category: cs.IT
     URL     : http://arxiv.org/abs/2508.17179v1
--------------------------------------------------------------------------------
[2] Title   : Colour Codes Reach Surface Code Performance using Vibe Decoding
     Authors : Stergios Koutsioumpas, Tamas Noszko, Hasan Sayginel, Mark Webster, Joschka Roffe
     Date    : 2025-08-21
     Category: quant-ph
     URL     : http://arxiv.org/abs/2508.15743v1
--------------------------------------------------------------------------------
```