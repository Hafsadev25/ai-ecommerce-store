# AI E-Commerce Store

An AI-powered e-commerce store built with **Streamlit** and **Groq LLM**. 
It lets users chat with an AI assistant to search, filter, and discover products naturally.

##  Features
- **AI Shopping Assistant**: Ask in plain English like "show me cheap laptops under 50k"
- **Smart Product Search**: The AI understands intent and filters from `products.json`
- **Modern UI**: Clean, responsive design that works on mobile + desktop

##  Tech Stack
- **Frontend**: Streamlit  
- **AI Model**: Groq `llama-3.1-70b-versatile`
- **Data**: Local `products.json` file
- **Secrets**: `.env` file for API key, hidden via `.gitignore`

##  Run Locally
1.  **Clone the repo**
    ```bash
    git clone https://github.com/Hafsadev25/ai-ecommerce-store
    cd ai-ecommerce-store
