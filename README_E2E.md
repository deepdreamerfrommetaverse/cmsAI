## Nowe scenariusze

* **prompt_agent_flow.spec.ts** – odzwierciedla cały przepływ “Prompt → Generator → karta z hero + WP ID”. Backend jest stubowany, więc test nie wymaga OpenAI ani WordPressa.
* **scheduler_display.spec.ts** – weryfikuje, że artykuł utworzony przez scheduler pojawia się na Dashboard (mock listy artykułów).

Uruchomienie:
```bash
cd frontend
npm run test -- --grep prompt_agent_flow
```
