# Tea Stall Management System with AI Chatbot

A Django-based tea stall (tea shop) management system with an integrated AI chatbot powered by Google Gemini 2.0.

---

## Features

### Stall Management

* **Menu Catalog**: Browse and search menu items by name, category (tea, snacks, drinks), or SKU.
* **Inventory Management**: Track ingredients and product stock levels; low-stock alerts.
* **Order Management**: Create and manage customer orders (dine-in, takeaway, delivery).
* **Billing & Invoicing**: Generate bills, apply discounts, and print receipts.
* **Employee Management**: Manage staff profiles, roles, and shifts.
* **Supplier Management**: Record suppliers and place restock orders.
* **Sales Dashboard**: View daily/weekly/monthly sales, best-sellers, and revenue.
* **Reservations / Table Management**: Reserve tables and manage seat availability.

### AI Chatbot Assistant

* **Intelligent Responses**: Powered by Google Gemini 2.0 AI.
* **Stall Context**: Knows current menu, prices, stock levels, and today's specials.
* **Order Help**: Assist with taking customer orders or preparing order summaries for staff.
* **Quick Responses**: Pre-defined common questions (hours, specials, popular items).
* **Real-time Chat**: Interactive chat interface with message history.
* **Floating Widget**: Access the chatbot from any page in the app.

---

## Chatbot Capabilities

The AI assistant can help with:

* Finding menu items by name, ingredient, or category.
* Checking if an item is in stock.
* Recommending popular or combo items based on time of day.
* Answering stall policies (refunds, returns, delivery areas).
* Creating quick order summaries (for kitchen printouts).
* Showing current sales statistics or today’s best-sellers.

---

## Setup Instructions

1. **Install Dependencies**:

```bash
pip install django pillow google-generativeai requests
```

2. **Configure Gemini API**:

* Get your API key from Google AI Studio (or your Google Cloud project).
* Add it to `settings.py` (or better: use environment variables):

```python
GEMINI_API_KEY = 'your-api-key-here'
```

3. **Run Migrations**:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Create Superuser**:

```bash
python manage.py createsuperuser
```

5. **Start Server**:

```bash
python manage.py runserver
```

---

## Usage

### Accessing the Chatbot

1. **Navigation Menu**: Click "Chat Assistant" in the top navigation.
2. **Floating Widget**: Click the robot icon in the bottom-right corner (available on all pages except the chat-only page).
3. **Direct URL**: Visit `/chatbot/` in your browser.

### Using the Chatbot

1. Type your question in the message input field.
2. Use quick response buttons for common stall/customer questions.
3. View conversation history in the chat window.
4. Clear chat history using the trash button (if your app stores history).

### Example Questions

* "What's on today's special menu?"
* "Do we have milk tea available right now?"
* "How many lemon teas were sold today?"
* "How do I create a takeaway order?"
* "Recommend a popular combo for evening customers."

---

## Technical Details

### Chatbot Architecture

* **Backend**: Django views and DRF (optional) handle API requests.
* **AI Service**: `StallChatbot` or `TeaStallChatbot` class manages Gemini AI interactions.
* **Frontend**: JavaScript handles the real-time chat interface (WebSocket or long-polling for near real-time).
* **Context Awareness**: Chatbot has access to current menu, inventory, and sales stats to provide informed answers.

### API Endpoints (examples)

* `GET /chatbot/`: Chatbot interface page.
* `POST /api/chatbot/`: Send message and receive AI response.
* `GET /api/menu/`: Get menu items.
* `POST /api/orders/`: Create a new order.
* `GET /api/sales/summary/`: Get sales statistics.

### Security

* CSRF protection on all forms.
* Input validation and sanitization.
* HTML escaping for user-generated content.
* Use authentication and permission checks for staff-only endpoints.

---

## Configuration

### Customizing the Chatbot

Edit `stall/chatbot.py` (or your chosen module) to:

* Modify system prompts and personality.
* Add custom stall context (menu, daily special, inventory thresholds).
* Implement additional search or ordering capabilities.
* Customize response formatting (JSON vs. rich text with action buttons).

### Adding Quick Responses

Update the `get_quick_responses()` method in the `TeaStallChatbot` class to add or modify pre-defined customer/staff questions.

---

## Production Considerations

1. **API Key Security**: Use environment variables or a secrets manager for the Gemini API key.
2. **Rate Limiting**: Implement rate limiting for the chatbot API to avoid abuse and control costs.
3. **Caching**: Cache frequent queries (menu, specials) to reduce AI API calls and latency.
4. **Monitoring**: Log chatbot interactions and errors for analysis and improvement.
5. **Backups**: Regularly backup order logs, inventory, and chat logs if stored.
6. **Scaling**: Use worker queues for heavy tasks (reports, analytics, bulk imports).

---

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your Gemini API key is valid, has correct permissions, and has sufficient quota.
2. **Network Issues**: Check internet connectivity for AI API calls.
3. **Long Response Times**: AI responses may take a few seconds — consider showing typing indicators or using a cached quick-answer layer for simple queries.
4. **Character Limits**: Ensure messages sent to the AI API obey size limits (truncate or summarize long contexts).

### Error Handling

The chatbot includes graceful error handling for:

* Network connectivity issues.
* API rate limiting and quota errors.
* Invalid or malformed responses from the AI service.
* Server-side exceptions (use structured logging to capture stack traces).

---

## Contributing

To add new features:

1. Update the chatbot class for new AI capabilities.
2. Modify templates for UI improvements.
3. Add new API endpoints as needed.
4. Update documentation and write tests for important flows (orders, inventory).

---

## License

This project is open source and available under the MIT License.
