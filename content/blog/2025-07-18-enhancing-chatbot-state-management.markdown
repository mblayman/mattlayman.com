---
title: "Enhancing Chatbot State Management with LangGraph"
description: >-
  A lively dive into a coding session where I upgraded a chatbot's state management to handle user data like names and birthdays using LangGraph.
image: img/python.png
type: post
categories:
  - Python
tags:
  - Python
  - LangGraph
  - chatbot
  - state management
date: 2025-07-18
---

Picture this: it's late and I'm deep in a coding
session, wrestling with a chatbot that's starting to feel more like a living
thing than a few lines of Python. Today's mission? Supercharge the chatbot's
ability to remember and verify user details like names and birthdays using
LangGraph. Let's unpack the journey, from shell commands to Git commits, and
see how this bot got a memory upgrade.

For clarity, this is my adventure running through the LangGraph docs.
I'm not teaching much here that you couldn't learn from reading their documentation,
but I'm sharing my experience.

## The Setup: Kicking Off the Chatbot

I started by firing up the chatbot server with a specific environment variable to enable checkpointing:

```bash
USE_CHECKPOINTER=yes uv run -m chat.chat_server
```

This command tells the system to use a `MemorySaver` checkpointer, which persists the chatbot's state between interactions. Why? Because I want the bot to *remember* things like a user's name and birthday, even if the conversation takes a detour. Checkpointing is like giving the bot a notepad to jot down key details, and `uv` (a Python package manager) ensures I'm running the latest dependencies cleanly.

Next, I ran:

```bash
uv run langgraph dev
```

This spun up LangGraph's development server, letting me test the chatbot's flow interactively. LangGraph is a nifty library for building stateful, graph-based workflows, perfect for a chatbot that needs to juggle multiple steps—like chatting, searching, or asking for human help. The `dev` mode is my playground for tweaking the graph and seeing changes live.

## The Challenge: Adding User Data to the State

The big task was to make the chatbot smarter about handling user info. The original code had a basic `State` class with just a `messages` list, but I needed to track `name` and `birthday` too. Why? Imagine the bot asking, "What's your name and birthday?" and then forgetting it mid-conversation. Not exactly user-friendly.

The Git commit at 23:57 tells the story:

```bash
gc
```

This shorthand for `git commit` sealed the deal, with the message: *Incorporate additional state into the chatbot flow.* Let's dive into the changes.

## The Code: Upgrading the State and Human Assistance

Here's the diff from the commit, showing the heart of the upgrade:

```diff
diff --git a/chat/chatbot.py b/chat/chatbot.py
index ad01afa..493aa1c 100644
--- a/chat/chatbot.py
+++ b/chat/chatbot.py
@@ -3,22 +3,45 @@ from typing import Annotated, TypedDict
 
 from dotenv import load_dotenv
 from langchain.chat_models import init_chat_model
-from langchain_core.tools import tool
+from langchain_core.messages import ToolMessage
+from langchain_core.tools import InjectedToolCallId, tool
 from langchain_tavily import TavilySearch
 from langgraph.checkpoint.memory import MemorySaver
 from langgraph.graph import StateGraph, START, END
 from langgraph.graph.message import add_messages
 from langgraph.prebuilt import ToolNode, tools_condition
-from langgraph.types import interrupt
+from langgraph.types import Command, interrupt
 
 load_dotenv()
 
 
 @tool
-def human_assistance(query: str) -> str:
+def human_assistance(
+    name: str, birthday: str,
+    tool_call_id: Annotated[str, InjectedToolCallId]
+) -> Command:
     """Request assistance from a human."""
-    human_response = interrupt({"query": query})
-    return human_response["data"]
+    human_response = interrupt(
+        {
+            "question": "Is this correct?",
+            "name": name,
+            "birthday": birthday,
+        }
+    )
+    if human_response.get("correct", "").lower().startswith("y"):
+        verified_name = name
+        verified_birthday = birthday
+        response = "Correct"
+    else:
+        verified_name = human_response.get("name", name)
+        verified_birthday = human_response.get("birthday", birthday)
+        response = f"Made a correction: {human_response}"
+
+    state_update = {
+        "name": verified_name,
+        "birthday": verified_birthday,
+        "messages": [ToolMessage(response, tool_call_id=tool_call_id)],
+    }
+    return Command(update=state_update)
 
 
 tavily_search = TavilySearch(max_results=2)
@@ -44,6 +67,8 @@ def select_checkpointer():
 
 class State(TypedDict):
     messages: Annotated[list, add_messages]
+    name: str
+    birthday: str
 
 
 def chatbot(state: State):
```

### Key Changes and Insights

1. **State Expansion**:
   I added `name` and `birthday` to the `State` class:

   ```python
   class State(TypedDict):
       messages: Annotated[list, add_messages]
       name: str
       birthday: str
   ```

   This lets the chatbot track user details persistently, thanks to LangGraph's state management. It’s like giving the bot a memory upgrade from a sticky note to a full-fledged database (well, almost).

2. **Human Assistance Overhaul**:
   The `human_assistance` tool got a major facelift. Before, it was a simple function taking a `query` string and returning a basic response. Now, it’s a powerhouse that handles name and birthday verification:

   ```python
   @tool
   def human_assistance(
       name: str, birthday: str,
       tool_call_id: Annotated[str, InjectedToolCallId]
   ) -> Command:
       """Request assistance from a human."""
       human_response = interrupt(
           {
               "question": "Is this correct?",
               "name": name,
               "birthday": birthday,
           }
       )
       if human_response.get(
           "correct", "").lower().startswith("y"):
           verified_name = name
           verified_birthday = birthday
           response = "Correct"
       else:
           verified_name = human_response.get("name", name)
           verified_birthday = human_response.get(
              "birthday", birthday)
           response = f"Made a correction: {human_response}"

       state_update = {
           "name": verified_name,
           "birthday": verified_birthday,
           "messages": [ToolMessage(
                          response, tool_call_id=tool_call_id)],
       }
       return Command(update=state_update)
   ```

   This tool now asks a human to verify the user’s name and birthday, updating the state if corrections are needed. The `Command` return type and `tool_call_id` ensure LangGraph can track the tool’s execution, keeping the conversation flow smooth. The `interrupt` mechanism pauses the bot to wait for human input, which is critical for handling sensitive data like birthdays accurately.

3. **Checkpointing Decision**:
   The `select_checkpointer` function checks for the `USE_CHECKPOINTER` environment variable:

   ```python
   def select_checkpointer():
       """Select the checkpointer to use.

       A "custom" checkpointer doesn't work with `langgraph dev`.
       """
       if os.environ.get("USE_CHECKPOINTER"):
           return MemorySaver()
       return None
   ```

   This was a pragmatic choice. The `langgraph dev` command doesn’t play nice with custom checkpointers, so I made checkpointing optional. When testing locally, I enable it with `USE_CHECKPOINTER=yes` to persist state, but in dev mode, I skip it to avoid compatibility headaches.

## Challenges and Triumphs

One challenge was ensuring the `human_assistance` tool didn’t overwhelm the state with unnecessary updates. By using `Command` and `ToolMessage`, I kept the state clean and focused, only updating `name`, `birthday`, and `messages` when needed. Another hurdle was debugging the `langgraph dev` environment, which threw errors with a custom checkpointer. Switching to a conditional checkpointer solved this, letting me test rapidly without sacrificing production-ready code.

The triumph? The chatbot now feels *alive*. It can ask, “Is your name Jane and birthday March 3rd?” and gracefully handle corrections like a pro. The stateful design means it won’t forget Jane’s details mid-chat, making the user experience smoother.

## Wrapping Up

This coding session was a blast—part detective work, part creative engineering. By expanding the state, revamping the human assistance tool, and navigating LangGraph’s quirks, I gave the chatbot a memory upgrade that makes it more reliable and user-friendly. The shell commands and Git commit tell a story of iterative progress, from testing with `uv run` to sealing the deal with a well-crafted commit.

Want to try something similar? Grab LangGraph, play with state management, and see how far you can push your chatbot. Got questions or cool tweaks? Drop them in the comments!
