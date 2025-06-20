# AI Travel Planner

**AI Travel Planner** is an intelligent, agentic travel and expense planning assistant. It leverages advanced LLMs and a suite of real-world APIs (Google Maps, Amadeus, weather, currency exchange, etc.) to generate highly personalized, actionable, and cost-aware travel itineraries for users.

---

## Features

- **Conversational Trip Planning:** Chat with the AI to plan trips, clarify preferences, and refine your itinerary.
- **Flight & Hotel Search:** Integrates with flight and hotel APIs for real-time options and pricing.
- **Daily Itinerary Generation:** Creates detailed, time-slotted daily plans based on your interests and trip duration.
- **Local Exploration:** Recommends attractions, restaurants, and activities using geolocation and user interests.
- **Expense Management:** Allocates your budget across flights, accommodation, food, activities, and more.
- **Weather & Currency Info:** Provides weather forecasts and real-time currency exchange rates.
- **Professional Summaries:** Outputs a comprehensive, easy-to-read trip summary with all logistics and recommendations.

---

## Setup

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/aitravelplanner.git
cd aitravelplanner
```

### 2. Create and Activate a Virtual Environment

```sh
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Configure API Keys

- Copy `.env.example` to `.env` and fill in your API keys for OpenAI, Google Maps, Amadeus, SerpAPI, etc.

---

## Usage

### Run the Chat Agent

From the project root, run:

```sh
python -m src.main
```

or (if using `uv`):

```sh
uv run -m src.main
```

### Interact

- Type your travel requests and preferences in the terminal.
- The assistant will ask clarifying questions if needed and generate a detailed plan.
- Type `exit` or `quit` to end the session.

---

## Project Structure

```
aitravelplanner/
│
├── src/
│   ├── main.py                # Main chat loop and agent logic
│   ├── config/                # API clients and settings
│   ├── models/                # Pydantic models for travel data
│   ├── tools/                 # Tool integrations (maps, flights, weather, etc.)
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## Extending

- Add new tools in `src/tools/` and register them in `main.py`.
- Add new models in `src/models/`.
- Update prompts and planning logic in `main.py` for more features.

---

## License

MIT License

---

## Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [OpenAI](https://openai.com/)
- [Google Maps API](https://developers.google.com/maps)
- [Amadeus Travel APIs](https://developers.amadeus.com/)
