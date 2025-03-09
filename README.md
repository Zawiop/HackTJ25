# Akinator-Style Career Matching App

This repository contains a Flask application that uses Google’s `genai` library to provide an **Akinator-style** experience for matching users to a career path. The AI asks a series of simple, free-response questions, refines its inquiries based on prior answers, and finally suggests an ideal career.

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Code Explanation](#code-explanation)
   - [Flask App (`app.py`)](#flask-app-apppy)
   - [Front-End (`index.html`)](#front-end-indexhtml)
7. [License](#license)

---

## Overview

This project demonstrates how to integrate the [Google genai library](https://pypi.org/project/genai/) with a Flask backend. The AI acts like an “Akinator” for careers, asking a series of questions in order to suggest a suitable career based on user responses. All conversation logic is stored and processed on the server, while a simple front-end displays questions and collects answers.

## Features

- **Akinator-Style Q&A**: The AI asks multiple questions and adapts based on previous user responses.
- **Simple UI**: A single-page interface that shows the current question and a free-response input (or optional multiple-choice).
- **Session History**: The conversation history is stored server-side so the AI can maintain context.
- **Final Answer**: Once the AI decides on a career suggestion, it returns a final message

## Prerequisites

- **Python 3.7+**
- A valid **Google genai API key**.
- [Flask](https://palletsprojects.com/p/flask/) and [requests](https://docs.python-requests.org/) (or other dependencies you may need).
- The `genai` Python library installed:  
  ```bash
  pip install genai

## Live Demo

Check out the live version of the Career Planner App here:  
[https://careerplannerest25.sites.tjhsst.edu/](https://careerplannerest25.sites.tjhsst.edu/)


...
