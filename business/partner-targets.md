```markdown
# Partner Integration Roadmap — care-privacy

> Priority order: revenue-share potential + user-job criticality + sector fit.

---

## 1. Auth0 (Okta)
**Category:** Identity & Access Management
**Rationale:** Healthcare and education orgs already have Auth0/Okta deployments. Plugging consent workflows into existing identity means zero new login friction — consent events are tied to verified user sessions from day one.
**Free tier:** 7,500 MAU free on Auth0 developer plan
**Integration effort:** M — OAuth2/OIDC callback hooks + Action extensibility
**Value-add:** Solves *"prove this specific person actually consented"* — links consent records to authenticated identity, essential for HIPAA audit trails
**Revenue-share:** Okta ISV Partner Program (up to 20% referral on sourced deals); Auth0 Marketplace listing drives inbound

---

## 2. DocuSign
**Category:** eSignature / Consent Collection
**Rationale:** Regulated consent (IRB forms, FERPA waivers, patient intake) still requires wet-or-eSignature in most US states. DocuSign is the default procurement-approved vendor in hospital systems and university legal departments.
**Free tier:** None (30-day trial); developer sandbox is unlimited
**Integration effort:** M — REST API, envelope webhooks, template management
**Value-add:** Solves *"collect legally defensible signed consent at scale"* — generates signed PDF audit artifacts automatically stored against the consent record
**Revenue-share:** DocuSign ISV Referral Program — 15% on net new ACV sourced; also unlocks healthcare-specific templates via DocuSign for Healthcare

---

## 3. Twilio (SMS/Voice)
**Category:** Consent Notification & Re-consent Campaigns
**Rationale:** Consent expiry re-requests and breach notifications require out-of-band channels; SMS has 98% open rates vs. 20% email. Twilio is universal and has healthcare-compliant messaging (Twilio Verify for 2FA consent).
**Free tier:** $15 trial credit; ~500 SMS
**Integration effort:** S — single REST endpoint, webhook for delivery receipts
**Value-add:** Solves *"re-obtain consent before it lapses without losing the patient/student"* — automates re-consent campaigns 30/7/1 day before expiry
**Revenue-share:** Twilio Referral Program — $500–$2,000 per qualified referral + revenue share tier for ISV partners (negotiate via Twilio Engage program)

---

## 4. Epic (FHIR R4 API)
**Category:** EHR / Healthcare Data Source
**Rationale:** 37% of US hospitals run Epic. FHIR R4 Consent resources are the canonical source of truth for patient consent in clinical settings. Bidirectional sync makes care-privacy the control plane rather than a silo.
**Free tier:** Epic on FHIR sandbox (open.epic.com) is free; production access requires Epic App Orchard review
**Integration effort:** L — SMART on FHIR auth, Consent resource CRUD, Provenance chain, App Orchard certification (~90 days)
**Value-add:** Solves *"keep consent state synchronized between the EHR and the AI system using patient data"* — eliminates dual-entry and compliance gaps
**Revenue-share:** No direct referral; Epic App Orchard listing drives inbound discovery from 37%+ of hospital IT buyers — strategic moat, not a commission play

---

## 5. Canvas LMS / Instructure
**Category:** Learning Management System (Education)
**Rationale:** Canvas holds 35%+ of US higher-ed LMS market. Student data flowing through AI tutoring tools (the exact use case) must have FERPA-compliant consent gates. Native Canvas integration means consent prompts appear inside the existing student workflow.
**Free tier:** Canvas Free for Teachers (limited); developer API is open
**Integration effort:** M — LTI 1.3 tool launch, Canvas Data API, OAuth2 per-institution
**Value-add:** Solves *"gate AI tool access in the LMS until FERPA consent is on file"* — prevents institutions from accidentally violating FERPA by deploying AI tools without consent records
**Revenue-share:** Instructure Partner Program — negotiated rev-share for marketplace listings; edu-sector deals typically $15K–$80K ACV, 10–15% referral available

---

## 6. Segment (Twilio CDP)
**Category:** Customer Data Platform
**Rationale:** SaaS companies building health/ed AI products use Segment to route user data to analytics, ML pipelines, and ad platforms. care-privacy can act as a Segment Destination Filter — data only flows downstream if consent is active for that specific purpose.
**Free tier:** Free plan up to 1,000 MTU/month
**Integration effort:** M — Segment Functions (source/destination), Protocols for consent event taxonomy
**Value-add:** Solves *"ensure our Segment data pipelines are consent-scoped, not fire-and-forget"* — turns care-privacy into the gating layer for all downstream data flows
**Revenue-share:** Segment Partner Program — catalog listing; Twilio (parent) has ISV rev-share; this integration also strengthens the Twilio/care-privacy partnership above

---

## 7. Stripe
**Category:** Billing & Subscription
**Rationale:** Monetizing consent management requires usage-based billing (per consent record, per API call, per active user). Stripe is the lowest-friction path to metered billing for B2B SaaS in this segment.
**Free tier:** No monthly fee; 2.9% + 30¢ per transaction
**Integration effort:** S — Stripe Billing + Metered Usage API + Customer Portal for self-serve plan changes
**Value-add:** Solves *"monetize at the right granularity without building billing infrastructure"* — enables per-record, per-seat, or per-API-call pricing models
**Revenue-share:** None direct; Stripe Partner Ecosystem listing drives discovery among SaaS founders building on top of care-privacy

---

## 8. Microsoft Azure Health Data Services (FHIR + DICOM)
**Category:** Cloud Healthcare Data Platform
**Rationale:** Azure is the dominant HIPAA-BAA-covered cloud in enterprise health systems. Azure Health Data Services exposes FHIR Consent resources natively. care-privacy running on Azure Marketplace unlocks enterprise procurement paths — many hospital IT budgets are pre-committed to Azure MACC spend.
**Free tier:** Free tier limited; $200 Azure credit for new accounts; FHIR service ~$0.36/1K API calls
**Integration effort:** L — Azure Marketplace certification, ARM template for deployment, FHIR sync, Managed Identity auth
**Value-add:** Solves *"deploy care-privacy inside our existing Azure security perimeter without new vendor procurement"* — reduces enterprise sales cycle by 6–12 weeks
**Revenue-share:** Azure Marketplace co-sell (IP co-sell eligible) — Microsoft sales team can source and co-sell; eligible for up to 20% margin on transacted deals; MACC-eligible listings draw down pre-committed enterprise spend

---

## Priority Matrix

| Partner | Effort | Revenue-Share | Time-to-Value |
|---|---|---|---|
| Twilio SMS | S | ✅ $500–$2K/referral | Week 2 |
| Auth0 | M | ✅ 20% ISV | Month 1 |
| DocuSign | M | ✅ 15% ACV | Month 1 |
| Segment | M | ✅ Twilio ISV | Month 2 |
| Stripe | S | — | Week 1 (billing) |
| Canvas LMS | M | ✅ negotiated | Month 3 |
| Epic FHIR | L | — (moat play) | Month 4–6 |
| Azure Marketplace | L | ✅ co-sell 20% | Month 5–7 |

**Sequence recommendation:** Ship Stripe + Twilio first (unblock billing + consent collection), then Auth0 + DocuSign (credibility with compliance buyers), then Canvas (edu vertical), then Epic + Azure (enterprise moat).
```