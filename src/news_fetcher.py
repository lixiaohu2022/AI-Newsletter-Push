"""
AI新闻获取和总结模块
使用Web搜索和Claude API进行内容总结
"""

import os
import json
import time
from typing import List, Dict, Any
import anthropic
import requests
from bs4 import BeautifulSoup


class NewsFetcher:
    """新闻获取和处理类"""

    def __init__(self):
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")

        self.client = anthropic.Anthropic(api_key=self.anthropic_api_key)
        self.search_api_key = os.getenv('SERPER_API_KEY')  # 使用Serper.dev作为搜索API

    def search_news(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """
        使用Serper API搜索新闻

        Args:
            query: 搜索关键词
            num_results: 返回结果数量

        Returns:
            搜索结果列表
        """
        if not self.search_api_key:
            print("Warning: SERPER_API_KEY not set, using mock data")
            return self._get_mock_results(query, num_results)

        url = "https://google.serper.dev/search"

        payload = json.dumps({
            "q": query,
            "num": num_results,
            "gl": "us",
            "hl": "en"
        })

        headers = {
            'X-API-KEY': self.search_api_key,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, data=payload, timeout=10)
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get('organic', [])[:num_results]:
                results.append({
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'date': item.get('date', '')
                })

            return results

        except Exception as e:
            print(f"Search error for query '{query}': {e}")
            return self._get_mock_results(query, num_results)

    def _get_mock_results(self, query: str, num: int) -> List[Dict[str, Any]]:
        """生成模拟搜索结果（用于测试）"""
        return [
            {
                'title': f'Mock AI News Article {i+1} for: {query[:30]}',
                'link': f'https://example.com/article-{i+1}',
                'snippet': f'This is a mock article snippet about {query}. It contains relevant information about the latest developments in AI.',
                'date': '2026-01-18'
            }
            for i in range(num)
        ]

    def summarize_with_claude(self, articles: List[Dict[str, Any]], category_name_en: str,
                             category_name_zh: str, num_items: int) -> List[Dict[str, Any]]:
        """
        使用Claude API总结和筛选新闻

        Args:
            articles: 原始文章列表
            category_name_en: 类别英文名
            category_name_zh: 类别中文名
            num_items: 需要的条目数量

        Returns:
            总结后的新闻列表
        """
        if not articles:
            return []

        # 构建提示词
        articles_text = "\n\n".join([
            f"[{i+1}] Title: {article['title']}\nURL: {article['link']}\nSnippet: {article['snippet']}\nDate: {article.get('date', 'N/A')}"
            for i, article in enumerate(articles)
        ])

        prompt = f"""You are an AI news curator. From the following search results about "{category_name_en} ({category_name_zh})",
please select the top {num_items} most relevant and important articles.

For each selected article, provide:
1. A detailed summary in English (5-7 sentences covering key points, context, and implications)
2. A detailed summary in Chinese (5-7句话，涵盖要点、背景和影响)
3. The original URL
4. Why this article is significant (2-3 sentences explaining the broader impact)

Guidelines for summaries:
- Include specific details, numbers, and key facts
- Provide context and background information
- Explain the implications and why it matters
- Make it informative and valuable for professionals in the AI field

Search Results:
{articles_text}

Please respond in JSON format:
[
  {{
    "title": "Article title",
    "url": "Article URL",
    "summary_en": "Detailed English summary with specific facts and context",
    "summary_zh": "详细的中文摘要，包含具体事实和背景",
    "significance": "Why this matters and its broader implications"
  }},
  ...
]

Important: Return ONLY valid JSON array, no additional text."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = message.content[0].text.strip()

            # 清理可能的markdown代码块
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
                response_text = response_text.strip()

            summaries = json.loads(response_text)
            return summaries[:num_items]

        except Exception as e:
            print(f"Claude summarization error: {e}")
            # 返回简化版本
            return [
                {
                    'title': article['title'],
                    'url': article['link'],
                    'summary_en': article['snippet'],
                    'summary_zh': '暂无中文摘要',
                    'significance': 'Latest development in AI'
                }
                for article in articles[:num_items]
            ]

    def fetch_category_news(self, category_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取某个类别的新闻

        Args:
            category_config: 类别配置信息

        Returns:
            包含新闻列表的字典
        """
        print(f"Fetching news for: {category_config['name_en']}")

        # 搜索新闻
        search_results = self.search_news(
            category_config['search_keywords'],
            num_results=10
        )

        # 使用Claude总结
        summarized_news = self.summarize_with_claude(
            search_results,
            category_config['name_en'],
            category_config['name_zh'],
            category_config['items_count']
        )

        return {
            'category_id': category_config['id'],
            'category_name_en': category_config['name_en'],
            'category_name_zh': category_config['name_zh'],
            'news_items': summarized_news
        }
