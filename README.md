# 🎯 B2B Lead Scraper - Roofing Contractors (USA)

> **A complete full-stack lead generation platform for scraping B2B roofing contractors with verified contact information and automated email outreach capabilities.**

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [What This Project Does](#what-this-project-does)
- [Technical Architecture](#technical-architecture)
- [Technology Stack](#technology-stack)
- [API Integrations](#api-integrations)
- [Features](#features)
- [Installation & Setup](#installation--setup)
- [How to Run](#how-to-run)
- [Testing the Application](#testing-the-application)
- [Project Structure](#project-structure)
- [Environment Configuration](#environment-configuration)
- [Production Deployment](#production-deployment)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

**B2B Lead Scraper** is a comprehensive lead generation platform designed to help businesses find and engage with roofing contractors across the United States. The system automates the entire workflow from data scraping to email outreach, making it perfect for:

- **Sales teams** targeting roofing contractors
- **B2B service providers** in the construction industry
- **Marketing agencies** running outreach campaigns
- **Software vendors** selling to roofing businesses

### Key Capabilities:

1. **Lead Scraping** - Extract business data from Google Maps and other sources
2. **Data Enrichment** - Verify and enhance contact information
3. **Lead Management** - Store, filter, and organize leads in a database
4. **Email Automation** - Send personalized outreach campaigns
5. **Analytics** - Track campaign performance and ROI

---

## 🚀 What This Project Does

### 1. **Scrapes Business Data**

The application connects to multiple data sources (via Apify and Apollo.io APIs) to extract:

- ✅ Business name and address
- ✅ Owner/decision maker names
- ✅ **Verified mobile phone numbers**
- ✅ Professional email addresses
- ✅ Google ratings and reviews
- ✅ Website URLs
- ✅ Verification status

**Current Demo**: Includes 100 sample roofing contractors across 12 US states (50% Texas-based)

### 2. **Manages Lead Database**

- **View all leads** in a sortable, filterable table
- **Export to CSV** for use in CRM systems
- **Filter by location** (state, city)
- **Filter by verification status** (verified/unverified)
- **Add leads to campaigns** with one click

### 3. **Automates Email Campaigns**

Send personalized emails using 4 professional templates:

1. **Introduction & Services** - Initial cold outreach
2. **Partnership Opportunity** - B2B partnership proposals
3. **Product Demo Offer** - Free trial/demo invitations
4. **Follow-up Message** - Nurture campaigns

**Email Features:**
- Personalized with business name, owner name, location
- HTML templates with professional design
- SMTP integration (local testing + production)
- Campaign tracking and metrics

### 4. **Provides Analytics Dashboard**

Track key metrics:
- Total leads scraped
- Verification rate
- Average business ratings
- Geographic coverage
- Campaign performance (opens, clicks, responses)

---

## 🏗️ Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       USER INTERFACE                        │
│            (HTML/CSS/JavaScript - Frontend)                 │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTPS/REST API
┌────────────────────▼────────────────────────────────────────┐
│                    FASTAPI BACKEND                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Scraper    │  │    Email     │  │  Analytics   │     │
│  │   Service    │  │   Service    │  │   Service    │     │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┘     │
└─────────┼──────────────────┼──────────────────────────────┘
          │                  │
          ▼                  ▼
┌─────────────────┐  ┌─────────────────┐
│  External APIs  │  │  SMTP Server    │
│  - Apify        │  │  - SendGrid     │
│  - Apollo.io    │  │  - Mailgun      │
│  - Google Maps  │  │  - Local Test   │
└─────────────────┘  └─────────────────┘
```

### Data Flow:

1. **User Request** → Frontend captures input (location, filters)
2. **API Call** → JavaScript sends POST request to FastAPI backend
3. **Data Scraping** → Backend calls external APIs (Apify/Apollo)
4. **Data Processing** → Validate, enrich, and store leads
5. **Response** → JSON data returned to frontend
6. **Rendering** → JavaScript displays results in UI

---

## 💻 Technology Stack

### Backend (Python)

| Technology | Version | Purpose |
|-----------|---------|---------|
| **FastAPI** | 0.104+ | High-performance REST API framework |
| **Uvicorn** | 0.24+ | ASGI server for async operations |
| **Pydantic** | 2.5+ | Data validation and serialization |
| **Python** | 3.13 | Core programming language |
| **smtplib** | Built-in | Email sending (SMTP client) |

**Why FastAPI?**
- ⚡ Fast performance (comparable to Node.js)
- 📚 Automatic API documentation (Swagger/OpenAPI)
- ✅ Built-in data validation
- 🔄 Async/await support
- 🎯 Easy to deploy

### Frontend (Vanilla JavaScript)

| Technology | Purpose |
|-----------|---------|
| **HTML5** | Structure and semantic markup |
| **CSS3** | Modern styling with gradients and animations |
| **JavaScript (ES6+)** | Frontend logic and API integration |
| **Fetch API** | HTTP requests to backend |

**Design Approach:**
- 🎨 **Dark theme** with glassmorphism effects
- 📱 **Responsive design** (mobile-first)
- ✨ **Micro-animations** for better UX
- 🚫 **No frameworks** - lightweight and fast


**Data Added:**
- ✅ Verified email addresses
- ✅ Direct mobile numbers
- ✅ Decision maker names & titles
- ✅ LinkedIn profiles
- ✅ Company size & revenue

## ✨ Features

### Frontend Features

- ✅ **4 Interactive Tabs**
  - Scraper (configure and run searches)
  - Leads Database (view and manage leads)
  - Email Campaigns (create outreach campaigns)
  - Analytics (track performance metrics)

- ✅ **Real-time Updates**
  - Live scraping status with loading animation
  - Instant results preview
  - Dynamic campaign metrics

- ✅ **Data Export**
  - Export leads to CSV
  - Compatible with Excel, Google Sheets, CRMs

- ✅ **Responsive Design**
  - Works on desktop, tablet, mobile
  - Touch-friendly interface

### Backend Features

- ✅ **RESTful API**
  - `/api/scrape` - Scrape leads by location
  - `/api/leads` - Get all scraped leads
  - `/api/campaigns` - Manage email campaigns
  - `/api/stats` - Get analytics data

- ✅ **Data Validation**
  - Pydantic models ensure data integrity
  - Type checking and serialization
  - Error handling and logging

- ✅ **CORS Enabled**
  - Frontend can call API from any origin
  - Configurable for production security

- ✅ **Async Operations**
  - Non-blocking email sending
  - Concurrent API calls
  - High performance under load

---

## 📦 Installation & Setup

### Prerequisites

- **Python 3.13+** (Download from [python.org](https://www.python.org/downloads/))
- **Web Browser** (Chrome, Firefox, Edge, Safari)
- **Text Editor** (VS Code, Sublime, Notepad++)

### Step 1: Clone/Download Project

```bash
cd "C:\Users\ayush.a\Self\Anoix Tech\b2b-lead-scraper"
```

### Step 2: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Dependencies installed:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `requests` - HTTP client (for external APIs)
- `python-multipart` - Form data parsing

