<h1 align="center">Ahtisham Dilawar</h1>

<p align="center">
  I build backends and AI agents for money things. The kind that have to be right.
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/ahtisham-dilawar">LinkedIn</a> ·
  <a href="mailto:ahtishamdilawar@gmail.com">Email</a> ·
  <a href="https://github.com/ahtishamdilawar?tab=repositories">Repos</a>
</p>

---

### About

I'm a software engineer. I spend most of my time on the boring-but-critical side of AI: the part where an LLM has to work with financial statements, transaction data and compliance evidence, and a real person has to be able to trust the output.

Right now I'm at **DeFa by Invoicemate**, building an agent that helps risk officers review payment-service providers before money moves. Before that I built AI backends for a non-profit finance platform, WhatsApp agents for a real-estate company, and MCP servers that let agents talk to QuickBooks, Salesforce and HubSpot.

### How I like to work

- **The model talks, the code decides.** LLMs are great at intent, terrible at bookkeeping. I let them handle the conversation and keep every balance, state change and decision in plain, testable code.
- **Humans stay in the loop.** Anything that touches money gets citations, an audit trail and a person who can say no. I design for that from day one instead of bolting it on.
- **Ship it to a real user early.** My favourite projects are the ones somebody outside my laptop actually depends on. A desktop invoicing app I built is used daily by a handful of small businesses, which taught me more than any tutorial.
- **Local-first when possible.** SQLite, plain files, offline modes. Fewer moving parts, fewer 3 AM pages.
- **Small, readable, done.** I'd rather delete a feature than ship one I can't explain in a paragraph.

### Things I've made

**[expense-tracker-skill](https://github.com/ahtishamdilawar/expense-tracker-skill)** is my take on personal finance for the agent era. A deterministic SQLite ledger with a portable Agent Skill on top, so Claude Code, Codex or Hermes can run it without ever being allowed to make up a number.

**[nuces-flex-MCP](https://github.com/ahtishamdilawar/nuces-flex-MCP)** started as a joke ("roast my transcript") and turned into a proper MCP server for my university's student portal. Ask Claude how many classes you've bunked and it'll tell you.

**[quickbook-OAuth-demo](https://github.com/ahtishamdilawar/quickbook-OAuth-demo)** and **[mcp-server-test](https://github.com/ahtishamdilawar/mcp-server-test)** are small, deliberately minimal reference implementations I keep coming back to when I need multi-tenant OAuth or a deployable MCP server done right.

**[CForge-mini-compiler](https://github.com/ahtishamdilawar/CForge-mini-compiler)** is a compiler for a made-up C-like language, all the way from lexer to LLVM IR and NASM. University project, but the one I'm proudest of from that era.

**[LoLQueueAssist](https://github.com/ahtishamdilawar/LoLQueueAssist)** auto-accepts League of Legends queues and handles champion pick/ban so I stop missing games. **[lazy-post-detector](https://github.com/ahtishamdilawar/lazy-post-detector)** flags LinkedIn posts with em dashes. It's a meme. It's not that deep.

Off GitHub: **FBR Invoicer**, an offline-first Tauri desktop app for Pakistan's digital tax invoicing, and **FuzzSeer**, an LLM-guided fuzzer for Solidity contracts that prioritises risky execution paths instead of brute-forcing.

### Currently

- Building agentic RAG pipelines on LangGraph and Azure AI Search for financial due diligence
- Going deep on MCP and Agent Skills as the interface between models and real systems
- Thinking about what "explainable" should mean when an agent recommends a credit decision

### Tools I reach for

<p>
  <img src="https://skillicons.dev/icons?i=python,ts,js,fastapi,nodejs,nextjs,azure,aws,docker,mongodb,sqlite,rust,tauri&perline=13" alt="tools" />
</p>

Plus LangGraph, LangChain, the OpenAI and Gemini APIs, Auth0, and whatever the problem actually needs.

---

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=ahtishamdilawar&layout=compact&hide_border=true&hide=jupyter%20notebook,css,html" alt="Top languages" height="150" />
</p>
