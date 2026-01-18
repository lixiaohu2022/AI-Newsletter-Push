# AI Weekly Newsletter - 项目概览

## 项目信息

**项目名称**: AI Weekly Newsletter (人工智能周报自动化系统)
**创建日期**: 2026-01-18
**目标用户**: Lingjian.li84@gmail.com
**运行频率**: 每周一上午9:00（北京时间）

---

## 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                   GitHub Actions                        │
│              (每周一 UTC 01:00 触发)                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   main.py                               │
│              (主程序协调器)                              │
└───────┬─────────────────────────┬───────────────────────┘
        │                         │
        ▼                         ▼
┌──────────────────┐    ┌────────────────────┐
│  news_fetcher.py │    │  email_sender.py   │
│   新闻获取模块    │    │   邮件发送模块      │
└────┬─────────────┘    └──────┬─────────────┘
     │                         │
     │  ┌──────────────┐      │  ┌─────────────────┐
     ├─→│ Serper API   │      └─→│  Gmail SMTP     │
     │  │ (Google搜索) │         │  (邮件发送)      │
     │  └──────────────┘         └─────────────────┘
     │
     │  ┌──────────────┐
     └─→│ Claude API   │
        │ (AI总结)     │
        └──────────────┘
```

---

## 数据流程

```
1. GitHub Actions定时触发
   ↓
2. 读取config.yaml配置
   ↓
3. 对每个新闻类别:
   ├─ 使用Serper API搜索最新新闻
   ├─ 使用Claude AI总结和筛选
   └─ 生成中英文双语摘要
   ↓
4. 使用Jinja2渲染HTML邮件模板
   ↓
5. 通过Gmail SMTP发送邮件
   ↓
6. 邮件送达: Lingjian.li84@gmail.com
```

---

## 核心功能模块

### 1. 新闻获取模块 (`src/news_fetcher.py`)

**主要功能**:
- 使用Serper API进行Google搜索
- 调用Claude API进行内容总结
- 支持中英文双语输出
- 内置错误处理和降级方案

**关键方法**:
- `search_news()`: 搜索新闻
- `summarize_with_claude()`: AI总结
- `fetch_category_news()`: 获取分类新闻

### 2. 邮件发送模块 (`src/email_sender.py`)

**主要功能**:
- HTML邮件模板渲染（Jinja2）
- Gmail SMTP发送
- 支持纯文本备用版本
- 邮件格式优化

**关键方法**:
- `render_newsletter()`: 渲染模板
- `send_newsletter()`: 发送邮件
- `_create_text_version()`: 生成纯文本版本

### 3. 主程序 (`main.py`)

**主要功能**:
- 协调整个流程
- 加载配置和环境变量
- 错误处理和日志输出
- 进度跟踪

---

## 配置文件说明

### `config.yaml` - 主配置

```yaml
# 邮件配置
newsletter:
  subject: "邮件主题"
  recipient: "收件人邮箱"
  sender_name: "发件人名称"

# 新闻类别 (可自定义)
categories:
  - id: "唯一标识"
    name_en: "英文名称"
    name_zh: "中文名称"
    search_keywords: "搜索关键词"
    items_count: 5  # 条目数量
```

### `.env` - 环境变量 (本地测试)

```env
ANTHROPIC_API_KEY=your_key
SERPER_API_KEY=your_key
GMAIL_SENDER=your_email
GMAIL_APP_PASSWORD=your_password
```

### GitHub Secrets (生产环境)

在GitHub仓库Settings中配置同名Secrets

---

## 新闻分类

当前配置了4个类别，每个类别3-5条新闻：

1. **全球AI最前沿动态** (5条)
   - 关键词: "artificial intelligence breakthrough latest 2026"
   - 关注最新技术突破和研究成果

2. **企业AI应用最佳实践** (4条)
   - 关键词: "AI enterprise implementation case study 2026"
   - 关注企业级应用案例

3. **工程咨询行业AI动态** (3条)
   - 关键词: "AI consulting engineering industry 2026"
   - 关注咨询和工程行业的AI应用

4. **AI职业发展** (4条)
   - 关键词: "AI career skills professional development 2026"
   - 关注个人技能提升和职业发展

**总计**: 16条新闻/周

---

## 运行时间安排

### GitHub Actions Cron设置
```yaml
cron: '0 1 * * 1'
```

**解释**:
- `0` - 第0分钟
- `1` - UTC时间1点
- `*` - 每月的每一天
- `*` - 每个月
- `1` - 星期一 (0=周日, 1=周一, ..., 6=周六)

**等价于**: 每周一 UTC 01:00 = 北京时间 09:00

---

## 依赖项

### Python包 (`requirements.txt`)
```
anthropic>=0.40.0      # Claude AI SDK
requests>=2.31.0       # HTTP请求
python-dotenv>=1.0.0   # 环境变量管理
jinja2>=3.1.2          # 模板引擎
beautifulsoup4>=4.12.0 # HTML解析
pyyaml>=6.0.1          # YAML配置解析
```

### 外部服务
- **Anthropic Claude API**: AI内容总结
- **Serper API**: Google搜索
- **Gmail SMTP**: 邮件发送
- **GitHub Actions**: 定时任务调度

---

## 成本分析

### 免费额度
- GitHub Actions: ✅ 无限制（公开仓库）
- Gmail SMTP: ✅ 500封/天
- Serper API: ✅ 2,500次搜索/月

### 付费部分
- Anthropic Claude API:
  - 模型: Claude Sonnet 4
  - 估算: $0.01-0.05/次运行
  - 月成本: ~$0.04-0.20
  - 年成本: ~$0.50-2.50

**结论**: 几乎免费（每月不到$0.20）

---

## 邮件内容结构

```html
┌─────────────────────────────────────┐
│      🤖 AI Weekly Newsletter       │
│         人工智能周报                │
├─────────────────────────────────────┤
│   📅 2026-01-20 Monday             │
├─────────────────────────────────────┤
│                                     │
│ ■ Global AI Frontier Trends        │
│   全球AI最前沿动态                  │
│   ├─ 新闻1 [标题+链接]             │
│   │  • English Summary             │
│   │  • 中文摘要                     │
│   │  💡 Significance               │
│   ├─ 新闻2-5 ...                   │
│                                     │
│ ■ Enterprise AI Best Practices     │
│   企业AI应用最佳实践                │
│   ├─ 新闻1-4 ...                   │
│                                     │
│ ■ Engineering & Consulting         │
│   工程咨询行业AI动态                │
│   ├─ 新闻1-3 ...                   │
│                                     │
│ ■ AI Career Development            │
│   AI职业发展                        │
│   ├─ 新闻1-4 ...                   │
│                                     │
├─────────────────────────────────────┤
│  Powered by Claude AI & Python     │
└─────────────────────────────────────┘
```

---

## 关键特性

✅ **完全自动化**: 无需人工干预
✅ **智能筛选**: AI自动选择最相关的新闻
✅ **双语支持**: 每条新闻都有中英文摘要
✅ **精美排版**: 响应式HTML设计
✅ **可靠稳定**: 内置错误处理和降级方案
✅ **易于扩展**: 模块化设计，便于添加功能
✅ **低成本**: 几乎免费运行

---

## 未来扩展可能性

### 短期优化
- [ ] 添加新闻去重功能
- [ ] 优化Claude提示词以提高摘要质量
- [ ] 添加邮件发送失败重试机制
- [ ] 支持多个收件人

### 中期功能
- [ ] 添加Web界面查看历史简报
- [ ] 支持RSS订阅输出
- [ ] 添加新闻来源多样性（不仅限于Google搜索）
- [ ] 支持用户自定义类别

### 长期愿景
- [ ] 开发用户订阅系统
- [ ] 支持个性化推荐
- [ ] 添加机器学习模型优化内容筛选
- [ ] 多语言支持（不仅限于中英文）

---

## 维护建议

### 定期检查
- ✓ 每月检查API额度使用情况
- ✓ 每季度检查邮件内容质量
- ✓ 每半年更新搜索关键词

### 监控指标
- GitHub Actions运行成功率
- 邮件送达率
- API调用成功率
- 成本变化趋势

---

## 文档索引

1. **README.md** - 完整使用文档
2. **SETUP_GUIDE.md** - 快速设置指南
3. **PROJECT_OVERVIEW.md** (本文件) - 项目概览
4. **.env.example** - 环境变量示例

---

**最后更新**: 2026-01-18
**维护者**: Lingjian Li
**状态**: ✅ 生产就绪
