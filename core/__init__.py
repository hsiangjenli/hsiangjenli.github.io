from .crawler import GitHubRepos, CrawlerMyBlogPosts
from .chore import CalculateKeywords

if __name__ == "__main__":
    # Crawl my blog posts
    crawler = CrawlerMyBlogPosts("https://github.com/hsiangjenli/blog/tree/main/source/_posts/tutorial")
    posts, count_blogs = crawler.get_blog_posts_name()
    print(posts, count_blogs)
    
    # Crawl my github repos
    github = GitHubRepos("hsiangjenli")
    repos, count_repos = github.get_tutorial_repos()
    print(repos, count_repos)

    # Calculate keywords
    cal = CalculateKeywords(posts, repos)
    keywords = cal.get_keywords(n=3)
    print(keywords)