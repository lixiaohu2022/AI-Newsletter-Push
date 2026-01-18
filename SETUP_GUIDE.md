# 快速设置指南 - Quick Setup Guide

## 5分钟快速部署

### 步骤1: 获取API密钥 (5-10分钟)

#### 1.1 Anthropic API密钥 ⭐ 必需
1. 访问: https://console.anthropic.com/
2. 注册/登录
3. 点击 "API Keys" → "Create Key"
4. 复制密钥（格式：`sk-ant-api03-...`）

#### 1.2 Serper API密钥 ⭐ 必需
1. 访问: https://serper.dev/
2. 使用Google账号登录
3. 复制Dashboard中的API密钥
4. 免费额度: 2,500次搜索/月

#### 1.3 Gmail应用专用密码 ⭐ 必需
1. 访问: https://myaccount.google.com/security
2. 确保已开启"两步验证"
3. 搜索"应用专用密码" (App Passwords)
4. 选择"邮件" + "其他设备"
5. 复制生成的16位密码（格式：`abcd efgh ijkl mnop`）

---

### 步骤2: 部署到GitHub (2分钟)

#### 2.1 Fork或上传代码到GitHub
```bash
# 方法1: 克隆现有仓库后上传到自己的GitHub
cd ai-news-newsletter
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/ai-news-newsletter.git
git push -u origin main
```

#### 2.2 配置Secrets
进入GitHub仓库 → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

添加以下4个Secrets:

| Name | Value |
|------|-------|
| `ANTHROPIC_API_KEY` | 您的Anthropic密钥 |
| `SERPER_API_KEY` | 您的Serper密钥 |
| `GMAIL_SENDER` | 您的Gmail邮箱地址 |
| `GMAIL_APP_PASSWORD` | Gmail应用专用密码 |

⚠️ **注意**: Secret名称必须完全一致（包括大小写）

---

### 步骤3: 测试运行 (1分钟)

#### 3.1 手动触发测试
1. 进入仓库的 **Actions** 标签页
2. 点击左侧 "Send AI Newsletter"
3. 点击右侧 "Run workflow" → "Run workflow"
4. 等待约2-3分钟查看结果

#### 3.2 检查邮件
- 查看您的邮箱 (Lingjian.li84@gmail.com)
- 如果没收到，检查垃圾邮件文件夹

---

### 步骤4: 自定义配置（可选）

#### 修改收件人邮箱
编辑 `config.yaml`:
```yaml
newsletter:
  recipient: "your-new-email@example.com"  # 修改这里
```

#### 修改发送时间
编辑 `.github/workflows/send-newsletter.yml`:
```yaml
schedule:
  - cron: '0 1 * * 1'  # 周一UTC 01:00 = 北京时间09:00
```

时区对照表:
- 北京时间 09:00 = UTC 01:00 → `'0 1 * * 1'`
- 北京时间 10:00 = UTC 02:00 → `'0 2 * * 1'`
- 北京时间 08:00 = UTC 00:00 → `'0 0 * * 1'`

---

## 故障排查速查表

### ❌ 邮件发送失败
```
错误信息: Authentication failed / 535 error
```
**解决方案**:
- 重新生成Gmail应用专用密码
- 确保密码中没有空格
- 确认两步验证已开启

### ❌ Claude API调用失败
```
错误信息: Invalid API key / 401 error
```
**解决方案**:
- 检查Anthropic API密钥格式（应以 `sk-ant-api03-` 开头）
- 确认账户有可用额度
- 重新生成并更新密钥

### ❌ GitHub Actions无法运行
```
错误信息: Workflow not found
```
**解决方案**:
- Settings → Actions → General
- 选择 "Allow all actions and reusable workflows"
- 保存后重新触发

### ❌ 没有收到邮件
**检查清单**:
1. ✓ 检查垃圾邮件文件夹
2. ✓ 确认GitHub Actions运行成功（绿色✓）
3. ✓ 查看Actions日志中是否有错误
4. ✓ 确认`config.yaml`中的邮箱地址正确

---

## 测试检查清单

完成以下检查确保系统正常:

- [ ] Anthropic API密钥已获取并配置
- [ ] Serper API密钥已获取并配置
- [ ] Gmail应用专用密码已生成并配置
- [ ] GitHub仓库已创建
- [ ] 4个Secrets已正确配置
- [ ] 手动触发workflow成功运行
- [ ] 收到测试邮件
- [ ] 邮件内容格式正常（中英文双语）
- [ ] 邮件中包含4个主题板块
- [ ] 所有链接可以正常打开

---

## 常见问题 FAQ

### Q1: 可以修改发送频率吗？
**A**: 可以。修改 `.github/workflows/send-newsletter.yml` 中的 cron 表达式：
- 每天: `'0 1 * * *'`
- 每周一和周五: `'0 1 * * 1,5'`
- 每月1号: `'0 1 1 * *'`

### Q2: 可以发送给多个人吗？
**A**: 需要修改代码。在 `config.yaml` 中将 `recipient` 改为列表，然后修改 `main.py` 中的发送逻辑。

### Q3: 运行成本是多少？
**A**:
- GitHub Actions: 免费（公开仓库）
- Gmail: 免费
- Serper API: 免费额度足够（每周运行一次）
- Anthropic Claude: 约$0.01-0.05/次，每月约$0.04-0.20

### Q4: 如果API额度用完了怎么办？
**A**:
- Serper: 代码已内置模拟数据作为备选
- Anthropic: 需要充值或升级套餐

### Q5: 可以更改新闻来源吗？
**A**: 可以。修改 `config.yaml` 中的 `search_keywords` 字段，使用不同的搜索关键词。

---

## 下一步

✅ 设置完成后，系统将自动:
1. 每周一上午9点运行
2. 搜索最新AI新闻
3. 使用Claude总结内容
4. 生成精美的HTML邮件
5. 发送到您的邮箱

🎉 享受自动化的AI资讯服务吧！

---

## 获取帮助

- 查看详细文档: [README.md](README.md)
- 提交问题: [GitHub Issues](https://github.com/YOUR_USERNAME/ai-news-newsletter/issues)
- 查看运行日志: Actions → 选择运行记录 → 查看详细日志
