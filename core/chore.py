STOP_WORDS = [
    "tutorial",
    "and",
    "script"
]

class CalculateKeywords:
    def __init__(self, *args: list) -> None:
        self.args = args
    
    @property
    def stop_words(self):
        return STOP_WORDS
    
    @property
    def flatten_data(self):
        flatten_args = []
        for arg in self.args:
            flatten_args.extend(arg)
        
        flatten_data = []
        for data in flatten_args:
            if '-' in data:
                flatten_data.extend(data.split('-'))
            elif '_' in data:
                flatten_data.extend(data.split('_'))
        
        return (flatten_data)
    
    def get_keywords(self, n=5):
        # remove stop words in keywords
        keywords = [keyword for keyword in self.flatten_data if keyword not in self.stop_words]        
    
        # calculate keywords frequency
        keywords_freq = {}
        for keyword in keywords:
            if keyword in keywords_freq:
                keywords_freq[keyword] += 1
            else:
                keywords_freq[keyword] = 1
        
        # return top n keywords
        keywords_freq = sorted(keywords_freq.items(), key=lambda x: x[1], reverse=True)
        return [keyword[0] for keyword in keywords_freq[:n]]
