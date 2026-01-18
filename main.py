#!/usr/bin/env python3
"""
AI新闻简报自动生成和发送主程序
"""

import os
import sys
import yaml
from datetime import datetime
from dotenv import load_dotenv

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from news_fetcher import NewsFetcher
from email_sender import EmailSender


def load_config(config_file: str = 'config.yaml') -> dict:
    """加载配置文件"""
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def main():
    """主函数"""
    print("=" * 70)
    print("AI Weekly Newsletter Generator")
    print("人工智能周报生成器")
    print("=" * 70)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 加载环境变量
    load_dotenv()

    # 加载配置
    try:
        config = load_config()
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)

    # 初始化新闻获取器和邮件发送器
    try:
        fetcher = NewsFetcher()
        sender = EmailSender()
    except Exception as e:
        print(f"Error initializing modules: {e}")
        sys.exit(1)

    # 获取各类别新闻
    all_categories = []
    print("\n" + "=" * 70)
    print("STEP 1: Fetching and summarizing news")
    print("=" * 70)

    for category_config in config['categories']:
        try:
            print(f"\n📰 Processing: {category_config['name_en']}")
            print(f"   {category_config['name_zh']}")
            print(f"   Keywords: {category_config['search_keywords']}")

            category_data = fetcher.fetch_category_news(category_config)
            all_categories.append(category_data)

            print(f"   ✅ Found {len(category_data['news_items'])} items")

        except Exception as e:
            print(f"   ❌ Error processing category: {e}")
            # 添加空类别以保持结构
            all_categories.append({
                'category_id': category_config['id'],
                'category_name_en': category_config['name_en'],
                'category_name_zh': category_config['name_zh'],
                'news_items': []
            })

    # 发送邮件
    print("\n" + "=" * 70)
    print("STEP 2: Sending newsletter email")
    print("=" * 70)

    newsletter_config = config['newsletter']

    try:
        print(f"\n📧 Sending to: {newsletter_config['recipient']}")
        print(f"   Subject: {newsletter_config['subject']}")

        success = sender.send_newsletter(
            recipient=newsletter_config['recipient'],
            subject=newsletter_config['subject'],
            categories=all_categories,
            sender_name=newsletter_config['sender_name']
        )

        if success:
            print("\n✅ Newsletter sent successfully!")
        else:
            print("\n❌ Failed to send newsletter")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error sending email: {e}")
        sys.exit(1)

    # 完成
    print("\n" + "=" * 70)
    print("Process completed successfully!")
    print("=" * 70)
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


if __name__ == "__main__":
    main()
