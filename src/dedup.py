"""
文章去重模块
维护已发送文章历史，过滤重复内容
"""

import json
import os
import re
from datetime import datetime, timedelta
from difflib import SequenceMatcher
from typing import List, Dict, Any, Tuple
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode


HISTORY_PATH = "data/sent_articles.json"
TITLE_SIMILARITY_THRESHOLD = 0.85
HISTORY_RETENTION_DAYS = 90
SCHEMA_VERSION = 1


class ArticleDeduplicator:
    """管理已发送文章历史并过滤重复文章"""

    def __init__(self, history_path: str = HISTORY_PATH):
        self.history_path = history_path
        self.history = self._load_history()

    def _load_history(self) -> Dict[str, Any]:
        """从JSON文件加载历史记录。首次运行或出错时返回空结构。"""
        if not os.path.exists(self.history_path):
            print(f"   [DEDUP] No history file found at {self.history_path}. Starting fresh.")
            return self._empty_history()

        try:
            with open(self.history_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if data.get("version") != SCHEMA_VERSION:
                print(f"   [DEDUP] Warning: History schema version mismatch. Starting fresh.")
                return self._empty_history()

            if "articles" not in data or not isinstance(data["articles"], list):
                print("   [DEDUP] Warning: Invalid history file structure. Starting fresh.")
                return self._empty_history()

            print(f"   [DEDUP] Loaded {len(data['articles'])} articles from history.")
            return data

        except (json.JSONDecodeError, IOError) as e:
            print(f"   [DEDUP] Warning: Could not load history file ({e}). Starting fresh.")
            return self._empty_history()

    @staticmethod
    def _empty_history() -> Dict[str, Any]:
        return {
            "version": SCHEMA_VERSION,
            "last_updated": None,
            "articles": []
        }

    @staticmethod
    def normalize_url(url: str) -> str:
        """标准化URL用于比较：小写域名、去跟踪参数、去尾部斜杠、去fragment"""
        try:
            parsed = urlparse(url)
            netloc = parsed.netloc.lower()
            if parsed.query:
                params = parse_qs(parsed.query, keep_blank_values=True)
                filtered = {
                    k: v for k, v in params.items()
                    if not k.startswith('utm_') and k not in ('ref', 'source', 'fbclid', 'gclid')
                }
                query = urlencode(filtered, doseq=True)
            else:
                query = ''
            path = parsed.path.rstrip('/')
            return urlunparse((parsed.scheme, netloc, path, parsed.params, query, ''))
        except Exception:
            return url.lower().rstrip('/')

    @staticmethod
    def title_similarity(title1: str, title2: str) -> float:
        """计算两个标题的相似度（0.0 到 1.0）"""
        t1 = re.sub(r'[^\w\s]', '', title1.lower().strip())
        t2 = re.sub(r'[^\w\s]', '', title2.lower().strip())
        return SequenceMatcher(None, t1, t2).ratio()

    def is_duplicate(self, url: str, title: str) -> bool:
        """检查文章是否与已发送的文章重复"""
        normalized_url = self.normalize_url(url)

        for article in self.history["articles"]:
            # 主要检查：URL精确匹配
            stored_url = article.get("url_normalized") or self.normalize_url(article.get("url", ""))
            if stored_url == normalized_url:
                return True

            # 辅助检查：标题相似度
            if self.title_similarity(title, article.get("title", "")) >= TITLE_SIMILARITY_THRESHOLD:
                return True

        return False

    def filter_articles(self, articles: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
        """过滤搜索结果中的重复文章。

        Args:
            articles: 搜索结果列表，每项包含 'title' 和 'link' 键。

        Returns:
            (过滤后的文章列表, 被移除的数量)
        """
        filtered = []
        removed = 0

        for article in articles:
            url = article.get('link', article.get('url', ''))
            title = article.get('title', '')

            if self.is_duplicate(url, title):
                print(f"   [DEDUP] Skipping duplicate: {title[:60]}...")
                removed += 1
            else:
                filtered.append(article)

        return filtered, removed

    def record_articles(self, articles: List[Dict[str, Any]], category_id: str):
        """将本次选中的文章记录到内存中的历史"""
        today = datetime.now().strftime('%Y-%m-%d')

        for article in articles:
            url = article.get('url', article.get('link', ''))
            title = article.get('title', '')

            self.history["articles"].append({
                "url": url,
                "url_normalized": self.normalize_url(url),
                "title": title,
                "category_id": category_id,
                "sent_date": today
            })

    def _prune_old_entries(self):
        """移除超过保留期限的历史条目"""
        cutoff = (datetime.now() - timedelta(days=HISTORY_RETENTION_DAYS)).strftime('%Y-%m-%d')
        original_count = len(self.history["articles"])

        self.history["articles"] = [
            a for a in self.history["articles"]
            if a.get("sent_date", "9999-99-99") >= cutoff
        ]

        pruned = original_count - len(self.history["articles"])
        if pruned > 0:
            print(f"   [DEDUP] Pruned {pruned} articles older than {HISTORY_RETENTION_DAYS} days")

    def save_history(self):
        """保存历史到JSON文件。自动创建目录并清理过期条目。"""
        self._prune_old_entries()
        self.history["last_updated"] = datetime.now().isoformat()

        os.makedirs(os.path.dirname(self.history_path), exist_ok=True)

        try:
            with open(self.history_path, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            print(f"   [DEDUP] History saved ({len(self.history['articles'])} articles)")
        except IOError as e:
            print(f"   [DEDUP] Warning: Failed to save history: {e}")
