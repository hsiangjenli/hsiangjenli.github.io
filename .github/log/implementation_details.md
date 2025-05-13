# Implementation Details

## 2025-05-13
- 本次針對 `.github/workflows/auto_update.yml` 進行註解優化，說明每個 job 與 step 的實際作用，並補充註解格式為繁體中文，便於日後維護與 onboarding。
- `config/_skill.toml` 新增 k8s（說明懂 k3s + kubectl 操作、部署）、Azure DevOps（說明懂建立個人 Agent）技能，技能結構與描述皆保持一致。
- Makefile 增加 PYTHON 變數，於執行時自動偵測 python3 或 python，確保不同作業系統及環境皆可正確執行 make html。
