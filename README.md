# AI Weekly Newsletter - 人工智能周报自动化系统

自动生成并发送AI新闻简报的系统，每周一上午9点自动运行。

## 功能特性

✅ **自动化运行**: 基于GitHub Actions，每周一上午9点自动触发
✅ **智能内容**: 使用Claude AI总结和筛选最新AI资讯
✅ **多主题覆盖**:
  - 全球AI最前沿动态
  - 企业AI应用最佳实践与案例
  - 工程咨询行业AI动态
  - AI职业发展与个人提升

✅ **双语支持**: 每条新闻提供中英文双语摘要
✅ **精美HTML邮件**: 响应式设计，适配各种邮件客户端
✅ **免费部署**: 完全基于免费服务（GitHub Actions + Gmail）

## 项目结构

```
ai-news-newsletter/
├── .github/
│   └── workflows/
│       └── send-newsletter.yml    # GitHub Actions工作流
├── src/
│   ├── news_fetcher.py           # 新闻获取和AI总结模块
│   └── email_sender.py           # 邮件发送模块
├── templates/
│   └── newsletter.html           # HTML邮件模板
├── config.yaml                   # 配置文件
├── main.py                       # 主程序
├── requirements.txt              # Python依赖
├── .env.example                  # 环境变量示例
└── README.md                     # 说明文档
```

## 部署步骤

### 1. 前置准备

#### 1.1 获取Anthropic API密钥
1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 注册/登录账号
3. 创建API密钥
4. 保存密钥备用

#### 1.2 获取搜索API密钥（Serper）
1. 访问 [Serper.dev](https://serper.dev/)
2. 注册账号（提供免费额度）
3. 获取API密钥
4. 保存密钥备用

#### 1.3 配置Gmail应用专用密码
1. 登录您的Gmail账号
2. 访问 [Google账号安全设置](https://myaccount.google.com/security)
3. 开启"两步验证"（如果未开启）
4. 搜索"应用专用密码"
5. 选择"邮件"和"其他设备"
6. 生成16位应用专用密码
7. 保存密码备用

### 2. GitHub仓库设置

#### 2.1 创建仓库并上传代码
```bash
cd ai-news-newsletter
git init
git add .
git commit -m "Initial commit: AI Newsletter automation"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-news-newsletter.git
git push -u origin main
```

#### 2.2 配置GitHub Secrets
在GitHub仓库中设置以下Secrets（Settings → Secrets and variables → Actions → New repository secret）:

| Secret名称 | 说明 | 示例 |
|-----------|------|------|
| `ANTHROPIC_API_KEY` | Anthropic API密钥 | `sk-ant-api03-...` |
| `SERPER_API_KEY` | Serper搜索API密钥 | `abc123...` |
| `GMAIL_SENDER` | Gmail发件人邮箱 | `your-email@gmail.com` |
| `GMAIL_APP_PASSWORD` | Gmail应用专用密码 | `abcd efgh ijkl mnop` |

### 3. 本地测试（可选）

#### 3.1 安装依赖
```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

#### 3.2 配置环境变量
创建 `.env` 文件：
```bash
cp .env.example .env
```

编辑 `.env` 文件，填入实际值：
```env
ANTHROPIC_API_KEY=your_anthropic_api_key
SERPER_API_KEY=your_serper_api_key
GMAIL_SENDER=your-email@gmail.com
GMAIL_APP_PASSWORD=your_app_password
```

#### 3.3 运行测试
```bash
python main.py
```

### 4. 启用自动化

#### 4.1 启用GitHub Actions
1. 进入GitHub仓库的 **Actions** 标签
2. 如果提示启用workflows，点击"I understand my workflows, go ahead and enable them"
3. 工作流将在每周一上午9点（北京时间）自动运行

#### 4.2 手动触发测试
1. 进入 **Actions** → **Send AI Newsletter**
2. 点击 **Run workflow** → **Run workflow**
3. 查看运行日志确认是否成功

## 配置说明

### 修改邮件接收地址
编辑 `config.yaml`:
```yaml
newsletter:
  recipient: "your-email@example.com"  # 修改为您的邮箱
```

### 修改发送时间
编辑 `.github/workflows/send-newsletter.yml`:
```yaml
on:
  schedule:
    - cron: '0 1 * * 1'  # 修改cron表达式
    # 格式: 分 时 日 月 周
    # 当前: 每周一UTC 01:00 = 北京时间09:00
```

常用时间示例：
- 每周一上午9点（北京时间）: `'0 1 * * 1'`
- 每周一上午10点（北京时间）: `'0 2 * * 1'`
- 每天上午9点（北京时间）: `'0 1 * * *'`

### 自定义新闻类别
编辑 `config.yaml` 中的 `categories` 部分：
```yaml
categories:
  - id: "custom_category"
    name_en: "Custom Category Name"
    name_zh: "自定义类别名称"
    search_keywords: "your search keywords here"
    items_count: 5  # 该类别包含的新闻条数
```

## 故障排查

### 问题1: 邮件发送失败
**可能原因**: Gmail应用专用密码配置错误
**解决方案**:
1. 确认已开启两步验证
2. 重新生成应用专用密码
3. 确保密钥中没有空格（复制粘贴时注意）
4. 检查GitHub Secrets配置是否正确

### 问题2: GitHub Actions无法运行
**可能原因**: Actions权限未启用
**解决方案**:
1. 前往 Settings → Actions → General
2. 确保 "Allow all actions and reusable workflows" 已选中
3. 保存设置后重新触发workflow

### 问题3: Claude API调用失败
**可能原因**: API密钥无效或额度不足
**解决方案**:
1. 检查Anthropic Console中的API密钥状态
2. 确认账户有足够的API额度
3. 检查API密钥是否正确配置在GitHub Secrets

### 问题4: 搜索结果为空
**可能原因**: Serper API密钥问题
**解决方案**:
1. 系统会自动使用模拟数据作为备选
2. 检查Serper账户额度
3. 验证API密钥是否正确

## 费用说明

### 完全免费方案
- **GitHub Actions**: 公开仓库免费无限使用
- **Gmail SMTP**: 免费（每天500封限额）
- **Serper API**: 提供免费额度（2,500次搜索/月）
- **Anthropic Claude API**: 需要付费，但用量很小

### 预估成本
以每周运行一次计算：
- **Claude API调用**: 约$0.01-0.05/次（取决于新闻数量）
- **月成本**: 约$0.04-0.20
- **年成本**: 约$0.50-2.50

## 技术栈

- **Python 3.11**: 主要编程语言
- **Claude Sonnet 4**: AI内容总结
- **Serper API**: Google搜索API
- **Jinja2**: HTML模板渲染
- **GitHub Actions**: 自动化调度
- **Gmail SMTP**: 邮件发送

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题，请通过GitHub Issues联系。

---

**提示**: 首次部署后，建议先手动触发一次workflow进行测试，确保所有配置正确。
