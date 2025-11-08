# Payment & Subscription Guide - Gematria Hive

**Date:** January 6, 2025  
**Status:** 💳 Payment Requirements Summary  
**Purpose:** Guide for payment/subscription requirements for all API keys

---

## 💳 Payment Requirements Summary

### ✅ FREE - No Payment Required

| Service | Free Tier | Notes |
|---------|-----------|-------|
| **Google Gemini API** | ✅ Yes | Free tier with generous limits, billing account may be required but won't be charged if within limits |
| **Google Drive API** | ✅ Yes | Free tier available, billing account may be required for OAuth setup |
| **Supabase** | ✅ Yes | Free tier available (already configured) |

### ⚠️ PAY-AS-YOU-GO - May Require Billing

| Service | Free Tier | Payment Required | Notes |
|---------|-----------|------------------|-------|
| **Anthropic Claude API** | ❌ No | 💳 Yes | Pay-as-you-go pricing |
| **Perplexity API** | ⚠️ Limited | 💳 Yes | Check current pricing |
| **Grok/X.ai API** | ⚠️ Limited | 💳 Yes | Check current pricing |

---

## 🔴 HIGH PRIORITY - Setup Required

### 1. Google Gemini API (FREE TIER AVAILABLE)

**Status:** ✅ Free tier available

**Payment Required:** ⚠️ Billing account may be required but won't be charged if within free limits

**Steps:**
1. **Open:** https://ai.google.dev
2. **Sign in** with Google account
3. **Click:** "Get API Key"
4. **If prompted for billing:**
   - ✅ **Select:** Free tier / Basic plan
   - ⚠️ **Note:** Billing account may be required but you won't be charged if within free limits
   - 💳 **If asked:** Choose the free tier option
5. **Copy:** API key
6. **Add to `.env`:** `GOOGLE_API_KEY=your-key-here`

**Pricing:** Free tier available with generous limits

**Action:** Get API key - billing account setup may be required but free tier is available

---

### 2. Google Drive OAuth (FREE TIER AVAILABLE)

**Status:** ✅ Free tier available

**Payment Required:** ⚠️ Billing account may be required for OAuth setup but won't be charged if within free limits

**Steps:**
1. **Open:** https://console.cloud.google.com
2. **Create project** (free)
3. **Enable Google Drive API** (free)
4. **Configure OAuth consent screen** (free)
5. **Create OAuth credentials** (free)
6. **If prompted for billing:**
   - ✅ **Select:** Free tier / Basic plan
   - ⚠️ **Note:** Billing account may be required but you won't be charged if within free limits
   - 💳 **If asked:** Choose the free tier option
7. **Add to `.env`:**
   ```bash
   GOOGLE_DRIVE_CLIENT_ID=your-client-id
   GOOGLE_DRIVE_CLIENT_SECRET=your-client-secret
   ```
8. **Run:** `python scripts/setup_google_drive_oauth.py`

**Pricing:** Free tier available

**Action:** Set up OAuth - billing account setup may be required but free tier is available

---

## 🟢 MEDIUM PRIORITY - Optional (Requires Payment)

### 3. Anthropic Claude API (PAY-AS-YOU-GO)

**Status:** 💳 Payment required

**Payment Required:** ✅ Yes - Pay-as-you-go pricing

**Steps:**
1. **Open:** https://console.anthropic.com
2. **Sign up** or sign in
3. **Go to:** API Keys
4. **If prompted for payment:**
   - 💳 **Select:** Pay-as-you-go plan
   - 💰 **Cost:** Check current pricing at https://www.anthropic.com/pricing
5. **Create:** API key
6. **Add to `.env`:** `ANTHROPIC_API_KEY=your-key-here`

**Pricing:** Pay-as-you-go, check current rates

**Action:** ⚠️ **REQUIRES PAYMENT** - Only set up if you want Claude integration

---

### 4. Perplexity API (PAY-AS-YOU-GO)

**Status:** 💳 Payment required

**Payment Required:** ✅ Yes - Check current pricing

**Steps:**
1. **Open:** https://www.perplexity.ai
2. **Sign up** for API access
3. **Go to:** API Settings
4. **If prompted for payment:**
   - 💳 **Select:** Appropriate plan
   - 💰 **Cost:** Check current pricing
5. **Create:** API key
6. **Add to `.env`:** `PERPLEXITY_API_KEY=your-key-here`

**Pricing:** Check current pricing

**Action:** ⚠️ **REQUIRES PAYMENT** - Only set up if you want Perplexity integration

---

### 5. Grok/X.ai API (PAY-AS-YOU-GO)

**Status:** 💳 Payment required

**Payment Required:** ✅ Yes - Check current pricing

**Steps:**
1. **Open:** https://x.ai
2. **Sign up** for API access
3. **Go to:** API Settings
4. **If prompted for payment:**
   - 💳 **Select:** Appropriate plan
   - 💰 **Cost:** Check current pricing
5. **Create:** API key
6. **Add to `.env`:** `GROK_API_KEY=your-key-here`

**Pricing:** Check current pricing

**Action:** ⚠️ **REQUIRES PAYMENT** - Only set up if you want Grok/Twitter integration

---

## 📋 Quick Decision Guide

### ✅ Set Up Now (Free Tier Available)
- [ ] **Google Gemini API** - Free tier available
- [ ] **Google Drive OAuth** - Free tier available

### ⚠️ Set Up Later (Requires Payment)
- [ ] **Anthropic Claude API** - Pay-as-you-go
- [ ] **Perplexity API** - Pay-as-you-go
- [ ] **Grok/X.ai API** - Pay-as-you-go

---

## 💰 Cost Estimates (Approximate)

| Service | Free Tier | Paid Tier | Notes |
|---------|-----------|-----------|-------|
| **Google Gemini** | ✅ Free | Pay-as-you-go | Free tier has generous limits |
| **Google Drive** | ✅ Free | Pay-as-you-go | Free tier covers typical usage |
| **Anthropic Claude** | ❌ None | ~$0.003/1K tokens | Check current pricing |
| **Perplexity** | ⚠️ Limited | Varies | Check current pricing |
| **Grok/X.ai** | ⚠️ Limited | Varies | Check current pricing |

---

## 🎯 Recommended Setup Order

### Phase 1: Free Services (No Payment Required)
1. ✅ **Google Gemini API** - Get API key (billing account may be required but free tier available)
2. ✅ **Google Drive OAuth** - Set up OAuth (billing account may be required but free tier available)

### Phase 2: Paid Services (Optional, Requires Payment)
3. 💳 **Anthropic Claude API** - Only if needed
4. 💳 **Perplexity API** - Only if needed
5. 💳 **Grok/X.ai API** - Only if needed

---

## ⚠️ Important Notes

### Billing Account Setup
- **Google Services:** May require billing account setup even for free tier
- **Why:** Google requires billing account for API access, but won't charge if within free limits
- **Action:** Set up billing account when prompted, but choose free tier option

### Payment Selection
- **If prompted for payment/subscription:**
  - **Google Gemini:** Choose free tier / basic plan
  - **Google Drive:** Choose free tier / basic plan
  - **Anthropic Claude:** Choose pay-as-you-go (requires payment)
  - **Perplexity:** Choose appropriate plan (requires payment)
  - **Grok:** Choose appropriate plan (requires payment)

### Free Tier Limits
- **Google Gemini:** Generous free tier limits
- **Google Drive:** Free tier covers typical usage
- **Monitor Usage:** Set up usage alerts to avoid unexpected charges

---

## 🚀 Next Steps

1. **Set up Google Gemini API** (Free tier available)
   - Get API key from https://ai.google.dev
   - If prompted for billing: Choose free tier option

2. **Set up Google Drive OAuth** (Free tier available)
   - Follow `BROWSER_SETUP_GUIDE.md`
   - If prompted for billing: Choose free tier option

3. **Optional: Set up paid services** (Only if needed)
   - Anthropic Claude (if needed)
   - Perplexity (if needed)
   - Grok (if needed)

---

**Last Updated:** January 6, 2025  
**Status:** 💳 Payment Requirements Documented

