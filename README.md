# productprices
Model built to predict the price of an item based on parameters parsed from a webshop.

# Run
To scrape TV's from euronics.hu to `data/products.json`:
```
python scrape.py
```
`Preprocess.ipnyb` can be run for preprocessing, `Modeling.ipynb` can be run for regression.

To launch streamlit application:
```
streamlit run dashboard.py
```

# Task
1. Scrape data from a webstore.
2. Create features.
3. Model prices.
4. Deploy model.

# Plan
1. Scraping: two solutions came to mind:
  - BeautifulSoup: simpler interface, less functionality, more suitable for limited time
  - Scrapy: more advanced tool for scraping, provides greater functionality. Might have to look for my previous codes for them, if data is hard to parse.
2. Feature engineering: based on data, one should
  - Encode
  - Normalize
  - Derive new ones
3. Modeling: regression task. Models I used before in similar scenarios:
  - (Linear) regression
  - SVM-regressor
  - XGBRegressor
4. Deploy: closest I used so far is Streamlit.io

For both 2. and 3. one should do an EDA as well, which could be put on a dashboard in streamlit.

# Timing
I got 3x2 hours. For each task that is ~1-2 hours depending on my experience and unforeseen challenges. Although I am more experienced in tasks 2 and 3, 1 is crucial to have, so I am planning to spend more time on these.

# Further developments
1. Scraping
  - Scrapy: could collect cleaner data by correct xpath
2. Feature engineering
3. Modeling
  - Explain model better 
4. Deploy
  - Dashboard: interactive charts could be made by Plotly for instance (has experience with them but would take up more time to freshen them)
