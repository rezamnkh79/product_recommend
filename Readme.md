# Advanced Recommendation System

## Project Overview

This project implements an advanced recommendation system for an e-commerce platform. The system recommends products to
users based on their browsing and purchase history, the browsing/purchase history of similar users, and contextual
signals (such as time of day, seasonality, and user device type).

## Setup Instructions

### Clone the Repository

```sh
git clone <repository_url>
cd <repository_directory>
```

### Install Dependencies

Ensure you have Python and Redis installed. Then, install the required Python packages:

```sh
pip install -r requirements.txt
```

### Run Redis Server

Make sure the Redis server is running on the default port `6379`.

### Setup Django Project

Initialize the Django project by running migrations and creating a superuser:

```sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Start Django Development Server

```sh
python manage.py runserver
```

## How to Use

### Product Recommendations

- The `RecommendationManager` class handles generating and fetching product recommendations.
- The recommendations are personalized based on the user's browsing history, cart items, purchase history, and popular
  products.

### Calculate Product Similarity

- The `calculate_product_similarity` method calculates the TF-IDF cosine similarity between products and stores the
  similarity matrix in Redis for quick access.

### Get Similar Products by Text

- The `get_similar_products_by_text` method fetches similar products based on the precomputed similarity matrix.

### Get Recommended Products

- The `get_recommended_products` method retrieves recommendations for a user, first checking Redis for cached
  recommendations before querying the database.

## Code Structure

- **Models**
    - `CartItemEntity`: Represents items in the user's shopping cart.
    - `ProductEntity`: Represents products in the catalog.
    - `BrowsingHistory`: Records products viewed by each user.
    - `PurchaseHistory`: Records products purchased by each user.
    - `RecommendationEntity`: Stores precomputed recommendations for users.

- **Serializers**
    - `RecommendationSerializer`: Serializes recommendation data for API responses.

- **RecommendationManager**
    - Handles all recommendation logic, including fetching user-specific recommendations and calculating product
      similarities.

## Optimization and Scaling

### Caching

- Recommendations and similarity matrices are cached in Redis to speed up retrieval and reduce load on the database.

### Pre-computation

- Similarity matrices are precomputed and stored, allowing for quick similarity lookups.

### Efficient Data Structures

- Efficient use of Django ORM for querying.
- Use of TF-IDF and cosine similarity for textual similarity calculations.

### Scheduled Task

There is a task that runs every 24 hours to generate product recommendations for all users. The recommendations are
stored both in the database and in Redis, with a 24-hour expiration in Redis.

## Future Improvements

1. **Enhanced Contextual Recommendations**
    - Incorporate more contextual signals like time of day and seasonality to improve the relevance of recommendations.

2. **Hybrid Recommendation Approach**
    - Combine collaborative filtering with content-based methods to leverage the strengths of both approaches.

3. **Scalability Enhancements**
    - Use parallel processing for large datasets.
    - Optimize query performance and reduce latency.

4. **Model Explainability**
    - Provide insights into why a particular product was recommended, improving transparency and user trust.

## Detailed Explanation of TF-IDF

**TF-IDF** (Term Frequency-Inverse Document Frequency) is a statistical measure used to evaluate the importance of a
word in a document relative to a collection of documents (corpus). The importance increases proportionally to the number
of times a word appears in the document but is offset by the frequency of the word in the corpus.

- **Term Frequency (TF)**: Measures how frequently a term occurs in a document.
  \`
  ext{TF}(t, d) = rac{ ext{Number of times term } t ext{ appears in document } d}{ ext{Total number of terms in
  document } d}
  \`

- **Inverse Document Frequency (IDF)**: Measures how important a term is.
  \`
  ext{IDF}(t) = \log\left( rac{ ext{Total number of documents}}{ ext{Number of documents with term } t}
  ight)
  \`

- **TF-IDF**: The product of TF and IDF, giving a composite score.
  \`
  ext{TF-IDF}(t, d) = ext{TF}(t, d)    imes ext{IDF}(t)
  \`

In this project, TF-IDF is used to transform product features (e.g., product name and category) into a numerical format
that allows for the computation of cosine similarity, which measures the cosine of the angle between two vectors,
providing a similarity score between products.

\`\`\`python
def calculate_product_similarity(self):
products = ProductEntity.objects.all()
product_features = [f"{product.name} {product.category}" for product in products]
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(product_features)
similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
self.redis_client.setex('product_similarity_matrix', 86400, pickle.dumps(similarity_matrix))  # 24 hours
return similarity_matrix
\`\`\`

This method extracts features from products, computes the TF-IDF matrix, and then calculates the cosine similarity
matrix, which is cached in Redis for efficient retrieval.

By following these guidelines, the recommendation system will be more efficient, scalable, and capable of providing
high-quality recommendations tailored to individual users.