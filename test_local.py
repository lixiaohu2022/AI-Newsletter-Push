#!/usr/bin/env python3
"""
本地测试脚本
用于测试各个模块功能而不实际发送邮件
"""

import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from news_fetcher import NewsFetcher
from email_sender import EmailSender


def test_search():
    """测试搜索功能"""
    print("\n" + "="*60)
    print("测试1: 搜索API")
    print("="*60)

    fetcher = NewsFetcher()

    # 测试搜索
    results = fetcher.search_news("artificial intelligence", num_results=3)

    print(f"\n找到 {len(results)} 条结果:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   URL: {result['link']}")
        print(f"   摘要: {result['snippet'][:100]}...")


def test_summarization():
    """测试AI总结功能"""
    print("\n" + "="*60)
    print("测试2: Claude AI总结")
    print("="*60)

    fetcher = NewsFetcher()

    # 获取测试数据
    articles = fetcher.search_news("AI breakthroughs 2026", num_results=5)

    print(f"\n正在使用Claude总结 {len(articles)} 条新闻...")

    # 总结
    summaries = fetcher.summarize_with_claude(
        articles,
        "AI Breakthroughs",
        "AI突破进展",
        num_items=3
    )

    print(f"\n总结完成，筛选出 {len(summaries)} 条:")
    for i, item in enumerate(summaries, 1):
        print(f"\n{i}. {item['title']}")
        print(f"   英文: {item['summary_en']}")
        print(f"   中文: {item['summary_zh']}")
        print(f"   重要性: {item.get('significance', 'N/A')}")


def test_email_rendering():
    """测试邮件渲染功能"""
    print("\n" + "="*60)
    print("测试3: HTML邮件渲染")
    print("="*60)

    sender = EmailSender()

    # 模拟数据
    test_data = [
        {
            'category_id': 'test',
            'category_name_en': 'Test Category',
            'category_name_zh': '测试类别',
            'news_items': [
                {
                    'title': 'Test Article 1',
                    'url': 'https://example.com/1',
                    'summary_en': 'This is a test English summary.',
                    'summary_zh': '这是测试中文摘要。',
                    'significance': 'This is a test significance note.'
                },
                {
                    'title': 'Test Article 2',
                    'url': 'https://example.com/2',
                    'summary_en': 'Another test English summary.',
                    'summary_zh': '另一个测试中文摘要。',
                    'significance': 'Another test significance note.'
                }
            ]
        }
    ]

    # 渲染
    html = sender.render_newsletter(test_data)

    # 保存到文件
    output_file = "test_newsletter.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n✅ HTML邮件已生成: {output_file}")
    print(f"   文件大小: {len(html)} 字节")
    print(f"   请在浏览器中打开查看效果")


def test_dedup():
    """测试去重功能"""
    print("\n" + "="*60)
    print("测试5: 文章去重")
    print("="*60)

    from dedup import ArticleDeduplicator

    test_path = "data/test_sent_articles.json"

    # 清理可能残留的测试文件
    if os.path.exists(test_path):
        os.remove(test_path)

    dedup = ArticleDeduplicator(history_path=test_path)

    # 模拟已发送文章
    dedup.record_articles([
        {"url": "https://example.com/article-1", "title": "AI Breakthrough in Healthcare"},
        {"url": "https://example.com/article-2?utm_source=twitter", "title": "New GPT Model Released"},
    ], category_id="test")

    print("\n已记录2篇历史文章:")
    print("  - AI Breakthrough in Healthcare (example.com/article-1)")
    print("  - New GPT Model Released (example.com/article-2?utm_source=twitter)")

    # 测试过滤
    new_articles = [
        {"title": "AI Breakthrough in Healthcare", "link": "https://example.com/article-1", "snippet": "Exact URL match"},
        {"title": "AI Breakthrough in Healthcare Sector", "link": "https://other.com/similar", "snippet": "Similar title"},
        {"title": "New GPT Model Released", "link": "https://example.com/article-2", "snippet": "Same URL without utm"},
        {"title": "Completely New Article About Robotics", "link": "https://example.com/article-3", "snippet": "Brand new"},
        {"title": "Another Fresh Article on Quantum Computing", "link": "https://example.com/article-4", "snippet": "Also new"},
    ]

    print(f"\n测试过滤 {len(new_articles)} 篇新文章:")
    filtered, removed = dedup.filter_articles(new_articles)

    print(f"\n结果: 移除 {removed} 篇重复, 保留 {len(filtered)} 篇")
    for a in filtered:
        print(f"  ✅ {a['title']}")

    # 验证
    assert removed == 3, f"Expected 3 removed, got {removed}"
    assert len(filtered) == 2, f"Expected 2 remaining, got {len(filtered)}"
    assert filtered[0]['title'] == "Completely New Article About Robotics"
    assert filtered[1]['title'] == "Another Fresh Article on Quantum Computing"

    # 测试保存和加载
    dedup.save_history()
    dedup2 = ArticleDeduplicator(history_path=test_path)
    assert len(dedup2.history["articles"]) == 2, "History should have 2 articles after save/load"

    # 清理
    os.remove(test_path)

    print("\n✅ 去重测试全部通过!")


def test_full_workflow():
    """测试完整工作流（不发送邮件）"""
    print("\n" + "="*60)
    print("测试4: 完整工作流（不发送邮件）")
    print("="*60)

    fetcher = NewsFetcher()
    sender = EmailSender()

    # 简化的配置
    test_categories = [
        {
            'id': 'test1',
            'name_en': 'Global AI Trends',
            'name_zh': '全球AI动态',
            'search_keywords': 'artificial intelligence news 2026',
            'items_count': 2
        }
    ]

    all_data = []

    for category in test_categories:
        print(f"\n处理类别: {category['name_en']}")
        category_data = fetcher.fetch_category_news(category)
        all_data.append(category_data)
        print(f"✅ 获取到 {len(category_data['news_items'])} 条新闻")

    # 渲染HTML
    html = sender.render_newsletter(all_data)

    # 保存
    output_file = "test_full_newsletter.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n✅ 完整简报已生成: {output_file}")


def main():
    """主函数"""
    print("="*60)
    print("AI Newsletter 本地测试工具")
    print("="*60)

    # 加载环境变量
    load_dotenv()

    # 检查必需的环境变量
    required_vars = ['ANTHROPIC_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"\n⚠️  警告: 缺少环境变量: {', '.join(missing_vars)}")
        print("   某些测试可能无法运行")
        print("   请创建 .env 文件并配置必要的API密钥\n")

    # 菜单
    while True:
        print("\n请选择测试项目:")
        print("1. 测试搜索API")
        print("2. 测试Claude AI总结")
        print("3. 测试HTML邮件渲染")
        print("4. 测试完整工作流")
        print("5. 测试文章去重")
        print("6. 运行所有测试")
        print("0. 退出")

        choice = input("\n输入选项 (0-6): ").strip()

        try:
            if choice == '0':
                print("\n再见！")
                break
            elif choice == '1':
                test_search()
            elif choice == '2':
                test_summarization()
            elif choice == '3':
                test_email_rendering()
            elif choice == '4':
                test_full_workflow()
            elif choice == '5':
                test_dedup()
            elif choice == '6':
                test_search()
                test_summarization()
                test_email_rendering()
                test_full_workflow()
                test_dedup()
            else:
                print("\n⚠️  无效选项，请重新选择")

        except KeyboardInterrupt:
            print("\n\n测试被中断")
            break
        except Exception as e:
            print(f"\n❌ 测试出错: {e}")
            import traceback
            traceback.print_exc()

        input("\n按回车键继续...")


if __name__ == "__main__":
    main()
