# Hackertion

This application helps users

- understand how news & global economics affect daily life

- receive AI-driven schedule insight

- track financial implications of events

- stay informed with personalized business news

### Clean Architecture

- presentation should not depend on other modules' adapters

    import only its own module service


### Custom AI

```
News Sources
     ↓
Gemini → summarization (5 topics)
     ↓
Learning AI Model (your custom layer)
     ↓
Learning Insights Engine
     ↓
Frontend (learning dashboard)
```