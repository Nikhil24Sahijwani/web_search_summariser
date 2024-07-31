from googlesearch import search

def get_unique_websites(query, num_results=10):
    # Using set to avoid duplicates
    seen_url = set()

    # List containing the unique SearchResult objects
    unique = []
    
    # Iterating over to find the unique SearchResult objects
    for i in search(query, num_results=num_results, advanced=True):
        if i.url not in seen_url:
            seen_url.add(i.url)
            unique.append(i)

            if len(unique) == 5:
                break
            
    # Returning the list of unique SearchResult objects
    return unique
