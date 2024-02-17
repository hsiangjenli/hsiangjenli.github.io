import requests
from bs4 import BeautifulSoup

class GitHubRepos:
    def __init__(self, user_name) -> None:
        self.GITHUB_API = "https://api.github.com/"
        self.user_name = user_name
        
    @property
    def GITHUB_API_REPOS(self):
        return self.GITHUB_API + f"users/{self.user_name}/repos"
    
    @property
    def user_repos(self):
        response = requests.get(self.GITHUB_API_REPOS)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
    def get_tutorial_repos(self):
        repos = self.user_repos
        tutorial_repos = [repo['name'].lower() for repo in repos if repo['name'].startswith('tutorial')]
        return tutorial_repos, len(tutorial_repos)
    

class CrawlerMyBlogPosts:
    def __init__(self, url) -> None:
        self.url = url
    
    def get(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    
    def soup(self):
        return BeautifulSoup(self.get(), 'html.parser')
    
    def get_blog_posts_name(self):
        soup = self.soup()
        data = soup.find_all(attrs={"role": "rowheader", "class": "flex-auto min-width-0 col-md-2 mr-3"})
        posts = [post.text.strip().lower().replace(".md", "") for post in data]
        return posts, len(posts)

if __name__ == "__main__":
    # Crawl my blog posts
    crawler = CrawlerMyBlogPosts("https://github.com/hsiangjenli/blog/tree/main/source/_posts/tutorial")
    posts, count_blogs = crawler.get_blog_posts_name()
    print(posts, count_blogs)
    
    # Crawl my github repos
    github = GitHubRepos("hsiangjenli")
    repos, count_repos = github.get_tutorial_repos()
    print(repos, count_repos)