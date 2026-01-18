# 快速开始 - Quick Start

## 🚀 3步完成部署

### 第1步: 获取API密钥 (5分钟)

#### 必需的3个API密钥:

1. **Anthropic API** → https://console.anthropic.com/
   - 用于AI内容总结
   - 格式: `sk-ant-api03-...`

2. **Serper API** → https://serper.dev/
   - 用于新闻搜索（免费2,500次/月）
   - 格式: 32位字符串

3. **Gmail应用密码** → https://myaccount.google.com/security
   - 在"两步验证"中创建"应用专用密码"
   - 格式: `xxxx xxxx xxxx xxxx` (16位)

---

### 第2步: 部署到GitHub (2分钟)

```bash
# 1. 上传代码到GitHub
cd ai-news-newsletter
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/ai-news-newsletter.git
git push -u origin main

# 2. 配置Secrets
# GitHub仓库 → Settings → Secrets → Actions → New secret
```

配置以下4个Secrets:
- `ANTHROPIC_API_KEY`
- `SERPER_API_KEY`
- `GMAIL_SENDER` (您的Gmail邮箱)
- `GMAIL_APP_PASSWORD`

---

### 第3步: 测试运行 (1分钟)

1. 进入GitHub仓库的 **Actions** 标签
2. 点击 "Send AI Newsletter"
3. 点击 "Run workflow"
4. 等待约2-3分钟
5. 检查邮箱: Lingjian.li84@gmail.com

---

## ✅ 完成！

系统将自动在**每周一上午9点**发送AI新闻简报。

---

## 📝 可选配置

### 修改收件人
编辑 `config.yaml`:
```yaml
newsletter:
  recipient: "new-email@example.com"
```

### 修改发送时间
编辑 `.github/workflows/send-newsletter.yml`:
```yaml
cron: '0 1 * * 1'  # 周一 09:00 北京时间
```

---

## 📚 完整文档

- **详细设置**: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **项目说明**: [README.md](README.md)
- **项目概览**: [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)

---

## ❓ 遇到问题？

### 常见问题解决:

**邮件发送失败?**
- 检查Gmail应用密码是否正确
- 确保已开启"两步验证"

**GitHub Actions失败?**
- 检查Secrets配置是否完整
- 查看Actions日志获取详细错误

**没收到邮件?**
- 检查垃圾邮件文件夹
- 确认收件人邮箱地址正确

---

## 💡 提示

首次部署后建议**手动触发一次**测试，确保所有配置正确！

---

**预计总时间**: 10分钟完成部署
**每月成本**: < $0.20 (几乎免费)
**维护工作**: 0 (完全自动化)
