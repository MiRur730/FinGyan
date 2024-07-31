def Recommender(keywords):
    import os
    import pandas as pd
    from sklearn.neighbors import NearestNeighbors
    import tensorflow as tf
    import tensorflow_hub as hub
    import kagglehub
    import pickle

    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disable oneDNN optimizations

    # Download latest version of the model
    try:
        path = kagglehub.model_download("google/universal-sentence-encoder/tensorFlow2/universal-sentence-encoder")
    except Exception as e:
        print(f"Error downloading model: {e}")
        path = "local_path_to_model"  # fallback to a local path if download fails

    # Load the Universal Sentence Encoder model from local directory
    try:
        model = hub.load(path)
        print("Universal Sentence Encoder model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        return []

    # Load datasets
    try:
        df1 = pd.read_csv(r"Zerodha_Varsity.csv")
        df2 = pd.read_csv(r"Copy_of_Finance_With_Sharan.csv")
    except Exception as e:
        print(f"Error loading datasets: {e}")
        return []

    # Fill missing values
    df1 = df1.fillna('')
    df2 = df2.fillna('')

    # Combine datasets
    df = pd.concat([df1, df2], ignore_index=True)

    # Keep only relevant columns
    df = df[['Title', 'Description', 'ids']]
    df['Title_Description'] = df['Title'] + ' ' + df['Description']

    # Define embedding function with batching
    def embed(texts, batch_size=100):
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            embeddings.append(model(batch))
        return tf.concat(embeddings, axis=0)

    embeddings_path = 'recommendation_embeddings.pkl'
    
    if not os.path.exists(embeddings_path):
        # Get embeddings for titles and descriptions
        titles = df['Title_Description'].tolist()
        embeddings = embed(titles)
        
        # Save embeddings to file
        with open(embeddings_path, 'wb') as f:
            pickle.dump(embeddings, f)
        print("Embeddings saved successfully.")
    else:
        # Load embeddings from file
        with open(embeddings_path, 'rb') as f:
            embeddings = pickle.load(f)
        print("Embeddings loaded successfully.")

    # Fit Nearest Neighbors model
    nn = NearestNeighbors(n_neighbors=10)
    nn.fit(embeddings)

    # Function to process YouTube URLs
    yt_url = "https://www.youtube.com/watch?v="
    def process(url):
        return yt_url + url

    # Function to recommend videos based on input text
    def recommend(text):
        try:
            emd = embed([text])
            neighbours = nn.kneighbors(emd, return_distance=False)[0]
            urls = df['ids'].iloc[neighbours].tolist()
            return [process(url) for url in urls]
        except Exception as e:
            print(f"Error in recommendation: {e}")
            return []

    # Get recommendations based on provided keywords
    recommendations = recommend(keywords)
    return recommendations

# Example usage
# keywords = "financial literacy for students"
# recommendations = Recommender(keywords)
# print(recommendations)