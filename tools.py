import os
import requests
from pydantic import BaseModel, Field
from typing import List, Dict
from dotenv import load_dotenv

from langchain.tools import Tool
from tavily import TavilyClient
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")

class QueryInput(BaseModel):
    query: str = Field(..., description="Search query string")

class ComponentsInput(BaseModel):
    components: str = Field(..., description="Comma-separated electronic components list")

class ToolsMain:
    def __init__(self):
        self.youtube_api_key = YOUTUBE_API_KEY
        self.github_api_key = GITHUB_API_KEY
        self.tavily_api_key = TAVILY_API_KEY

        self.tavily_client = TavilyClient(api_key=self.tavily_api_key) if self.tavily_api_key else None
        self.ddg = DuckDuckGoSearchAPIWrapper()

        self.youtube_tool = Tool(
            name="youtube_search",
            description="Search YouTube and return top videos with titles, channels, and links.",
            func=self.search_youtube_wrapped,
            args_schema=QueryInput,
        )

        self.github_tool = Tool(
            name="github_search",
            description="Search GitHub repositories by topic and return top starred repos.",
            func=self.github_search_tool,
            args_schema=QueryInput,
        )

        self.tavily_tool = Tool(
            name="component_info_search",
            description="Fetch component specs, prices, and purchase links from online stores.",
            func=self.component_info_tool,
            args_schema=ComponentsInput,
        )

        self.ddg_tool = Tool(
            name="duckduckgo_search",
            description="General-purpose web search using DuckDuckGo for project information.",
            func=self.ddg_search,
            args_schema=QueryInput,
        )

    # Expert-Level YouTube API Integration
    def search_youtube(self, query: str, max_results: int = 10, 
                      advanced_params: Dict = None) -> List[Dict]:
        """Expert-level YouTube search with advanced filtering and parameters"""
        
        if not self.youtube_api_key:
            raise RuntimeError("Missing YOUTUBE_API_KEY in environment.")

        # Simplified parameter configuration to avoid API issues
        default_params = {
            "part": "snippet",
            "type": "video",
            "maxResults": max_results,
            "key": self.youtube_api_key,
            "safeSearch": "moderate",
            "videoDuration": "medium",  # 4-20 minutes
            "order": "relevance"
        }
        
        # Apply advanced parameters if provided
        if advanced_params:
            default_params.update(advanced_params)
        
        # Enhanced query construction with exclusions
        enhanced_query = self._build_enhanced_query(query)
        default_params["q"] = enhanced_query
        
        print(f"🔍 Expert YouTube Search: {enhanced_query}")
        print(f"📊 Advanced Parameters: {advanced_params}")

        # Execute search API call
        url = "https://www.googleapis.com/youtube/v3/search"
        try:
            resp = requests.get(url, params=default_params, timeout=20)
            resp.raise_for_status()
            search_data = resp.json()
        except Exception as e:
            raise RuntimeError(f"YouTube search API failed: {e}")

        # Get additional video details for better filtering
        video_ids = []
        for item in search_data.get("items", []):
            vid = (item.get("id", {}) or {}).get("videoId")
            if vid:
                video_ids.append(vid)
        
        # Fetch detailed video information
        detailed_videos = {}
        if video_ids:
            detailed_videos = self._fetch_video_details(video_ids)
        
        # Process and filter results with expert criteria
        results = self._process_expert_youtube_results(
            search_data.get("items", []), detailed_videos, query
        )
        
        return results
    
    def _build_enhanced_query(self, query: str) -> str:
        """Build enhanced search query with smart exclusions and inclusions"""
        
        # Simplified exclusions to avoid query length issues
        exclusions = ["-shorts", "-meme", "-funny", "-reaction"]
        
        # Smart inclusions for quality tutorial content
        if any(term in query.lower() for term in ['tutorial', 'guide', 'how to']):
            # Already has tutorial indicators
            enhanced_query = query
        else:
            # Add tutorial context
            enhanced_query = f"{query} tutorial"
        
        # Add key exclusions only
        enhanced_query += " " + " ".join(exclusions[:3])  # Limit to 3 exclusions
        
        return enhanced_query
    
    def _fetch_video_details(self, video_ids: List[str]) -> Dict[str, Dict]:
        """Fetch detailed video information including duration, views, etc."""
        
        if not video_ids:
            return {}
        
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "contentDetails,statistics,snippet",
            "id": ",".join(video_ids),
            "key": self.youtube_api_key
        }
        
        try:
            resp = requests.get(url, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            
            # Create lookup dictionary
            video_details = {}
            for item in data.get("items", []):
                video_id = item.get("id")
                if video_id:
                    content_details = item.get("contentDetails", {})
                    statistics = item.get("statistics", {})
                    snippet = item.get("snippet", {})
                    
                    video_details[video_id] = {
                        "duration": content_details.get("duration", ""),
                        "view_count": int(statistics.get("viewCount", 0)),
                        "like_count": int(statistics.get("likeCount", 0)),
                        "comment_count": int(statistics.get("commentCount", 0)),
                        "published_at": snippet.get("publishedAt", ""),
                        "category_id": snippet.get("categoryId", ""),
                        "tags": snippet.get("tags", [])
                    }
            
            return video_details
            
        except Exception as e:
            print(f"⚠️ Failed to fetch video details: {e}")
            return {}
    
    def _process_expert_youtube_results(self, search_items: List[Dict], 
                                      detailed_videos: Dict[str, Dict], 
                                      original_query: str) -> List[Dict]:
        """Process search results with expert-level filtering and scoring"""
        
        results = []
        
        for item in search_items:
            snippet = item.get("snippet", {}) or {}
            vid = (item.get("id", {}) or {}).get("videoId")
            if not vid:
                continue

            title = snippet.get("title", "Untitled")
            description = snippet.get("description", "") or ""
            channel = snippet.get("channelTitle", "Unknown")
            published = snippet.get("publishedAt", "")
            
            # Get detailed video information
            video_details = detailed_videos.get(vid, {})
            duration_seconds = self._parse_youtube_duration(video_details.get("duration", ""))
            view_count = video_details.get("view_count", 0)
            like_count = video_details.get("like_count", 0)
            tags = video_details.get("tags", [])
            
            # Apply expert-level quality filtering
            quality_score = self._calculate_expert_video_quality(
                title, description, channel, duration_seconds, 
                view_count, like_count, tags, original_query
            )
            
            # Filter based on quality threshold
            if quality_score < 50:  # Minimum quality threshold
                continue
            
            # Build enhanced result object
            thumbs = (snippet.get("thumbnails", {}) or {})
            thumb = (
                (thumbs.get("high") or {}).get("url")
                or (thumbs.get("medium") or {}).get("url")
                or (thumbs.get("default") or {}).get("url")
            )

            result = {
                "title": title,
                "description": description,
                "video_url": f"https://www.youtube.com/watch?v={vid}",
                "thumbnail": thumb or "",
                "channel": channel,
                "published_at": published,
                "duration_seconds": duration_seconds,
                "duration_formatted": self._format_duration(duration_seconds),
                "view_count": view_count,
                "like_count": like_count,
                "quality_score": quality_score,
                "tags": tags[:5]  # Top 5 tags
            }
            
            results.append(result)
        
        # Sort by quality score (descending)
        results.sort(key=lambda x: x.get("quality_score", 0), reverse=True)
        
        return results
    
    def _parse_youtube_duration(self, duration_str: str) -> int:
        """Parse YouTube API duration format (PT4M13S) to seconds"""
        
        if not duration_str or not duration_str.startswith('PT'):
            return 0
        
        import re
        
        # Extract hours, minutes, seconds using regex
        pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
        match = re.match(pattern, duration_str)
        
        if not match:
            return 0
        
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        seconds = int(match.group(3)) if match.group(3) else 0
        
        return hours * 3600 + minutes * 60 + seconds
    
    def _format_duration(self, seconds: int) -> str:
        """Format duration in human-readable format"""
        
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            secs = seconds % 60
            return f"{minutes}m {secs}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h {minutes}m"
    
    def _calculate_expert_video_quality(self, title: str, description: str, 
                                      channel: str, duration: int, views: int, 
                                      likes: int, tags: List[str], query: str) -> int:
        """Calculate expert-level video quality score"""
        
        score = 0
        title_lower = title.lower()
        desc_lower = description.lower()
        query_lower = query.lower()
        
        # 1. Content Quality Indicators (40 points max)
        premium_terms = [
            'complete', 'full course', 'comprehensive', 'step by step', 
            'tutorial', 'guide', 'masterclass', 'from scratch', 'build'
        ]
        score += sum(8 for term in premium_terms if term in title_lower) * 0.5
        
        # 2. Query Relevance (30 points max)
        query_words = query_lower.split()
        title_matches = sum(10 for word in query_words if word in title_lower)
        desc_matches = sum(5 for word in query_words if word in desc_lower)
        score += min(30, title_matches + desc_matches)
        
        # 3. Duration Quality (15 points max)
        if 300 <= duration <= 3600:  # 5-60 minutes (ideal for tutorials)
            score += 15
        elif 180 <= duration < 300 or 3600 < duration <= 7200:  # 3-5 min or 1-2 hours
            score += 10
        elif duration > 60:  # At least 1 minute
            score += 5
        
        # 4. Engagement Metrics (10 points max)
        if views > 50000:
            score += 6
        elif views > 10000:
            score += 4
        elif views > 1000:
            score += 2
        
        if likes > 0 and views > 0:
            like_ratio = likes / views
            if like_ratio > 0.05:  # 5% like ratio
                score += 4
            elif like_ratio > 0.02:  # 2% like ratio
                score += 2
        
        # 5. Channel Quality (5 points max)
        quality_channels = [
            'traversy media', 'freecodecamp', 'code with mosh', 'programming with mosh',
            'the net ninja', 'academind', 'clever programmer', 'tech with tim',
            'corey schafer', 'sentdex', 'derek banas', 'new think tank'
        ]
        
        if any(ch in channel.lower() for ch in quality_channels):
            score += 5
        elif len(channel) > 5 and not any(word in channel.lower() for word in ['test', 'temp']):
            score += 2
        
        # Penalties for low-quality indicators
        exclude_terms = [
            'shorts', '#shorts', 'meme', 'funny', 'reaction', 'tiktok', 
            'quick', '60 seconds', '1 minute', 'clickbait'
        ]
        
        penalty = sum(15 for term in exclude_terms if term in title_lower)
        score = max(0, score - penalty)
        
        return min(100, score)  # Cap at 100
    
    def search_youtube_with_google_custom_search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Optional: Enhanced YouTube search using Google Custom Search API for validation"""
        
        # This method can be implemented if Google Custom Search API key is available
        # It would provide additional validation and supplementary results
        
        try:
            # Primary YouTube API search
            youtube_results = self.search_youtube(query, max_results)
            
            # Optional: Add Google Custom Search validation here
            # This would require GOOGLE_CUSTOM_SEARCH_API_KEY and SEARCH_ENGINE_ID
            
            return youtube_results
            
        except Exception as e:
            print(f"Enhanced YouTube search failed, falling back to standard search: {e}")
            return self.search_youtube(query, max_results)


    def search_youtube_wrapped(self, query: str) -> str:
        """Enhanced YouTube search wrapper with expert-level results formatting"""
        
        q = (query or "").strip()
        if not q:
            return "Please provide a non-empty search query for YouTube."

        try:
            # Use expert-level search with advanced parameters
            advanced_params = {
                "videoDuration": "medium",  # Prefer 4-20 minute videos
                "order": "relevance",
                "videoDefinition": "high",
                "relevanceLanguage": "en"
            }
            
            results = self.search_youtube(q, max_results=6, advanced_params=advanced_params)
        except Exception as e:
            return f"Error: {e}"

        if not results:
            return "No videos found."

        # Format results with enhanced information
        lines = []
        for i, r in enumerate(results, 1):
            title = r.get('title', 'Untitled')
            channel = r.get('channel', 'Unknown')
            url = r.get('video_url', '')
            duration = r.get('duration_formatted', 'Unknown duration')
            views = r.get('view_count', 0)
            quality_score = r.get('quality_score', 0)
            
            # Format view count
            if views >= 1000000:
                view_str = f"{views/1000000:.1f}M views"
            elif views >= 1000:
                view_str = f"{views/1000:.1f}K views"
            else:
                view_str = f"{views} views"
            
            # Description with smart truncation
            desc = (r.get("description") or "").strip()
            if len(desc) > 180:
                desc = desc[:177] + "..."
            
            # Enhanced formatting with metadata
            lines.append(
                f"🎥 {title}\n"
                f"   📺 Channel: {channel} | ⏱️ Duration: {duration} | 👀 {view_str}\n"
                f"   🔗 {url}\n"
                f"   📝 {desc}\n"
                f"   ⭐ Quality Score: {quality_score}/100"
            )
        
        header = f"🔍 Found {len(results)} high-quality YouTube tutorials for: '{q}'\n" + "="*60 + "\n"
        return header + "\n\n".join(lines)

    # GitHub 
    def github_search_tool(self, query: str) -> str:
        q = (query or "").strip()
        if not q:
            return "Please provide a non-empty search query for GitHub."

        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "langchain-tool",
        }
        if self.github_api_key:
            headers["Authorization"] = f"Bearer {self.github_api_key}"

        # Enhanced search with better filtering
        search_query = f"{q} NOT homework NOT assignment NOT practice NOT test NOT hello-world"
        url = f"https://api.github.com/search/repositories?q={search_query}&sort=stars&order=desc&per_page=8"

        try:
            res = requests.get(url, headers=headers, timeout=15)
            res.raise_for_status()
            data = res.json()
        except requests.HTTPError as e:
            status = e.response.status_code if e.response else "unknown"
            if status in (401, 403):
                auth_msg = " (authentication may be missing or rate limit exceeded)"
            else:
                auth_msg = ""
            return f"GitHub search failed with HTTP {status}{auth_msg}."
        except Exception as e:
            return f"GitHub search failed: {e}"

        items = data.get("items", []) or []
        if not items:
            return "No results found."

        # Filter and rank repositories
        quality_repos = []
        for repo in items:
            if self._is_quality_repo(repo, q):
                quality_repos.append(repo)

        if not quality_repos:
            quality_repos = items[:5]  # Fallback to original results

        out_lines = []
        for repo in quality_repos[:5]:
            name = repo.get("full_name", "unknown")
            stars = repo.get("stargazers_count", 0)
            html = repo.get("html_url", "")
            desc = (repo.get("description") or "").strip()
            language = repo.get("language", "")
            updated = repo.get("updated_at", "")[:10]  # Get date part only
            
            desc_with_info = f"{desc}"
            if language:
                desc_with_info += f" | Language: {language}"
            if updated:
                desc_with_info += f" | Updated: {updated}"
                
            out_lines.append(f"- {name} ⭐ ({stars} stars)\n  {html}\n  {desc_with_info}")
        return "\n\n".join(out_lines)
    
    def _is_quality_repo(self, repo: dict, query: str) -> bool:
        """Filter for quality repositories"""
        name = repo.get("full_name", "").lower()
        desc = (repo.get("description") or "").lower()
        stars = repo.get("stargazers_count", 0)
        
        # Exclude low-quality indicators
        exclude_terms = ['homework', 'assignment', 'practice', 'test', 'hello-world', 'copy', 'clone', 'fork-only']
        if any(term in name or term in desc for term in exclude_terms):
            return False
            
        # Prefer repositories with good descriptions and some stars
        if not desc.strip() and stars < 5:
            return False
            
        # Check query relevance
        query_words = query.lower().split()
        relevance_score = sum(1 for word in query_words if word in name or word in desc)
        
        return relevance_score > 0 or stars > 50  # Either relevant or popular

    # Tavily (components) 
    def component_info_tool(self, components: str) -> str:
        raw = (components or "").strip()
        if not raw:
            return "Please provide at least one component name (comma-separated)."
        if not self.tavily_client:
            return "Missing TAVILY_API_KEY in environment."

        components_list = [c.strip() for c in raw.split(",") if c.strip()]
        if not components_list:
            return "Please provide valid component names."

        sections: List[str] = []
        for component in components_list:
            search_query = (
                f"{component} specs price datasheet site:aliexpress.com OR site:amazon.com OR site:daraz.pk"
            )
            try:
                resp = self.tavily_client.search(
                    query=search_query,
                    search_depth="advanced",
                    include_answer=True,
                    include_images=False,
                    max_results=5,
                )
            except Exception as e:
                sections.append(f"{component}:\n  Error fetching data: {e}")
                continue

            answer = (resp.get("answer") or "").strip()
            results = resp.get("results", []) or []

            lines = [f"{component}:"]
            if answer:
                lines.append(f"  Summary: {answer}")

            for r in results[:5]:
                title = r.get("title", "").strip() or "Result"
                url = r.get("url", "").strip()
                content = (r.get("content") or "").strip()
                if len(content) > 220:
                    content = content[:217] + "..."
                lines.append(f"  - {title}\n    {url}\n    {content}")

            sections.append("\n".join(lines))

        return "\n\n".join(sections)

    # DuckDuckGo 
    def ddg_search(self, query: str) -> str:
        q = (query or "").strip()
        if not q:
            return "Please provide a non-empty search query."
        try:
            results = self.ddg.results(q, num_results=5)
        except Exception as e:
            return f"DuckDuckGo search failed: {e}"

        if not results:
            return "No results found."

        lines = []
        for r in results:
            title = r.get("title", "").strip() or "Result"
            link = r.get("link", "").strip() or r.get("href", "")
            snippet = (r.get("snippet") or r.get("body") or "").strip()
            if len(snippet) > 220:
                snippet = snippet[:217] + "..."
            lines.append(f"- {title}\n  {link}\n  {snippet}")
        return "\n\n".join(lines)

    def __call__(self):
        return [self.ddg_tool, self.youtube_tool, self.github_tool, self.tavily_tool]